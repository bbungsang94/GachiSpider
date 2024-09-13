import logging
import requests
from urllib.parse import urljoin
from spider.structure import Node
from . import __name__
from .matcher import Matcher
from .state import State, Fetch

class Crawler:
    def __init__(self, init_url, valid_robots=False, name="Crawler"):
        self.logger = logging.getLogger(name=name)
        self.init_url = init_url
        
        response = requests.get(urljoin(base=self.init_url, url='robots.txt'))
        self.matcher = Matcher(mass=response.text, name=self.name)
        
        self.name = __name__
        self.state = None
        self.cache = None
        self.trajectory = set()
    
    def crawl(self, url):
        if url in self.trajectory:
            return
        
        self.trajectory.add(url)
        allow, reason = True, ""
        if self.matcher is not None:
            allow, reason = self.matcher.allow_by(url=url)
        self.logger.info("%s, %s, url:%s" % (allow, reason, url))
        if allow:
            return self.transit(Fetch(Node(url=url), parent=self))
        
    def transit(self, next_state: State, auto_run: bool = True):          
        self.state = next_state
        if auto_run:
            self.state.run()
            