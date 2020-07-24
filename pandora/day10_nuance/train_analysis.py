# coding=utf-8
import json
import os
import matplotlib.pyplot as plt
import numpy as np


class Train(object):
    def __init__(self):
        object.__init__(self)
        self.data_path_test = "./data/wiki_test_lable.txt"
        self.data_path_train = "./data/wiki_train_lable.txt"
        self.data_path_face_test = "./data/UTKFace_test_lable.txt"
        self.data_path_face_train = "./data/UTKFace_train_lable.txt"

        self.data_path_test_json = "./data/json/wiki_test_lable.json"
        self.data_path_train_json = "./data/json/wiki_train_lable.json"
        self.data_path_face_test_json = "./data/json/UTKFace_test_lable.json"
        self.data_path_face_train_json = "./data/json/UTKFace_train_lable.json"

        self.png_name_test = "./png/wiki_test_lable.png"
        self.png_name_train = "./png/wiki_train_lable.png"
        self.png_name_face_test = "./png/UTKFace_test_lable.png"
        self.png_name_face_train = "./png/UTKFace_train_lable.png"

    def read_data(self, file_data):
        """按行读取"""
        # 返回该文件中包含的所有行,是一个列表
        file = open(file_data, "r", encoding="utf-8")
        content_list = file.readlines()
        print("内容大小: size = %d,type = %s" % (len(content_list), type(content_list)))
        print(content_list)
        data_array = []
        for line in content_list:
            data_array.append(line.strip())  # 去除\n

        # 关闭流
        file.close()
        return data_array

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

    def parse_data(self, src_file, des_file):
        """解析数据"""
        data = self.read_data(src_file)
        self.writer2json(des_file, data)

    def parse_test(self):
        """解析txt文件"""
        self.parse_data(self.data_path_test, self.data_path_test_json)

    def parse_train(self):
        """解析txt文件"""
        self.parse_data(self.data_path_train, self.data_path_train_json)

    def parse_face_test(self):
        """解析txt文件"""
        self.parse_data(self.data_path_face_test, self.data_path_face_test_json)

    def parse_face_train(self):
        """解析txt文件"""
        self.parse_data(self.data_path_face_train, self.data_path_face_train_json)

    def analysis_graph(self, data_file, title, png_name):
        """分析.json数据"""
        print("============  分析.json数据  ==============")
        json_data = self.read2json(data_file)
        json_data = sorted(json_data)
        print("json_data:\n{}".format(json_data))

        # 统计出现的元素有哪些
        unique_data = np.unique(json_data)
        print("unique_data:\n{}".format(unique_data))

        # 统计某个元素出现的次数
        resdata = []
        for ii in unique_data:
            resdata.append(json_data.count(ii))
        print("resdata:\n{}".format(resdata))

        plt.figure(figsize=(35, 30), dpi=80)
        plt.title(title)
        plt.xlabel("Number")
        plt.ylabel("Count")
        plt.grid()
        plt.plot(unique_data, resdata, linewidth=1)
        plt.savefig(png_name)
        plt.show()
        plt.clf()  # 重置画布

    def analysis_graph_test(self):
        """分析test.json数据"""
        self.analysis_graph(self.data_path_test_json, "wiki_test_lable", self.png_name_test)

    def analysis_graph_train(self):
        """分析train.json数据"""
        self.analysis_graph(self.data_path_train_json, "wiki_train_lablee", self.png_name_train)

    def analysis_graph_face_test(self):
        """分析test.json数据"""
        self.analysis_graph(self.data_path_face_test_json, "UTKFace_test_lable", self.png_name_face_test)

    def analysis_graph_face_train(self):
        """分析train.json数据"""
        self.analysis_graph(self.data_path_face_train_json, "UTKFace_train_lable", self.png_name_face_train)


if __name__ == "__main__":
    train = Train()
    # 数据转化
    train.parse_test()
    train.parse_train()
    train.parse_face_test()
    train.parse_face_train()

    # 数据分析
    train.analysis_graph_test()
    train.analysis_graph_train()
    train.analysis_graph_face_test()
    train.analysis_graph_face_train()
