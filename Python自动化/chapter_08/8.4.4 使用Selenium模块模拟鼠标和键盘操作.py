from selenium import webdriver

# XPath法
browser1 = webdriver.Chrome()
browser1.get('https://www.baidu.com')
# //*[@id="kw"]
# find_element_by_xpath 已经在高版本中被移除
# browser1.find_element_by_xpath('//*[@id="kw"]').send_keys('python')
browser1.find_element("xpath", '//*[@id="kw"]').send_keys('python')
# //*[@id="su"]
# browser1.find_element_by_xpath('//*[@id="su"]').click()
browser1.find_element("xpath", '//*[@id="su"]').click()
browser1.quit()

# css_selector法
browser2 = webdriver.Chrome()
browser2.get('https://www.baidu.com')
# find_element_by_css_selector  已经在高版本中被移除
# browser2.find_element_by_css_selector('#kw').send_keys('python')
browser2.find_element("css selector", '#kw').send_keys('python')
# browser2.find_element_by_css_selector('#su').click()
browser2.find_element("css selector", '#su').click()
browser2.quit()
