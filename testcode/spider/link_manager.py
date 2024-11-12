import os.path as osp
import json
import logging

import boto3
from botocore.exceptions import ClientError
from spider.manager.linker import CloudLinker
from spider.utils.logging import init_logging

def get_configs(root, filename):
    with open(osp.join(root, filename)) as f:
        config = json.load(f)
    
    return config

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
    init_logging(logging.DEBUG, "linker-test-above-cloud.log")
    credential_root = "./credential/aws_authorization_key"
    db_credential = get_configs(credential_root, "iam.json")['document-db']
    db_config = get_secret(**db_credential)
    
    link_manager = CloudLinker(init_url="https://aagag.com/", db_ip=db_config['uri'], db_port=None)
    next_url = link_manager.crawl(url="https://aagag.com/mirror/?select=multi&site=82cook|bobae|clien|damoang|ddanzi|etoland|fmkorea|humor|inven|mlbpark|ou|ppomppu|ruli|slrclub")
    
    

if __name__ == "__main__":
    main()