import copy
from datetime import datetime
import json
import time
from typing import Dict, List
from logging import Logger
from spider.manager.state import UpdateMongo
from spider.structure import DocumentDB, Node
from spider.utils.math import clamp

class Scheduler:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):         
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config: Dict[str, object],
                 roots: Dict[str, object],
                 logger: Logger,
                 db_handle: DocumentDB,
                 link_manager):
        
        self.logger = logger
        self.logger.name = "SCHEDULER"
        self.logger.info("Instantiate scheduler")
        self.config, self.roots = config, roots
        
        self.logger.info("Check root urls in DB, searching spaces are")
        self.db_handle, self.link_manager = db_handle, link_manager
        self.documents = self._scan_freshness(list(self.roots.keys()))
  
        for node in self.documents:
            self.logger.info("%s, freshness: %d" % (node.url, node.freshness))
    
    def __adjust_freshness(self, last_visited, period):
        gap_hours, _ = divmod(time.time() - last_visited, 3600)
        return clamp(gap_hours / period, 0., 1.)
        
    def _request_to(self, platform, **payload):
        self.logger.info("Request to %s" % (platform))
        
        kwargs = self.config['credential'][platform]
        response = self.link_manager.invoke(**kwargs, Payload=json.dumps(payload))
        payload = json.loads(response['Payload'].read())
        return payload
    
    def _scan_freshness(self, links: List[str]) -> List[Node]:
        new_links = copy.deepcopy(self.roots)
        exists = self.db_handle.find({"url": {"$in": links}})
        nodes = []
        for node in exists:
            node = Node.from_dict(node)
            properties = self.roots[node.url]
            del new_links[node.url]
            node.freshness = self.__adjust_freshness(node.last_visited, properties['period'])
            node.label = "Root"
            nodes.append(node)
        
        new_nodes = []
        for link in new_links.keys():
            new_nodes.append(Node(url=link, freshness=1, label="Root"))
        
        if len(new_nodes) > 0:
            self.db_handle.insert_many([node.to_dict() for node in new_nodes])
        return nodes + new_nodes
    
    def _replace_public_ip(self):
        pass
    
    def _set_depth(self):
        pass
    
    def _dispatch_crawler(self, handle):
        pass
    
    def transit(self, *args, **kwargs):
        pass
        
    def run(self, **kwargs):
        self.logger.info("Run a cycle")
        for node in self.documents:
            if node.freshness == 1:
                response = self._request_to("manager", url=node.url, **kwargs)
                if "errorMessage" in response:
                    self.logger.error(response['errorMessage'])
                if "statusCode" in response:
                    self.logger.info(response['statusCode'])
                    if response['statusCode'] == 501:
                        node.label = "Root, Connection Error"
                        self._replace_public_ip()
                    
                node.last_visited = datetime.timestamp(datetime.now())
                node.freshness = 0
                state = UpdateMongo(node=node, parent=self, collection=self.db_handle, label_pass=True)
                state.run() 
        
        self.logger.info("Scan freshness after processing")
        self.documents = self._scan_freshness(list(self.roots.keys()))