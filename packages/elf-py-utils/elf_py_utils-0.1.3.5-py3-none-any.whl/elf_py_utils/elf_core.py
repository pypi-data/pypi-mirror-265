"""Elf工具类的核心模块，用户配置的加载

"""
from elf_py_utils import config_util, logger_util


def set_logging(name: str = 'Main'):
    return logger_util.set_logging(name)


def get_config() -> config_util.ConfigReader:
    return config_util.Config().get_config()
