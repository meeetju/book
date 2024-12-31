# Kafka cheat sheet

## References

https://hub.docker.com/r/confluentinc/cp-kafka

## What is Kafka

It is distributed publish-subscribe messaging system.

## Broker

PRODUCER -> BROKER -> CONSUMER

Brokers:
- Consume messages from producers (append to files)
- Store messages (as files)
- Give consumers ability to read messages (read from files)

Multiple Producers and multiple Consumers may communicate with one Broker.

## Broker Cluster

The cluster is composed of one or more `kafka brokers (servers)`.

## Zookeeper

Zookeeper:
- Maintains list of active brokers (which are healthy, which failed)
- Manages configuration of the topics and partitionss
- Elects controller (there is one controller in each kafka cluster among brokers)

There may be also a cluster of zookepers (ensemble).

## Kafka cluster

The cluster is composed of one or more `kafka brokers (servers)` and the `zookeeper`.

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

We can use for example the built in console consumer provided with the `kafka` installation.

In the `/usr/bin` we have `kafka-console-consumer`:

    ./kafka-console-consumer --bootstrap-server localhost:9092 --topic cities

Now the consumer will consume all the messages sent by the producer staring from the new message.

If we want to consume all the messages from the beginning assuming that the producer was producing before the consumer started:

    ./kafka-console-consumer --bootstrap-server localhost:9092 --topic cities --from-beginning

> Kafka cluster stores messages even if they were already consumed by one of the consumers

> Multiple consumers and multiple producers could exchange messages via single centralized storage point - kafka cluster

> Producers and consumers may appear and disappear. But kafka doesn't care about that. It's job is to store messages and receive or send them on demand

> Every consumer has to belong to a consumer group

### Where the messages are stored

Depending on the configuration provided in the `server.properties` under the `log.dirs`. Based on the kafka logs we know that the messages are stored in `/var/lib/kafka/data/cities-0` 

The folder `cities-0` consists of the log files we are interested in.

#### Messages log file

The `00000000000000000000.log` consists of the messages that were sent by the producers.

> Kafka doesn't store all the massages forever and after specific amount of time (or when size of the log exceeds configure max size) messages are deleted. Default log retention period is 7 days (168 hours)

> Every message inside of the topic has an unique number called `offset`. First message in each topic has an offset 0. Consumers start reading messages starting form specific offset.