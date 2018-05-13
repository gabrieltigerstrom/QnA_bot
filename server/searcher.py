import argparse
import os
from elasticsearch import Elasticsearch
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Search
from sent_sim import *
import nltk

if __name__ == "__main__":
    nltk.download('punkt')
    parser = argparse.ArgumentParser(prog='searcher.py',
            description='Search related subforums')
    parser.add_argument('forum',type=str)
    parser.add_argument('doc_type',type=str,choices=['questions'])
    parser.add_argument('query',type=str)
    parser.add_argument('--max_size',type=int,default=10)
    parser.add_argument('--mark',default='main',type=str,help='for DEBUG')

    args = parser.parse_args()
    index = '{forum}_{doc_type}_{mark}'.format(**vars(args))
    
    # connections.create_connection(hosts=['elasticsearch'])

    # The following is for local testing w/o running docker
    # (won't build again and again ^^")
    es = Elasticsearch([{'host': 'elasticsearch'}])
    if not es.ping():
        raise ValueError("Connection failed")
    else:
        print("[INFO] Connection estabished!")

    similar_queires = find_similar_query(args.query,es,index,args.max_size)
    for q in similar_queires:
        print(q['sim_score'])


## deprecated code
# s= s.query({
   # "more_like_this":{
      # "fields":[
         # "body",
      # ],
      # "like":"release pokemon",
      # "min_term_freq":1,
      # "max_query_terms":12
   # }
# })
