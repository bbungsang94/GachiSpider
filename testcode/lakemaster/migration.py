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

def read_key(full_path: str = r"D:\Shared\GachiSpider\ncp_authorization_key\access_key-secret.json"):
    with open(full_path, 'r') as f:
        data = json.load(f)
    return data

def read_storages(key_pair):
    url = "https://kr.object.ncloudstorage.com"
    region = "kr-standard"
    latest_client = None
    for key_id, secret_key in key_pair.items():
        latest_client = boto3.client("s3", endpoint_url=url,
                          aws_access_key_id=key_id,
                          aws_secret_access_key=secret_key)
        response = latest_client.list_buckets()
        for bucket in response.get("Buckets", []):
            print(bucket.get('Name'))
    return latest_client
    
def upload_zone(client, bucket_name, cache_root, **kwargs):
    bucket_root = kwargs['bucket_root'] if 'bucket_root' in kwargs else '' 
    folders = os.listdir(cache_root)
    for folder in tqdm(folders):
        storage_path = os.path.join(bucket_root, folder) + '/'
        client.put_object(Bucket=bucket_name, Key=storage_path)
        files = os.listdir(os.path.join(cache_root, folder))
        for filename in files:
            cache_path = os.path.join(cache_root, folder, filename)
            upload_path = os.path.join(storage_path, filename)
            result = client.upload_file(cache_path, bucket_name, upload_path, Callback=ProgressPercentage(cache_path))

def main():
    key = read_key()
    client = read_storages(key)
    upload_zone(client, bucket_name='creadto-hadoop-bucket',
                cache_root=r"D:\Creadto\GachiSpider\datalake\red_zone",
                bucket_root="red_zone/")
    
    
if __name__ == "__main__":
    main()