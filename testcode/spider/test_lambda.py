import logging
from spider.crawler.base import LambdaCrawler
from spider.utils.logging import init_logging

def main():
    init_logging(logging.DEBUG, "crawler-test-using-lambda.log")
    crawler = LambdaCrawler(db_ip="localhost", db_port=27017)
    next_url = crawler.crawl(url=r"https://bbs.ruliweb.com/community/board/300143/read/67752603")
    pass
    

if __name__ == "__main__":
    main()