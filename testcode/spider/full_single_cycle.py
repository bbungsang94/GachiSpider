import logging
import os
import os.path as osp
import json

import boto3
from pymongo import MongoClient
from spider.scheduler import Scheduler
from spider.utils.logging import init_logging

def get_configs(root, filename):
    with open(osp.join(root, filename)) as f:
        config = json.load(f)
    
    return config

def get_logger():
    init_logging(logging.INFO, "batch_test.log")
    return logging.getLogger("Base")

def get_db_client(db_ip, db_port):
    client = MongoClient(host=db_ip, port=db_port)
    runtime_db = client['RuntimeDB']
    collection = runtime_db['Trajectories']
    return collection

def main():
    config_root = "./spider/configs"
    credential_root = "./credential/aws_authorization_key"
    lambda_credential = get_configs(credential_root, "iam.json")['lambda']
    scheduler_config = get_configs(config_root, "scheduler.json")
    scheduler_config.update({"credential": lambda_credential})
    root_nodes = get_configs(config_root, "root nodes.json")

    link_manager_client = boto3.client(lambda_credential['name'], **lambda_credential['key'])  
    
    scheduler = Scheduler(config=scheduler_config, roots=root_nodes, logger=get_logger(),
                          db_handle=get_db_client("110.165.19.253", 27017),
                          link_manager=link_manager_client)
    scheduler.run()
    
if __name__ == "__main__":
    print(os.getcwd())
    main()