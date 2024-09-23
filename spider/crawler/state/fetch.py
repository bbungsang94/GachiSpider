from datetime import datetime 
from typing import List
from bs4 import BeautifulSoup as bs
from spider.structure import Node
from spider.utils.web import get_unwrapped_url
from .base import State
from .failed import Failed
from .gather import Parse


class Fetch(State):
    def __init__(self, node: Node, parent):
        super(Fetch, self).__init__("fetch", node=node, parent=parent)
        
    def run(self):
        try:
            if self.node.cache is None:
                contents, url = get_unwrapped_url(self.node.url)
            else:
                contents, url = self.node.cache, self.node.url
                
            if url is not None:
                self.node.url = url
                soup = bs(contents, 'html.parser')
                self.node.last_visited = datetime.timestamp(datetime.now())
                self.node.cache = soup
                self.node.fan_out = self._get_links()
                self.parent.transit(Parse(node=self.node, parent=self.parent))
            else:
                self.logger.warning("Invalid connection, from %s" % (self.node.url))
                self.node.label = "Connection Failed"
                raise ConnectionError
        except Exception as e:
            import traceback
            self.logger.error(traceback.print_exc())
            self.parent.transit(Failed(node=self.node, parent=self.parent))
    
    def pause(self):
        raise NotImplementedError
    
    def stop(self):
        raise NotImplementedError
    
    def _get_links(self) -> List[Node]:
        links = self.node.cache.find_all('a')
        nodes = []
        for link in links:
            href = link.get('href')
            if href:
                node = Node(url=href, fan_in=[self.node.url])
                nodes.append(node)
        return nodes