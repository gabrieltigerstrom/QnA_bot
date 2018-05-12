import json
import argparse
import os
from tqdm import tqdm
from elasticsearch import Elasticsearch
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

    args = parser.parse_args()
    data_path = "resources/{}".format(args.forum)

    connections.create_connection(hosts=['elasticsearch'])

    index = '{forum}_{doc_type}_{mark}'.format(**vars(args))
    with open('{}/{forum}_{doc_type}.json'.format(data_path,**vars(args))) as fin:
        data = json.load(fin)
        # data = dict((k,data[k]) for k in ('110556','17796','89379') if k in data)
        if args.doc_type == 'answers':
            Answer.init(index=index)
        else:
            Question.init(index=index)

    if args.doc_type == 'answers':
        for k in tqdm(data):
            process_answer(k,data[k],index)
        Answer._doc_type.refresh()
    else:
        for k in tqdm(data):
            process_question(k,data[k],index)
        Question._doc_type.refresh()
