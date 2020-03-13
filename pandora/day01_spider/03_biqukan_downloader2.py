# coding=utf-8
from lxml import etree
import requests
import re
import collections
import json
import os

"""
笔趣看网络小说下载器
    笔趣看url: https://www.biqukan.com
    小说《一念永恒》大纲目录页url: https://www.biqukan.com/1_1094/
"""


class Downloader(object):

    # 构造函数
    def __init__(self, target):
        requests.packages.urllib3.disable_warnings()  # 去除警告
        self.__host = "https://www.biqukan.com"
        self.__target_url = target
        self.__head = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19',
        }
        self._novel_dict = collections.OrderedDict()  # 保存章信息的字典
        self.novel_info = collections.OrderedDict()  # 小说信息的字典
        self._novel_details = []  # 保存小说详情的列表
        self.__novel_name = "无名称"  # 小说名

    # 网络请求
    def __requests_get(self, target):
        # 请求响应
        response = requests.get(url=target, headers=self.__head, verify=False)
        # 方式1: 解决中文乱码问题
        html = response.content
        # html = html.decode('utf-8', 'ignore')
        html = html.decode('gbk', 'ignore')

        # 方式2: 解决中文乱码问题
        # response.encoding = "utf-8"
        # response.encoding = "gbk"
        # html = response.text
        # print(html)
        return html

    # 获取小说详情和大纲目录
    def get_novel_info(self):
        html = self.__requests_get(self.__target_url)
        # 解析HTML
        dom_tree = etree.HTML(html)

        # 1.图书详情
        # 小说名
        novel_name = dom_tree.xpath('//div[contains(@class,"book")]/div[contains(@class,"info")]//h2/text()')[0]
        # 封面
        novel_poster = dom_tree.xpath(
            '//div[contains(@class,"book")]/div[contains(@class,"info")]/div[@class="cover"]/img/@src')[0]
        novel_poster = self.__host + novel_poster
        # 作者
        novel_author = dom_tree.xpath(
            '//div[contains(@class,"book")]/div[contains(@class,"info")]//div[@class="small"]/span[1]/text()')[0]
        novel_author = novel_author.split("：")[1]
        # 简介
        novel_intro = \
            dom_tree.xpath('//div[contains(@class,"book")]/div[contains(@class,"info")]//div[@class="intro"]/text()')[0]
        novel_intro = re.sub(r"\s", "", novel_intro)
        print("******************** 小说详情 **************************")
        print("小说名: {}".format(novel_name))
        print("作  者: {}".format(novel_author))
        print("封面图: {}".format(novel_poster))
        print("简  介: {}".format(novel_intro))

        # 2.每一章
        # 章标题
        catalog_titles = dom_tree.xpath('//div[contains(@class,"listmain")]//dd/a/text()')
        # 章连接
        catalog_links = dom_tree.xpath('//div[@class="listmain"]//dd/a/@href')
        print("******************** 大纲目录 **************************")
        print("章标题: {}".format(catalog_titles))
        print("章连接: {}".format(catalog_links))
        # 正则处理有效章节标题和连接
        pattern = re.compile(r'[第弟](.+)[章张]', re.IGNORECASE)
        numbers = 1  # 保存章节索引
        for title, link in zip(catalog_titles, catalog_links):
            print("{},{}".format(title, link))
            # 正则匹配
            matchObj = pattern.match(title)
            # print("{0},matchObj = {1}".format(title, matchObj))
            if matchObj != None:
                names = str(title).split('章')
                names2 = str(title).split('张')
                index = pattern.findall(names[0] + '章')
                if names2[0] != str(title):
                    index = pattern.findall(names2[0] + "张")
                    names = names2
                    # print("1 index: {},names: {}".format(index, names))
                # print("index: {},name: {}".format(index, names[1]))
                key = "第" + str(numbers) + "章" + names[1]
                self._novel_dict[key] = self.__host + link  # 添加有效章节名称+下载连接到字典
                numbers += 1
                print(key)

        # 添加小说字典信息
        self.__novel_name = novel_name
        self.novel_info["name"] = novel_name
        self.novel_info["author"] = novel_author
        self.novel_info["poster"] = novel_poster
        self.novel_info["intro"] = novel_intro
        self.novel_info["novels"] = self._novel_dict

        print("**************** 小说详情 JSON字符串 ************************")
        file_name = "./novel/" + novel_name + "_大纲.json"
        # 删除旧文件
        if file_name in os.listdir():
            os.remove(file_name)

        # 将字典转化为JSON字符串,禁用ascii编码格式，返回的Unicode字符串，方便使用
        details = json.dumps(self.novel_info, ensure_ascii=False)  # 小说详情
        print(details)
        # 将Unicode字符串以utf-8编码写人文件
        with open(file_name, "wb") as fp:
            fp.write(details.encode("utf-8"))

        # 返回小说详情JSON
        return details

    # 下载每一章小说
    def download(self):
        # 3.具体内容
        # 章内容
        # 上一章
        # 下一章
        # 获取小说下载列表信息
        file_name_text = "./novel/" + self.__novel_name + ".txt"
        file_name = "./novel/" + self.__novel_name + ".json"
        # 删除旧文件
        if file_name_text in os.listdir():
            os.remove(file_name_text)

        for title, link in self._novel_dict.items():
            print("\n{}: {}\n".format(title, link))
            html = self.__requests_get(link)  # 网络请求
            dom_tree = etree.HTML(html)  # 解析HTML
            novel_text = []
            # 标题
            title = dom_tree.xpath('//div[@class="book reader"]/div[@class="content"]/h1/text()')[0]
            # print("\ntitle: {}".format(title))
            novel_text.append("\n" + title + "\n\n")

            # 内容
            contents = dom_tree.xpath('//div[@class="showtxt"]/text()')
            for content in contents:
                content = content.replace('\xa0', '').replace("app2();", "")
                # content = re.sub(r"[\n]+", "\n", content)  # 去除空行和空白
                if content != "\r":
                    content_list = content.split("\r\n")  # 去除空行和空白
                    # print("============== start ==================")
                    # print("content size = {},type(content_list) = {}".format(len(content), type(content_list)))
                    # print(content_list)
                    content = "".join(content_list)
                    novel_text.append(content)
                    # print("============== end ==================")
                    # print(content)

            # 将列表转化为字符串
            text = "\n" + "".join(novel_text) + "\n"
            self.writer(file_name_text, text)

            # 保存小说详情到字典列表
            self._novel_details.append({"title": title, "content": text})

        # 保存字典到json文件
        self.writer2json(file_name, self._novel_details)

    # 下载每一章小说
    def download2(self):
        # 3.具体内容
        # 章内容
        # 上一章
        # 下一章
        # 获取小说下载列表信息
        link = "https://www.biqukan.com/1_1094/5403177.html"
        html = self.__requests_get(link)  # 网络请求
        dom_tree = etree.HTML(html)  # 解析HTML
        novel_text = []
        # 标题
        title = dom_tree.xpath('//div[@class="book reader"]/div[@class="content"]/h1/text()')[0]
        print("\ntitle: {}".format(title))
        novel_text.append("\n" + title + "\n")

        # 内容
        contents = dom_tree.xpath('//div[@class="showtxt"]/text()')
        for content in contents:
            content = content.replace('\xa0', '').replace("app2();", "")
            novel_text.append(content)
            print(content)

        # 将列表转化为字符串
        text = "\n".join(novel_text)

        file_name = "./novel/" + self.__novel_name + ".txt"
        # 删除旧文件
        if file_name in os.listdir():
            os.remove(file_name)

        self.writer(file_name, text)

    # 写入文件
    def writer(self, file_name, content):
        # with open(file_name, "wb") as fp:
        #     fp.write(content.encode("utf-8"))

        with open(file_name, 'a', encoding='utf-8') as f:
            f.write(content)

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


# 程序入口
if __name__ == "__main__":
    print("\n\t\t欢迎使用《笔趣看》小说下载小工具\n\n\t\t作者:JACK-CHEN\t时间:2020-03-12\n")
    print("*************************************************************************")

    # 小说地址
    # target_url = str(input("请输入小说目录下载地址:\n"))
    target_url = "https://www.biqukan.com/1_1094/"

    # 创建下载器
    dl = Downloader(target_url)
    # 获取下载列表信息
    details_novel = dl.get_novel_info()
    print("***************************** 获取小说字典信息  ****************************")
    # 获取小说字典信息
    for key, value in dl.novel_info.items():
        print("{}:{}".format(key, value))

    print("***************************** 获取小说JSON信息  ****************************")
    # 使用JSON解析处理
    print(details_novel)

    print("***************************** 下载小说  ************************************")
    # 下载每页小说并保存
    dl.download()
    print("^_^...恭喜您下载完成...!!!")

if __name__ == "__main2__":
    target_url = "https://www.biqukan.com/1_1094/"

    # 创建下载器
    dl = Downloader(target_url)
    dl.download2()
