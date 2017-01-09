import redis
from neo4jrestclient.client import GraphDatabase
from settings import DATABASE_NEO4J, DATABASE_REDIS


class Graph:
    _db = GraphDatabase(
        url=DATABASE_NEO4J["connection"],
        username=DATABASE_NEO4J["username"],
        password=DATABASE_NEO4J["password"]
    )


class RedisDatabase:
    _db = redis.StrictRedis(
        host=DATABASE_REDIS['host'],
        port=DATABASE_REDIS['port'],
        db=DATABASE_REDIS['db']
    )
