#!/usr/bin/env python3
import sys
import os
import csv
import json
from datetime import datetime
from elasticsearch import Elasticsearch

# addQuestion takes a row represented as an array and adds it to elasticsearch
def addQuestion(question, es):
    id = int(question[0])
    score = int(question[4])
    title = str(question[5])
    body = str(question[6])
    json_body = json.dumps({"title": title, "score" : score ,"body" : body})
    #print(json_body)
    es.index(index='stackoverflow', doc_type='questions', id=id, body=json_body)

def addAnswer(answer, es):
    id = int(answer[0])
    score = int(answer[4])
    body = str(answer[5])
    json_body = json.dumps({"score" : score ,"body" : body})
    #print(json_body)
    es.index(index='stackoverflow', doc_type='answers', id=id, body=json_body)

# Read from command line if we're parsing questions, answers or tags
questions = False
answers = False
tags = False
print('Argument List:', str(sys.argv))
if sys.argv[1] is "q":
    questions = True
elif sys.argv[1] is "a":
    answers = True
elif sys.argv[1] is "t":
    tags = True
else:
    raise RuntimeError("Wrong parameter to program")
    sys.exit(1)

# Select which file to read
if questions:
    file = open("resources/Questions.csv", "r", encoding="ISO-8859-1")
elif answers:
    file = open("resources/Answers.csv", "r", encoding="ISO-8859-1")
else:
    file = open("resources/Tags.csv", "r", encoding="ISO-8859-1")

# Connect to elasticsearch
es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])
if not es.ping():
    raise ValueError("Connection failed")
else:
    print("Connection estabished!")

# Use the CSV reader to easily parse the content of the file
reader = csv.reader(file, delimiter=',')
for i, row in enumerate(reader):
    if i == 0:
        # Skip the first line
        continue
    if i % 100 is 0:
        print("Added",i, "questions" if questions else "answers")
    if questions:
        addQuestion(row, es)
    elif answers:
        addAnswer(row, es)
    else:
        print("Not supported yet!")
        break
file.close()



    

