# !/usr/bin/python
# -*- coding: utf-8 -*-
import json


def load_json() -> dict:
    json_file = open('EntityInfo.json', 'r', encoding='utf-8')
    json_str = ''
    for line in json_file.readlines():
        json_str += line
    json_str.replace('\n', '')
    json_str.replace('\t', '')
    json_str.replace(' ', '')

    json_dict: dict = json.loads(json_str)
    return json_dict


def generate_py(dict_info: dict):
    entity_info = dict_info.get('entity_info')
    column_info = dict_info.get('column_info')
    # 1.文件头部内容
    text = "# !/usr/bin/python\n# -*- coding: utf-8 -*-\n"
    text += "from common.BaseEntity import BaseEntity\n\n"
    text += "column_name_list = ['id', 'create_time', 'create_by', 'update_time', 'update_by', 'remark'\n"
    for item in column_info.keys():
        text += ", '%s'" % item
    text += "]\n\n\n"
    # 2.类内容
    # 2.1 字段属性初始化
    text += "class %s(BaseEntity):\n" % entity_info
    for item in column_info.keys():
        column = "\t%s: %s = %s\n"
        if column_info.get(item).get('type') == 'str':
            column = column % (item, 'str', "''")
        elif column_info.get(item).get('type') == 'int':
            column = column % (item, 'int', 0)
        text += column
    # 2.2 类方法-__set方法
    for item in column_info.keys():
        line = "\n\tdef __set_%s(self, value: %s):\n\t\tself.%s = value\n"
        line = line % (item, column_info.get(item).get('type'), item)
        text += line
    text += '\n'
    # 2.3 类方法-通用get方法
    text += "\t# 通用get方法\n"
    text += "\tdef __get_id(self) -> str:\n\t\treturn self._get_sql_value(self.id)\n\n" \
            "\tdef __get_create_time(self) -> str:\n\t\treturn self._get_sql_value(self.create_time)\n\n" \
            "\tdef __get_create_by(self) -> str:\n\t\treturn self._get_sql_value(self.create_by)\n\n" \
            "\tdef __get_update_time(self) -> str:\n\t\treturn self._get_sql_value(self.update_time)\n\n" \
            "\tdef __get_update_by(self) -> str:\n\t\treturn self._get_sql_value(self.update_by)\n\n" \
            "\tdef __get_remark(self) -> str:\n\t\treturn self._get_sql_value(self.remark)\n\n"
    # 2.4 特有get方法
    text += "\t# 特有get方法-private-获取sql语句所需的value\n"
    for item in column_info.keys():
        line = "\tdef __get_%s(self) -> %s:\n\t\treturn self._get_sql_value(self.%s)\n\n"
        line = line % (item, column_info.get(item).get('type'), item)
        text += line
    # 2.5 set_value方法
    text += "\tdef set_value(self, value, value_name):\n\t\t" \
            "fun = self.value_name_map.get(value_name)\n\t\t" \
            "fun(self, value)\n\n"
    # 2.6 get_value方法
    text += "\tdef get_value(self, value_name: str):\n\t\t" \
            "value_name_get_dict = {\n"
    for item in column_info.keys():
        line = "\t\t\t'%s': self.%s,\n"
        line = line % (column_info.get(item).get('comment'), item)
        text += line
    text = text[:-2]
    text += "\n\t\t}\n"
    text += "\t\treturn value_name_get_dict.get(value_name)\n"
    # 2.7 generate_insert_sql生成insert的sql
    text += '\n'
    text += "\tdef generate_insert_sql(self) -> str:\n" \
            "\t\tsql = '(%s)'\n" \
            "\t\tvalue = ''\n" \
            "\t\tfor column_name in column_name_list:\n" \
            "\t\t\tvalue += str(self.value_name_get_dict[column_name](self))\n" \
            "\t\t\tvalue += ','\n" \
            "\t\tvalue = value[:-1]\n" \
            "\n" \
            "\t\treturn sql % value\n"
    # 2.8 value_name_map
    text += '\n'
    text += "\tvalue_name_map = {\n"
    for item in column_info.keys():
        line = "\t\t'%s': __set_%s,\n"
        line = line % (column_info.get(item).get('comment'), item)
        text += line
    text += '\t}\n\n'
    # 2.9 value_name_get_dict
    basic_column_list = ['id', 'create_time', 'create_by', 'update_time', 'update_by', 'remark']
    text += "\tvalue_name_get_dict = {\n"
    for item in column_info.keys():
        line = "\t\t'%s': __get_%s,\n"
        line = line % (item, item)
        text += line
    for item in basic_column_list:
        line = "\t\t'%s': __get_%s,\n"
        line = line % (item, item)
        text += line
    text += '\t}\n'

    out_file = open(entity_info + '.py', 'w', encoding='utf-8')
    out_file.writelines(text)
    out_file.close()


def main():
    json_dict = load_json()
    generate_py(json_dict)


if __name__ == '__main__':
    main()
