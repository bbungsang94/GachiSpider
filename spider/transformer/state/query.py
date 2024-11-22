from spider.structure import Node, State

class Query(State):
    def __init__(self, node: Node, parent):
        super(Query, self).__init__("query", node=node, parent=parent)
    
    def run(self):
        pass
        
    def pause(self):
        pass
    
    def stop(self):
        pass
    