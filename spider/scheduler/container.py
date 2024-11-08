import json
import time
from typing import Dict, List
from logging import Logger
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
        
        links = [x.url for x in self.documents]    
        for url in self.roots.keys():
            if url in links:
                exists = "true"
            else:
                exists = "false"
                self.documents.append(Node(url, freshness=1))
            self.logger.info("%s, exists: %s" % (url, exists))
    
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
        exists = self.db_handle.find({"url": {"$in": links}})
        nodes = []
        for node in exists:
            node = Node.from_dict(node)
            properties = self.roots[node.url]
            node.freshness = self.__adjust_freshness(node.last_visited, properties['period'])
            nodes.append(node)
        return nodes
    
    def _replace_public_ip(self):
        pass
    
    def _set_depth(self):
        pass
    
    def _dispatch_crawler(self, handle):
        pass
    
    def run(self):
        self.logger.info("Run a cycle")
        db_ip, db_port = self.db_handle.database.client.address # raise RuntimeError if not MongoDBClient
        for node in self.documents:
            if node.freshness == 1:
                response = self._request_to("manager", url=node.url, db_ip=db_ip, db_port=db_port)
                self.logger.info(response['statusCode'])
                if response['statusCode'] == 501:
                    self._replace_public_ip()
        
        self.logger.info("Scan freshness after processing")
        self._scan_freshness(list(self.roots.keys()))