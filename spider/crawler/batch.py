import math
import logging
from urllib.parse import urljoin
from typing import List
import requests
from bs4 import BeautifulSoup as bs
from spider.structure import Node
from .state import State, Fetch, Parse
from . import Crawler
from . import __name__


class BatchCrawler(Crawler):
    def __init__(self, base_url, batch_code: str = '', batch_size: int = 16):
        super(BatchCrawler, self).__init__(base_url=base_url)
        self.logger = logging.getLogger(name="BatchCrawler")
        self.nodes = None
        self.trajectory = set()
        self.batch = None
        self.batch_code = batch_code
        self.batch_size = batch_size
        self._pivot = -1
        
    def crawl(self, url):
        self._update_links(url)
        n_cycle = math.ceil(len(self.nodes) / self.batch_size)
        new_nodes = []
        for cycle in range(n_cycle):
            begin = (cycle * self.batch_size)
            end = begin + self.batch_size
            end = end if end <= len(self.nodes) else len(self.nodes)
            self.batch = self.nodes[begin:end]
            
            for i, node in enumerate(self.batch):
                init_state = Fetch(node=node, parent=self)
                self._pivot = i
                init_state.run()  
                new_nodes.append(self.crawl_once(node=self.batch[self._pivot]))
    
    def transit(self, next_state: State, auto_run: bool = True):          
        if self.nodes is None:
            self.nodes = next_state.node.fan_out
        else:
            self.batch[self._pivot] = next_state.node
    
    def _update_links(self, url):
        self.logger.info("Tried to visit site: %s" % url)
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')
        parser = Parse(Node(url=url, cache=soup), parent=self)
        parser.run()
        
        #특정 링크 지우기
        for i, node in reversed(list(enumerate(self.nodes))):
            cond1 = not self.batch_code in node.url
            cond2 = node.url in self.trajectory
            if cond1 or cond2:
                del self.nodes[i]
            else:
                node.url = urljoin(self.base_url, node.url)
                self.nodes[i] = node
        
        self.logger.info("Found new links(%d)" % len(self.nodes))
        
    def crawl_once(self, node: Node):
        from .parallel import Parser
        
        parser = Parser(node=node)
        parser.crawl(node.url)
        return parser.state.node