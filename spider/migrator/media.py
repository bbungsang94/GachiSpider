from abc import ABC, abstractmethod
import os

class DataDownloader(ABC):
    @abstractmethod
    def read_data(self):
        pass
    
    @abstractmethod
    def update_data(self):
        pass
    
    @abstractmethod
    def extract_urls(self, data):
        pass
    
    @abstractmethod
    def download_media(self, url, save_path):
        pass
    
    def run(self, save_dir):
        """
        작업 흐름을 실행하는 메소드. 데이터를 읽고 URL을 추출한 뒤, 해당 URL에서 미디어를 다운로드.
        """
        data = self.read_data()
        urls = self.extract_urls(data)
        
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        for url in urls:
            filename = os.path.join(save_dir, url.split('/')[-1])  # 파일 이름을 URL에서 추출
            self.download_media(url, filename)

class MongoDBDownloader(DataDownloader):
    """_summary_
    # 매칭되는 이미지, 비디오, 텍스트를 확인하고
    # 이미지, 비디오는 다운로드 후 링크를 가지고 있는다.
    Args:
        DataDownloader (_type_): _description_
    """
    def __init__(self, db_ip, db_port):
        pass
    
    def read_data(self):
        return super().read_data()
    
    def update_data(self):
        return super().update_data()
    
    def extract_urls(self, data):
        return super().extract_urls(data)
    
    def download_media(self, url, save_path):
        return super().download_media(url, save_path)