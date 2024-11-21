import logging
from spider.crawler import LambdaCrawler
from spider.utils.logging import init_logging

def main():
    init_logging(logging.DEBUG, "crawler-test-using-lambda.log")      
    db_ip, db_port = "110.165.19.253", 27017
    crawler = LambdaCrawler(db_ip=db_ip, db_port=db_port)
    next_url = crawler.crawl(url=r"https://www.bobaedream.co.kr/view?code=strange&No=6301703")
    pass
    

if __name__ == "__main__":
    main()