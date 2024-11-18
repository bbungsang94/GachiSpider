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

if __name__ == "__main__":
    main()