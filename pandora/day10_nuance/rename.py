# coding=utf-8
import os
import re
import shutil
import time


class MyOS(object):
    def __init__(self):
        object.__init__(self)
        self.dest_name = "my_dir"

    def rename_all(self):
        """批处理修改文件名称"""
        # path = "E:\爬虫资源"
        # path = "."
        path = os.getcwd()  # 返回当前工作目录
        dirs = os.listdir(path)  # 获取所有文件和文件夹
        # print(dirs)
        number = 3

        print("=**=" * 60)
        # 输出所有文件和文件夹
        for file in dirs:
            print(file)
            if os.path.isdir(file):
                print("*" * 60)
                # print(file, "是目录")
                # path = path + os.sep + "png"
                # print("path: ", path)

                # 获得指定路径下的所有文件及文件夹下子文件的目录列表
                for parent, dirnames, filenames in os.walk(path):
                    for filename in filenames:
                        # print("parent: {}, filename: {}".format(parent, filename))
                        file = os.path.join(parent, filename)
                        print(file)

                        # 获取文件后缀
                        index = filename.rfind(r".")  # 最后一次出现点的位置
                        name = filename[0:index]
                        file_suffix = filename[index:]
                        print("index:{}, name:{}, file_suffix:{}".format(index, name, file_suffix))
                        if file_suffix == ".mp3":
                            # new_name = re.sub(r"_\[.*\]_", "_[浪漫巴厘岛]_", name)
                            try:
                                new_name = re.sub(r"^\d.*[^\.]+", "_[Harry Potter]_A", name)
                                print("new_name: {}".format(new_name))
                                new_file = parent + os.sep + str(number) + "_" + new_name + file_suffix
                                print("number: {}, new_file: {}".format(number, new_file))
                                os.rename(file, new_file)
                                number = number + 1
                                time.sleep(0.2)#延迟200ms
                            except Exception as e:
                                print(e)

    def move_all(self):
        """移动全部文件到指定目录"""
        dest_dir = os.getcwd() + os.sep + self.dest_name
        print(dest_dir)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        path = os.getcwd()  # 返回当前工作目录
        dirs = os.listdir(path)  # 获取所有文件和文件夹
        print(dirs)

        print("*" * 60)
        # 输出所有文件和文件夹
        for src_file in dirs:
            print(src_file)
            if os.path.isdir(src_file):
                print("*" * 60)
                # print(src_file, "是目录")
                # path = path + os.sep + "png"
                # print("path: ", path)

                # 获得指定路径下的所有文件及文件夹下子文件的目录列表
                for parent, dirnames, filenames in os.walk(path):
                    for filename in filenames:
                        # print("parent: {}, filename: {}".format(parent, filename))
                        src_file = os.path.join(parent, filename)
                        print(src_file)

                        # 获取文件后缀
                        index = filename.rfind(r".")  # 最后一次出现点的位置
                        name = filename[0:index]
                        file_suffix = filename[index:]
                        print("index:{}, name:{}, file_suffix:{}".format(index, name, file_suffix))
                        if file_suffix == ".mp3":
                            # 移动文件
                            dest_file = dest_dir + os.sep
                            try:
                                shutil.move(src_file, dest_file)
                            except:
                                pass


if __name__ == "__main__":
    myos = MyOS()
    myos.rename_all()
    myos.move_all()
