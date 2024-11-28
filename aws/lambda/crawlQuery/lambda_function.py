import logging
import os

from spider.query import GachiGaHandler
from spider.structure import Node
from spider.utils.logging import init_logging

def lambda_handler(event, context):
    kw_map = {'statusCode': 'status', 'message': 'message',
              'root': 'root_url', 'urls': 'urls',
              'db_ip': 'db_ip', 'db_port': 'db_port',
              'nodes': 'nodes'}
    
    kwargs = dict()
    for event_key, key in kw_map.items():
        kwargs[key] = event.get(event_key)

    init_logging(logging.INFO, "query-to-rdb-using-lambda.log", dir_path='/tmp/')
    handler_kwargs = {
        "host": os.getenv("host"),
        "user": os.getenv("user"),
        "password": os.getenv("password"),
        "database": os.getenv("database"),
    }
    try:
        handler = GachiGaHandler(**handler_kwargs)
        for node_raw in kwargs['nodes']:
            node = Node.from_dict(node_raw)
            handler.run(node=node)
        handler.db_client.close()
        return {'statusCode': 200, 'message': "Succeeded"}
    
    except Exception as e:
        pass
        return {'statusCode': -1, 'message': "Unexpected exit"}

def make_dummy_nodes(db_ip, db_port=None):
    from pymongo import MongoClient
    from spider.utils.mongo import get_data_with
    
    client = MongoClient(host=db_ip, port=db_port)
    server_info = client.server_info()
    collection = client['Pages']
    collection = collection['Nodes']
    
    alternatives = get_data_with(collection, label='Transformed')
    return [x.to_dict() for x in alternatives]
