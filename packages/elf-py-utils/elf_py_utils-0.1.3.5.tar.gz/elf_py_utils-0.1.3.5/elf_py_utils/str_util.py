"""
字符串常用判断方法工具类
"""


def is_null(string: str) -> bool:
    return string is None


def is_not_null(string: str) -> bool:
    return string is not None


def is_blank(string: str) -> bool:
    return not bool(string)


def is_not_blank(string: str) -> bool:
    return bool(string)
