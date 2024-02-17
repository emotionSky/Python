import smtplib
from email.mime.text import MIMEText

user = '***@qq.com'
code = 'thoh****vbbb****'
to = '****@qq.com'
message = MIMEText('邮件正文内容')
message['Subject'] = '邮件主题'
message['From'] = user
message['To'] = to
server = smtplib.SMTP_SSL('smtp.qq.com', 465)
server.login(user, code)
server.send_message(message)
server.quit()
print('邮件发送成功！')
