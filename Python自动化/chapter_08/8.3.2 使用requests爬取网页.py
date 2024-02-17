import requests  # pip install requests --user
import re

headers = {
    'User_Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}
url = 'https://www.cnblogs.com'

# 参数 headers 用于指定以哪种浏览器的身份发起请求，如果省略，可能导致某些网页爬取失败
response = requests.get(url=url, headers=headers)
code = response.encoding
print(code)
result = response.text
# print(result)
source = '<a class="post-item-title" href=".*?" target="_blank">(.*?)</a>'
title = re.findall(source, result, re.S)
print(title)
