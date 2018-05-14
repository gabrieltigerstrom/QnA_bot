from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qsl
from elasticsearch import Elasticsearch
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.query import Match
from elasticsearch_dsl import Search
from sent_sim import *
import json

ESConnection = None

class QueryHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        parsed_path = urlparse(self.path)
        print("Path", self.path)
        print("Connection", ESConnection)
        queries = dict(parse_qsl(parsed_path.query))
        print(queries)
        print(queries['q'])
        answer = self.search(queries['q'], "gaming")
        if answer is not None:
            self.wfile.write(json.dumps({'answer':answer}).encode())
        else:
            self.wfile.write(json.dumps({'error':'no_match'}).encode())
        return

    def search(self, query, forum):
        q_index = '{}_questions_main'.format(forum)
        a_index = '{}_answers_main'.format(forum)
        similar_queries = find_similar_query(query,ESConnection,q_index,1)
        if similar_queries[0]['acceptedAnswer'] is not None:
            s = Search(using=ESConnection,index=a_index).query(Match(_id=int(similar_queries[0]['acceptedAnswer'])))
            res = s.execute()
            return res['hits']['hits'][0]['_source']['body']
        else:
            return None

if __name__ == '__main__':
    connections.create_connection(hosts=['elasticsearch'])
    ESConnection = connections.get_connection()
    
    address, port = '0.0.0.0', 4000
    connection = "hello"
    server = HTTPServer((address, port), QueryHandler)
    #server = HTTPServer((address, port), QueryHandler(connections.getConnections()))
    try:
        print("Server was started on {}:{}".format(address, port))
        server.serve_forever()

    except KeyboardInterrupt:
        pass
    server.server_close()
    print("Server shut down")
