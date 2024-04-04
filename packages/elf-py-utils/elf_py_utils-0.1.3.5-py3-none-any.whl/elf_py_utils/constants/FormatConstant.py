import re

# 正整数
number_pattern = "^\d*$"
# UTC时间格式
utc_time_format = '{}-{}-{}T{}:{}:{}.{}Z'
# YYYY-MM-DD hh:mm:ss
common_time_format = '{}-{}-{} {}:{}:{}'

if __name__ == '__main__':
    print(re.match(number_pattern, "0132132156"))

