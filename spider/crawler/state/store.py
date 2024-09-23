import os
import re
import copy
import pickle
from typing import List
from urllib.parse import urlparse, urljoin
from spider.structure import Node
from .base import State
from .failed import Failed
from .succeeded import Succeeded

class UpdateMongo(State):
    def __init__(self, node: Node, parent, collection):
        super(UpdateMongo, self).__init__("store", node=node, parent=parent)
        self.collection = collection
        
    def run(self):
        try:
            result = self._store_node()
            self.parent.transit(Succeeded(node=self.node, parent=self.parent))
            if result.modified_count == 0:
                raise ValueError
        except:
            self.parent.transit(Failed(node=self.node, parent=self.parent))
            
    def pause(self):
        raise NotImplementedError
    
    def stop(self):
        raise NotImplementedError
    
    def _store_node(self):
        nodes = copy.deepcopy(self.node.fan_out)
        self.node.fan_out = [x.url for x in nodes]
        self.node.cache = None
        
        query = {'url': self.node.url}      
        contents = {"$set": self.node.to_dict()}
        result = self.collection.update_one(query, contents)
        return result
    
      
class StoreLocal(State):
    def __init__(self, node: Node, parent, root='./datalake/red_zone'):
        super(StoreLocal, self).__init__("store", node=node, parent=parent)
        if not os.path.exists(root):
            self.logger.warning("Not found root directory, Made temp directory to : %s" % root)
            os.makedirs(root)
        self.root = root
        
    def run(self):
        try:
            self._store_node()
            self.parent.transit(Succeeded(node=self.node, parent=self.parent))
        except:
            self.parent.transit(Failed(node=self.node, parent=self.parent))
            
    def pause(self):
        raise NotImplementedError
    
    def stop(self):
        raise NotImplementedError
    
    def _store_node(self):
        parsed_url = urlparse(self.node.url.replace('www.', ''))
        folder_path = os.path.join(self.root, parsed_url.netloc)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        numbers = re.findall(self.node.pattern, urljoin(parsed_url.path, parsed_url.query))
        numbers = re.findall(r"\d+", numbers[0])
        full_path = os.path.join(folder_path, numbers[0] + '.pkl')
        self.node.cache = None
        with open(full_path, 'wb') as f:
            pickle.dump(self.node, f, pickle.HIGHEST_PROTOCOL)