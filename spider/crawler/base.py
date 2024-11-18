import logging
import requests
from pymongo import MongoClient
from urllib.parse import urljoin
from spider.structure import Node
from .matcher import Matcher
from spider.manager.state import State, Fetch, UpdateMongo

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
    
    def eliminate_duplicated_data(self, nodes, collection):
        duplicated_dict = dict()
        for node in nodes:
            if node.url not in duplicated_dict:
                duplicated_dict[node.url] = []
            duplicated_dict[node.url].append(node)
        
        for url, node_list in duplicated_dict.items():
            if len(node_list) == 1:
                continue
            for idx in range(1, len(node_list)):
                query = {'url': node_list[idx].url, "last_visited": node_list[idx].last_visited}
                result = collection.delete_one(query)
        
        return nodes[0]

class LambdaCrawler(Crawler):
    def __init__(self, db_ip, db_port, **kwargs):
        super(LambdaCrawler, self).__init__(init_url=None)
        self.logger = logging.getLogger(name="Lambda script")
        
        try:
            client = MongoClient(host=db_ip, port=db_port)
            self.logger.info("Mongo Client: {0}".format(client))
            server_info = client.server_info()
            self.logger.info("Server Information: {0}".format(server_info))
            self.collection = client['Pages']
            self.collection = self.collection['Nodes']
        except Exception as e:
            self.logger.error("Failed DB connection")
            return None
        
    def crawl(self, url):
        try:
            existing_nodes = self.collection.find({"url": {"$in": [url]}}, Node.get_fields(begin=1))
            existing_nodes = [Node.from_dict(node) for node in existing_nodes]
        except Exception as e:
            self.logger.error("Not found url, Please check endpoint")
            return "Not found url, Please check endpoint"
        
        if len(existing_nodes) != 1:
            self.logger.warning("Duplicated %s, Merge information" % (existing_nodes[0].url))
            existing_nodes = self.eliminate_duplicated_data(existing_nodes, self.collection)
        existing_node = existing_nodes[-1]
        if existing_node.label == None:
            self.state = Fetch(node=existing_node, parent=self)
            self.state.run()
            return self.state.node.label
        else:
            return existing_node.label
    
    def transit(self, next_state: State, auto_run: bool = True):
        self.state = next_state
        if next_state.name == "store":
            self.state = UpdateMongo(node=next_state.node, parent=self,
                                     collection=self.collection)         
        elif next_state.name == "failed":
            self.state = UpdateMongo(node=next_state.node, parent=self,
                                     collection=self.collection,
                                     leaf=True, label_pass=True)
        if auto_run:
            self.state.run()