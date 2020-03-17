#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
import os
import random
from lxml import etree
import logging
import time
import re
import urllib

"""
在当前目录下创建目录管理器
"""


class CreatePathManager:
    def __init__(self):
        self.path = os.getcwd()
        self.path = self.path
        print("CreatePathManager,cur_path = {}".format(self.path))

    # 在当前目录下创建目录
    def mkdir(self, dir_name):
        # files = dir_name + '_' + time.strftime('%Y-%m-%d', time.localtime(time.time()))
        path = self.path + dir_name
        isExists = os.path.exists(path)
        print("CreatePathManager,isExists = {}".format(isExists))

        if not isExists:
            os.makedirs(path)
            # print('创建成功:{}'.format(path))
        else:
            pass
            # print(path + ' 目录已存在')
        print("mkdir,path = {}".format(path))
        return path


"""
火影忍者爬虫
"""


class NarutoSpider(object):

    # 构造函数
    def __init__(self):
        object.__init__(self)
        requests.packages.urllib3.disable_warnings()  # 去除警告
        logging.captureWarnings(True)
        self.host = "http://comic.ikkdm.com"
        self.host_img = "http://v2.kukudm.com/"
        self.target = " http://comic.ikkdm.com/comiclist/3/"  # 火影忍者url
        #self.parent_name = "\\火影忍者\\"
        self.parent_name = r"/火影忍者/"
        self.file_name = "火影忍者.json"
        self.init_headers()

    # 初始化请求头
    def init_headers(self):
        ua_list = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Mobile Safari/537.36'
        ]
        user_agent = random.choice(ua_list)
        self.headers = {'User-Agent': user_agent,
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
                        }

    # 获取html页码结果
    def get_html(self, target):
        response = requests.get(url=target, headers=self.headers, verify=False)
        # 方式1: 解决中文乱码问题
        # html = response.content
        # html = html.decode('utf-8', 'ignore')
        # html = html.decode('gbk', 'ignore')

        # 方式2: 解决中文乱码问题
        # response.encoding = "utf-8"
        response.encoding = "gbk"
        html = response.text
        # print(html)
        return html

    # 下载图片
    def download_pic(self, path, img_url, number):
        try:
            # 下载每页大图
            urllib.request.urlretrieve(img_url, path + "/" + str(number) + '.jpg')
            print('正在保存,第%s张图片' % (number))
        except urllib.error.HTTPError as e:
            print("靠,HTTPError 无法下载第{}张".format(number))
        except urllib.error.URLError as e:
            print("靠,URLError 无法下载第{}张".format(number))
        except:
            print("靠,无法下载第{}张".format(number))

        # 休眠2秒一下
        time.sleep(1)

    # 读取json文件,并转换为字典/列表
    def read2json(self, file_name):
        with open(file_name, "r", encoding="utf-8") as fp:
            chapters = json.load(fp)
        print(chapters)
        return chapters

    # 将列表保存为json
    def writer2json(self, file_name, dict):
        # 删除旧文件
        if file_name in os.listdir():
            os.remove(file_name)

        # dumps()默认中文为ascii编码格式，ensure_ascii默认为Ture
        # 禁用ascii编码格式，返回的Unicode字符串，方便使用
        json_str = json.dumps(dict, ensure_ascii=False)
        with open(file_name, "wb") as fp:
            fp.write(json_str.encode('utf-8'))

    # 解析目录页
    def parse_home(self, html):
        """
            1、在线漫画书
               章节:  //dl[@id="comiclistn"]/dd/a[1]/text()
               连接：//dl[@id="comiclistn"]/dd/a[1]/@href
        """
        dom_tree = etree.HTML(html)  # 解析HTML
        chapters = dom_tree.xpath('//dl[@id="comiclistn"]/dd/a[1]/text()')  # 章节
        links = dom_tree.xpath('//dl[@id="comiclistn"]/dd/a[1]/@href')  # 章节连接
        chapters_list = []  # 保存章节列表
        for chapter, link in zip(chapters, links):
            # print("{}: {}".format(chapter, link))
            chapters_list.append({"title": chapter, "link": self.host + link})
        # print(chapters_list)
        return chapters_list

    """
    函数说明:解析每一章
    Parameters:
        html - HTML页面
    Returns:
        next_page, img_url, count - 下一页的url,当前页的动漫图url,图片总数
    """

    def parse_chapter(self, title, html):
        """
        每个章节
            总页数:  //tbody//td[@valign="top"]/text().re('共(\d+)页')[0]
            图片连接：//tbody//td//a/img/@src
                     //tbody//td//a[1]/img/@src

            下一页: //tbody//td//a[1]/@href
        """
        # 解析
        dom_tree = etree.HTML(html)

        # count = dom_tree.xpath('//tbody//td[@valign="top"]/text()')
        intro = dom_tree.xpath('//table[2]//td[@valign="top"]/text()')[0]
        next_page = dom_tree.xpath('//table[2]//td[@valign="top"]/script[1]')[0]
        img_src = dom_tree.xpath('//table[2]//td[@valign="top"]/script[1]')[0]
        img_src = str(etree.tostring(img_src, encoding="utf-8"))  # 将获取到的节点内容转换为string字符串
        next_page = str(etree.tostring(next_page, encoding="utf-8"))  # 将获取到的节点内容转换为string字符串

        # print("type(intro) = {},size = {}".format(type(intro), len(intro)))
        # print("type(next_page) = {},size = {}".format(type(next_page), len(next_page)))
        # print("type(img_src) = {},size = {}".format(type(img_src), len(img_src)))
        # print("该页图片总数: {}".format(intro))
        # print("type(img_src) = {}".format(type(img_src)))
        # print("图片: {}".format(img_src))
        # print("下一张: {}".format(next_page))

        # 查找数字
        pattern_page = re.compile(r"共(\d+)页")
        pageMatch = pattern_page.search(intro)
        count = int(pageMatch.group(1))
        # print("pageMatch: {}".format(pageMatch))
        # print("pageMatch.groups(): {}".format(pageMatch.groups()))
        # print("pageMatch.group(0): {}".format(pageMatch.group(0)))

        # 匹配图片地址的正则表达式
        # pattern_img = re.compile(r'\+"(.+)\'><span')
        pattern_img = re.compile(r'\+"(.+)\'&gt;&lt;/a&gt;&lt;span')
        pattern_next_page = re.compile(r'&lt;a href=\\\'(.*)\'&gt;&lt;IMG SRC=')
        imgMatch = pattern_img.search(img_src)
        nextPageMatch = pattern_next_page.search(next_page)

        # imgMatch = re.findall(pattern_img, img_src)
        img_url = self.host_img + str(imgMatch.group(1))
        next_page = self.host + str(nextPageMatch.group(1))
        img_url = eval(repr(img_url).replace('\\', ''))  # 替换掉字符中的,反斜杠\
        next_page = eval(repr(next_page).replace('\\', ''))  # 替换掉字符中的,反斜杠\

        # print("imgMatch: {}".format(imgMatch))
        # print("imgMatch.groups(): {}".format(imgMatch.groups()))
        # print("imgMatch.group(0): {}".format(imgMatch.group(0)))
        # print("imgMatch.group(1): {}".format(img_url))
        print("{}章有图片张数: count = {}".format(title, count))
        print("next_page: {}".format(next_page))
        print("img_url: {}".format(img_url))

        return next_page, img_url, count

    # 启动爬虫
    def start(self):
        # 解析目录页
        html = self.get_html(self.target)
        chapters_list = self.parse_home(html)

        # 获取创建子目录管理器
        create = CreatePathManager()
        parent_name = create.mkdir(self.parent_name)

        # 保存到json文件
        self.writer2json(parent_name + self.file_name, chapters_list)

        # 读取json文件
        chapters = self.read2json(parent_name + self.file_name)

        # 循环获取每一章的动漫图片
        chapter_num = 1  # 章节变量
        for chapter in chapters:
            print("******************** 下载第{}章图片 *************************".format(chapter_num))
            # 创建文件夹
            path = create.mkdir(self.parent_name + str(chapter_num))
            # print("path = {}".format(path))

            # 获取每一章动漫的html
            html = self.get_html(chapter["link"])

            # 解析每一章,获取下一页的url,当前页的动漫图url
            next_page, img_url, count = self.parse_chapter(chapter["title"], html)

            # 下载每一章的全部大图
            index_pic = 1
            self.download_pic(path, img_url, index_pic)  # 下载第一张
            index_pic += 1

            # 循环获取每一章的动漫图片
            if count >= 1:
                for page in range(2, count):
                    # 获取每章动漫下一张图片的html
                    html = self.get_html(next_page)

                    # 解析每一章,获取下一页的url,当前页的动漫图url
                    next_page, img_url, count = self.parse_chapter(chapter["title"], html)
                    self.download_pic(path, img_url, index_pic)  # 下载第一张
                    index_pic += 1

            # 继续下一章
            chapter_num += 1


if __name__ == "__main__":
    # 启动爬虫
    narutoSpider = NarutoSpider()
    narutoSpider.start()
