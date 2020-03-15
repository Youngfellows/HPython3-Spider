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
        while True:
            try:
                # 等待页面元素可见
                # self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "job-list")))
                self.wait.until(EC.visibility_of_element_located((By.XPATH, u'//div[@class="job-list"]')))
                # 获取当前页的职位详情
                self.job_detail()

                # 查找下一个元素是否存在,循环爬取每一页的内容
                # 如果在页面源码里找到"下一页"为隐藏的标签，就退出循环
                # if self.driver.page_source.find("shark-pager-disable-next") != -1:
                # if self.driver.page_source.find("dy-Pagination-item-next") != -1:
                # if self.driver.page_source.find("dy-Pagination-disabled dy-Pagination-next") != -1:
                try:
                    # next_disable = self.browser.page_source.find("next disabled")
                    next_disable = self.browser.find_element_by_class_name("next disabled")
                    print("next_disable: {}".format(next_disable))
                    print("最后一页...")
                    break
                except selenium.common.exceptions.InvalidSelectorException:
                    print("没到最后一页...")

                # 一直点击下一页
                next = self.browser.find_element_by_class_name("next")
                cur_page = self.browser.find_element_by_class_name("cur")
                print("cur_page: {}".format(cur_page.text))
                print("next: {}".format(next))
                next.click()

            except TimeoutError as e:
                print("超时了....{}".format_map(e))

        return self.spider()

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
        self.browser.quit()


if __name__ == "__main__":
    boss = BossSpider()
    boss.spider()
