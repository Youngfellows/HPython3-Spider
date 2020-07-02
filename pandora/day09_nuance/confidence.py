# coding=utf-8
import json
import os
import numpy


class Nuance(object):
    def __init__(self):
        """构造函数"""
        object.__init__(self)
        self.origin_data_path = "./json/nuance_asr.json"
        self.filter_path = "./json/confidence_asr.json"
        self.average_path = "./json/average_confidence_asr.json"

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

    def filter(self):
        """数据清洗"""
        commands = self.read2json(self.origin_data_path)
        print("================ 数据清洗 ========================")
        filter_commands = []  # 过滤结果列表

        for i, command in enumerate(commands):
            print("{} cmd: {} ,confidence: {} ,score: {}".format(i, command["cmd"], command["confidence"],
                                                                 command["score"]))
            new_command = {}
            exist = False  # 是否存在
            for j, new_cmd in enumerate(filter_commands):
                # print("{} cmdn: {}".format(j, new_cmd["cmd"]))
                if new_cmd["cmd"] == command["cmd"]:
                    exist = True
                    # 取出旧元素,添加新值
                    print("旧元素: j: {} ,len: {},{}".format(j, len(filter_commands), new_cmd))
                    new_cmd["confidences"].append(command["confidence"])
                    new_cmd["scores"].append(command["score"])

            if not exist:  # 不存在
                new_command["cmd"] = command["cmd"]
                new_command["confidences"] = [command["confidence"]]
                new_command["scores"] = [command["score"]]
                filter_commands.append(new_command)
            else:  # 存在
                print("exits {} ... ".format(command["cmd"]))

        # 保存清洗后的数据到本地
        print(filter_commands)
        self.writer2json(self.filter_path, filter_commands)
        self.average()

    def average(self):
        """求取均值"""
        print("================== 求取均值 ====================")
        filter_commands = self.read2json(self.filter_path)
        for index, command in enumerate(filter_commands):
            print("{},{}".format(index, command))
            confidences = command["confidences"]
            scores = command["scores"]
            # print("confidences: {} ,scores: {}".format(confidences, scores))
            average_confidence = numpy.mean(confidences)
            average_score = numpy.mean(scores)
            print("average_confidence: {},average_score: {}".format(average_confidence, average_score))
            command["average_confidence"] = int(average_confidence)
            command["average_score"] = int(average_score)

        print(filter_commands)
        self.writer2json(self.average_path, filter_commands)


if __name__ == "__main__":
    nuance = Nuance()
    nuance.filter()
