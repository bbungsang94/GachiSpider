import logging
from spider.crawler import BatchCrawler
from spider.utils.logging import init_logging


def main(url):
    from spider.utils.web import get_base_url
    init_logging(logging.INFO, "batch_test.log")
    base_url = get_base_url(url)
    crawler = BatchCrawler(base_url=base_url, batch_code="/mirror/re.php?ss=")
    crawler.crawl(url)
    pass

if __name__ == "__main__":
    import sys
    # sys.setrecursionlimit(10000)
    # "https://aagag.com/mirror/?select=multi&site=bobae|clien|fmkorea|inven|mlbpark|ou|ppomppu|ruli|slrclub"
    for stub in ["ruli", "inven", "fmkorea", "bobae", "clien", "ou", "ppomppu", "mlbpark", "slrclub"]:
        #https://aagag.com/mirror/?site=inven&select=multi
        main("https://aagag.com/mirror/?site=%s&time=24&select=multi" % stub)