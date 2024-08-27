import logging
import requests
from urllib.parse import urljoin
from spider.structure import Node
from . import __name__
from .matcher import Matcher
from .state import State, Fetch

class Crawler:
    def __init__(self, base_url, valid_robots=False):
        self.logger = logging.getLogger(name="Crawler")
        self.base_url = base_url
        
        self.matcher = None
        if valid_robots:
            response = requests.get(urljoin(base=self.base_url, url='robots.txt'))
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
            