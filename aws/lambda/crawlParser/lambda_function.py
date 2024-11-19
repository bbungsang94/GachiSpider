import logging
from spider.crawler import LambdaCrawler
from spider.utils.logging import init_logging

def lambda_handler(event, context):
    kw_map = {'statusCode': 'status', 'message': 'message',
              'root': 'root_url', 'urls': 'urls',
              'db_ip': 'db_ip', 'db_port': 'db_port'}
    
    kwargs = dict()
    for event_key, key in kw_map.items():
        kwargs[key] = event.get(event_key)

    init_logging(logging.DEBUG, "parser-using-lambda.log", dir_path='/tmp/')
    parser = LambdaCrawler(**kwargs)
    
    result_dict = kwargs
    if parser == None:
        result_dict.update({'statusCode': 301, 'message': "Failed DB Connection"})
    else:
        for url in kwargs['urls']:
            stub = {url: parser.crawl(url=url)}
            result_dict.update(stub)
        result_dict.update({'statusCode': 201, 'message': "Unclearly Succeeded"})
    return result_dict

    
if __name__ == "__main__":
    kw_event = {
        "root": "https://aagag.com/mirror/?orderby=hit&site=bobae|inven|ruli|mlbpark|ppomppu&time=12&select=multi",
        "db_ip": "mongodb://lakemaster:zmflxh1004!@creadto-gachirok-datalake.cluster-cbtcjvjycynl.ap-northeast-2.docdb.amazonaws.com:27017/?ssl=true&retryWrites=false&tlsAllowInvalidCertificates=true",
        "urls": [
            "https://www.bobaedream.co.kr/view?code=strange&No=6349621",
            "https://bbs.ruliweb.com/community/board/300143/read/68459669",
            "https://bbs.ruliweb.com/community/board/300143/read/68456866",
            "https://mlbpark.donga.com/mp/b.php?p=1&b=bullpen&id=202411180099294108&select=&query=&subselect=&subquery=&user=&site=&reply=&source=&pos=&sig=h6jLGY2Akh6RKfX2hfjXGY-gLmlq",
            "https://bbs.ruliweb.com/community/board/300143/read/68459732",
            "https://bbs.ruliweb.com/community/board/300143/read/68457968",
            "https://bbs.ruliweb.com/community/board/300143/read/68457261",
            ]
        }
    print(lambda_handler(event=kw_event, context=None))