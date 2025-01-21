import csv
import redis

r = redis.Redis(password='redisPassword', host='localhost', port=6379)


with open("OnlineRetail.csv", encoding='utf-8-sig') as csvf:
	csvReader = csv.DictReader(csvf)

	for row in csvReader:
		r.xadd("orders", row)
