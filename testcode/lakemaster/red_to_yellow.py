import os
import filter
from spider.structure import Node


def main(red_root=r"D:\Creadto\GachiSpider\datalake\red_zone"):
    filter.app.control.purge()
    # node 불러옴
    # 글 포맷 저장
    # 글 순서 저장
    # 멀티미디어가 있을 경우 저장 후 로컬링크로 변환
    yellow_root = r"D:\Creadto\GachiSpider\datalake\yellow_zone"
    
    folder_list = os.listdir(red_root)
    for folder in folder_list:
        filter.working.delay(search_space=os.path.join(red_root, folder))

def debug(red_root=r"D:\Creadto\GachiSpider\datalake\red_zone"):
    filt = filter.YellowFilter(os.path.join(red_root, "mlbpark.donga.com"))
    filt.migrate(fast=False)
    
if __name__ == "__main__":
    main()