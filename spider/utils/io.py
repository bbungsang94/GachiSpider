import json
import os.path as osp

def get_json(root, filename):
    with open(osp.join(root, filename)) as f:
        config = json.load(f)
    
    return config
