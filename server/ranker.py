from operator import itemgetter



keyword_match = 10
accepted_bonus = 10
cosine_multiplier = 2
upvote_multiplier = 0.1
queryscore_multiplier = 0.5

"""
    input:
        input: A list of entries, each entry containing the qwuestion, answer and scores for each
        query: A list of keywords with their respective scores of importance
    output:
        ranked_list: A list of the input entries sorted after their relevance score
"""
def rank(input, query):

    #print(keywords)
    #print("Unsorted:")
    for entry in input:
        #print(entry['title'])
        #print(entry['score'])
        entry['score'] = calculate_score(entry, query)

    

    input.sort(key=itemgetter('score'), reverse=True)

    """
    print("\nSorted:")
    for entry in input:
        print(entry['title'])
        print(entry['score'])
    """


    return input


    


"""
    Calculate the score of one entry of Q&A using the 
    ineherent upvotes of the entry and the scor4es of
    the query keywords
    input:
        entry: One entry containing the question, answer and number of upvotes of both
        query: A list of keywords with their respective scores of importance
    output:
        score: An overall score of importance of the entry in regards to the query

"""
def calculate_score(entry, query):
    score = 0

    keywords = query.lower().split()
    title_vector = entry['title'].lower().split()

    cosine = 0

    
    for key in keywords:
        # Add score for each tag that matches a keyword
        for tag in entry['tags']:
            tag = tag.lower()
            if key in tag:
                score += keyword_match

        # Simple nestled for loops for cosine dot product
        for title_word in title_vector:
            if key in title_word:
                cosine += 1

    # Cosine score
    cosine /= len(keywords) + len(title_vector)

    score += cosine * cosine_multiplier

    # Bonus if the question had an accepted answer
    if entry['acceptedAnswer']:
        score += accepted_bonus


    # Add upvote scores and elasticsearch's query-score
    score += entry['score'] * upvote_multiplier

    score += entry['sim_score'] * queryscore_multiplier


    return score







