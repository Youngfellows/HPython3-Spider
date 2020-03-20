# coding=utf-8

import traceback
import sys
import json
import os

try:
    print("1 = ", os.path)
    print("2 = ", os.sep)
    print("3 = ", os.path.realpath(__file__))
    print("4 = ", os.path.split(os.path.realpath(__file__)))
    print("5 = ", os.path.split(os.path.realpath(__file__))[0])

    config_path = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'config.json'
    if not os.path.isfile(config_path):
        sys.exit(u'当前路径：%s 不存在配置文件config.json' %
                 (os.path.split(os.path.realpath(__file__))[0] + os.sep))
    with open(config_path) as f:
        try:
            config = json.loads(f.read())
        except ValueError:
            sys.exit(u'config.json 格式不正确，请参考 '
                     u'https://github.com/dataabc/weibo-crawler#3程序设置')
    # wb = Weibo(config)
    # wb.start()  # 爬取微博信息
    print("config: {}".format(config))

except Exception as e:
    print('Error: ', e)
    traceback.print_exc()
