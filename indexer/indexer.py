#!/usr/bin/env python3
from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])
if not es.ping():
    raise ValueError("Connection failed")
