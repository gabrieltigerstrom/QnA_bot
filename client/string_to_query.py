#!/usr/bin/python3

import sys
import pprint
from urllib.parse import unquote_plus
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Bool, Range, MultiMatch, FunctionScore, Exists
from elasticsearch_dsl.function import FieldValueFactor

def string_to_query(query_string):
    """Converts a query string into an ElasticSearch query body"""

    # TODO: Do we need to do this, or is this already taken care of?
    # Not that it breaks anything if this is not URL-encoded, but still worth wondering.
    query_string = unquote_plus(query_string)

    # Query to match the title or the body,
    # and rank using both TF-IDF and the score of the question
    q1 = FunctionScore(
        query=MultiMatch(
            query=query_string,
            fields=["title^3", "body"], # Title has a weight 3 times higher
            fuzziness="AUTO"),          # Allows for misspellings
        functions=[                     # Factor in the score of the question
            FieldValueFactor(field="rankinfo.score", modifier="log1p")
        ])
    
    # Filter to ensure no negative score is taken into account (may have to change in the future)
    q2 = Range(**{"rankinfo.score" : {"gte" : 0}})

    # If a question has an accepted answer, it might be preferable to score it higher
    q3 = Exists(field="acceptedAnswer", boost=0.5)

    # We must both filter positive scores and match the query
    q = Bool(must=q1, filter=q2, should=q3)

    # Also allow the engine to return suggestions using both the title and the body.
    # In the future, we could use one of them to propose to the user
    # in case there are not enough results
    s = Search(index="questions")\
        .query(q)\
        .suggest("title-term-suggest", query_string, term={"field" : "title"})\
        .suggest("title-phrase-suggest", query_string, phrase={"field" : "title"})\
        .suggest("body-term-suggest", query_string, term={"field" : "body"})\
        .suggest("body-phrase-suggest", query_string, phrase={"field" : "body"})
    
    # Serialization (NB: we could also return the object directly and execute it using elasticsearch_dsl)
    return s.to_dict()

if __name__ == "__main__":
    # Prints a constructed query as an example
    query_string = "Hello world!"
    if len(sys.argv) >= 2:
        query_string = sys.argv[1]
    pprint.pprint(string_to_query(query_string))
