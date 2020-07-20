# coding=utf-8
from pandora.day05_spider.file_path_anager import FilePathManager
from lxml import etree
from tqdm import tqdm
import random
import os
import requests
import json
import re


class XinBiQuGeNovel(object):
    '''新笔趣阁小说下载'''

    def __init__(self):
        object.__init__(self)
        requests.packages.urllib3.disable_warnings()  # 去除警告
        self.base_url = 'https://www.xsbiquge.com'
        self.init_headers()
        self.parent_name = os.sep + "novel" + os.sep
        self.path_manager = FilePathManager()
        self.path = self.path_manager.mkdir(self.parent_name)

    def init_headers(self):
        """初始化请求头"""
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

    def get_html(self, target):
        """获取html页码结果"""
        response = requests.get(url=target, headers=self.headers, verify=False)
        # 方式1: 解决中文乱码问题
        # html = response.content
        # html = html.decode('utf-8', 'ignore')
        # html = html.decode('gbk', 'ignore')

        # 方式2: 解决中文乱码问题
        response.encoding = "utf-8"
        # response.encoding = "gbk"
        html = response.text
        # print(html)
        return html

    def parse_novel_catalog(self, url):
        '''获取小说的目录'''
        html = self.get_html(url)
        dom_tree = etree.HTML(html)
        book_name = dom_tree.xpath('//div[@id="info"]/h1/text()')[0]
        book_author = dom_tree.xpath('//div[@id="info"]/p[1]/text()')[0]
        cover_image = dom_tree.xpath('//div[@class="box_con"]/div[@id="sidebar"]/div[@id="fmimg"]/img/@src')[0]
        intro = dom_tree.xpath('//div[@id="intro"]/p[1]/text()')
        catalogs = dom_tree.xpath('//div[@class="box_con"]/div[@id="list"]/dl/dd/a/text()')
        catalog_urls = dom_tree.xpath('//div[@class="box_con"]/div[@id="list"]/dl/dd/a/@href')
        author = re.split(r'：', book_author)[1]
        intro = "".join(intro)
        print("book_name: {}".format(book_name))
        print("author: {}".format(author))
        print("cover_image: {}".format(cover_image))
        print("intro: {}".format(intro))
        print("tpye(intro): size: {}, {}".format(len(intro), type(intro)))

        # 小说简介的字典
        novel = {"book_name": book_name, "author": author, "cover_image": cover_image, "intro": intro}

        # 小说章节列表
        chapters = []
        for chapter_name, chapter_url in zip(catalogs, catalog_urls):
            chapter = {"chapter_name": chapter_name, "chapter_url": self.base_url + chapter_url}
            chapters.append(chapter)
        novel["chapters"] = chapters
        print(novel)
        return novel

    def save_to_json(self, novel):
        '''保存到本地'''
        file_name = self.path + novel["book_name"] + "_" + novel["author"] + ".json"
        # print("file_name: {}".format(file_name))
        self.writer2json(file_name, novel)

    def down_noval(self, novel):
        '''下载小说'''
        book_name = self.path + novel["book_name"] + ".txt"
        for chapter in tqdm(novel["chapters"]):
            url = chapter["chapter_url"]
            html = self.get_html(url)
            dom_tree = etree.HTML(html)
            chapter_name = dom_tree.xpath(
                '//div[@class="content_read"]/div[@class="box_con"]/div[@class="bookname"]/h1/text()')[0]
            content = dom_tree.xpath('//div[@class="content_read"]/div[@class="box_con"]/div[@id="content"]/text()')
            content = "".join(content).strip().split('\xa0' * 4)
            print("chapter_name: {}".format(chapter_name))
            print("content: {}".format(content))
            with open(book_name, 'a', encoding='utf-8') as f:
                f.write(chapter_name)
                f.write('\n')
                f.write('\n'.join(content))
                f.write('\n\n')

    def read2json(self, file_name):
        """读取json文件,并转换为字典/列表"""
        with open(file_name, "r", encoding="utf-8") as fp:
            chapters = json.load(fp)
        # print(chapters)
        return chapters

    def writer2json(self, file_name, dict):
        """将列表保存为json"""
        # 删除旧文件
        if file_name in os.listdir():
            os.remove(file_name)

        # dumps()默认中文为ascii编码格式，ensure_ascii默认为Ture
        # 禁用ascii编码格式，返回的Unicode字符串，方便使用
        json_str = json.dumps(dict, ensure_ascii=False)
        with open(file_name, "wb") as fp:
            fp.write(json_str.encode('utf-8'))


if __name__ == "__main__":
    xinbiqu = XinBiQuGeNovel()
    book_url = 'https://www.xsbiquge.com/15_15338/'
    novel = xinbiqu.parse_novel_catalog(book_url)
    xinbiqu.save_to_json(novel)
    xinbiqu.down_noval(novel)
