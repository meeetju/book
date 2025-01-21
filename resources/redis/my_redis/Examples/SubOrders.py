import redis
import datetime
import time

r = redis.Redis(password='redisPassword', host='localhost', port=6379, decode_responses=True)

while True:
	received = r.xread({"orders": '0'}, 1, 5000)
	for result in received:
		data = result[1]
		for tuple in data:
			orderDict = tuple[1];
			print(orderDict)

	# time.sleep(1)

