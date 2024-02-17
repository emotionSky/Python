from selenium import webdriver  # pip install selenium --user

chrome_options = webdriver.ChromeOptions()
# 使用 --headless 参数可启用无界面浏览器模式，即在运行中并不会弹出浏览器窗口
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)
browser.get('http://finance.sina.com.cn/realstock/company/sh000001/nc.shtml')
data = browser.page_source
print(data)
title = browser.title
print("当前浏览器标题: ", title)
browser.quit()
