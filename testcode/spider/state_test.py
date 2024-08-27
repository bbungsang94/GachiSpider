import logging
from spider.crawler import Crawler
from spider.utils.logging import init_logging

def main():
    init_logging(logging.DEBUG, "parser_test.log")
    crawler = Crawler("https://mlbpark.donga.com/")
    crawler.crawl("https://mlbpark.donga.com/mp/b.php?p=1&b=bullpen&id=202408170096347919&select=&query=&subselect=&subquery=&user=&site=&reply=&source=&pos=&sig=h4aTGf-1j3HRKfX2hfj9RY-g5mlq")
    # url 탐색도 하고, 
    crawler.cache
    pass

if __name__ == "__main__":
    main()