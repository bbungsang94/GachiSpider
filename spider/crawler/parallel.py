import logging
from celery import Celery
from spider.structure import Node
from spider.utils.web import get_base_url
from . import Crawler
from .state import State, Gather, Failed

app = Celery('crawls', broker='amqp://bbungsang94:151212kyhASH@localhost:5672//')
 
@app.task
def crawl_once(node):
    parser = Parser(node=node)
    parser.run()
    return parser.state.node


class Parser(Crawler):
    def __init__(self, node: Node):
        super(Parser, self).__init__(init_url=get_base_url(node.url))
        self.logger = logging.getLogger(name="RabbitMQ Parser")
        self.node = node
                
    def crawl(self, url):
        if self.node.cache is None:
            self.transit(Failed(self.node, parent=self))
        else:
            self.transit(Gather(self.node, parent=self))
    
    def transit(self, next_state: State, auto_run: bool = True):          
        self.state = next_state
        if auto_run:
            self.state.run()
    