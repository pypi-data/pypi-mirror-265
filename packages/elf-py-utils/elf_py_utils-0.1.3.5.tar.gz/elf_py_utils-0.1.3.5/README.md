# elf-py-utils项目说明

> 小精灵Python工具包

## 前言

- 目标使用者：从事运维工程师、后端开发工程师等相关岗位，并熟悉python基础语法规则
- 本包的工作：在前人的基础上，对当前已有的工具包进行二次封装，并提供一个统一的配置文件来进行配置管理，意图提供一个类似于Spring Boot的框架方便使用

## 当前功能

### Redis工具类

#### 配置示例

通过配置文件，实现一种代码连接多种Redis部署方式

```yaml
redis:
  # 需要在同一命名空间中定义redis的服务发现
  # redis部署方式 单节点-single 集群模式-cluster 哨兵模式-sentinel
  type: cluster
  single:
    host_port: redis
  cluster:
    host_port: redis-cluster:6379
  sentinel:
    db: 1
    password: password
    service_name: mymaster
    host_port: redis-sentinel-01:6379,redis-sentinel-02:6379,redis-sentinel-03:6379
```

### 调用

```python
from elf_py_utils import redis_util

redis = redis_util.connect_redis()
```

### 依赖

```txt
redis==3.5.3
redis-py-cluster==2.1.3
```


