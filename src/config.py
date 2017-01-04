from neo4jrestclient.client import GraphDatabase

DATABASE = {
    'connection': "http://localhost:7474",
    'username': "neo4j",
    "password": "admin"
}


class Graph:
    _db = GraphDatabase(DATABASE["connection"], username=DATABASE["username"], password=DATABASE["password"])
