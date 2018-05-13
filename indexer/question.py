from elasticsearch_dsl import DocType, Date, Integer, Nested, analyzer, InnerDoc, Keyword, Text
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
    favoritecnt = Integer()
    acceptedAnswer = Integer()
    answers = Integer()
    creationdate = Date()
    body = Text(analyzer = html_strip)

    def save(self,**kwargs):
        return super().save(** kwargs)

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
        dup = q['dups'],
        viewcnt=q['viewcount'],
        score=q['score'],
        favoritecnt=q['favoritecount'],
        creationdate=q['creationdate'],
        body = q['body'],
        answers = q['answers']
    )
    if q['acceptedanswer']:
        q_obj.acceptedAnswer = q['acceptedanswer']
    # q_obj.rankinfo = RankInfo(viewcnt=q['viewcount'],score=q['score'],favoritecnt=q['favoritecount'])

    q_obj.meta.id=int(k)
    q_obj.meta.index= index

    q_obj.save()
