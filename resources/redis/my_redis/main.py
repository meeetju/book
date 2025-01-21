import redis

r = redis.Redis(password='redisPassword', host='localhost', port=6379, decode_responses=True)

r.set('foo', 'bar')
print(r.get('foo'))

r.mset({'beer': 'paulaner', 'pizza': 'diavola'})
print(r.get('beer'))

r.hset('my_name', 'key_1', 'value_1')
r.hset('my_name', 'key_2', 'value_2')
print(r.hget('my_name', 'key_1'))

r.lpush('beers', 'paluaner')
r.lpush('beers', 'recraft')
print(r.rpop('beers'))