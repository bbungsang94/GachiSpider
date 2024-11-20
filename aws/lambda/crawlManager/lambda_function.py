import logging
from spider.manager.linker import CloudLinker
from spider.utils.logging import init_logging

def lambda_handler(event, context):
    url = event.get('url')
    db_ip = event.get('db_ip')
    db_port = event.get('db_port')
    
    init_logging(logging.DEBUG, "link-manager-using-lambda.log", dir_path='/tmp/')
    link_manager = CloudLinker(init_url=None, db_ip=db_ip, db_port=db_port)
    
    result_dict = {'root': url, 'db_ip': db_ip, 'db_port': db_port}
    if link_manager.collection == None:
        result_dict.update({'statusCode': 301, 'message': "Failed DB Connection"})
    else:
        result_dict.update(link_manager.crawl(url=url))
    return result_dict