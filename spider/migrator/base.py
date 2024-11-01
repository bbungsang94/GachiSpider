from typing import List

from pymongo import MongoClient
from spider.structure import Node
from spider.utils.web import get_unwrapped_url


class Migrator:
    def __init__(self, db_ip, db_port):
        client = MongoClient(host=db_ip, port=db_port)
        self.logger.info("Mongo Client: {0}".format(client))
        server_info = client.server_info()
        self.logger.info("Server Information: {0}".format(server_info))
        self.runtime_db = client['RuntimeDB']
        self.collection = self.runtime_db['Trajectories']
        
    def run(self, nodes: List[Node]):
        # html을 통해서
        # 매칭되는 이미지, 비디오, 텍스트를 확인하고
        # 이미지, 비디오는 다운로드 후 링크를 가지고 있는다.
        # 그 링크를 html과 대체한다.
        # # 이 때 필요한 text, image, video 태그는 정해져있다. 그러므로 태그대체식을 사용한다.
        # 이게 완료되면 freshness는 프리즈(-1)로 변경된다.
        pass
    
    def _download_to_link(self, url):
        pass