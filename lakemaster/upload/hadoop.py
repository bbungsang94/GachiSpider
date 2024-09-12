import os
import json
from pyarrow import fs

class HadoopUploader:
    def __init__(self, ip: str, port: int):
        self.url = "hdfs://%s" % (ip)
        self._hdfs = fs.HadoopFileSystem(ip, port, user="hdfs")
    
    def upload(self, file, filename, path="./"):
        full_path = os.path.join(path, filename)
        with self._hdfs.open_output_stream(full_path) as native_f:
            json.dump(file, native_f)
            

if __name__ == "__main__":
    test_path = r"D:\Creadto\GachiSpider\datalake\yellow_zone\fmkorea\7382399770.json"
    with open(test_path, 'r', encoding='utf-8-sig') as f:
        json_dict = json.load(f)
     
    uploader = HadoopUploader(ip="211.188.54.139", port=9000)
    uploader.upload(json_dict, filename="dump.json")
    