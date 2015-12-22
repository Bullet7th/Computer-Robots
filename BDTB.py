# -*- coding:utf-8 -*-
import urllib2
import re
import codecs

#处理页面标签类
class Tool:
    # 去除img标签,7位长空格
    removeImg = re.compile('<img.*?src="')
    # 删除图片链接后面多余部分
    removeother = re.compile('".*?pic_ext=.*?>')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    # 把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    # 图片链接前缀
    replaceA = re.compile('http:')
    # 图片链接后缀
    replaceB = re.compile('jpg')
    # 过长空格7
    removespace7 = re.compile('       ')
    # 过长空格2
    removespace2 = re.compile('  ')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n\n    ", x)
        x = re.sub(self.replaceBR, "\n\n", x)
        x = re.sub(self.replaceA, "![](http:", x)
        x = re.sub(self.replaceB, "jpg)", x)
        x = re.sub(self.removeother, "", x)
        x = re.sub(self.removespace7, "", x)
        x = re.sub(self.removespace2, "", x)
        x = re.sub(self.removeExtraTag, "", x)
        # strip()将前后多余内容删除
        return x.strip()


class BDTB:
    # 定义参数
    def __init__(self, baseUrl, seeLZ):
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.replaceTool = Tool()
        self.fq = None

    # 获取指定页数的页面
    def getPage(self, pageNum):
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"SOMETHING IS WRONG!", e.reason
                return None

    # 获取总页数
    def getpageNum(self):
        page = self.getPage(1)
        pattern = re.compile('<span.*?class="red">(.*?)</span>.*?</li>.*?l_reply_num', re.S)
        result = re.search(pattern, page)
        if result:
            # strip()去除字符串开头的空格
            return result.group(1).strip()
        else:
            return None

    # 获取主题
    def getTitle(self):
        page = self.getPage(1)
        pattern = re.compile('h3.*?class.*?title=.*?style=.*?width:.*?>(.*?)</h3>.*?<span', re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None

    # 获取指定页的各楼内容
    def getContent(self, page):
        pattern = re.compile('j_d_post_content.*?>(.*?)</div>', re.S)
        result = re.findall(pattern, page)
        return result

    def writeData(self,content):
        for i in range(len(content)):
            content[i] = self.replaceTool.replace(content[i])
            self.fq.write(content[i])
            self.fq.write('\n\n' + u'-----------------------------------------line-----------------------------------------' + '\n\n')

    def start(self):
        pageNum = self.getpageNum()
        title = self.getTitle()
        filename = title + '.txt'
        self.fq = codecs.open(filename, 'w', 'utf-8')
        if pageNum == None:
            print u"URL is wrong"
            return
        try:
            print "there are " + str(pageNum) + "pages"
            for i in range(1, int(pageNum) + 1):
                print "it is the " + str(i) + "st page"
                page = self.getPage(i)
                content = self.getContent(page)
                self.writeData(content)
            self.fq.close()
        except IOError, e:
            print "写入异常，原因" + e.message
        finally:
            print "写入任务完成"


replaceTool = Tool()
# 此处为贴吧帖子地址
baseUrl = ''
bdtb = BDTB(baseUrl, 1)
bdtb.start()

