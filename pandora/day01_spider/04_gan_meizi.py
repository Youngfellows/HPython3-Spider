#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import urllib
import requests
import os

# 指定url路径,经过查看url获取的信息:0/0是全部的json信息
pre_url = "http://gank.io/api/data/福利/0/0"

# http://gank.io/
# 分类数据: http://gank.io/api/data/数据类型/请求个数/第几页
# 数据类型： 福利 | Android | iOS | 休息视频 | 拓展资源 | 前端 | all
# http://gank.io/api/data/福利/10/1
# 请求个数： 数字，大于0
# 第几页：数字，大于0


# 图片路径列表，有些图片地址是https的，爬取的话需要验证证书,不爬取https开头的图片
http_image_list = []

# 1.获取路径的json数据
response = requests.get(pre_url).text

# 2.jsong格式转换成字符串
data_dict = json.loads(response)

# 3.获取图片地址数量
num = len(data_dict['results'])
for i in range(0, num):
    url_web = data_dict['results'][i]['url']
    # http开头的图片路径,.jpeg图片下载不下了
    if url_web.split(':')[0] == 'http' and url_web.endswith(".jpg"):
        http_image_list.append(url_web)

print("http_image_list: {}".format(http_image_list))

# 保存图片地址为文件
file_name = './images/http_image.txt'

# 删除旧文件
if file_name in os.listdir():
    os.remove(file_name)
with open(file_name, 'wb') as fp:
    data = json.dumps(http_image_list)
    fp.write(data.encode("utf-8"))

# 图片保存路径
http_save_path = "./images/"

# 具体格式可以调整
for x in range(0, 304):
    try:
        urllib.request.urlretrieve(http_image_list[x], http_save_path + str(x) + '.jpg')
        print('正在保存,第%s张图片' % x)
    except urllib.error.HTTPError as e:
        print("靠,无法下载第{}张".format(x))

# 网站有反爬机制，爬取到303个时被拦截报错，此时，翻转过来，倒着爬取
rev = http_image_list[::-1]
for x in range(0, 244):
    try:
        urllib.request.urlretrieve(rev[x], http_save_path + str(x + 244) + '.jpg')
        print('正在保存,第%s张图片' % (x+244))
    except urllib.error.HTTPError as e:
        print("靠,无法下载第{}张".format(x + 244))

print("恭喜您,妹子图已经下载完毕了...")
