import re

str = '**8!123**?Qwe!_@#你我他'
# 指挥返回匹配的第一个字符串的位置和值
# python 3.12 会报警告，3.12的bug
result = re.search('\w', str)
value = result.group()
location = result.span()
print(value)
print(location)
