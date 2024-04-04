from kafka import KafkaConsumer, KafkaProducer

from elf_py_utils import elf_core

logger = elf_core.set_logging('KafkaUtil')
config = elf_core.get_config()

kafka_config = config.read_config('kafka')
servers = str(config.read_config('kafka.servers')).split(',')
consumer_topic = str(config.read_config('kafka.consumer.topic'))
consumer_group_id = str(config.read_config('kafka.consumer.id'))


# 连接kafka
def producer_connect_kafka():
    logger.info("Connect to Kafka start")
    producer = KafkaProducer(bootstrap_servers=servers, key_serializer=str.encode, value_serializer=str.encode)
    logger.info("Connect to Kafka success")
    return producer


# 消费默认kafka
def consumer_connect_kafka():
    # 默认从最早一条消息进行消费
    logger.info("Connect to Kafka start")
    consumer = KafkaConsumer(consumer_topic, bootstrap_servers=servers, group_id=consumer_group_id)
    logger.info("Consumer connect to Kafka success")
    return consumer


# 消费kafka指定topic
def consumer_kafka(topic: str, group_id: str) -> KafkaConsumer:
    logger.info("Connect to Kafka start")
    consumer = KafkaConsumer(topic, bootstrap_servers=servers, group_id=group_id)
    logger.info("Consumer connect to Kafka success")
    return consumer
