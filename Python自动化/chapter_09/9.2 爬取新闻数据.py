from selenium import webdriver # pip install selenium --user
import re


def sina_news(company):
    chrome_options = webdriver.ChromeOptions()
    # 运行的时候不显示浏览器窗口
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(options=chrome_options)
    # 新浪新闻得搜索挂了，浏览器访问也不行……
    url = f'https://search.sina.com.cn/?q={company}&c=news&sort=time'
    browser.get(url)
    data = browser.page_source
    browser.quit()
    p_title = '<div class="box-result clearfix".*?<a href=".*?" target="_blank">(.*?)</a>'
    p_href = '<div class="box-result clearfix".*?<a href="(.*?)" target="_blank">'
    p_date = '<span class="fgray_time">(.*?)</span>'
    
    # 这里加上参数 re.S ，这样才能在查找的时候考虑换行，否则会提取不到内容
    title = re.findall(p_title, data, re.S)
    href = re.findall(p_href, data, re.S)
    date = re.findall(p_date, data, re.S)
    
    for i in range(len(title)):
        # 将 <.*?> 替换为空字符，等效于删除
        title[i] = re.sub('<.*?>', '', title[i])
        date[i] = date[i].split(' ')[1]
        print(f'{i + 1}.{title[i]} | {date[i]}')
        print(href[i])


companies = ['阿里巴巴', '京东', '万科', '腾讯']
for i in companies:
    try:
        sina_news(i)
        print(f'【{i}】的信息爬取成功')
    except:
        print(f'【{i}】的信息爬取失败')
