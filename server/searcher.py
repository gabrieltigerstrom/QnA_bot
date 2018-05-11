import argparse
import os
from elasticsearch import Elasticsearch

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='searcher.py',
            description='Search related subforums')
    parser.add_argument('forum',type=str)
    parser.add_argument('doc_type',type=str,choices=['answers','questions'])
    parser.add_argument('--mark',default='main',type=str,help='for DEBUG')

    args = parser.parse_args()

    es = Elasticsearch()
    res = es.search(index=args.forum+"_"+args.doc_type+"_" + args,mark, body={"query": {"term": {"userid": "4310"}}})
    print("Got %d Hits:" % res['hits']['total'])
    for hit in res['hits']['hits']:
        print(hits["_source"])
        # print("%(creationdate)s %(userid)s: %(title)s" % hit["_source"])

