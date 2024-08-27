import pickle
import os.path as osp
from scheduler.linear import LinearScheduler
from utils.graph import to_graph
            
def main(root="./"):
    if osp.exists(osp.join(root, 'latest_adj_table.pickle')):
        with open(osp.join(root, 'latest_adj_table.pickle'), 'rb') as f_adj:
            adj = pickle.load(f_adj)
    
    if osp.exists(osp.join(root, 'latest_search_space.pickle')):
        with open(osp.join(root, 'latest_search_space.pickle'), 'rb') as f_space:
            space = pickle.load(f_space)

    graph = to_graph(adj_table=adj)
    scheduler = LinearScheduler()

if __name__ == "__main__":
    main()