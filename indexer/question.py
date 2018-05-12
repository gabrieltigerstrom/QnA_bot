from elasticsearch_dsl import DocType, Date, Integer, Nested, analyzer, InnerDoc, Keyword, Text
from marcos import *

class RankInfo(InnerDoc):
    viewcnt = Integer()
    score = Integer()
    favoritecnt = Integer()

class Question(DocType):
    title = Text(analyzer='snowball',required=True)
    # title = Text()
    rankinfo = Nested(RankInfo)
    tags = Keyword()
    userid = Integer()
    related = Integer()
    dup = Integer()
    #TODO: how to add list type? ( The following seems correct ,maybe
    acceptedAnswer = Integer()
    answers = Integer()
    creationdate = Date()
    body = Text(analyzer = html_strip)

    ## will always be overwritten, but needed to add here
    class Meta:
        index='questions'

    def save(self,**kwargs):
        return super().save(** kwargs)

def process_question(k,q,index):
    """
        k: str
        q: dict
        index: str
    """
    q_obj = Question(
        title=q['title'],
        tags=q['tags'],
        userid=int(q['userid']),
        related=q['related'],
        dup = q['dups'],
        creationdate=q['creationdate'],
        body = q['body']
    )
    if q['acceptedanswer']:
        q_obj.acceptedAnswer = q['acceptedanswer']

    q_obj.rank_info = RankInfo(viewcnt=q['viewcount'],score=q['score'],favoritecnt=q['favoritecount'])

    q_obj.meta.id=int(k)
    q_obj.meta.index= index

    q_obj.save()

