import logging
from abc import ABCMeta, abstractmethod
from typing import List
from spider.structure import Node


class State(metaclass=ABCMeta):
    def __init__(self, name: str, node: Node, parent):
        self.logger = logging.getLogger(name="state: " + name)
        self.name = name
        self.parent = parent
        node.label = name
        self.node = node
        self.logger.debug("activated")
            
    @abstractmethod
    def run(self):
        raise NotImplementedError

    @abstractmethod
    def pause(self):
        raise NotImplementedError
    
    @abstractmethod
    def stop(self):
        raise NotImplementedError
