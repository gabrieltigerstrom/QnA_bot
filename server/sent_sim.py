from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Bool, Range, MultiMatch, FunctionScore, Exists,Match
from elasticsearch_dsl.function import FieldValueFactor,ScriptScore

# The following is for outside semantic analyzer, refer to all_requirements
# import numpy as np
# import torch
# from scipy.spatial.distance import cdist

# if running on gpu, the calculation is instant
# infersent = torch.load('resources/model/infersent.allnli.pickle')

# infersent.set_glove_path('resources/GloVe/glove.840B.300d.txt')
# infersent.build_vocab_k_words(K=1000)

def find_similar_query(qu,client,index,max_size=10):
    """ Find related queries from ES
    Args:
        qu: string, the query (at NLP level)
        client: connected ElasticSearch() object
        index: str, index want to search
        max_size: at most return that number of related queries
    """

    #TODO: One experiment I can think is compare these results with the outside semantic analyzer
    #FIXME: use ScriptScore to consider other fields maybe? (not work now)
    # Query to match the title or body(should we match body?)
    q1 = FunctionScore(
        query = MultiMatch(
            query=qu,
            fields=["title^3","body"], # Title has a weight 3 times higher
            fuzziness="AUTO"), # Allows for misspellings
        functions=[
            FieldValueFactor(field="score",modifier="log1p")
            # ScriptScore(script="_score *log1p(score + favoritecnt)"),
        ]
    )

    # Filter to ensure no negative score is taken into account (may have to change in the future)
    q2 = Range(**{"score" : {"gte" : 0}})

    # If a question has an accepted answer, it might be preferable to score it higher
    q3 = Exists(field="acceptedAnswer", boost=0.5)

    # We must both filter positive scores and match the query
    q = Bool(must=q1, filter=q2, should=q3)

    # Also allow the engine to return suggestions using both the title and the body.
    # In the future, we could use one of them to propose to the user
    # in case there are not enough results
    s = Search(using=client,index=index)\
        .query(q)\
        .suggest("title-term-suggest",qu, term={"field" : "title"})\
        .suggest("title-phrase-suggest", qu, phrase={"field" : "title"})\

    # Pagination issue
    if max_size > 10:
        res = s.scan()
    else:
        res = s.execute()

    # what will pass to ranker
    candidates = []
    for hit in res:
        try:
            candidates.append({'title':hit.title,
                               # 'id':int(hit.meta.id),
                               'acceptedAnswer':hit.acceptedAnswer,
                               'answers': hit.answers,
                               'favoritecnt':hit.favoritecnt,
                               'score':hit.score,
                               'sim_score':hit.meta.score,
                               })
        except AttributeError: # discard those queries w/o answer
            continue

    if len(candidates) == 0:
        print("[INFO] No matching")
        return list()
    else:
        return candidates
    
#FIXME: The running time is about 3 sec on my NB cpu ^^" (but instant if using gpu)
# just for experimental usage
def find_semantic_similar_query(qu,client,index,max_size=10):
    """ Find related queries from ES using Infersent
    Args:
        qu: string, the query (at NLP level)
        client: connected ElasticSearch() object
        index: str, index want to search
        max_size: at most return that number of related queries
    """

    # Use ES to do phase selection
    s = Search(using=client,index=index).Match(title=qu)

    if max_size > 10:
        res = s.scan()
    else:
        res = s.execute()

    candidates = []
    for hit in res:
        try:
            candidates.append({'title':hit.title,
                               # 'id':int(hit.meta.id),
                               'acceptedAnswer':hit.acceptedAnswer,
                               'answers': hit.answers,
                               'favoritecnt':hit.favoritecnt,
                               'score':hit.score
                               })
        except AttributeError: # discard those queries w/o acceptedAnswer
            continue

    if len(candidates) == 0:
        print("[INFO] No matching")
        return list()
    else:
        candidate_titles = [ c['title'] for c in candidates]
        infersent.update_vocab([qu] + candidate_titles,tokenize=True)
        embeddings = infersent.encode([qu] + candidate_titles,tokenize=True)

        # calculate cosine similarity between query vectors
        dist = cdist(embeddings[0:1],embeddings[1:],metric='cosine')[0]
        for i in range(len(candidates)):
            candidates[i]['sim_score'] = dist[i]
        return reversed([candidates[i] for i in np.argsort(dist).tolist()])
