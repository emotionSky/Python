from selenium import webdriver  # pip install selenium --user
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from pathlib import Path

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(browser, 10)


def index_page(page):
    try:
        url = 'http://data.eastmoney.com/bbsj/201909/lrb.html'
        browser.get(url)
        print(f'正在爬取第{page}页')
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 '#dataview > div.dataview-center > div.dataview-body > table'
                 )))
        if page > 1:
            pg_no = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="gotopageindex"]')))
            pg_no.clear()
            pg_no.send_keys(page)
            submit = wait.until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    '#dataview > div.dataview-pagination.tablepager > div.gotopage > form > input.btn'
                )))
            submit.click()
            time.sleep(5)
        wait.until(
            EC.text_to_be_present_in_element((
                By.CSS_SELECTOR,
                '#dataview > div.dataview-pagination.tablepager > div.pagerbox > a.active'
            ), str(page)))
    except Exception:
        return None


import pandas as pd  # pip install pyarrow --user      pip install pandas --user


def parse_table(n):
    all_data = pd.DataFrame()
    for page in range(1, n + 1):
        index_page(page)
        table = browser.find_element(
            By.CSS_SELECTOR,
            '#dataview > div.dataview-center > div.dataview-body > table')
        table_content = table.find_elements_by_tag_name('td')
        lists = []
        for i in table_content:
            lists.append(i.text)
        column = len(
            table.find_elements(By.CSS_SELECTOR, 'tbody > tr:nth-child(1) td'))
        lists = [lists[i:i + column] for i in range(0, len(lists), column)]
        lists_link = []
        links = table.find_elements(By.CSS_SELECTOR, 'td:nth-child(4) > a.red')
        for i in links:
            url = i.get_attribute('href')
            lists_link.append(url)
        lists_link = pd.Series(lists_link)
        df_table = pd.DataFrame(lists)
        df_table['url'] = lists_link
        all_data = pd.concat([all_data, df_table], ignore_index=True)
    return all_data


dst_folder = Path('./输出文件')
if not dst_folder.exists():
    dst_folder.mkdir(parents=True)
all_data = parse_table(3)
all_data.to_excel(dst_folder / '利润表1.xlsx', sheet_name='Sheet1', index=False)
