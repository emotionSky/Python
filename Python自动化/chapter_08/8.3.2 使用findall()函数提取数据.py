import re

str = '123Qwe!_@#你我他'

# findall
# 匹配数字、字母、下划线、汉字
result1 = re.findall('\w', str)
result2 = re.findall('\W', str)
print('result1: ', result1)
print('result2: ', result2)

# 匹配任意空白字符
result3 = re.findall('\s', str)
result4 = re.findall('\S', str)
print('result3: ', result3)
print('result4: ', result4)

# 匹配数字
result5 = re.findall('\d', str)
result6 = re.findall('\D', str)
print('result5: ', result5)
print('result6: ', result6)

str = '你好吗？我很好！'

# 匹配字符串开始结束位置
result7 = re.findall('^你好', str)
result8 = re.findall('好！$', str)
print('result7: ', result7)
print('result8: ', result8)

str = "abcaaabb"
# . 用于匹配除换行符以外的任意字符
# * 用于匹配0或多个字符
# . 和 * 组合后， .* 为贪婪匹配
# .*? 组合后，为非贪婪匹配
result9 = re.findall('a.b', str)
result10 = re.findall('a?b', str)
result11 = re.findall('a*b', str)
result12 = re.findall('a.*b', str)
result13 = re.findall('a.*?b', str)
print('result9: ', result9)
print('result10: ', result10)
print('result11: ', result11)
print('result12: ', result12)
print('result13: ', result13)

str = "aab abb acb azb a1b"
# 中间的内容匹配
result14 = re.findall('a[a-z]b', str)
result15 = re.findall('a[0-9]b', str)
result16 = re.findall('a[ac1]b', str)
print('result14: ', result14)
print('result15: ', result15)
print('result16: ', result16)

str = "123qwer"
# \w+ 表示匹配一个或多个数字、字母、下划线
# (\w+)q(\w+) 表示取出字符 q 前后的一个或多个数字、字母、下划线
result17 = re.findall('(\w+)q(\w+)', str)
print('result17: ', result17)

str = "先生们，女士们，欢迎来到这里！"
# 多种匹配
result18 = re.findall('女士|先生', str)
print('result18: ', result18)

str = "<h2>文本A<变化的网址>文本B新闻标题</h2>"
# .*? 代表不确定的文本，并且不需要提取
# (.*?) 代表需要提取的文本，不确定格式
regex = "<h2>文本A.*?文本B(.*?)</h2>"
result19 = re.findall(regex, str)
print('result19: ', result19)
