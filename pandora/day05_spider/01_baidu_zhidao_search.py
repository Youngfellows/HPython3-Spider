# coding=utf-8
import urllib
import requests
from bs4 import BeautifulSoup
# from . import file_path_anager

# 使用完整路径导入
from pandora.day05_spider.file_path_anager import FilePathManager


def search(question, alternative_answers):
    dir_name = r"/json/"  # 目录名称
    file_name = "baidu_zhidao.txt"  # 文件名

    # 百度知道搜索接口
    baidu = 'http://zhidao.baidu.com/search?'
    print("问题: {}".format(question))
    print("期望答案: {}".format(alternative_answers))

    infos = {"word": question}
    # 调用百度接口
    url = baidu + 'lm=0&rn=10&pn=0&fr=search&ie=gbk&' + urllib.parse.urlencode(infos, encoding='GB2312')
    print("\n请求URL: {}".format(url), end="\n\n")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
    }
    sess = requests.Session()
    req = sess.get(url=url, headers=headers, verify=False)
    req.encoding = 'gbk'
    # print(req.text)

    bf = BeautifulSoup(req.text, 'lxml')
    answers = bf.find_all('dd', class_='dd answer')
    for answer in answers:
        print(answer.text)

    print("\n***************** 匹配推荐答案 ***************************")
    # 推荐答案
    recommend = ''
    if alternative_answers != []:
        # 最佳推荐答案列表
        best = []
        # print('\n')
        for answer in answers:
            # print(answer.text)
            for each_answer in alternative_answers:
                if each_answer in answer.text:
                    best.append(each_answer)
                    print(answer.text)
                    print("推荐答案是: {}".format(each_answer), end='\n\n')
                    # print('\n')
                    break

        print("====================== 推荐结果 ==============================")
        print(best)

        # 推荐结果统计,{'纽约': 8, '华盛顿': 1}
        statistics = {}

        for each in best:
            if each not in statistics.keys():
                statistics[each] = 1
            else:
                statistics[each] += 1
        print(statistics)

        # lambda,
        # map() 会根据提供的函数对指定序列做映射。
        # python3可将map转换为list列表
        # 使用 lambda 匿名函数,x是参数,也就是errors列表的各个元素
        errors = ['没有', '不是', '不对', '不正确', '错误', '不包括', '不包含', '不在', '错']
        error_list = list(map(lambda x: x in question, errors))
        # print(error_list)
        # print(statistics.items())
        # print(sum(error_list))

        if sum(error_list) >= 1:
            for each_answer in alternative_answers:
                if each_answer not in statistics.items():
                    recommend = each_answer
                    print('推荐答案：', recommend)
                    break
        elif statistics != {}:
            # 从python2.4开始，list.sort()和sorted()函数增加了key参数来指定一个函数，此函数将在每个元素比较前被调用
            # key参数的值为一个函数，此函数只有一个参数且返回一个值用来进行比较。
            # 按照value排序,降序
            # lambda e: e[1] 等价于
            # def f(e):
            #     return e[1]
            # 方式1,按照value排序,降序
            recommends = sorted(statistics.items(), key=lambda e: e[1], reverse=True)
            print('recommend：', recommends)
            recommend = recommends[0][0]
            print('推荐答案：', recommend)

            # 方式2,按照value排序,降序
            # recommends = sorted(statistics, key=lambda e: statistics[e], reverse=True)
            # recommend = recommends[0]
            # print('推荐答案：', recommend)

    # 写入文件
    file_manager = FilePathManager()
    path = file_manager.mkdir(dir_name)
    file_name = path + file_name
    #print("file_name = {}".format(file_name))
    file_manager.delete_file(file_name)

    with open(file_name, 'w', encoding="utf-8") as f:
        f.write('问题：' + question)
        f.write('\n')
        f.write('*' * 50)
        f.write('\n')
        if alternative_answers != []:
            f.write('选项：')
            for i in range(len(alternative_answers)):
                f.write(alternative_answers[i])
                f.write('  ')
        f.write('\n')
        f.write('*' * 50)
        f.write('\n')
        f.write('参考答案：\n')
        for answer in answers:
            f.write(answer.text)
            f.write('\n')
        f.write('*' * 50)
        f.write('\n')
        if recommend != '':
            f.write('最终答案请自行斟酌！\t')
            f.write('推荐答案：' + sorted(statistics.items(), key=lambda e: e[1], reverse=True)[0][0])


if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()  # 去除警告
    """
    1、北京大学的前身是? 答案：京师大学堂
        A.国子监 B.京师大学堂 C.北洋大学
    """
    # 根据问题和备选答案搜索答案
    # question = "北京大学的前身是"
    # alternative_answers = ["国子监", "京师大学堂", "北洋大学"]

    question = "联合国总部在个城市"
    alternative_answers = ["北京", "东京", "华盛顿", "纽约", "伦敦", "巴黎"]
    search(question, alternative_answers)
