# Kafka cheat sheet

## References

https://hub.docker.com/r/confluentinc/cp-kafka

[Resources](resources/kafka/)

## What is Kafka

It is distributed publish-subscribe messaging system.

## Kafka Broker (server)

PRODUCER -> BROKER -> CONSUMER

Brokers:
- Consume messages from producers (append to files)
- Store messages (as files)
- Give consumers ability to read messages (read from files)

Multiple Producers and multiple Consumers may communicate with one Broker.

The default port is `localhost:9092`.

If broker should be publicly accessible we need to:
- On hosting service firewall allow remote access and open ports 2181 (Zookeeper) and 9092 (Broker)
- Adjust the `advertised.listeners` property, example `advertised.listeners=PLAINTEXT://ec2-54-123-123-123.compute-1.amazonaws.com:9092`.

## Broker Cluster

The cluster is composed of one or more `kafka brokers (servers)`.

## Zookeeper

Zookeeper:
- Maintains list of active brokers (which are healthy, which failed)
- Manages configuration of the topics and partitionss
- Elects controller (there is one controller in each kafka cluster among brokers)

There may be also a cluster of zookepers (ensemble).

The default port is `localhost:2181`.

## Kafka cluster

The cluster is composed of one or more `kafka brokers (servers)` and the `zookeeper`.

There may be many Kafka clusters which may be in sync.

## Topic

Topic has to have a unique name. It stores messages with offsets. 
Records in the log and the order are immutable, except for the situation when the records are deleted due to the retention policy.

Every topic may exist in different brokers.

## Message

Message is immutable and has the following structure:
- Timestamp
- Offset number (unique accross partition)
- Key (optional, allows us to send the message to a specific partition)
- Value (sequence of bytes)

## Partition

Partitions are used to spread messages among different brokers when the same topic which is present in multiple brokers.

|           | Broker 0 | Broker 1 | Broker 2 | Broker 3 |
|-----------|----------|----------|----------|----------|
| Topic     |          |    A     |    A     |    A     |
| Partition |          |    0     |    1     |    2     |

|           | Broker 0 | Broker 1 | Broker 2 | Broker 3 |
|-----------|----------|----------|----------|----------|
| Topic     |    B     |    B     |          |          |
| Partition |    0     |    1     |          |          |

|           | Broker 0 | Broker 1 | Broker 2 | Broker 3 |
|-----------|----------|----------|----------|----------|
| Topic     |          |          |    C     |          |
| Partition |          |          |    0     |          |

There may be also more than one partition on one broker for a one topic.

Partitions optimise the read and write operations as the writing is spread across different brokers,
so different files are used to store messages for the topic. Partitions also increase falut tolerance.

It is the producer that decides to which partition to write. This causes a problem, that if one broker fails its
messages stored in the partition are lost. To avoid this we need to enable replication.

## Partition Leader

When we run replicas of partitions. So given we run N partitions on N brokers, one is a Leader and others are Followers.

|           | Broker 0 | Broker 1 | Broker 2 |
|-----------|----------|----------|----------|
| Topic     |    A     |    A     |    A     |
| Partition |    0     |    0     |    0     |
| Type      | Follower | Leader   | Follower |

Followers:
- Get new messages from the Leader
- Write them to a specific partition
- Do not accept messages from producers
- Do not serve consumers
- May become leader when leader fails

Leader:
- Performs most operations
- Communicates with producers and consumers
- Sends copies of each message to al Followers

The recommended replication factor for a topic in production environments is 3.

## Controller

Is picked by Zookeeper among kafka brokers.

Responsibilities:
- elect leaders
- reassign partitions
- create new partitions for new topics

## Running

Inside the [kafka resources](resources/kafka)

Start the POD

    docker compose up -d

Run the terminal to interact with the kafka

    docker exec -it <container_id> /bin/bash

Stop the POD

    docker compose down

### Kafka image structure

| Path                  | What           | Description                                                       |
|-----------------------|----------------|-------------------------------------------------------------------|
| `/usr/bin`            | console sripts | We can find there for example the `kafka-server-start` script     |
| `/etc/kafka`          | configuration  | we can find there the `server.properties` file                    |
| `/var/lib/kafka/data` | messages       | We can find there catalogs for topics which contain messages logs |

### Start Kafka

Kafka is started with the command followed by the config

    bin/kafka-server-start config/server.properties

### Kafka logs

Usually `kafka` logs that are visible as a docker container logs are stored in the `server.log` file.

When the server started successfully we should see like:

    INFO [KafkaServer id=1] started (kafka.server.KafkaServer)
    INFO [SocketServer listenerType=ZK_BROKER, nodeId=1]

Every Broker/Kafka server has a unique id. In the config file we can find `broker.id=0` but it was overriden by the `KAFKA_BROKER_ID` value. This id has to be unique accross the kafka cluster.

Kafka is awaiting connections:

    INFO Awaiting socket connections on 0.0.0.0:9092
    INFO Awaiting socket connections on 0.0.0.0:29092

Kafka informs where the logs are:

    INFO Loading logs from log dirs ArrayBuffer(/var/lib/kafka/data)

### Create a Kafka Topic

In order to create a Topic, we have to use a script `kafka-topics`.

To create a new `topic` named `cities` for the `kafka` server running on port `9092`, from within the `/usr/bin` run:

    ./kafka-topics --create --bootstrap-server localhost:9092 --topic cities

In the `kafka` logs we will see:

    INFO [Partition cities-0 broker=1]
    INFO Created log for partition cities-0 in /var/lib/kafka/data/cities-0 with properties {} (kafka.log.LogManager)

In the `/var/lib/kafka/data` we will see a new folder `cities-0`. It will consist of empty `index` and `log` files as there are no messages sent yet. The `-0` comes from the number of partitions defined ofr each topic defined in `server.properties` file under `num.partitions`. If the `num.partitions=2` then we would get `cities-0` and `cities-1`.

#### Example with multiple brokers and partitions

Create a topic `cities` on 5 partitions among different brokers

    ./kafka-topics --bootstrap-server localhost:9092 --create --replication-factor 1 --partitions 5 --topic cities


### List Kafka topics

From within the `/usr/bin` run:

    ./kafka-topics --list --bootstrap-server localhost:9092

The `cities` topic should be displayed.

### Details about Kafka topic

From within the `/usr/bin` run:

    ./kafka-topics --describe --bootstrap-server localhost:9092 --topic cities

We should se something like

    Topic: cities	TopicId: QsVfCq3rT1qDrNp8-erMUg	PartitionCount: 1	ReplicationFactor: 1	Configs: 
	Topic: cities	Partition: 0	Leader: 1	Replicas: 1	Isr: 1	Elr: N/A	LastKnownElr: N/A

### Produce messages to the topic

We can use for example the built in console producer provided with the `kafka` installation.

In the `/usr/bin` we have `kafka-console-producer`:

    ./kafka-console-producer --broker-list localhost:9092 --topic cities

Now we can send messagec to the topic. We use the `broker-list` as we may provide more than one `kafka` broker addresses.

### Consume messages

Usually every consumer is connectod to only one topic, but it is possible to connect to multiple topics.
Cosumer may consumer from all or from one partition. Consumer may read from beginning (offset 0),
or it may be just waiting for the new messages.

We can use for example the built in console consumer provided with the `kafka` installation.

In the `/usr/bin` we have `kafka-console-consumer`:

    ./kafka-console-consumer --bootstrap-server localhost:9092 --topic cities

Now the consumer will consume all the messages sent by the producer staring from the new message.

If we want to consume all the messages from the beginning assuming that the producer was producing before the consumer started:

    ./kafka-console-consumer --bootstrap-server localhost:9092 --topic cities --from-beginning

Optionally we can specify the `--partition` parameter if we want to consume only from specific partition.
Instead of `--from-beginning` we can use `--offset` which will set the starting offset, but this requires `--partition`.

Also we can 

> Kafka cluster stores messages even if they were already consumed by one of the consumers

> Multiple consumers and multiple producers could exchange messages via single centralized storage point - kafka cluster

> Producers and consumers may appear and disappear. But kafka doesn't care about that. It's job is to store messages and receive or send them on demand

> Every consumer has to belong to a consumer group. By default each consumer becomes a member of a new group.

#### Consumer groups

Single consumer may not be able to consume all produced messages at the high rates as producers produce.
That's why consumers may be organized into consumer groups to share consumption of the messages.


To read details from within the `/usr/bin` run:

    ./kafka-consumer-groups --describe --bootstrap-server localhost:9092 --group <GROUP_NAME>

To create a consumer with a consumer group from within the `/usr/bin` run:

    ./kafka-console-consumer --bootstrap-server localhost:9092 --topic cities --group <GROUP_NAME>

### Where the messages are stored

Depending on the configuration provided in the `server.properties` under the `log.dirs`. Based on the kafka logs we know that the messages are stored in `/var/lib/kafka/data/cities-0` 

The folder `cities-0` consists of the log files we are interested in.

#### Messages log file

The `00000000000000000000.log` consists of the messages that were sent by the producers.

> Kafka doesn't store all the massages forever and after specific amount of time (or when size of the log exceeds configure max size) messages are deleted. Default log retention period is 7 days (168 hours)

> Every message inside of the topic has an unique number called `offset`. First message in each topic has an offset 0. Consumers start reading messages starting form specific offset.

### Zookeper

#### List all active brokers ids

    ./zookeeper-shell localhost:2181 ls /brokers/ids

We will get in case of 3 different brokers that have ids 1-3:

    Connecting to localhost:2181
    WATCHER::
    WatchedEvent state:SyncConnected type:None path:null
    [1, 2, 3]

#### List details of broker with id 1

    ./zookeeper-shell localhost:2181 get /brokers/ids/1

We will get:

    Connecting to localhost:2181
    WATCHER::
    WatchedEvent state:SyncConnected type:None path:null
    {"features":{},"listener_security_protocol_map":{"PLAINTEXT":"PLAINTEXT","PLAINTEXT_HOST":"PLAINTEXT"},"endpoints":["PLAINTEXT://kafka:9092","PLAINTEXT_HOST://localhost:29092"],"jmx_port":-1,"port":9092,"host":"kafka","version":5,"timestamp":"1736198272985"}

### Performance test

To run the produce test from within the `/usr/bin` run:

    ./kafka-producer-perf-test --topic cities --num-records 1000 --throughput 100 --record-size 1000 --producer-props bootstrap.servers=localhost:9092

The output would be the following

    502 records sent, 100.3 records/sec (0.10 MB/sec), 5.2 ms avg latency, 332.0 ms max latency.
    1000 records sent, 99.571841 records/sec (0.09 MB/sec), 4.03 ms avg latency, 332.00 ms max latency, 3 ms 50th, 7 ms 95th, 27 ms 99th, 332 ms 99.9th.
