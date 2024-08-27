from typing import List
from spider.structure import Node
from .base import State
from .store import Store
from .failed import Failed

class Parse(State):
    def __init__(self, node: Node, parent):
        super(Parse, self).__init__("parse", node=node, parent=parent)
        
    def run(self):
        try:
            self.node.fan_out = self._get_links()
            self.parent.transit(Store(node=self.node, parent=self.parent))
        except:
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
                node = Node(url=href, fan_in=[self.node])
                nodes.append(node)
        return nodes