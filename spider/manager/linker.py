import copy
import logging
from pymongo import MongoClient
from typing import List
from urllib.parse import urljoin, urlparse

from spider.structure import Node
from spider.utils.web import get_base_url, get_unwrapped_url
from .state import State, Fetch
from spider.crawler import Crawler

class CloudLinker(Crawler):
    def __init__(self, init_url, db_ip: str, db_port: int=27017):
        super(CloudLinker, self).__init__(init_url=init_url)
        self.logger = logging.getLogger(name="LinkManager")
        self.logger.info("Initialize LinkManager as Cloud Linker")
        self.node = Node(url=init_url)
        self.logger.info("Try to connect runtime db")
        try:
            client = MongoClient(host=db_ip, port=db_port)
            self.logger.info("Mongo Client: {0}".format(client))
            server_info = client.server_info()
            self.logger.info("Server Information: {0}".format(server_info))
        except Exception as e:
            self.logger.error("Failed DB connection")
            return None
        self.runtime_db = client['Pages']
        self.alternatives = None
        
    def crawl(self, url):
        self.node.url = url
        self.logger.info("Fetch url: %s" % (self.node.url))
        state = Fetch(node=self.node, parent=self)
        state.run()
        
        if self.node.label == "Connection Failed":
            self.logger.info("You should replace public IP")
            return {
                'statusCode': 501,
                'message': "Replace IP"
                }
        self._extract_links()
        
        self.logger.info("Unwrap redirected URLs with Check available site")
        nodes = copy.deepcopy(self.node.fan_out)
        self.node.fan_out = [x.url for x in nodes]
        nodes = self._check_sanity(nodes)
        
        self.logger.info("Eliminate URLs on Freshness after matched runtime DB")
        self.alternatives = self._match_database(nodes)
        
        self.logger.info("Prioritize URLs")
        self.alternatives.sort(key=lambda node: node.freshness, reverse=True)
        
        self.logger.info("Validate robots")
        if self.matcher is not None:
            allow, reason = self.matcher.allow_by(url=self.alternatives[0].url)
        
        return {
            'statusCode': 200,
            'message': "Succeeded",
            'urls': [x.url for x in self.alternatives]
            }
    
    def transit(self, next_state: State, auto_run: bool = True):          
        self.node = next_state.node
    
    def _check_sanity(self, nodes: List[Node]) -> List[Node]:
        for i, node in enumerate(nodes):
            contents, url = get_unwrapped_url(node.url)
            if url is not None:
                nodes[i].url = url
                nodes[i].cache = contents
            else:
                self.logger.info("Unwrap failed url: %s" % (node.url))
                nodes[i].label = "Unwrap Failed"
        return nodes
    
    def _extract_links(self):
        base_url = get_base_url(self.node.url)
        for i, node in reversed(list(enumerate(self.node.fan_out))):
            parsed_url = urlparse(node.url)
            if parsed_url.hostname == None:
                self.node.fan_out[i].url = urljoin(base_url, node.url)
            else:
                del self.node.fan_out[i]
    
    def _match_database(self, nodes: List[Node]):
        collection = self.runtime_db['Nodes']
        existing_nodes = collection.find({"url": {"$in": self.node.fan_out}}, Node.get_fields(begin=1))
        existing_nodes = [Node.from_dict(node) for node in existing_nodes]
        existing_set = {node.url for node in existing_nodes}
        
        new_nodes = [node for node in nodes if node.url not in existing_set]
        if len(new_nodes) > 0:
            collection.insert_many([node.to_dict() for node in new_nodes])
        return existing_nodes + new_nodes