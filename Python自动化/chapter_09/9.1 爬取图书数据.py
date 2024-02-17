import requests  # pip install requests --user
import re
import pandas as pd  # pip install pyarrow --user      pip install pandas --user
from pathlib import Path


def dangdang(page):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    # 页数变化
    url = 'http://bang.dangdang.com/books/bestsellers/1-' + str(page)
    response = requests.get(url=url, headers=headers).text

    p_rank = '<div class="list_num.*?">(.*?).</div>'                                              # 获取排名
    p_picture = '<div class="pic">.*?<img src="(.*?)".*?></a>'                                    # 获取图书封面的图片url
    p_name = '<div class="name".*?title="(.*?)">.*?</a>'                                          # 获取图书的名字
    p_comments = '<div class="star">.*?target="_blank">(.*?)</a>'                                 # 获取图书的评论数
    p_price_discount = '<div class="price">.*?<span class="price_n">&yen;(.*?)</span>.*?</span>'  # 获取图书的折扣价
    p_price = '<div class="price">.*?<span class="price_r">&yen;(.*?)</span>'                     # 获取图书的原价

    # 使用正则表达式拿到数据
    rank = re.findall(p_rank, response)
    picture = re.findall(p_picture, response)
    name = re.findall(p_name, response)
    comments = re.findall(p_comments, response)
    # 这里加上参数 re.S ，这样才能在查找的时候考虑换行，否则会提取不到内容
    price_discount = re.findall(p_price_discount, response, re.S)
    price = re.findall(p_price, response, re.S)

    # 将数据做成字典
    data = {
        '排名': rank,
        '图书封面': picture,
        '书名': name,
        '评论数': comments,
        '折扣价': price_discount,
        '原价': price
    }

    # 将字典转换为 DataFrame 格式的数据
    data = pd.DataFrame(data)
    return data


dst_folder = Path('./输出文件')
if not dst_folder.exists():
    dst_folder.mkdir(parents=True)
all_data = pd.DataFrame()
for i in range(1, 6):
    all_data = all_data._append(dangdang(i))
all_data.to_excel(dst_folder / '当当网图书畅销榜.xlsx', index=False)
