from elasticsearch_dsl import DocType, Date, Integer, Nested, analyzer, InnerDoc, Keyword, Text
from elasticsearch.helpers import bulk
from tqdm import tqdm
from marcos import *

#FIXME: Don't why I cannot get rankinfo.viewcnt, so not packed here
# class RankInfo(InnerDoc):
    # viewcnt = Integer()
    # score = Integer()
    # favoritecnt = Integer()

class Question(DocType):

    # use BM25 to well consider high-freq. words properly (can change back to # tf-idf if needed)
    title = Text(analyzer='snowball',similarity='BM25',required=True)
    # rankinfo = Nested(RankInfo)
    tags = Keyword()
    userid = Integer()
    related = Integer()
    viewcnt = Integer()
    score = Integer()
    dup = Integer()
    favoritecnt = Integer()
    acceptedAnswer = Integer()
    answers = Integer()
    creationdate = Date()
    body = Text(analyzer = html_strip)

    def save(self,**kwargs):
        return super().save(** kwargs)

def bulk_process_question(questions,index,client,bulksize):
    """
    Args:
        questions: dict., json dump
        index: str
        client: connections() object
        bulksize: int., suggested range: 1K - 5K (depend on your RAM)
    """
    data = [ {
        '_type': 'doc',
        '_index': index,
        '_id': int(k),
        '_source':{
            'title': q['title'],
            'tags': q['tags'],
            'userid': q['userid'] if q['userid'] else None,
            'related': q['related'] if len(q['related']) else None,
            'dup': q['dups'] if len(q['dups']) else None,
            'viewcnt': q['viewcount'],
            'score': q['score'],
            'favoritecnt': q['favoritecount'],
            'creationdate': q['creationdate'],
            'body': q['body'],
            'answers': q['answers'] if len(q['answers']) else None,
            'acceptedAnswer': q['acceptedanswer'] if q['acceptedanswer'] else None
        } } for k,q in questions.items()]
    
    data = [data[i:i+bulksize] for i in range(0,len(data),bulksize)]
    
    for d in tqdm(data):
        bulk(client,d,raise_on_error=True,refresh=True)

def process_question(k,q,index):
    """
    Args:
        k: str, the id of question
        q: dict, info. of question
        index: str, index want to insert
    """
    q_obj = Question(
        title=q['title'],
        tags=q['tags'],
        userid=int(q['userid']),
        related=q['related'],
        viewcnt=q['viewcount'],
        dup = q['dups'],
        score=q['score'],
        favoritecnt=q['favoritecount'],
        creationdate=q['creationdate'],
        body = q['body'],
        answers = q['answers'],
        acceptedAnswer = q['acceptedanswer'] if q['acceptedanswer'] else None
    )
    # q_obj.rankinfo = RankInfo(viewcnt=q['viewcount'],score=q['score'],favoritecnt=q['favoritecount'])

    q_obj.meta.id=int(k)
    q_obj.meta.index= index

    q_obj.save()
