import json
import argparse
import os
from tqdm import tqdm
from elasticsearch import Elasticsearch
from itertools import islice

def process_question(qu):
    """
    Preprocessing the question before indexing

    qu: dict. contains body,title,score... check the json file
    """

    ## global ranking
    rank_info = {}
    rank_info_k = ["viewcount","score","favoritecount"]
    for k in rank_info_k:
        rank_info[k] = int(qu[k])
        qu.pop(k,None)

    rank_info["creationdate"] = qu["creationdate"]

    if qu["acceptedanswer"]:
        qu["acceptedanswer"] = list(qu["acceptedanswer"])
    else:
        qu["acceptedanswer"] = []

    qu.pop('comments',None) # discard comments, maybe add back later
    qu["rank_info"] = rank_info

    return qu

def process_answer(ans):
    """
    Preprocessing the answer before indexing

    ans: dict. contains body, parentid ,userid ,score... check the json file
    """

    #TODO: check whether need type coversion?
    ans['parentid'] = int(ans['parentid'])
    ## I remain comments here, maybe can do some sentiment analysis to evaluate score of answer
    return ans
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='indexer.py',
            description='Index related subforums')
    parser.add_argument('forum',type=str)
    parser.add_argument('doc_type',type=str,choices=['answers','questions'])
    parser.add_argument('--mark',default='main',type=str,help='for DEBUG')

    args = parser.parse_args()
    data_path = "resources/{}".format(args.forum)

    with open('{}/{forum}_{doc_type}.json'.format(data_path,**vars(args))) as fin:
        data = json.load(fin)
        if args.doc_type == 'answers':
            data = {k:process_answer(v) for k,v in data.items()}
        else:
            data = {k:process_question(v) for k,v in data.items()}

    # Start ES engine
    es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])
    if not es.ping():
        raise ValueError("[ERROR] Connection failed")
    else:
        print("[INFO] Connection estabished!")

    for k in tqdm(data):
        # print("[INFO] {} {doc_type} have been processed into {forum}".format(i,**vars(args)))
        res = es.index(index=args.forum+'_'+args.doc_type+"_"+args.mark,doc_type=args.doc_type,id=int(k),body=data[k])

    es.indices.refresh(index=args.forum+'_'+args.doc_type+"_" + args.mark)
