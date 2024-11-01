import logging
from spider.manager.linker import CloudLinker
from spider.utils.logging import init_logging

def main():
    init_logging(logging.DEBUG, "linker-test-above-cloud.log")
    link_manager = CloudLinker(init_url="https://aagag.com/", db_ip="localhost", db_port=27017)
    next_url = link_manager.crawl(url="https://aagag.com/mirror/?select=multi&site=82cook|bobae|clien|damoang|ddanzi|etoland|fmkorea|humor|inven|mlbpark|ou|ppomppu|ruli|slrclub")
    
    

if __name__ == "__main__":
    main()