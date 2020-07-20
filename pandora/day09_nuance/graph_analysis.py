# coding=utf-8
import json
import os
import matplotlib.pyplot as plt
from pandora.day09_nuance.file_path_manager import FilePathManager


class NuanceGraphAnalysis(object):
    def __init__(self):
        object.__init__(self)
        self.origin_filter_average_path = "json/origin/filter_origin_average_confidence.json"  # 筛选后的全部识别结果每一条指令数据
        self.origin_png_name = "origin"

        self.vip_filter_average_path = "json/vip/filter_vip_average_confidence.json"  # 筛选后的全部识别结果每一条指令数据
        self.vip_png_name = "vip"

    def json2dict(self, json_data):
        """将json字符串转化为python的字典对象"""
        return json.loads(json_data)

    def read2json(self, file_name):
        """读取json文件,并转换为字典/列表"""
        with open(file_name, "r", encoding="utf-8") as fp:
            dict = json.load(fp)
        # print(dict)
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

    def analysis(self):
        """数据分析,绘制图表"""
        commands = self.read2json(self.origin_filter_average_path)
        if commands:
            plt.figure(figsize=(35, 20), dpi=80)
            plt.title("Nuance Commands Analysis")
            plt.xlabel("times")
            plt.ylabel("confidence")
            plt.grid()
            legends = []
            for i, command in enumerate(commands):
                # print(command)
                if i == 1 or i == 2:
                    cmd = command["cmd"]
                    confidences = command["confidences"]  # 置信度
                    scores = command["scores"]  # 评分
                    xaxis = range(len(confidences))
                    plt.plot(xaxis, confidences, linewidth=1)
                    legends.append(cmd)

            plt.legend(tuple(legends), loc='upper right')
            plt.show()

    def analysis_plot(self, data_path, save_path):
        """数据分析,绘制图表"""
        print("==================  数据分析,绘制图表 ======================")
        commands = self.read2json(data_path)
        dir_manager = FilePathManager()
        if commands:
            for i, command in enumerate(commands):
                print("{} command: {}, {}".format(i, command["cmd"], command))
                title = command["cmd"]
                confidences = command["confidences"]  # 置信度
                scores = command["scores"]  # 评分

                # 处理只有一次不绘制曲线
                if len(confidences) == 1:
                    confidences.insert(0, "5000")
                    scores.insert(0, "30000")
                print("len: {}".format(len(confidences)))
                xaxis = range(len(confidences))
                # print(scores)

                # 开启一个窗口，num设置子图数量，这里如果在add_subplot里写了子图数量，num设置多少就没影响了
                # figsize设置窗口大小，dpi设置分辨率
                fig = plt.figure(num=2, figsize=(20, 8), dpi=80)
                fig.suptitle(title, fontsize=14, fontweight='bold')

                # 使用add_subplot在窗口加子图，其本质就是添加坐标系
                # 三个参数分别为：行数，列数，本子图是所有子图中的第几个，最后一个参数设置错了子图可能发生重叠
                ax1 = fig.add_subplot(2, 1, 1)
                ax2 = fig.add_subplot(2, 1, 2)

                # 绘制曲线
                # ax1.set_title("Open Google Map")
                ax1.set_xlabel("times")
                ax1.set_ylabel("confidence")
                ax1.grid()
                ax1.plot(xaxis, confidences, color='g')

                # 在第二个子图上画图
                # ax2.set_title("Open Google Map")
                ax2.set_xlabel("times")
                ax2.set_ylabel("scores")
                ax2.grid()
                ax2.plot(xaxis, scores, color='r')
                # dir_name = dir_manager.mkdir(os.sep + "png" + os.sep + title + os.sep)
                dir_name = dir_manager.mkdir(os.sep + "png" + os.sep + save_path + os.sep)
                png_path = dir_name + str((i + 1)) + "_" + title + ".png";
                print("dir_name: {}".format(png_path))
                plt.savefig(str(png_path))
                plt.tight_layout()
                # plt.show()
                plt.clf()  # 重置画布

    def analysis_bar(self, data_path, save_path, figsize=(20, 15)):
        """数据分析,绘制直方图"""
        commands = self.read2json(data_path)
        dir_manager = FilePathManager()
        if commands:
            xaxis = []
            yaxis = []

            for i, command in enumerate(commands):
                print(command)
                # if i != 0:
                cmd = command["cmd"]
                confidences = command["confidences"]  # 置信度
                scores = command["scores"]  # 评分

                # 横轴、纵轴赋值
                xaxis.append(cmd)
                yaxis.append(len(confidences))

        # 绘制直方图
        # plt.figure(figsize=(20, 15), dpi=80)
        plt.figure(figsize=figsize, dpi=80)
        plt.title("Nuance Commands Analysis")
        # plt.bar(range(len(xaxis)), yaxis, width=0.3, color="orange")
        # plt.xticks(range(len(xaxis)), xaxis)

        plt.barh(range(len(xaxis)), yaxis, height=0.8, color="orange")
        plt.yticks(range(len(xaxis)), xaxis)
        plt.grid()
        dir_name = dir_manager.mkdir(os.sep + "png" + os.sep + save_path + os.sep)
        png_path = dir_name + "0_histogram2.png";
        print("dir_name: {}".format(png_path))
        plt.savefig(str(png_path))
        # plt.show()
        plt.clf()  # 重置画布

    def origin_analysis(self):
        """分析原始数据"""
        self.analysis_bar(self.origin_filter_average_path, self.origin_png_name, figsize=(20, 40))
        self.analysis_plot(self.origin_filter_average_path, self.origin_png_name)

    def vip_analysis(self):
        """分析误识别数据"""
        self.analysis_bar(self.vip_filter_average_path, self.vip_png_name)
        self.analysis_plot(self.vip_filter_average_path, self.vip_png_name)


if __name__ == "__main__":
    analysis = NuanceGraphAnalysis()
    # analysis.analysis()

    # 1. 图表分析原始数据
    analysis.origin_analysis()

    # 2. 图表分析已经误识别数据
    analysis.vip_analysis()
