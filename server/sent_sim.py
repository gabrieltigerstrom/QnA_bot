import torch
import numpy as np
from scipy.spatial.distance import cdist
from elasticsearch_dsl import Search

# if running on gpu, not the last argument
infersent = torch.load('resources/model/infersent.allnli.pickle', map_location=lambda storage, loc: storage)

infersent.set_glove_path('resources/GloVe/glove.840B.300d.txt')
infersent.build_vocab_k_words(K=1000)

def find_similar_query(qu,client,index,max_size=10):

    s = Search(using=client,index=index).query("match",title=qu)

    if max_size > 10:
        res = s.scan()
    else:
        res = s.execute()

    candidates = []
    for hit in res:
        try:
            candidates.append({'rank_info':hit.rank_info,
                               'title':hit.title,
                               # 'id':int(hit.meta.id),
                               'acceptedAnswer':hit.acceptedAnswer
                               })
        except AttributeError: # discard those queries w/o answer
            continue

    if len(candidates) == 0:
        print("[INFO] No matching")
        return list()
    else:
        candidate_titles = [ c['title'] for c in candidates]
        infersent.update_vocab([qu] + candidate_titles,tokenize=True)
        embeddings = infersent.encode([qu] + candidate_titles,tokenize=True)
        dist = cdist(embeddings[0:1],embeddings[1:],metric='cosine')[0]
        for i in range(len(candidates)):
            candidates[i]['sim_score'] = dist[i]
        return reversed([candidates[i] for i in np.argsort(dist).tolist()])
