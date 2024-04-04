# -*- coding: UTF-8 -*-
import redis
import rediscluster
from redis.sentinel import Sentinel

from elf_py_utils import elf_core

logger = elf_core.set_logging('RedisUtil')
config = elf_core.get_config()


def connect_redis_single():
    """连接Redis-单节点

    配置示例（yaml格式）：
    redis:
      type: sentinel
      single:
        host_port: redis

    :return: redis_client
    """
    host_port = config.read_config('redis.single.host_port')
    host = host_port.split(':')[0]
    port = host_port.split(':')[1]
    pool = redis.ConnectionPool(host=host,
                                port=port,
                                decode_responses=True)
    redis_client = redis.Redis(connection_pool=pool, charset='utf-8', encoding='utf-8')
    logger.info("Connect to Redis success")
    return redis_client


# 连接集群Redis
def connect_redis_cluster() -> rediscluster.client:
    """连接Redis-集群

    配置示例（yaml格式）：

    redis:
      type: cluster
      cluster:
        host_port: 127.0.0.1:6379,127.0.0.2:6379,127.0.0.3:6379

    :return: redis_client
    """
    host_port_list = config.read_config('redis.cluster.host_port').split(',')
    startup_nodes = []
    for host_port in host_port_list:
        host = host_port.split(':')[0]
        port = host_port.split(':')[1]
        startup_nodes.append({'host': host, 'port': port})
    redis_client = rediscluster.RedisCluster(startup_nodes=startup_nodes,
                                             decode_responses=True,
                                             skip_full_coverage_check=True)
    logger.info("Connect to Redis Cluster success")
    return redis_client


# 连接哨兵Redis
def connect_redis_sentinel() -> redis.client:
    """连接Redis-哨兵

    配置示例（yaml格式）：
    redis:
      type: sentinel
      sentinel:
        db: 1
        password: 7crplVt9TnunDrMY7tu
        service_name: mymaster
        host_port: 10.147.243.20:26379,10.147.243.21:26379,10.147.243.22:26379

    :return: redis_client
    """
    host_port_list = config.read_config('redis.sentinel.host_port').split(',')
    db = int(config.read_config('redis.sentinel.db'))
    password = str(config.read_config('redis.sentinel.password'))
    service_name = str(config.read_config('redis.sentinel.service_name'))

    sentinel_address = []
    for host_port in host_port_list:
        sentinel_address.append((host_port.split(':')[0], int(host_port.split(':')[1])))

    my_sentinel = Sentinel(sentinel_address, socket_timeout=2000)
    master = my_sentinel.master_for(service_name, socket_timeout=2000, db=db, password=password, encoding='utf-8')
    slave = my_sentinel.slave_for(service_name, socket_timeout=2000, db=db, password=password, encoding='utf-8')

    return master


connect_redis_type_dict = {
    'single': connect_redis_single,
    'cluster': connect_redis_cluster,
    'sentinel': connect_redis_sentinel

}

redis_is_cluster_dict = {'true': connect_redis_cluster,
                         'false': connect_redis_single}


def connect_redis() -> redis.client:
    """连接Redis
    根据配置文件获取Redis的部署模式，
    并根据是否为集群模式来执行不同的连接过程

    :return: redis_client
    """
    redis_type = config.read_config('redis.type')
    logger.info('Redis Type: {}'.format(redis_type))

    redis_client = connect_redis_type_dict[redis_type]()

    if redis_client is None:
        logger.error('连接失败，请检查配置信息')

    return redis_client
