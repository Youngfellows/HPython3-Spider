#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
import os
import random
from lxml import etree
import logging
import time


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


if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()  # 去除警告
    logging.captureWarnings(True)

    """
    1.妹子图首页url
    """
    target = "https://www.tupianzj.com/meinv/"
    ua_list = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Mobile Safari/537.36'
    ]
    user_agent = random.choice(ua_list)
    headers = {'User-Agent': user_agent, }
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
     2. 美女分类
         分类名称：//div[@class="list_nav clearfix"]//li/a/text()
         分类url：//div[@class="list_nav clearfix"]//li/a/@href
    """
    dom_tree = etree.HTML(html)  # 解析HTML
    category_names = dom_tree.xpath('//div[@class="list_nav clearfix"]//li/a/text()')  # 分类名称
    category_links = dom_tree.xpath('//div[@class="list_nav clearfix"]//li/a/@href')  # 分类url
    # print("category_names: {}".format(category_names))
    # print("category_links: {}".format(category_links))
    categorys = []  # 保存分类美女列表
    for name, link in zip(category_names, category_links):
        # print("{}: {}".format(name, link))
        categorys.append({"category": name, "link": link})
    # print(categorys)

    """
    3. 分类美女
    热门美女专题: 先放着不管
        分类名称: //div[@class="list_con bgff"][2]/h3/text()
        首页url: 上一步2的 url 
        第二页url:  //div[@class="pages"]/ul/li[3]/a/@href
        末尾页url：//div[@class="pages"]/ul/li[last()-1]/a/@href

        每个美女图片title: //div[@class="list_con_box"]/ul/li/a/@title
        每个美女图片连接: //div[@class="list_con_box"]/ul/li/a/@href
    """
    print("*" * 50)
    photo_list = []  # 保存全部图片页的列表
    for category in categorys:
        type = category["category"]
        link = category["link"]
        print("{}:{}".format(type, link))
        category_item = {}  # 分类美女item
        category_item["type"] = type
        link_list = []  # 页面连接url连接列表

        # 获取分类美女页面信息
        if type == "丝袜美女":
            response = requests.get(url=link, headers=headers, verify=False)
            response.encoding = "gbk"
            html = response.text
            # print(html)

            """
            3. 分类美女
              热门美女专题: 先放着不管
              分类名称: //div[@class="list_con bgff"][2]/h3/text()
              首 页url: 上一步2的 url 
              第二页url:  //div[@class="pages"]/ul/li[3]/a/@href
              末尾页url：//div[@class="pages"]/ul/li[last()-1]/a/@href
              下一页url：//div[@class="pages"]/ul/li[last()-2]/a/@href
            
              每个美女图片title: //div[@class="list_con_box"]/ul/li/a/@title
              每个美女图片连接: //div[@class="list_con_box"]/ul/li/a/@href
            """
            dom_tree = etree.HTML(html)  # 解析HTML
            first_url = link
            name = dom_tree.xpath('//div[@class="list_con bgff"][2]/h3/text()')[0]
            second_url = link + dom_tree.xpath('//div[@class="pages"]/ul/li[3]/a/@href')[0]  # 首 页url
            final_url = link + dom_tree.xpath('//div[@class="pages"]/ul/li[last()-1]/a/@href')[0]  # 末尾页url
            next_url = link + dom_tree.xpath('//div[@class="pages"]/ul/li[last()-2]/a/@href')[0]  # 下一页url
            print("分类名称: -->>> {}".format(name))
            print("首页url: -->>> {}".format(first_url))
            print("第二页url: -->>> {}".format(second_url))
            print("下一页url: -->>> {}".format(next_url))
            print("末尾页url: -->>> {}".format(final_url))
            link_list.append(first_url)

            # 继续获取下一页,直至最后一页
            while next_url != final_url:
                # 获取下一页html
                response = requests.get(url=next_url, headers=headers, verify=False)
                response.encoding = "gbk"
                html = response.text

                dom_tree = etree.HTML(html)  # 解析HTML
                name = dom_tree.xpath('//div[@class="list_con bgff"][2]/h3/text()')[0]
                next_url = link + dom_tree.xpath('//div[@class="pages"]/ul/li[last()-2]/a/@href')[0]  # 下一页url
                final_url = link + dom_tree.xpath('//div[@class="pages"]/ul/li[last()-1]/a/@href')[0]  # 末尾页url
                print("2分类名称: -->>> {}".format(name))
                print("2首页url: -->>> {}".format(first_url))
                print("2下一页url: -->>> {}".format(next_url))
                print("2末尾页url: -->>> {}".format(final_url))
                link_list.append(next_url)

                # time.sleep(3)

            category_item["links"] = link_list
            photo_list.append(category_item)

    print("-----------------------------------------")
    print(photo_list)
    writer2json("./images/美女分类列表.json", photo_list)
