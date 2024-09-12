import os
import mimetypes
import swiftclient
from keystoneauth1 import session
from keystoneauth1.identity import v3

def put_file(handle, bucket_name, upload_path, cache_path):
    content_type, _ = mimetypes.guess_type(cache_path)
    if content_type is None:
        content_type = 'application/octet-stream'  # MIME 타입

    with open(cache_path, 'rb') as local_file:
        handle.put_object(bucket_name, upload_path,
                          contents=local_file,
                          content_type=content_type)

def put_dir(handle, bucket_name, folder_path):
    content_type = 'application/directory'

    handle.put_object(bucket_name, folder_path,
                      contents='',  # empty content
                      content_type=content_type)

def upload_zone(handle, bucket_name, cache_root, **kwargs):
    bucket_root = kwargs['bucket_root'] if 'bucket_root' in kwargs else '' 
    files = os.listdir(cache_root)
    for file in files:
        cache_path = os.path.join(cache_root, file)
        if os.path.isdir(cache_path):
            storage_path = os.path.join(bucket_root, file) + '/'
            # put_dir(handle, bucket_name, storage_path)
            upload_zone(handle, bucket_name, cache_root=cache_path, bucket_root=storage_path)
        else:
            upload_path = os.path.join(bucket_root, file)
            put_file(handle, bucket_name, upload_path, cache_path)
        
        
def main():
    endpoint = 'https://kr.archive.ncloudstorage.com:5000/v3'
    username = 'ncp_iam_BPAMKR3ktoHzF2YpH50p'
    password = 'ncp_iam_BPKMKRF8qsRo8ltMmd6FI7aceUHsH2DoEG'
    domain_id = 'default'
    project_id = 'cef7ff5f42d546febca16eefbada6a1d'

    auth = v3.Password(auth_url=endpoint, username=username, password=password, project_id=project_id, user_domain_id=domain_id)
    auth_session = session.Session(auth=auth)

    swift_connection = swiftclient.Connection(retries=5, session=auth_session)

    upload_zone(swift_connection, bucket_name='creadto-archive',
            cache_root=r"D:\Shared",
            bucket_root="")


if __name__ == "__main__":
    main()