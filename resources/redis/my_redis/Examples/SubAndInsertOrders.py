import redis
import datetime
import time
from pydantic import ValidationError
from Schema import  *

r = redis.Redis(password='redisPassword', host='localhost', port=6379, decode_responses=True)

received = r.xread({"orders": '0'}, None, 0)
print(received)

for result in received:
	data = result[1]
	for tuple in data:
		orderDict = tuple[1]
		print(orderDict)

		try:
			item = Product(
				StockCode=orderDict['StockCode'],
				Description=orderDict['Description'],
				UnitPrice=orderDict['UnitPrice']
			)

			order = Order(
				InvoiceNo=orderDict['InvoiceNo'],
				Item = item,
				Quantity=orderDict['Quantity'],
				InvoiceDate=datetime.datetime.strptime(orderDict['InvoiceDate'], '%m/%d/%Y %H:%M'),
				CustomerID=orderDict['CustomerID'],
				Country=orderDict['Country']
			)

		except ValidationError as e:
			print(e)
			continue

		print(order.key())
		order.save()
