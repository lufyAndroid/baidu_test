#!/usr/bin/env python
# -*- coding:utf-8 -*-
import smtplib
from smtplib import SMTP
from email.mime.text import MIMEText
from socket import error,gaierror
from email.mime.multipart import MIMEMultipart
from utils.log import logger


# --*--发送邮件--*---
# smtpservice = 'smtp.163.com'
# user = '18511069163@163.com'
# password = 'qwer123456'
# sender = '18511069163@163.com'
# receiver = '16601184986@163.com'
# subject = '邮件测试'
# # msg = MIMEText('<html><h1>ni hao </h1></html>', 'html', 'utf-8')
# msg = MIMEText('你好', 'plain', 'utf-8')
# msg['Subject'] = Header(subject, 'utf-8')
# msg['From'] = 'Lu<18511069163@163.com>'
# msg['To'] = '16601184986@163.com'
# smtp = SMTP()
# smtp.connect(smtpservice)
# smtp.login(user, password)
# smtp.sendmail(sender, receiver, msg.as_string())
# smtp.quit()
class Email:
    def __init__(self, server, sender, receiver, message, password, title=None):
        self.server = server
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.password = password
        self.title = title
        self.msg = MIMEMultipart('related')

    def send(self):
        self.msg['Subject'] = self.title
        self.msg['From'] = self.sender
        self.msg['To'] = self.receiver

        if self.message:
            self.msg.attach(MIMEText(self.message))

        try:
            smtp_server = SMTP(self.server)
        except (gaierror and error) as e:
            logger.exception('发送邮件失败,无法连接到SMTP服务器，检查网络以及SMTP服务器. %s', e)
        else:
            try:
                smtp_server.login(self.sender, self.password)  # 登录
            except smtplib.SMTPAuthenticationError as e:
                logger.exception('用户名密码验证失败！%s', e)
            else:
                smtp_server.sendmail(self.sender, self.receiver.split(';'), self.msg.as_string())  # 发送邮件
            finally:
                smtp_server.quit()  # 断开连接
                logger.info('发送邮件"{0}"成功! 收件人：{1}。如果没有收到邮件，请检查垃圾箱，'
                            '同时检查收件人地址是否正确'.format(self.title, self.receiver))
