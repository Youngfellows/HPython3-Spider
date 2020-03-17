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

"""
在当前目录下创建目录
"""


class CreatePath:
    def __init__(self):
        self.path = os.getcwd()
        self.path = self.path
        print("cur_path = {}".format(self.path))

    def mkdir(self, dir_name):
        # files = dir_name + '_' + time.strftime('%Y-%m-%d', time.localtime(time.time()))
        path = self.path + dir_name
        isExists = os.path.exists(path)
        print(path)
        print("isExists = {}".format(isExists))
        if not isExists:
            os.makedirs(path)
            print('创建成功:{}'.format(path))
        else:
            print(path + ' 目录已存在')
        return path


# 读取json文件,并转换为字典/列表
def read2json(file_name):
    with open(file_name, "r", encoding="utf-8") as fp:
        chapters = json.load(fp)
    print(chapters)
    return chapters


# 将列表保存为json
def writer2json(file_name, dict):
    # 删除旧文件
    if file_name in os.listdir():
        os.remove(file_name)

    # dumps()默认中文为ascii编码格式，ensure_ascii默认为Ture
    # 禁用ascii编码格式，返回的Unicode字符串，方便使用
    json_str = json.dumps(dict, ensure_ascii=False)
    with open(file_name, "wb") as fp:
        fp.write(json_str.encode('utf-8'))


# 获取html页码结果
def get_html():
    pass


if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()  # 去除警告
    logging.captureWarnings(True)

    """
    1.妹子图首页url
    """
    host = "http://comic.ikkdm.com"
    host_img = "http://v2.kukudm.com/"
    target = " http://comic.ikkdm.com/comiclist/3/"
    ua_list = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Mobile Safari/537.36'
    ]
    user_agent = random.choice(ua_list)
    headers = {'User-Agent': user_agent,
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
               }
    response = requests.get(url=target, headers=headers, verify=False)

    # 方式1: 解决中文乱码问题
    # html = response.content
    # html = html.decode('utf-8', 'ignore')
    # html = html.decode('gbk', 'ignore')

    # 方式2: 解决中文乱码问题
    # response.encoding = "utf-8"
    response.encoding = "gbk"
    html = response.text
    # print(html)

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
        chapters_list.append({"chapter": chapter, "link": host + link})
    # print(chapters_list)

    file_name = "./images/火影忍者.json"
    # 保存到json文件
    writer2json(file_name, chapters_list)

    # 读取json文件
    chapters = read2json(file_name)
    create = CreatePath()

    number = 1
    # 循环获取每一章的动漫图片
    for chapter in chapters:
        # create.mkdir("\\火影忍者\\" + str(number))
        # number += 1
        response = requests.get(url=chapter["link"], headers=headers, verify=False)

        # 方式2: 解决中文乱码问题
        # response.encoding = "utf-8"
        response.encoding = "gbk"
        html = response.text
        print(html)

        # 解析结果
        dom_tree = etree.HTML(html)

        """
        每个章节
               总页数:   //tbody//td[@valign="top"]/text().re('共(\d+)页')[0]
            图片连接：//tbody//td//a/img/@src
                     //tbody//td//a[1]/img/@src
    
            下一页: //tbody//td//a[1]/@href
        """
        # count = dom_tree.xpath('//tbody//td[@valign="top"]/text()')
        intro = dom_tree.xpath('//table[2]//td[@valign="top"]/text()')[0]
        img_src = dom_tree.xpath('//table[2]//td[@valign="top"]/script[1]')[0]
        img_src = str(etree.tostring(img_src, encoding="utf-8"))  # 将获取到的节点内容转换为string字符串

        print("type(intro) = {},size = {}".format(type(intro), len(intro)))
        print("type(img_src) = {},size = {}".format(type(img_src), len(img_src)))
        print("该页图片总数: {}".format(intro))
        print("type(img_src) = {}".format(type(img_src)))
        print("图片: {}".format(img_src))

        # 查找数字
        pattern_page = re.compile(r"共(\d+)页")
        pageMatch = pattern_page.search(intro)
        count = pageMatch.group(1)
        # print("pageMatch: {}".format(pageMatch))
        # print("pageMatch.groups(): {}".format(pageMatch.groups()))
        # print("pageMatch.group(0): {}".format(pageMatch.group(0)))
        print("count: {}".format(count))

        # 匹配图片地址的正则表达式
        # pattern_img = re.compile(r'\+"(.+)\'><span')
        pattern_img = re.compile(r'\+"(.+)\'&gt;&lt;/a&gt;&lt;span')
        imgMatch = pattern_img.search(img_src)
        # imgMatch = re.findall(pattern_img, img_src)
        img_url = host_img + str(imgMatch.group(1))
        img_url = eval(repr(img_url).replace('\\', '')) #替换掉字符中的,反斜杠\

        print("imgMatch: {}".format(imgMatch))
        print("imgMatch.groups(): {}".format(imgMatch.groups()))
        print("imgMatch.group(0): {}".format(imgMatch.group(0)))
        print("imgMatch.group(1): {}".format(img_url))
        print("img_url: {}".format(img_url))

        time.sleep(3)
