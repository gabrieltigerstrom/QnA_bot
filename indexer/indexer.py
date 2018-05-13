import json
import argparse
import os
import random
from tqdm import tqdm
from elasticsearch_dsl.connections import connections
from itertools import islice
from answer import *
from question import *

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='indexer.py',
            description='Index related subforums')
    parser.add_argument('forum',type=str)
    parser.add_argument('doc_type',type=str,choices=['answers','questions'])
    parser.add_argument('--mark',default='main',type=str,help='for DEBUG')
    parser.add_argument('--size',type=int,help='for sub-test')
    parser.add_argument('--nobulk',action='store_true')
    parser.add_argument('--bulksize',type=int,default=2000)
    parser.add_argument('--local',action='store_true',help='for local test')

    args = parser.parse_args()
    data_path = "resources/{}".format(args.forum)
    random.seed(101)

    if args.local:
        connections.create_connection(hosts=['localhost'])
    else:
        connections.create_connection(hosts=['elasticsearch'])

    index = '{forum}_{doc_type}_{mark}'.format(**vars(args))
    with open('{}/{forum}_{doc_type}.json'.format(data_path,**vars(args))) as fin:
        data = json.load(fin)
        if args.size is not None:
            chose_idx = random.sample(list(data.keys()),args.size)
            data = dict((k,data[k]) for k in chose_idx)

        if args.doc_type == 'answers':
            Answer.init(index=index)
        else:
            Question.init(index=index)


    # Start indexing
    if args.doc_type == 'answers':
        if args.nobulk:
            for k in tqdm(data):
                process_answer(k,data[k],index)
            Answer._doc_type.refresh()
        else:
            bulk_process_answer(data,index,connections.get_connection(),args.bulksize)
    else:
        if args.nobulk:
            for k in tqdm(data):
                process_question(k,data[k],index)
            Question._doc_type.refresh()
        else:
            bulk_process_question(data,index,connections.get_connection(),args.bulksize)
