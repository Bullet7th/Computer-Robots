# -*- coding:utf-8 -*-
import urllib2
import re
import codecs
filename = 'QSBK.txt'
fq = codecs.open(filename, 'w', 'utf-8')


# 定义类
class QSBK:
    # 初始化方法，定义一些变量
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Google Update/1.3.28.15;winhttp;cup-ecdsa'
        # 初始化headers
        self.headers = {'User-Agent': self.user_agent}
        # 存放段子的变量
        self.stories = []
        # 判断程序是否继续运行的变量
        self.enable = False

    # 传入页的索引，获得页面代码
    def getPage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex) + '?s=4830650'
            # 构建request
            request = urllib2.Request(url,headers = self.headers)
            # 用urlopen获取页面代码
            response = urllib2.urlopen(request)
            # 将页面转化为utf-8编码
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接失败，错误原因",e.reason
                return None

    # 传入某一页的代码，返回本页段子列表
    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "页面加载失败……"
            return None
        pattern = re.compile('<div.*?class="article.*?<div.*?class="content">(.*?)<!--.*?</div>', re.S)
        items = pattern.findall(pageCode)
        # 把段子存入文件
        fq.write(u'第' + str(pageIndex) + u'页：\n\n')
        for i in range(len(items)):
            items[i] = items[i].replace(u'<br/>', '\n')
            fq.write(items[i].strip() + '\n')
        print u"已存入第" + str(pageIndex) + u"页的段子"

    # 开始方法
    def start(self):
        print u"开始存储QSBK段子"
        self.enable = True
        for pageIndex in range(1,11):
            self.getPageItems(pageIndex)
        fq.close()
        print u"段子已存储结束"

QSBK_spider = QSBK()
QSBK_spider.start()



