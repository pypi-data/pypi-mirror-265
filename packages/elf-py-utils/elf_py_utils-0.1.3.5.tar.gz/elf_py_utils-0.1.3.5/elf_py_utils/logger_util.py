import logging

from elf_py_utils.config_util import Config


def set_logging(name: str = 'Main'):
    """配置日志设置

    :param name:
    :return:
    """
    log_formatter = logging.Formatter(Config().get_config().read_config('logging.formatter'))
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    return logger
