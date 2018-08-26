#-*- coding:utf-8 -*-
# 根据输入的名称在百度图片下载
import urllib2
import re
import sys
import os
import time

class Spider:
    def __init__(self, keyword):
        #初始网页加关键字形成新网页
        self.siteURL = 'https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + keyword
        self.i = 1

    # 设置爬取图片数量，打开网页进行爬取
    def getPage(self, pageIndex):
        page = (pageIndex-1)*20
        url = self.siteURL + "&pn=" + str(page)
        headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}
        # 设置睡眠时间，防止ip被封
        sleep_download_time = 10
        try:
            time.sleep(sleep_download_time)
            request = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(request)
            return response.read()
        except urllib2.URLError, e:
            print e.reason

    # 正则匹配，获取图片地址
    def getContents(self, pageIndex, keyword):
        page = self.getPage(pageIndex)
        pattern = re.compile('"objURL":"(.*?)",', re.S)
        items = re.findall(pattern, page)
        #创建文件夹
        self.mkdir(keyword)
        for item in items:
            name = keyword + "/" + keyword + str(self.i) + ".jpg"
            # 保存图片名字为name
            self.saveImg(item, name)
            self.i += 1

    #创建新目录
    def mkdir(self, path):
        path = path.strip()
        #判断路径是否存在
        #存在为True 不存在为False
        isExists = os.path.exists(path)
        if not isExists:
            #如果不存在则创建目录
            print u"新建了名为", path, u"的文件夹"
            #创建目录操作函数
            os.makedirs(path)
            return True
        else:
            #如果目录存在则不创建，并提示目录已存在
            print u"名为", path, u"的文件夹已存在"
            return False

    #保存图片到文件夹
    def saveImg(self, imageURL, fileName):
        try:
            u = urllib2.urlopen(imageURL)
            data = u.read()
            f = open(fileName, 'wb')
            f.write(data)
            print u"正在保存图片为", fileName, u"图片地址为：", imageURL
            f.close()
        except urllib2.URLError, e:
            print e.reason

    #传入起止页码，获取图片
    # def savePagesInfo(self, start, end):
    #     for i in range(start,end+1):
    #         print u"正在查找第",i,u"个地方"
    #         self.getContents(i, self.title)

# 设置编码
reload(sys)
sys.setdefaultencoding('utf-8')
# 获得系统编码格式
type = sys.getfilesystemencoding()
word = raw_input("请输入关键字: ".decode('utf-8').encode('gbk')).decode(type)
spider = Spider(word)
spider.getContents(1, word)


