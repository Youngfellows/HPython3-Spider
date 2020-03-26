# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
import platform
import os
import json
from lxml import etree
import selenium
from selenium.common.exceptions import NoSuchElementException


# 爬取Boss直聘
class BossSpider(object):
    def __init__(self):
        object.__init__(self)
        self.initBrowser()
        self.host = "https://www.zhipin.com"
        self.url = "https://www.zhipin.com/c101280600-p100202/?query=Android&page=1&ka=page-1"
        self.jobs_list = []  # 保存岗位信息的列表

    # 初始化浏览器对象
    def initBrowser(self):
        system_type = platform.system()
        print("操作系统类型:{}".format(system_type))
        if system_type == "Windows":
            # browser = webdriver.Chrome()
            self.browser = webdriver.Chrome(
                executable_path="D:\Python\Chrome_Driver_selenium\chromedriver_win32\chromedriver.exe")
        elif system_type == "Linux":
            # browser = webdriver.Chrome()
            self.browser = webdriver.Chrome(
                executable_path="/mnt/samba/share/Selenium_PhantomJS_Driver/Chrome_Driver_selenium/chromedriver_linux64/chromedriver")

        # 设置显示等待时间10秒
        self.wait = WebDriverWait(self.browser, 10)

    # 爬取的入口
    def spider(self):
        # 获取html页面
        self.browser.get(self.url)
        self.end_page = False
        while not self.end_page:
            try:
                print("是否到最后一页: end_page = {}".format(self.end_page))
                # 等待页面元素可见
                # self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "job-list")))
                self.wait.until(EC.visibility_of_element_located((By.XPATH, u'//div[@class="job-list"]')))
                # 获取当前页的职位详情
                self.job_detail()

                cur_page = self.browser.find_element_by_xpath('//div[@class="page"]/a[@class="cur"]').text
                print("cur_page: {}".format(cur_page))
                # if self.isElementPresent("class", 'next disabled'):
                if self.isElementPresent2('//div[@class="page"]/a[@class="next disabled"]'):
                    print("已经到最后一页了...")
                    self.end_page = True
                    self.quit_browser()
                else:
                    print("最后一个元素不存在...")
                    # 一直点击下一页
                    next = self.browser.find_element_by_class_name("next")
                    next.click()
                    print("next: {}".format(next))
            except TimeoutError as e:
                print("超时了....{}".format_map(e))

    # 获取职位详情
    def job_detail(self):
        print("get_job_detail 获取当前页面的职位详情...")
        # 解析html
        html = self.browser.page_source
        # print(html)

        dom_tree = etree.HTML(html)
        jobs = dom_tree.xpath(
            ' //div[@class="job-list"]//div[@class="job-primary"]//div[@class="job-title"]/span[@class="job-name"]/text()')
        companys = dom_tree.xpath(
            ' //div[@class="job-list"]//div[@class="job-primary"]//div[@class="company-text"]/h3[@class="name"]/a/text()')
        details = dom_tree.xpath(
            '//div[@class="job-list"]//div[@class="job-primary"]//div[@class="info-primary"]//a[@class="primary-box"]/@href')
        backgrounds = dom_tree.xpath(
            '//div[@class="job-list"]//div[@class="job-primary"]//div[@class="info-primary"]//a[@class="primary-box"]//p/text()')
        salarys = dom_tree.xpath(
            '//div[@class="job-list"]//div[@class="job-primary"]//div[@class="info-primary"]//a[@class="primary-box"]//span[@class="red"]/text()')

        # print("招聘公司:{},{}".format(len(companys), companys))
        # print("招聘岗位:{},{}".format(len(jobs), jobs))
        # print("学历背景:{},{}".format(len(backgrounds), backgrounds))
        # print("薪资待遇:{},{}".format(len(salarys), salarys))
        # print("岗位详情:{},{}".format(len(details), details))

        # 整合招聘信息
        for company, job, salary, detail in zip(companys, jobs, salarys, details):
            link = self.host + detail
            # print("{},{},{},{}".format(company, job, salary, link))
            self.jobs_list.append({
                "job": job,
                "company": company,
                "salary": salary,
                "link": link
            })

    # 推出浏览器
    def quit_browser(self):
        print(self.jobs_list)
        self.writer2json()
        self.browser.quit()

    # 封装一个函数，用来判断属性值是否存在
    def isElementPresent(self, by, value):
        """
        用来判断元素标签是否存在，
        """
        try:
            element = self.browser.find_element(by=by, value=value)
        # 原文是except NoSuchElementException, e:
        except NoSuchElementException as e:
            # 发生了NoSuchElementException异常，说明页面中未找到该元素，返回False
            return False
        else:
            # 没有发生异常，表示在页面中找到了该元素，返回True
            return True

        # 封装一个函数，用来判断属性值是否存在

    def isElementPresent2(self, path):
        """
        用来判断元素标签是否存在，
        """
        try:
            element = self.browser.find_element_by_xpath(path)
        # 原文是except NoSuchElementException, e:
        except NoSuchElementException as e:
            # 发生了NoSuchElementException异常，说明页面中未找到该元素，返回False
            return False
        else:
            # 没有发生异常，表示在页面中找到了该元素，返回True
            return True

    # 保存列表到json文件
    def writer2json(self):
        global sina_news_list
        file_name = "./json/boss_zhipin_job.json"
        # 删除旧文件
        if file_name in os.listdir():
            os.remove(file_name)

        # dumps()默认中文为ascii编码格式，ensure_ascii默认为Ture
        # 禁用ascii编码格式，返回的Unicode字符串，方便使用
        json_str = json.dumps(self.jobs_list, ensure_ascii=False)
        with open(file_name, "wb") as fp:
            fp.write(json_str.encode('utf-8'))


if __name__ == "__main__":
    boss = BossSpider()
    boss.spider()
