# coding=utf-8
# 使用完整路径导入
from pandora.day05_spider.file_path_anager import FilePathManager
import json
import requests
import traceback
from lxml import etree
import os
import random
import urllib
import time

"""
人教版中小学教材电子版
"""


class EducationPDF(object):
    def __init__(self):
        """构造函数"""
        object.__init__(self)
        requests.packages.urllib3.disable_warnings()  # 去除警告
        self.base_url = "http://bp.pep.com.cn/jc"
        self.parent_name = r"/pdf/"
        self.file_name = "人教版中小学教材电子版.json"
        self.init_headers()
        self.path_manager = FilePathManager()

    def init_headers(self):
        """初始化请求头"""
        ua_list = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Mobile Safari/537.36'
        ]
        user_agent = random.choice(ua_list)
        self.headers = {'User-Agent': user_agent,
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
                        }

    def get_html(self, target):
        """获取html页码结果"""
        response = requests.get(url=target, headers=self.headers, verify=False)
        # 方式1: 解决中文乱码问题
        # html = response.content
        # html = html.decode('utf-8', 'ignore')
        # html = html.decode('gbk', 'ignore')

        # 方式2: 解决中文乱码问题
        response.encoding = "utf-8"
        # response.encoding = "gbk"
        html = response.text
        # print(html)
        return html

    def download_pdf(self, path, pdf_url, number):
        """下载图片"""
        try:
            # 下载每页大图
            urllib.request.urlretrieve(pdf_url, path + "/" + str(number) + '.jpg')
            print('正在保存,第%s张pdf' % (number))
        except urllib.error.HTTPError as e:
            print("靠,HTTPError 无法下载第{}张pdf".format(number))
        except urllib.error.URLError as e:
            print("靠,URLError 无法下载第{}张pdf".format(number))
        except:
            print("靠,无法下载第{}张pdf".format(number))

        # 休眠2秒一下
        time.sleep(1)

    def read2json(self, file_name):
        """读取json文件,并转换为字典/列表"""
        with open(file_name, "r", encoding="utf-8") as fp:
            chapters = json.load(fp)
        print(chapters)
        return chapters

    def writer2json(self, file_name, dict):
        """将列表保存为json"""
        # 删除旧文件
        if file_name in os.listdir():
            os.remove(file_name)

        # dumps()默认中文为ascii编码格式，ensure_ascii默认为Ture
        # 禁用ascii编码格式，返回的Unicode字符串，方便使用
        json_str = json.dumps(dict, ensure_ascii=False)
        with open(file_name, "wb") as fp:
            fp.write(json_str.encode('utf-8'))

    def star(self):
        """启动爬虫"""
        # 获取教材信息
        course_list = self.parse_courses()

        # 保存到JSON文件
        path = self.path_manager.mkdir(self.parent_name)
        self.writer2json(path + self.file_name, course_list)

        # 读取json文件,获取教材下载信息

    def parse_courses(self):
        """解析html获取教材信息"""
        """
            1、大类(小学/初中/高中....)名称
        """
        html = self.get_html(self.base_url)
        dom_tree = etree.HTML(html)
        # 教育阶段名称
        phase_list = dom_tree.xpath('//div[@id="container"]/div[@class="list_sjzl_jcdzs2020"]')
        # print(phase_list)
        # 获取子节点
        courses = []  # 保存课程信息的列表
        for phase in phase_list:
            # 教育阶段名称
            phase_title = phase.xpath('./div[@class="container_title_jcdzs2020"]/h5/text()')[0]
            print("\n教育阶段: {}".format(phase_title))

            phase_item = {}  # 每个教育阶段的字典
            phase_item["phase"] = phase_title
            course_array = []  # 每个教育阶段的课程列表

            # 每一个教育阶段的课程
            course_list = phase.xpath('./ul/li/a')
            for course in course_list:
                course_name = course.text  # 课程名称
                course_link = self.base_url + course.xpath('@href')[0][1:]
                print("{},{}".format(course_name, course_link))

                # 获取每一个教材的下载详情
                details = self.parse_details(course_link)

                course_item = {}
                course_item["course"] = course_name
                course_item["link"] = course_link
                course_item["details"] = details
                course_array.append(course_item)

            phase_item["courses"] = course_array
            courses.append(phase_item)

        return courses

    def parse_details(self, course_link):
        """解析获取每门教材的下载详情"""
        html = self.get_html(course_link)
        dom_tree = etree.HTML(html)
        details = []  # pdf教材列表
        pdf_list = dom_tree.xpath('//div[@id="container"]/div[@class="con_list_jcdzs2020"]/ul/li')
        for pdf in pdf_list:
            cover = course_link + pdf.xpath('.//a/img/@src')[0][2:]
            pdf_name = pdf.xpath('./h6/a/text()')[0]
            pdf_link = course_link + pdf.xpath('./div[@class="con_type_link_jcdzs2020"]/a[2]/@href')[0][2:]
            print("{},pdf down url: {} , cover: {}".format(pdf_name, pdf_link, cover))
            details.append({
                "phase": pdf_name,
                "cover": cover,
                "url": pdf_link
            })

        return details


if __name__ == "__main__":
    edu_pdf = EducationPDF()
    edu_pdf.star()
