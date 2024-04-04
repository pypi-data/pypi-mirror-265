"""配置信息 工具类
"""
import configparser
import os

import yaml

CONFIG_TYPE_INT = 'ini'
CONFIG_TYPE_YAML = 'yaml'
CONFIG_TYPE_XML = 'xml'


class ConfigReader:
    """配置读取.
    """

    def __init__(self, config_path, config_type):
        self.config_path: str = config_path
        self.config_type: str = config_type
        self.config_dict: dict = self.__load_config()

    def _load_config_ini(self) -> dict:
        """读取配置文件-ini

        :return: dict格式的配置信息
        """
        # 创建配置文件并获取内容
        config = configparser.ConfigParser()
        config.read(self.config_path, encoding="utf-8")
        # 遍历配置文件组装配置信息字典
        config_dict = {}
        for section in config.sections():
            config_dict[section] = dict(config.items(section, raw=True))

        return config_dict

    def _load_config_yaml(self) -> dict:
        """读取配置文件-yaml

        :return: dict格式的配置信息
        """
        # 读取文件，获取字符串格式的配置信息
        config_file = open(self.config_path, 'r', encoding='utf-8')
        config = config_file.read()
        # 用yaml.load()方法将配置转化为字典
        config_dict = yaml.load(config, Loader=yaml.FullLoader)
        # 显示关闭文件流
        config_file.close()

        return config_dict

    _config_type_dict = {
        CONFIG_TYPE_INT: _load_config_ini,
        CONFIG_TYPE_YAML: _load_config_yaml
    }

    def __load_config(self):
        func = self._config_type_dict.get(self.config_type)
        return func(self)

    def read_config(self, item_path: str):
        """
        根据配置项路径获取配置信息

        :param item_path: 配置项路径，以英文句号.分隔
        :return: 根据具体配置内容，决定返回体的类型
        """
        item_path_list = item_path.split('.')
        config_dict = self.config_dict
        for item in item_path_list:
            config_dict = config_dict[item]

        config_item = config_dict
        return config_item

    def get(self, key):
        """获取配置信息.

       1.优先从环境变量中获取配置
       2.从配置文件中获取配置

       :param key: 配置对应的键路径（在yaml文件中的格式，环境变量中配置时要把英文句号.改为英文下划线_）
       :return:
       """
        env_key = key.replace(".", "_")

        value = os.getenv(env_key)
        if value:
            return value

        try:
            value = self.read_config(key)
        except KeyError as ex:
            print(ex)
        return value


class Config:
    def get_config(self) -> ConfigReader:
        """获取配置信息类

        :return: 配置信息类
        """
        bootstrap = self._get_bootstrap()
        config_file_name = str(bootstrap.read_config('profiles.config.name'))
        config_file_path = str(bootstrap.read_config('profiles.config.path'))
        config_file_type = config_file_name.split('.')[1]
        config_path_yaml = os.path.join(config_file_path)
        config = ConfigReader(config_path_yaml, config_file_type)

        return config

    @staticmethod
    def _get_bootstrap() -> ConfigReader:
        """获取bootstrap信息类

        :return: bootstrap配置信息类
        """
        return ConfigReader('bootstrap.yaml', CONFIG_TYPE_YAML)
