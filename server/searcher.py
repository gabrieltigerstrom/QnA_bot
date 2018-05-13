import argparse
import os
from elasticsearch import Elasticsearch
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Search
from sent_sim import *
# import nltk

if __name__ == "__main__":
    # nltk.download('punkt')
    parser = argparse.ArgumentParser(prog='searcher.py',
            description='Testing script for searching related subforums')
    parser.add_argument('forum',type=str)
    parser.add_argument('doc_type',type=str,choices=['questions'])
    parser.add_argument('query',type=str)
    parser.add_argument('--max_size',type=int,default=10,help="at most return that number of q")
    parser.add_argument('--mark',default='main',type=str,help='for DEBUG')
    parser.add_argument('--local',action='store_true',help='for local test')

    args = parser.parse_args()
    index = '{forum}_{doc_type}_{mark}'.format(**vars(args))
    
    if args.local:
        connections.create_connection(hosts=['localhost'])
    else:
        connections.create_connection(hosts=['elasticsearch'])

    similar_queires = find_similar_query(args.query,connections.get_connection(),index,args.max_size)
    for q in similar_queires:
        print(q['sim_score'])
