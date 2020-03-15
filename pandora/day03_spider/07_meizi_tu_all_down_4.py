# coding=utf-8
import json
import requests
import os
import random
from lxml import etree
import logging
import time
import re
import urllib

# 保存图片的索引
number = 1


# 根据图片url下载图片
def download_picture(tupian_url):
    global number
    try:
        # 下载每页大图
        urllib.request.urlretrieve(tupian_url, "./images/bigpic/" + str(number) + '.jpg')
        print('正在保存,第%s张图片' % (number))
    except urllib.error.HTTPError as e:
        print("靠,HTTPError 无法下载第{}张".format(number))
    except urllib.error.URLError as e:
        print("靠,URLError 无法下载第{}张".format(number))
    except:
        print("靠,无法下载第{}张".format(number))
    number += 1

    # 休眠2秒
    time.sleep(2)


# 获取每页美女的html信息
def get_meinv_html(url):
    requests.packages.urllib3.disable_warnings()  # 去除警告
    logging.captureWarnings(True)
    target = url
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
    return html


# 从json文件中读取需要下载的每一页没有url连接
def read_url_for_json():
    global number
    # 获取分类美女每一页的美个美女大图
    # 可以读取./images/美女分类列表.jso解析
    with open("./images/美女分类列表.json", "r", encoding="utf-8") as fp:
        meinu_dict = json.load(fp)
    print(meinu_dict)

    for meinv_item in meinu_dict:
        print(type(meinv_item))
        # print(meinv_item)
        # for key, value in meinv_item.items():
        #     print("{}: {}".format(key, value))

        # 获取连接列表
        meinv_type = meinv_item["type"]
        link_list = meinv_item["links"]
        print("美 女 类 型: {}".format(meinv_type))
        print("美女每页url:")
        # print(link_list)
        for link in link_list:
            print(link)
            # get_meinv_html(link)
            """
                    注意: 测试时，只获取第一页的第一个美女图片

                    获取每一页的美女信息
                    1. 美女分类
                        每个美女图片title: //div[@class="list_con_box"]/ul/li/a/@title
                        每个美女图片连接: //div[@class="list_con_box"]/ul/li/a/@href
                    """
            # html = get_meinv_html(link_list[0])
            html = get_meinv_html(link)
            dom_tree = etree.HTML(html)  # 解析HTML
            photo_titles = dom_tree.xpath('//div[@class="list_con_box"]/ul/li/a/@title')  # 图片title
            photo_links = dom_tree.xpath('//div[@class="list_con_box"]/ul/li/a/@href')  # 大图片连接
            print("photo_titles -->> {}".format(photo_titles))
            print("photo_links -->> {}".format(photo_links))
            host = "https://www.tupianzj.com"
            new_poto_linsk = []  # 大图详情连接列表
            for link in photo_links:
                new_poto_linsk.append(host + link)
            print(new_poto_linsk)

            # 获取每个美女的大图
            for meinv_name, link in zip(photo_titles, new_poto_linsk):
                print(meinv_name)
                print(link)
                # 获取美女大图
                # html = get_meinv_html(link)
                # print(html)

                # 临时测试,只获取第一个美女的
                """
                4. 每个美女图片详情
                首图url:  3中的每个美女图片连接
                          https://www.tupianzj.com/meinv/20200225/204976.html
                第二图url: https://www.tupianzj.com/meinv/20200225/204976_2.html
                末尾图url: https://www.tupianzj.com/meinv/20200225/204976_总张的数字.html

                 大图片url:  //div[@id="bigpic"]//a/img/@src
                 总 张  数:  //div[@class="pages"]/ul/li[1]/a/text()
                 下 一  张:  //div[@class="pages"]/ul/li[last()]/a/@href
                             //div[@class="pages"]/ul/li[last()]/a/text()
                """

                # html = get_meinv_html(new_poto_linsk[0])
                html = get_meinv_html(link)
                # print(html)
                dom_tree = etree.HTML(html)  # 解析HTML
                first_url = new_poto_linsk[0]  # 首图url
                count_str = dom_tree.xpath('//div[@class="pages"]/ul/li[1]/a/text()')[0]  # 图片总数
                tupian_url = dom_tree.xpath('//div[@id="bigpic"]//a/img/@src')[0]  # 大图片连接
                pattern = re.compile(r"(\d+)")
                matchObj = pattern.search(count_str)
                count = matchObj.group(0)

                print("matchObj = {}".format(matchObj))
                print("matchObj = {}".format(matchObj.groups()))
                print("matchObj = {}".format(matchObj.group(0)))
                print("首图url: {}".format(first_url))
                print("图片总数: {} -->> {} ".format(count_str, count))
                print("大图片连接: {}".format(tupian_url))

                # 下载首页大图
                download_picture(tupian_url)

                # 轮询下载,第二页到最后一页的图片
                index = first_url.rfind(".html")
                pre_url = first_url[0:index]
                print("index = {}".format(index))
                print(pre_url)

                for page in range(2, int(count) + 1):
                    try:
                        page_url = pre_url + "_" + str(page) + ".html"
                        print("page_url: {}".format(page_url))
                        html = get_meinv_html(page_url)
                        dom_tree = etree.HTML(html)  # 解析HTML
                        tupian_url = dom_tree.xpath('//div[@id="bigpic"]//a/img/@src')[0]  # 大图片连接
                        download_picture(tupian_url)
                    except:
                        print("解析html大图页异常...,继续下一张")


if __name__ == "__main__":
    read_url_for_json()
