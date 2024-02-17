from selenium import webdriver  # pip install selenium --user
import time
import re

use_test = True
test_cycle = 2

# 访问网页获取数据源
browser = webdriver.Chrome()
url = 'http://www.cninfo.com.cn/new/fulltextSearch?notautosubmit=&keyWord=理财'
browser.get(url)
time.sleep(3)
data = browser.page_source
p_count = '<span class="total-box" style="">约(.*?)条'  # 使用正则表达式来提取公告总数
count = re.findall(p_count, data)[0]
pages = int(int(count) / 10)
datas = []
datas.append(data)

page_cycle = test_cycle
if use_test == False:
    page_cycle = pages
for i in range(page_cycle):
    # find_element_by_xpath 已经在高版本中被移除
    # browser.find_element_by_xpath(
    #     '//*[@id="fulltext-search"]/div[2]/div/div/div[2]/div[4]/div[2]/div/button[2]'
    # ).click()
    browser.find_element(
        "xpath",
        '//*[@id="fulltext-search"]/div[2]/div/div/div[2]/div[4]/div[2]/div/button[2]'
    ).click()
    # //*[@id="fulltext-search"]/div[2]/div/div/div[2]/div[4]/div[2]/div/button[2]
    # 通过在网页上查找 下一页 按钮元素对应的js代码后，拷贝 xpath 得到的
    time.sleep(3)
    data = browser.page_source
    datas.append(data)
    time.sleep(3)

alldata = ''.join(datas)  # 使用空字符串作为连接符完成转换成字符串的操作
browser.quit()

# 处理数据
p_title = '<span title="(.*?)" class="r-title">'  # 得到公告标题的正则表达式
p_href = '<a target="_blank" href="(.*?)".*?<span title='  # 得到公告uri的正则表达式
title = re.findall(p_title, alldata)
href = re.findall(p_href, alldata)

title_cycle = test_cycle
if use_test == False:
    title_cycle = len(title)
for i in range(title_cycle):
    # 在标题中会存在 <em> 这些元素的填充，所以需要将这些元素删除
    title[i] = re.sub('<.*?>', '', title[i])
    # 在uri前补足网址，得到完整的url
    href[i] = 'http://www.cninfo.com.cn' + href[i]
    # url中会有字符串 amp; 需要删除，这个字符串是html中用于实现空格的
    href[i] = re.sub('amp;', '', href[i])
    print(str(i + 1) + '.' + title[i])
    print(href[i])

href_cycle = test_cycle
if use_test == False:
    href_cycle = len(href)
for i in range(href_cycle):
    browser = webdriver.Chrome()
    browser.get(href[i])
    try:
        # //*[@id="noticeDetail"]/div/div[1]/div[3]/div[1]/button
        # 随便点开一个公告，然后还是找到 公告下载 按钮对应的js代码，然后复制 XPath 得到
        # browser.find_element_by_xpath(
        #     '//*[@id="noticeDetail"]/div/div[1]/div[3]/div[1]/button').click()
        browser.find_element(
            "xpath",
            '//*[@id="noticeDetail"]/div/div[1]/div[3]/div[1]/button').click()
        time.sleep(3)
        browser.quit()
        print(str(i + 1) + '.' + title[i] + '下载完毕')
    except:
        print(title[i] + '没有PDF文件')
