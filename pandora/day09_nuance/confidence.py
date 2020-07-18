# coding=utf-8
import json
import os
import numpy


class Nuance(object):
    def __init__(self):
        """构造函数"""
        object.__init__(self)
        # 全部识别结果
        self.origin_filter_confidence_path = "./json/origin/filter_origin_confidence.json"
        self.origin_filter_average_path = "./json/origin/filter_origin_average_confidence.json"  # 筛选后的全部识别结果每一条指令数据
        self.origin_filter_first_all_path = "./json/origin/filter_origin_first_all.json"  # 筛选的全部识别结果的第一条数据
        # self.origin_all_data_path = "json/2020-07-08/nuance_asr_all.json"  # 全部识别结果数据
        # self.origin_all_data_path = "./json/2020-07-10/nuance_asr_all.json"  # 全部识别结果数据
        self.origin_all_data_path = "./json/2020-07-13/nuance_asr.json"  # 全部识别结果数据
        # self.origin_all_data_path = "./json/2020-07-14/nuance_asr.json"  # 全部识别结果数据

        # VIP识别结果
        self.vip_filter_confidence_path = "./json/vip/filter_vip_confidence.json"
        self.vip_filter_average_path = "./json/vip/filter_vip_average_confidence.json"  # 筛选后的全部识别结果每一条指令数据
        self.vip_filter_first_all_path = "./json/vip/filter_vip_first_all.json"  # 筛选的全部识别结果的第一条数据
        # self.vip_data_path = "./json/2020-07-10/nuance_asr_result.json"  # 全部识别结果数据
        self.vip_data_path = "./json/2020-07-13/nuance_asr_result.json"  # 全部识别结果数据
        # self.vip_data_path = "./json/2020-07-14/nuance_asr_result.json"  # 全部识别结果数据

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

    def filter(self, fitler_path, confidence_path, average_path):
        """数据清洗"""
        commands = self.read2json(fitler_path)
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
        print("保存清洗后的数据到本地")
        print(filter_commands)
        self.writer2json(confidence_path, filter_commands)

        # 求取均值
        self.average(confidence_path, average_path)

    def average(self, confidence_path, average_path):
        """求取均值"""
        print("================== 求取均值 ====================")
        filter_commands = self.read2json(confidence_path)
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
        self.writer2json(average_path, filter_commands)

    def filter_all(self, origin_data_path):
        """清洗全部数据,第一条识别结果"""
        print("================ 清洗全部数据 ========================")
        nuance_asr_array = self.read2json(origin_data_path)
        print("nuance_asr_array: size: {}".format(len(nuance_asr_array)))
        commonds = []  # 保存清洗后的列表
        for i, nuance_asr in enumerate(nuance_asr_array):
            print("index: {} , {}".format(i, nuance_asr))
            # 筛选出每一次结果的第一条数据
            hypotheses = nuance_asr["hypotheses"]
            # for j,hypothese in enumerate(hypotheses):
            #     #一次识别的多个结果
            #     print(hypothese)
            if hypotheses:
                hypothese = hypotheses[0]
                items = hypothese["items"]
                item = items[0]
                command = {"cmd": item["orthography"],
                           "confidence": item["confidence"],
                           "score": item["score"],
                           "beginTime": item["beginTime"],
                           "endTime": item["endTime"]}
                commonds.append(command)

        return commonds

    def filter_all_new(self, origin_data_path):
        """新,清洗全部数据,第一条识别结果"""
        print("================ 清洗全部数据 ========================")
        nuance_asr_array = self.read2json(origin_data_path)
        print("nuance_asr_array: size: {}".format(len(nuance_asr_array)))
        commonds = []  # 保存清洗后的列表
        for i, nuance_asr in enumerate(nuance_asr_array):
            print("index: {} , {}".format(i, nuance_asr))
            # 筛选出每一次结果的第一条数据
            hypotheses = nuance_asr["hypotheses"]
            # for j,hypothese in enumerate(hypotheses):
            #     #一次识别的多个结果
            #     print(hypothese)
            if hypotheses:
                hypothese = hypotheses[0]
                items = hypothese["items"]
                # print("items: {}".format(items))
                cmd_items = [item["orthography"] for item in items]  # 列表循环式
                cmd = " ".join(cmd_items)  # 列表转化为字符串
                command = {"cmd": cmd,
                           "confidence": hypothese["confidence"],
                           "score": hypothese["score"],
                           "beginTime": hypothese["beginTime"],
                           "endTime": hypothese["endTime"]}
                commonds.append(command)
        return commonds

    def filter_origin_all_first(self):
        """筛选原始数据的第一条识别结果"""
        print("=======================   筛选原始数据的第一条识别结果  ===============================")
        # commonds = self.filter_all(self.origin_all_data_path)
        commonds = self.filter_all_new(self.origin_all_data_path)

        # 把清洗后的第一条数据保存到JSON
        self.writer2json(self.origin_filter_first_all_path, commonds)
        for i, command in enumerate(commonds):
            print("{}: {}".format(i, command))

        # 分析
        self.filter(self.origin_filter_first_all_path, self.origin_filter_confidence_path,
                    self.origin_filter_average_path)

    def filter_vip_first(self):
        """筛选VIP识别结果的第一条"""
        print("=======================   筛选VIP识别结果的第一条  ===============================")
        # commonds = self.filter_all(self.vip_data_path)
        commonds = self.filter_all_new(self.vip_data_path)

        # 把清洗后的第一条数据保存到JSON
        self.writer2json(self.vip_filter_first_all_path, commonds)
        for i, command in enumerate(commonds):
            print("{}: {}".format(i, command))

        # 分析
        self.filter(self.vip_filter_first_all_path, self.vip_filter_confidence_path,
                    self.vip_filter_average_path)


if __name__ == "__main__":
    nuance = Nuance()

    # 1. 筛选全部识别结果的第一条
    nuance.filter_origin_all_first()

    # 2. 筛选VIP识别结果的第一条
    nuance.filter_vip_first()
