from elasticsearch_dsl import DocType, Date, Integer, analyzer , Text
from elasticsearch.helpers import bulk
from tqdm import tqdm
from marcos import *

class Answer(DocType):
    body = Text(analyzer = html_strip)
    userid = Integer()
    score = Integer()
    parentid = Integer(required=True) #trace back to corresponding question
    creationdate = Date()

    def save(self,**kwargs):
        return super().save(**kwargs)

def bulk_process_answer(answers,index,client,bulksize):
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
            'body': a['body'],
            'userid': a['userid'] if a['userid'] else None,
            'score': a['score'],
            'parentid': a['parentid'],
            'creationdate': a['creationdate']
        } } for k,a in answers.items()]
    
    data = [data[i:i+bulksize] for i in range(0,len(data),bulksize)]
    
    for d in tqdm(data):
        bulk(client,d,raise_on_error=True,refresh=True)

def process_answer(k,a,index):
    """
    Args:
        k: str, the id of question
        a: dict, info. of answer
        index: str, index want to insert
    """
    a_obj = Answer(
        body = a['body'],
        userid = a['userid'] if a['userid'] else None,
        score = a['score'],
        parentid = a['parentid'],
        creationdate = a['creationdate']
    )
    a_obj.meta.id=int(k)
    a_obj.meta.index=index
    a_obj.save()
