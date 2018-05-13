from elasticsearch_dsl import DocType, Date, Integer, analyzer , Text
from marcos import *

class Answer(DocType):
    body = Text(analyzer = html_strip)
    userid = Integer()
    score = Integer()
    parentid = Integer() #trace back to corresponding question
    creationdate = Date()

    def save(self,**kwargs):
        return super().save(**kwargs)

def process_answer(k,a,index):
    """
    Args:
        k: str, the id of question
        a: dict, info. of answer
        index: str, index want to insert
    """
    a_obj = Answer(
        body = a['body'],
        userid = a['userid'],
        score = a['score'],
        parentid = a['parentid'],
        creationdate = a['creationdate']
    )
    a_obj.meta.id=int(k)
    a_obj.meta.index=index
    a_obj.save()
