from datetime import datetime 
from urllib.request import Request, urlopen
from typing import List
from bs4 import BeautifulSoup as bs
from spider.structure import Node
from .base import State
from .failed import Failed
from .gather import Gather


class Fetch(State):
    def __init__(self, node: Node, parent):
        super(Fetch, self).__init__("fetch", node=node, parent=parent)
        
    def run(self):
        try:
            req = Request(self.node.url, headers={'User-Agent': self.parent.name})
            context = urlopen(req)
            if context.status == 200:
                self.node.url = context.url
                soup = bs(context.read(), 'html.parser')
                self.node.last_visited = datetime.timestamp(datetime.now())
                self.node.cache = soup
                self.parent.transit(Gather(node=self.node, parent=self.parent))
            else:
                self.logger.warning("Invalid connection(%d), from %s" % (context.status, self.node.url))
                self.node.label = "Connection Blocked"
                raise ConnectionError
        except Exception as e:
            import traceback
            self.logger.error(traceback.print_exc())
            self.parent.transit(Failed(node=self.node, parent=self.parent))
    
    def pause(self):
        raise NotImplementedError
    
    def stop(self):
        raise NotImplementedError