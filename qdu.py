# -*- coding:utf-8 -*-
import urllib2
import re
import smtplib
import time

from email.mime.text import MIMEText

mailto_list = ['']
mail_host = 'smtp.163.com'
mail_user = ''
mail_pass = ''
mail_postfix = '163.com'


class mail:
    def send_mail(self, to_list, sub, content):
        me = "hello" + "<" + mail_user +"@" + mail_postfix + ">"
        msg = MIMEText(content, _subtype='plain', _charset='utf-8')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ';'.join(to_list)
        try:
            server = smtplib.SMTP()
            server.connect(mail_host)
            server.login(mail_user,mail_pass)
            server.sendmail(me, to_list, msg.as_string())
            server.close()
            return True
        except Exception, e:
            print str(e)
            return False
    def send(self):
        if self.send_mail(mailto_list, '教务已扒下', '\n'.join(stories)):
            print u"发送成功"
        else:
            print u"发送失败"

# 存放的变量
stories = []
# 定义类
class qdu:
    # 初始化方法，定义一些变量
    def __init__(self):
        self.user_agent = 'Google Update/1.3.28.15;winhttp;cup-ecdsa'
        # 初始化headers
        self.headers = {'User-Agent': self.user_agent}
        # 判断程序是否继续运行的变量
        self.enable = False

    # 传入页的索引，获得页面代码
    def getPage(self):
        try:
            url = 'http://jw.qdu.edu.cn/homepage/index.do'
            # 构建request
            request = urllib2.Request(url, headers=self.headers)
            # 用urlopen获取页面代码
            response = urllib2.urlopen(request)
            # 将页面转化为utf-8编码
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接失败，错误原因",e.reason
                return None

    # 传入页代码，返回本页列表
    def getPageItems(self):
        pageCode = self.getPage()
        if not pageCode:
            print "页面加载失败……"
            return None
        pattern = re.compile('<tr>.*?<div>.*?</span>.*?href="(.*?)".*?class.*?title=(.*?)>.*?</span>', re.S)
        items = pattern.findall(pageCode)
        for item in items:
            stories.append(item[1].strip() + '\n')
            stories.append('http://jw.qdu.edu.cn' + item[0].strip() + '\n')

    # 开始方法
    def start(self):
        print u"开始进入教务查看"
        self.enable = True
        self.getPageItems()


qdu_spider = qdu()
qq_mail = mail()
while True:
    time.sleep(1)
    if time.ctime()[12:19]=="6:00:00":
        qdu_spider.start()
        qq_mail.send()


