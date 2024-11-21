import os
import json
import requests
import pickle
import logging
from urllib.parse import urljoin
from celery import Celery
from spider.structure import Node
from spider.utils.logging import init_logging
    
    
app = Celery('tasks', broker='amqp://bbungsang94:151212kyhASH@localhost:5672//')
 
@app.task
def working(search_space):                
    filter = YellowFilter(search_space)
    filter.migrate()


class YellowFilter:
    def __init__(self, search_space, root=r"D:\Creadto\GachiSpider\datalake"):
        self.search_files = os.listdir(search_space)
        self.search_files = [os.path.join(search_space, x) for x in self.search_files]
        domain = os.path.split(search_space)[-1]
        self.domain = domain.split('.')[0]
        self.yellow_root = os.path.join(root, "yellow_zone")
        
        init_logging(logging.INFO, self.domain + "-unsync-worker.log")
        self.logger = logging.getLogger(name=self.domain + "-worker")
        
    def migrate(self, fast=True):
        folder_path = os.path.join(self.yellow_root, self.domain)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
                
        for filename in self.search_files:
            save_path = os.path.join(folder_path, os.path.split(filename)[-1])
            save_path = save_path.replace(".pkl", ".json")
            if os.path.exists(save_path):
                self.logger.info("Already exists file")
                if fast:
                    continue
            
            self.logger.info("Load node file: %s" % filename)
            with open(filename, 'rb') as f:
                node: Node = pickle.load(f)
            data = node.data
            
            docs = dict()
            for key, contents in data.items():
                values = []
                self.logger.info("Processed %s" % key)
                for content in contents:
                    if 'src' in content['attrs']:
                        media_path = os.path.join(self.yellow_root, key)
                        media_list = os.listdir(media_path)
                        try:
                            # multi-media는 platform=-free 영역임
                            self.logger.info("Download media file from %s" % content['attrs']['src'])
                            response = requests.get(urljoin("https://", content['attrs']['src']), headers={'User-Agent': 'Media-Checker'})
                            if response.status_code != 200:
                                raise ConnectionError
                            media_link = os.path.join(media_path, self.domain + "-%08d" % (len(media_list)))
                            # 확장자를 자동으로 찾아야함
                            if key == "images":
                                if ".gif" in content['attrs']['src']:
                                    media_link += ".gif"
                                else:
                                    media_link += ".jpg"
                            elif key == "videos":
                                media_link += ".mp4"
                            
                            self.logger.info("Save media file into %s" % media_link)
                            with open(media_link, 'wb') as file:
                                file.write(response.content)
                        except Exception as e:
                            self.logger.warning("Failed download file(%s) \n reason: %s" % (content['attrs']['src'], e))
                            media_link = "Failed"
                        values.append(media_link)
                    else:
                        values.append(content['text'])
                docs[key] = values
            
            self.logger.info("Save new docs in yellow zone")
            docs['source'] = node.url
            with open(save_path, 'w', encoding='utf-8-sig') as json_f:
                json.dump(docs, json_f, ensure_ascii=False)