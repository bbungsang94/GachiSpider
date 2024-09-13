import logging
from spider.crawler.linker import CloudLinker
from spider.utils.logging import init_logging

def main():
    init_logging(logging.DEBUG, "linker-test-above-cloud.log")
    link_manager = CloudLinker(init_url="https://aagag.com/", db_ip="localhost", db_port=27017)
    link_manager.crawl(url="https://aagag.com/mirror/?site=mlbpark&time=24&select=multi")
    

if __name__ == "__main__":
    main()