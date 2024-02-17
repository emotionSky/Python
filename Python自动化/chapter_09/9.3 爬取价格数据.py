from selenium import webdriver  # pip install selenium --user
import pandas as pd  # pip install pyarrow --user      pip install pandas --user
import time
from pathlib import Path

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)
browser.get('http://zdscxx.moa.gov.cn:8080/nyb/pc/frequency.jsp')
time.sleep(2)
# find_element_by_xpath 在高版本中被弃用
# /html/body/div[1]/div[3]/div[3]/div[1]/i
# browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[3]/div[1]/i').click()
browser.find_element("xpath",
                     '/html/body/div[1]/div[3]/div[3]/div[1]/i').click()
# /html/body/div[1]/div[3]/div[3]/div[2]/ul/li[1]/a
# browser.find_element_by_xpath(
#     '/html/body/div[1]/div[3]/div[3]/div[2]/ul/li[1]').click()
browser.find_element(
    "xpath", '/html/body/div[1]/div[3]/div[3]/div[2]/ul/li[1]/a').click()

all_data = pd.DataFrame()
for page in range(7):
    time.sleep(2)
    data = browser.page_source
    # read_html() 函数是根据HTML标签来解析表格
    table = pd.read_html(data)[0]
    all_data = all_data._append(table)
    # browser.find_element_by_link_text('下一页').click()
    browser.find_element("link text", '下一页').click()

browser.quit()

dst_folder = Path('./输出文件')
if not dst_folder.exists():
    dst_folder.mkdir(parents=True)
all_data.to_excel(dst_folder / '农产品批发价格.xlsx', index=False)
