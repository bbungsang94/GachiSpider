import logging

from pymongo import MongoClient
from spider.structure import Node
from spider.scheduler.event import LambdaScheduler
from spider.utils.logging import init_logging

def main():
    init_logging(logging.DEBUG, "parser-test-using-lambda.log")
    db_ip, db_port = "110.165.19.253", 27017
    nodes = get_null_labels(db_ip=db_ip, db_port=db_port)
    crawler = LambdaScheduler(db_ip=db_ip, db_port=db_port)
    for node in nodes:
        crawler.parse(url=node.url)
    pass

def get_null_labels(db_ip="localhost", db_port=27017):
    client = MongoClient(host=db_ip, port=db_port)
    server_info = client.server_info()
    runtime_db = client['RuntimeDB']
    collection = runtime_db['Trajectories']
    existing_nodes = collection.find({"url": {"$regex": "https://mlbpark.donga.com/"}}, Node.get_fields(begin=1))
    existing_nodes = [Node.from_dict(node) for node in existing_nodes]
    eliminate_duplicated_data(existing_nodes, collection)
    return existing_nodes

def eliminate_duplicated_data(nodes, collection):
    duplicated_dict = dict()
    for node in nodes:
        if node.url not in duplicated_dict:
            duplicated_dict[node.url] = []
        duplicated_dict[node.url].append(node)
    
    for url, node_list in duplicated_dict.items():
        if len(node_list) == 1:
            continue
        for idx in range(1, len(node_list)):
            query = {'url': node_list[idx].url, "last_visited": node_list[idx].last_visited}
            result = collection.delete_one(query)

if __name__ == "__main__":
    main()