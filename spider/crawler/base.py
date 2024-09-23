import logging
import requests
from pymongo import MongoClient
from urllib.parse import urljoin
from spider.structure import Node
from .matcher import Matcher
from .state import State, Fetch, UpdateMongo

class Crawler:
    def __init__(self, init_url, valid_robots=False, name="Crawler"):
        self.logger = logging.getLogger(name=name)
        self.init_url, self.matcher = None, None
        if init_url is not None:
            self.init_url = init_url
            
            response = requests.get(urljoin(base=self.init_url, url='robots.txt'))
            self.matcher = Matcher(mass=response.text)
        
        self.name = name
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

class LambdaCrawler(Crawler):
    def __init__(self, db_ip, db_port):
        super(LambdaCrawler, self).__init__(init_url=None)
        self.logger = logging.getLogger(name="Lambda script")
        
        client = MongoClient(host=db_ip, port=db_port)
        self.logger.info("Mongo Client: {0}".format(client))
        server_info = client.server_info()
        self.logger.info("Server Information: {0}".format(server_info))
        self.runtime_db = client['RuntimeDB']
        
    def crawl(self, url):
        collection = self.runtime_db['Trajectories']
        existing_nodes = collection.find({"url": {"$in": [url]}}, Node.get_fields(begin=1))
        if existing_nodes is None:
            raise FileNotFoundError
        existing_nodes = [Node.from_dict(node) for node in existing_nodes]
        if len(existing_nodes) != 1:
            raise "Duplicated information"
        existing_node = existing_nodes[-1]
        state = Fetch(node=existing_node, parent=self)
        state.run()
    
    def transit(self, next_state: State, auto_run: bool = True):
        self.state = next_state
        if next_state.name == "store":
            self.state = UpdateMongo(node=next_state.node, parent=self, collection=self.runtime_db['Trajectories'])         
        if auto_run:
            self.state.run()