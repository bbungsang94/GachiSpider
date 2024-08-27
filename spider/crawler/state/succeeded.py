from .base import State
from spider.structure import Node


class Succeeded(State):
    def __init__(self, node: Node, parent):
        super(Succeeded, self).__init__("succeeded", node=node, parent=parent)
        
    def run(self):
        pass
    
    def pause(self):
        pass
    
    def stop(self):
        pass
    