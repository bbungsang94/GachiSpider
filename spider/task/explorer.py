import os.path as osp
import logging
from typing import List
from spider.crawler.parse import Parse
from spider.structure import Node


class GraphExplorer:
    def __init__(self, source_urls: List[str]):
        self.logger = logging.getLogger(name="explorer")
        self.search_space = set()
        # Crawler define
        self.crawler = Parse(source_urls[0])
        next_urls, _ = self.crawler.run()
        self.search_space.update([x.url for x in next_urls])
        # Graph structures
        self.adj_list = dict()
        self.insert_adj(source_urls[0], next_urls)
        
        self.load_checkpoint()
            
    def step(self):
        iteration = 0
        while(len(self.search_space) != 0):
            iteration += 1
            
            url = self.get_next_url()
            self.crawler.attach(url)
            next_urls, next_nodes = self.crawler.run()
            self.search_space.update([x.url for x in next_urls])
            
            self.insert_adj(url, next_nodes)
            display = "Search space: %d, Get Found Urls: %d" % (len(self.search_space), len(next_urls))
            self.logger.info(display)
            
            if iteration % 10 == 0:
                self.save_checkpoint()

    def get_next_url(self):
        url = self.search_space.pop()
        if url in self.adj_list:
            self.logger.info("Search space: %d, Exists url: %s" % (len(self.search_space), url))
            return self.get_next_url()
        else:
            return url
    
    def insert_adj(self, key, nodes: List[Node]):
        urls = set([x.url for x in nodes])
        if key not in self.adj_list:
            self.adj_list[key] = urls
        
    def save_checkpoint(self):
        import pickle
        with open('latest_adj_table.pickle','wb') as fw:
            pickle.dump(self.adj_list, fw)
        with open('latest_search_space.pickle','wb') as fw:
            pickle.dump(list(self.search_space), fw)

    def load_checkpoint(self, root=""):
        import pickle
        if osp.exists(osp.join(root, 'latest_adj_table.pickle')):
            with open(osp.join(root, 'latest_adj_table.pickle'), 'rb') as f_adj:
                adj = pickle.load(f_adj)
            self.adj_list = adj
        
        if osp.exists(osp.join(root, 'latest_search_space.pickle')):
            with open(osp.join(root, 'latest_search_space.pickle'), 'rb') as f_space:
                space = pickle.load(f_space)
            self.search_space = set(space)
            