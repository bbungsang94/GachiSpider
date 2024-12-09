from bs4 import BeautifulSoup as bs
from spider.structure import Node, State
from spider.utils.io import get_form
from spider.utils.web import clean_text
from .store import StoreLocal
from .failed import Failed

class Parse(State):
    def __init__(self, node: Node, parent):
        super(Parse, self).__init__("parse", node=node, parent=parent)
        form_dict = get_form(node=self.node, logger=self.logger)
        self.node = form_dict['node']
        if form_dict['form'] is None:
            self.node.label = "Not found correct form"
            self.parent.transit(Failed(node=self.node, parent=self.parent))
        
    def run(self):
        try:
            self.node.data = self._parse()
            self.parent.transit(StoreLocal(node=self.node, parent=self.parent, root='/tmp/datalake/red_zone'))
        except Exception as e:
            import traceback
            self.node.label = "Not found correct form"
            self.logger.error(traceback.print_exc())
            self.parent.transit(Failed(node=self.node, parent=self.parent))
            
    def pause(self):
        raise NotImplementedError
    
    def stop(self):
        raise NotImplementedError
    
    def _parse(self):
        gathered = dict()
        soup = bs(self.node.cache, 'html.parser')
        for tag, value in self.form.items():
            self.logger.info(tag)
            result = getattr(soup, value['method'])(value['tag'])
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
                text_content = stub.get_text(strip=True)  # 텍스트에서 공백 제거
                cleaned_text = clean_text(text_content)
                gathered[tag] = [{'text': cleaned_text, 'attrs': stub.attrs} for stub in result]

        return gathered
    
