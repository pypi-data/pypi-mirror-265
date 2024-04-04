import sys

sys.path.append('')

from elf_py_utils import BaseUtil, redis_util

logger = BaseUtil.set_logging('RedisCMD')

redis = redis_util.connect_redis()


def redis_get(param: str):
    key = param.split(' ')[1]
    result = redis.get(key)
    if result is None:
        result = 'nil'
    print(result)


def redis_set(param: str):
    key = param.split(' ')[1]
    value = param.split(' ')[2]
    redis.set(key, value)
    print(1)


def redis_hget(param: str):
    key = param.split(' ')[1]
    filed = param.split(' ')[2]
    result = redis.hget(key, filed)
    if result is None:
        result = 'nil'
    print(result)


def redis_hgetall(param: str):
    key = param.split(' ')[1]
    result = redis.hgetall(key)
    if result is None:
        result = 'nil'
    print(result)


cmd_dict = {
    'get': redis_get,
    'set': redis_set,
    'hget': redis_hget,
    'hgetall': redis_hgetall
}

"""
del
hgetset


"""

while True:
    cmd = str(input('> '))
    cmd_type = cmd.split(' ')[0]
    if cmd == 'quit':
        break
    elif cmd_type in cmd_dict:
        cmd_param = cmd[len(cmd_type):]
        func = cmd_dict[cmd_type]
        func(cmd_param)
    else:
        print("Can't resolve command like %s" % cmd)
