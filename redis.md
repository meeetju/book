# Redis cheat sheet

## References

https://www.udemy.com/course/redis-cloud/learn/lecture/30830164#overview

## Purpose

When there are a lot of requests for example to the database the systems may choke.
Thefore we use a caching layer, so the Redis comes here. Redis stores the data in the RAM memory.

Besides of caching, redis may also stream the data, pubsub etc.

Redis may have many modules:
- RedisGears
- RedisJSON
- RedisSearch
- RedisGraph
- RedisAI
- RedisTimeSeries
- RedisBloom

## Redis CLI

### Instalation and check

Install redis

    sudo apt-get install redis-server

Check if CLI functions

    redis-cli ping

To stop redis if we get port error when staring an instance in the container 

    sudo systemctl stop redis-server

### Log in

    redis-cli -p 6379 -a redisPassword

### Flush the redis data

    redis-cli -p 6379 -a redisPassword flushall

### Displaying the redis info

From within `127.0.0.1:6379` run:

    info

### PubSub

Publish Subscribe is based on a concept of channels.

Publisher publishes a message to the channel and subscriber consumes it. There may be many publishers and subscribers to one channel. Subscriber may subscribe to many channels.

It is a fire and forget messaging system. There is no persistence of messages. There is no way for new subscribers to read old messages. So this is the main difference between PubSub and streaming.

This is only a communication channel. So redis is just routing the messages where they need to go.

Publisher does not know who subscribers are. Subscribers though may subscribe to channes using some pattern. Like `Channel*` which will match `Channel1` and `Channel2`.

### Streaming

Streams are appended to infinitely. Typical use case is publishing log data. With streams we are persisting the data. New consumers will get the whole historical data.

Consumers may query for ranges of data form the streams (much like Kafka Consumer Groups) - XRANGE.

Consumers may listen only for new itmes - XREAD (so just like PubSub).

Examples:
- StreamOrders.py
- SubOrders.py

### RedisJSON

A horizontally scalable NoSQL document store. Allows atomic updating of individual fields, otherwise we would have to deal with the intire value string.

### Redis OM

Redis Object Mapping - high level API that lets us deal with native data structures.

Examples:
> Make sure to use the `REDIS_OM_URL` env
- export REDIS_OM_URL=redis://default:redisPassword@localhost:6379
> Publish the orders data to redis with xadd command, the data is added as columns like `InvoiceNo` and values
- StreamOrders.py
> Receiving the orders previously published with xread and inser them back using redis json
- SubAndInsertOrders.py # 
- Schema.py # defines the structure of json
  
### RedisSearch

- Indexing and Querying
- Full-text and Fuzzy Search

Examples:
- export REDIS_OM_URL=redis://default:redisPassword@localhost:6379
- StreamOrders.py
- SubAndInsertOrders.py
- IndexOrder.py
- FindOrder.py

### RedisTimeSeries

- Query by start and end time
- Aggregations:
  - min max avg sum range count first last
- Set max retention period
- Indexed labels for querying
- Integration into Prometheus, Grafana, Telegraph

Examples:
- export REDIS_OM_URL=redis://default:redisPassword@localhost:6379
- TimeSeries.py
- In the workbench run `TS.RANGE quantity 1291220760000 1291594200000`