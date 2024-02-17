import requests  # pip install requests --user
import re
import pandas as pd  # pip install pyarrow --user      pip install pandas --user
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule  # pip install schedule --user
import time
from pathlib import Path

user = '***@qq.com'
code = 'thoh****vbbb****'
to = '****@qq.com'


def e_mail():

    def dangdang(page):
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        }
        url = 'http://search.dangdang.com/?key=python&act=input&page_index=' + str(
            page)
        response = requests.get(url=url, headers=headers).text
        p_name = '<p class="name".*?title="(.*?)"'
        p_comments = '<span class="search_star_black">.*?<a href=".*?".*?>(.*?)</a>'
        p_link = '<p class="name".*?href="(.*?)"'
        name = re.findall(p_name, response, re.S)
        comments = re.findall(p_comments, response, re.S)
        link = re.findall(p_link, response, re.S)
        data = {'书名': name, '评论数': comments, '链接': link}
        data = pd.DataFrame(data)
        return data

    dst_folder = Path('./输出文件')
    if not dst_folder.exists():
        dst_folder.mkdir(parents=True)
    all_data = pd.DataFrame()
    for i in range(1, 3):
        all_data = all_data._append(dangdang(i))
    all_data.to_excel(dst_folder / 'python.xlsx', index=False)
    message = MIMEMultipart()
    attachment = MIMEText(
        open(dst_folder / 'python.xlsx', 'rb').read(), 'base64', 'utf-8')
    attachment['Content-Type'] = 'application/octet-stream'
    attachment.add_header('Content-Disposition',
                          'attachment',
                          filename=('utf-8', '', 'python.xlsx'))
    message.attach(attachment)
    message['Subject'] = '邮件主题'
    message['From'] = user
    message['To'] = to
    server = smtplib.SMTP_SSL('smtp.qq.com', 465)
    server.login(user, code)
    server.send_message(message)
    server.quit()
    print('邮件发送成功！')


schedule.every().day.at('11:30').do(e_mail)
while True:
    schedule.run_pending()
    time.sleep(10)
