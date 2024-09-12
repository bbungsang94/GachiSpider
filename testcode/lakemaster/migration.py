import os
import json
import sys
import threading
import boto3
from tqdm import tqdm

class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()

def read_key_chain(full_path: str = r"D:\Shared\05.GachiSpider\ncp_authorization_key\access_key-secret.json"):
    with open(full_path, 'r') as f:
        data = json.load(f)
    return data

def read_storages(key_pair, url="https://kr.object.ncloudstorage.com", region="kr-standard"):
    latest_client = None
    for key_id, secret_key in key_pair.items():
        latest_client = boto3.client("s3", endpoint_url=url,
                          aws_access_key_id=key_id,
                          aws_secret_access_key=secret_key,
                          region_name=region)
        response = latest_client.list_buckets()
        for bucket in response.get("Buckets", []):
            print(bucket.get('Name'))
    return latest_client

def upload_zone(client, bucket_name, cache_root, **kwargs):
    bucket_root = kwargs['bucket_root'] if 'bucket_root' in kwargs else '' 
    files = os.listdir(cache_root)
    for file in files:
        cache_path = os.path.join(cache_root, file)
        if os.path.isdir(cache_path):
            storage_path = os.path.join(bucket_root, file) + '/'
            client.put_object(Bucket=bucket_name, Key=storage_path)
            upload_zone(client, bucket_name, cache_root=cache_path, bucket_root=storage_path)
        else:
            upload_path = os.path.join(bucket_root, file)
            result = client.upload_file(cache_path, bucket_name, upload_path, Callback=ProgressPercentage(cache_path))
            pass
            
def main():
    key = read_key_chain()
    client = read_storages(key['ROOT'], url="https://kr.archive.ncloudstorage.com", region="kr")
    upload_zone(client, bucket_name='creadto-archive',
                cache_root=r"D:\Shared",
                bucket_root="")
    
    
if __name__ == "__main__":
    main()