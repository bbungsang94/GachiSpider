import copy
from typing import List
from spider.structure.node import Node


def sync_database(nodes: List[Node], collection, use_cache=True):
    nodes = copy.deepcopy(nodes)
    urls = [x.url for x in nodes]
    
    for i, node in enumerate(nodes):
        if len(node.fan_out) > 0 and isinstance(node.fan_out[0], Node):
            nodes[i].fan_out = [x.url for x in nodes]
        if use_cache == False:
            nodes[i].cache = None
            
    existing_nodes = collection.find({"url": {"$in": urls}}, Node.get_fields(begin=1))
    existing_nodes = [Node.from_dict(node) for node in existing_nodes]
    for node in existing_nodes:
        query = {'url': node.url}      
        contents = {"$set": node.to_dict()}
        collection.update_one(query, contents)
    
    existing_set = {node.url for node in existing_nodes}
    new_nodes = [node for node in nodes if node.url not in existing_set]
    if len(new_nodes) > 0:
        collection.insert_many([node.to_dict() for node in new_nodes])
    
    return existing_nodes + new_nodes