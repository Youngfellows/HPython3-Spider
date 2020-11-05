# coding=utf-8
import json
import os
import json
import shlex
import subprocess
import time
from threading import Thread
import threading


class CloneThread(Thread):
    """
    创建自定义线程
    """

    def __init__(self, source):
        Thread.__init__(self)
        self.source = source

    def run(self):
        # name属性中保存的是当前线程的名字
        msg = "I'm " + self.name + " @ " + self.source
        print(msg)
        self.clone_task(source=self.source)

    def clone_task(self, source):
        """
        开启线程clone 代码
        :param sources: 仓库地址
        :return:
        """
        # 打印出当前线程的名称和id
        print("当前线程的名称:{},线程的ID:{}".format(threading.currentThread().name, threading.currentThread().ident))
        print("开启{}线程,clone代码:{}".format(threading.currentThread().name, source))
        project_url = source
        # project_url = 'https://github.com/NanBox/NestedCalendar.git'

        # 正则获取文件名
        start = project_url.rfind(r'/')
        end = project_url.rfind(r'.git')
        project_name = project_url[start + 1:end]
        # print("start:{},end:{},project_name:{}".format(start, end, project_name))

        # 项目保存路径
        dest = './Calendar/%s' % (project_name)
        print("dest:{}".format(dest))

        # os.system('ls')
        os.system('git clone %s  %s' % (project_url, dest))
        print("in {} ,clone project {} success ...\n\n".format(threading.currentThread().name, project_name))

        # 更新代码
        # os.chdir('NestedCalendar')
        # os.system('git pull')

        # 用完后下面代码可以自动删除。
        # os.system('rm -rf NestedCalendar')


class CalendarClone(object):
    """
    git clone 工具
    """

    def __init__(self):
        object.__init__(self)
        self.file_path = './json/calendar.json'  # 下载列表

    def json2dict(self, json_data):
        """将json字符串转化为python的字典对象"""
        return json.loads(json_data)

    def read2json(self, file_name):
        """读取json文件,并转换为字典/列表"""
        with open(file_name, "r", encoding="utf-8") as fp:
            dict = json.load(fp)
        print(dict)
        return dict

    def writer2json(self, file_name, dict):
        """将字典对象保存为json字符串"""
        # 删除旧文件
        if file_name in os.listdir():
            os.remove(file_name)

        # dumps()默认中文为ascii编码格式，ensure_ascii默认为Ture
        # 禁用ascii编码格式，返回的Unicode字符串，方便使用
        json_str = json.dumps(dict, ensure_ascii=False)
        with open(file_name, "wb") as fp:
            fp.write(json_str.encode('utf-8'))

    def parse_repositories_clone(self):
        """
        解析源代码仓库地址,并clone
        :return: 转化后的字典或者列表
        """
        sources = self.read2json(self.file_path)
        new_sources = []
        for index, source in enumerate(sources):
            print("{} ==>>> {}".format(index, source))
            new_sources.append(source + ".git")
        print(new_sources)

        # 开启多线程线程clone 代码
        for index, source in enumerate(new_sources):
            # self.clone_task(new_sources)
            thread = CloneThread(source=source)
            thread.start()

    def clone_task(self, source):
        """
        开启线程clone 代码
        :param sources: 仓库地址
        :return:
        """
        # 打印出当前线程的名称和id
        print(threading.currentThread().name)
        print(threading.currentThread().ident)
        print("开启{}线程,clone代码:{}".format(threading.currentThread().name, source))
        project_url = source
        # project_url = 'https://github.com/NanBox/NestedCalendar.git'

        # 正则获取文件名
        start = project_url.rfind(r'/')
        end = project_url.rfind(r'.git')
        project_name = project_url[start + 1:end]
        # print("start:{},end:{},project_name:{}".format(start, end, project_name))

        # 项目保存路径
        dest = './Calendar/%s' % (project_name)
        print("dest:{}".format(dest))

        # os.system('ls')
        # os.system('git clone %s  %s' % (project_url, dest))
        print("in {} ,clone project {} success ...\n\n".format(threading.currentThread().name, project_name))

        # 更新代码
        # os.chdir('NestedCalendar')
        # os.system('git pull')

        # 用完后下面代码可以自动删除。
        # os.system('rm -rf NestedCalendar')

    def clone_task2(self):
        """
        克隆代码方式2
        :return:
        """
        project_url = 'https://github.com/NanBox/NestedCalendar.git'
        try:
            # command = shlex.split('git clone %s %s' % (project_url, 'G:/gitClone/' + name_with_namespace))
            command = shlex.split('git clone %s %s' % (project_url, './Calendar/' + "NestedCalendar"))
            # command = shlex.split('git clone %s' % (project_url))
            resultCode = subprocess.Popen(command)
        except Exception as e:
            print("Error on %s: %s" % (project_url, e.strerror))
        time.sleep(5)


if __name__ == "__main__":
    calendar = CalendarClone()
    calendar.parse_repositories_clone()
