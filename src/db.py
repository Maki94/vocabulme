import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)
# r.set('foo', 'bar')
print(r.get('foo'))

print(r.ping())
seq = ["hello1", "hello2", "hello3"]
# r.lpush('hello_world', *seq)

print(r.lrange(name='hello_world', start=0, end=5)[0])
