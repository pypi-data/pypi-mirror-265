from time import localtime, strftime

# print(strftime('%Y-%m-%d %H:%M:%S', localtime(1650038400)))

format_second = "%d秒"
format_minute = "%d分%d秒"
format_hour = "%d时%d分%d秒"


def format_time_by_second(time_second: int):
    """
    根据输入的时间，格式化输出时间
    x时x分x秒

    :param time_second: 时间（单位：秒）
    :return:
    """
    if time_second:
        second = time_second % 60
        if second == time_second:
            # 秒
            return format_second % second
        else:
            minute = int((time_second / 60) % 60)
            if minute * 60 + second == time_second:
                # 分 秒
                return format_minute % (minute, second)
            else:
                # 时 分 秒
                hour = int(time_second / 60 / 60)
                return format_hour % (hour, minute, second)


if __name__ == '__main__':
    print(format_time_by_second(15))
    print(format_time_by_second(375))
    print(format_time_by_second(10552))
