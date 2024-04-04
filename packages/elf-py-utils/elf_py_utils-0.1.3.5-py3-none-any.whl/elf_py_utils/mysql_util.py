import pymysql

from elf_py_utils import elf_core

logger = elf_core.set_logging('DatabaseUtil')
config = elf_core.get_config()


# 连接mysql数据库
def connect_mysql() -> [pymysql, pymysql.cursors]:
    database = pymysql.connect(host=str(config.read_config('mysql.host')),
                               port=int(config.read_config('mysql.port')),
                               user=str(config.read_config('mysql.user')),
                               password=str(config.read_config('mysql.password')),
                               database=str(config.read_config('mysql.database')))
    logger.info("Connect to MySQL success")
    return [database, database.cursor()]
