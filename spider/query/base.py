
from datetime import datetime
import logging

import pymysql

from spider.structure import State


class Handler:
    def __init__(self, **kwargs):
        self.logger = logging.getLogger(name="QueryHandler")
      
        try:
            self.db_client = pymysql.connect(**kwargs)
            self.created_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            raise ConnectionError

    def run(self):
        pass
    
    def transit(self, next_state: State, auto_run: bool = True):          
        self.state = next_state
        
        if auto_run:
            self.state.run()


if __name__ == "__main__":
    import os
    DB_HOST = os.getenv('host')  # RDS Endpoint
    DB_USER = os.getenv('user')  # 사용자 이름
    DB_PASSWORD = os.getenv('password')  # 비밀번호
    DB_NAME = os.getenv('database')  # 데이터베이스 이름
