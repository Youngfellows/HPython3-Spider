# coding=utf-8
from lxml import etree
import requests
import re

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

    # 获取小说每一张的名字和下载连接
    def get_download_url(self):
        # 请求响应
        response = requests.get(url=self.__target_url, headers=self.__head, verify=False)
        # 方式1: 解决中文乱码问题
        html = response.content
        # html = html.decode('utf-8', 'ignore')
        html = html.decode('gbk', 'ignore')

        # 方式2: 解决中文乱码问题
        # response.encoding = "utf-8"
        # response.encoding = "gbk"
        # html = response.text
        print(html)

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

        # 3.具体内容
        # 章内容
        # 上一章
        # 下一章


# 下载每一章小说
def download(self):
    pass


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
    dl.get_download_url()
