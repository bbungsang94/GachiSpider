import logging
import os
import os.path as osp
import json

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
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

def get_db_client(config):
    config['database'] = get_secret(**config)
    client = MongoClient(config['database']['uri'])
    runtime_db = client['Pages']
    collection = runtime_db['Nodes']
    return collection

def get_secret(name, region, pem, key, **kwargs):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region,
        **key
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=name
        )
    except ClientError as e:
        raise e

    secret = json.loads(get_secret_value_response['SecretString'])
    username = secret["username"]
    password = secret["password"]
    host = secret["host"]
    port = secret.get("port", 27017)
    
    # MongoDB URI 설정
    uri = f"mongodb://{username}:{password}@{host}:{port}/?ssl=true&retryWrites=false&tlsAllowInvalidCertificates=true"
    
    args = {
        'username': username,
        'password': password,
        'host': host,
        'port': port,
        'uri': uri
    }
    return args

def main():
    config_root = "./spider/configs"
    credential_root = "./credential/aws_authorization_key"
    lambda_credential = get_configs(credential_root, "iam.json")['lambda']
    db_credential = get_configs(credential_root, "iam.json")['document-db']
    scheduler_config = get_configs(config_root, "scheduler.json")
    scheduler_config.update({"credential": lambda_credential})
    root_nodes = get_configs(config_root, "root nodes.json")
    
    boto_config = Config(
        read_timeout=60 * 15
    )
    link_manager_client = boto3.client(lambda_credential['name'], **lambda_credential['key'], config=boto_config)  
    scheduler = Scheduler(config=scheduler_config, roots=root_nodes, logger=get_logger(),
                          db_handle=get_db_client(db_credential),
                          link_manager=link_manager_client)
    scheduler.run()
    
if __name__ == "__main__":
    print(os.getcwd())
    main()