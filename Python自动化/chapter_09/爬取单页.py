from selenium import webdriver  # pip install selenium --user
from selenium.webdriver.common.by import By
from pathlib import Path

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)
url = 'http://data.eastmoney.com/bbsj/201909/lrb.html'
browser.get(url)

table = browser.find_element(
    By.CSS_SELECTOR,
    '#dataview > div.dataview-center > div.dataview-body > table')
table_content = table.find_elements(By.TAG_NAME, 'td')
lists = []
for i in table_content:
    lists.append(i.text)
print(lists)

import pandas as pd  # pip install pyarrow --user      pip install pandas --user

column = len(table.find_elements('tbody > tr:nth-child(1) td'))
lists = [lists[i:i + column] for i in range(0, len(lists), column)]
lists_link = []
links = table.find_elements(By.CSS_SELECTOR, 'td:nth-child(4) > a.red')
for i in links:
    url = i.get_attribute('href')
    lists_link.append(url)
lists_link = pd.Series(lists_link)
df_table = pd.DataFrame(lists)
df_table['url'] = lists_link
print(df_table)

dst_folder = Path('./输出文件')
if not dst_folder.exists():
    dst_folder.mkdir(parents=True)
df_table.to_excel(dst_folder / '利润表.xlsx', sheet_name='Sheet1', index=False)
