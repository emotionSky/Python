from selenium import webdriver  # pip install selenium --user
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import pandas as pd  # pip install pyarrow --user      pip install pandas --user
from pathlib import Path

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(browser, 10)


def index_page(page):
    try:
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


def parse_table():
    table = browser.find_element(
        By.CSS_SELECTOR,
        '#dataview > div.dataview-center > div.dataview-body > table')
    table_content = table.find_elements(By.TAG_NAME, 'td')
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
    return df_table


def write_to_file(df_table, category, folder):
    df_table.to_excel(folder / f'{category}.xlsx',
                      sheet_name='Sheet1',
                      index=False)


def set_table():
    year = int(float(input('请输入要查询的年份(如2020)：')))
    while (year < 2009) or (year > 2021):
        year = int(float(input('年份输入错误，请重新输入：')))
    quarter = int(float(input('请输入季度对应的数字(1-一季报；2-年中报；3-三季报；4-年报)：')))
    while (quarter < 1) or (quarter > 4):
        quarter = int(float(input('季度输入错误，请重新输入：')))
    quarter = f'{quarter * 3:02d}'
    date = f'{year}{quarter}'
    tables = int(
        input(
            '请输入报表种类对应的数字(1-业绩报表；2-业绩快报；3-业绩预告；4-预约披露时间；5-资产负债表；6-利润表；7-现金流量表)：'
        ))
    dict_tables = {
        1: '业绩报表',
        2: '业绩快报',
        3: '业绩预告',
        4: '预约披露时间',
        5: '资产负债表',
        6: '利润表',
        7: '现金流量表'
    }
    dict_abbr = {
        1: 'yjbb',
        2: 'yjkb',
        3: 'yjyg',
        4: 'yysj',
        5: 'zcfz',
        6: 'lrb',
        7: 'xjll'
    }
    category = dict_abbr[tables]
    url = f'http://data.eastmoney.com/bbsj/{date}/{category}.html'
    print(url)
    start_page = int(input('请输入爬取的起始页码：'))
    nums = input('请输入爬取的页数(若需爬取全部则按Enter键)：')
    browser.get(url)
    pn_list = browser.find_element(By.CSS_SELECTOR, '.pagerbox > a')
    max_page = int(pn_list.text)
    if nums.isdigit():
        end_page = start_page + int(nums) - 1
        if end_page > max_page:
            end_page = max_page
    elif nums == '':
        end_page = max_page
    else:
        print('页数输入错误')
    print(f'准备爬取：{date}-{dict_tables[tables]}-第{start_page}～{end_page}页')
    yield {
        'url': url,
        'category': dict_tables[tables],
        'start_page': start_page,
        'end_page': end_page
    }


def main(page):
    try:
        index_page(page)
        df_table = parse_table()
        print(f'第{page}页爬取完成')
        return df_table
    except Exception:
        print('爬取失败')


dst_folder = Path('./输出文件/财务数据')
if not dst_folder.exists():
    dst_folder.mkdir(parents=True)
for i in set_table():
    category = i.get('category')
    start_page = i.get('start_page')
    end_page = i.get('end_page')
all_data = pd.DataFrame()
for page in range(start_page, end_page + 1):
    df_table = main(page)
    all_data = pd.concat([all_data, df_table], ignore_index=True)
write_to_file(all_data, category, dst_folder)
print('爬取完成')
