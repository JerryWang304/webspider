#!/usr/bin/python
#encoding:utf-8
"""
输入: 花瓣网相册地址
输出: 相册里的图片
"""

import urllib2,urllib
import re
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class HuaBan:
    def __init__(self,album_url):
        self.url = album_url

    # 得到网页的HTML代码
    def get_page(self):
        try:
            request = urllib2.Request(self.url)
            response = urllib2.urlopen(request)
            page = response.read().decode('utf-8')
            return page
        except urllib2.URLError, e:
            if hasattr(e,'reason'):
                print "连接失败："+e.reason
            return None

    # 获取相册标题
    def get_title(self):
        pattern = re.compile('<h1 class="board-name">(.*?)</h1>')
        page = self.get_page()
        title = re.search(pattern,page)
        title = title.group(1)
        # 如果title含有'/'字符，则将其替换为'-'

        pattern = re.compile(r'/+')
        has_slash = re.search(pattern,title)
        if has_slash:
            print "这个相册的名字包含/,将其替换为-"
            title = re.sub(pattern,'-',title)
        return title


    # 得到相册里每张图片的url
    def get_picture_urls(self):
        page = self.get_page()
        pattern = re.compile('<div data-id=.*?<img src="//(.*?)"',re.S)
        # result: list
        result = re.findall(pattern,page)
        if result:
            for el in result:
                el = "http://"+el
            return result
        else:
            return None

    # 为这个相册创建一个文件夹
    def mkdir(self):
        # 获取当前文件位置
        current_dir = os.getcwd()
        path = current_dir+'/'+str(self.get_title())
        if not os.path.exists(path):
            os.makedirs(path)
            return path
        else:
            print "文件夹已经存在！"

    # 将文件保存到新建的文件夹中
    # urls: list
    def save_images(self,urls):
        number = 0
        # 新建文件夹
        dir = self.mkdir()
        print "dir: "
        print dir
        for url in urls:
            # 从url获取图片
            print "current url: ",
            print url
            url = "http://"+url
            u = urllib.urlopen(url)
            
            image = u.read()
            # 文件按编号命名
            filename = dir+'/'+str(number)+'.jpg'
            number += 1
            print "文件名：",filename
            f = open(filename,'wb')
            f.write(image)
            f.close()
        print "文件下载完毕！"
    # 调用前面的函数，完成图片下载任务
    def run(self):
        urls = self.get_picture_urls()
        self.save_images(urls)



if __name__ == '__main__':
    album = 'http://huaban.com/boards/25074520/'
    hb = HuaBan(album)
    #pictures = hb.get_picture_urls()
    #hb.mkdir()
    #print hb.get_title()
    #print pictures
    hb.run()

