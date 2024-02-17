import re

str = '123**?Qwe!_@#你我他'
# 从开头匹配，如果开头不满足正则表达式，则之后满足的字符串也不会被匹配到
# python 3.12 会报警告，3.12的bug
result = re.match('\w', str)
value = result.group()
print(value)
