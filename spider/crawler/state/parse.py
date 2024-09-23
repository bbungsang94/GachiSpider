import re
import json
import json
import os.path as osp
from urllib.parse import urlparse, urljoin

from spider.structure import Node
from .base import State
from .store import StoreLocal
from .failed import Failed

class Parse(State):
    def __init__(self, node: Node, parent):
        super(Parse, self).__init__("parse", node=node, parent=parent)
        self.form = self._get_form()
        if self.form is None:
            self.parent.transit(Failed(node=self.node, parent=self.parent))
        
    def run(self):
        try:
            self.node.data = self._parse()
            self.parent.transit(StoreLocal(node=self.node, parent=self.parent))
        except Exception as e:
            import traceback
            self.logger.error(traceback.print_exc())
            self.parent.transit(Failed(node=self.node, parent=self.parent))
            
    def pause(self):
        raise NotImplementedError
    
    def stop(self):
        raise NotImplementedError
    
    def _get_form(self):
        root = "./spider/form"
        parsed_url = urlparse(self.node.url.replace('www.', ''))
        root = osp.join(root, parsed_url.netloc)
        file_path = osp.join(root, 'index.json') 
        if not osp.exists(file_path):
            self.logger.warning("Not found %s" % parsed_url.netloc)
            return None
        
        with open (file_path, "r") as f:
            data = json.load(f)
        
        for key, form in data.items():
            self.logger.debug("Compare key: %s" % key)
            result = re.search(key, urljoin(parsed_url.path, parsed_url.query))
            if result is not None:
                self.node.pattern = key
                self.logger.info("Found form from: %s" % file_path)
                return form
        return None
    
    def _parse(self):
        gathered = dict()
        for tag, value in self.form.items():
            self.logger.info(tag)
            result = getattr(self.node.cache, value['method'])(value['tag'])
            for i in range(len(result)):
                self.logger.debug(result[i])
            
            if 'attrs' in value:
                attrs = value['attrs']
                for i, stub in reversed(list(enumerate(result))):
                    if attrs is None:
                        cond = not bool(stub.attrs)
                    else:
                        cond = attrs[0] in stub.attrs and stub.attrs[attrs[0]] == attrs[1]
                    if cond is False:
                        del result[i]
            
            if 'html' in value and value['html']:
                gathered[tag] = [{'text': stub.prettify(), 'attrs': None} for stub in result]
            else:
                gathered[tag] = [{'text': stub.get_text(), 'attrs': stub.attrs} for stub in result]

        return gathered
    