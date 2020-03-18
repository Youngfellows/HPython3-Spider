# coding=utf-8

import os
import shutil

"""
在当前路径下中创建文件夹
"""


class FilePathManager:

    def __init__(self):
        self.path = os.getcwd()
        self.path = self.path
        print("CreatePathManager,cur_path = {}".format(self.path))

    """
    在当前目录下创建目录
    """

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
    删除目录及文件
    """

    def delete_dir(self, path):
        shutil.rmtree(path)

    """
    删除旧文件
    """

    def delete_file(self, file_name):
        if file_name in os.listdir():
            os.remove(file_name)
