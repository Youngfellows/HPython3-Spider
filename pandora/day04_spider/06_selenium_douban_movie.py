# coding=utf-8
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import platform

"""
豆瓣电影爬虫
"""


class DouBan_Movies:
    def __init__(self):
        # 初始化chromedriver
        # self.driver = webdriver.Chrome()
        self.initChrome()
        # 调用函数进入豆瓣电影top250官网
        self.__enter_douban()
        # 在当前目录下建一个文本文件用来写入电影信息
        # self.fs = open(os.getcwd() + r"\douban_top250.txt", "w+", encoding="utf-8")
        self.fs = open("./json/douban_top250.txt", "w+", encoding="utf-8")

    # 初始化浏览器对象
    def initChrome(self):
        system_type = platform.system()
        print("操作系统类型:{}".format(system_type))
        if system_type == "Windows":
            # driver = webdriver.Chrome()
            self.driver = webdriver.Chrome(
                executable_path="D:\Python\Chrome_Driver_selenium\chromedriver_win32\chromedriver.exe")
        elif system_type == "Linux":
            # driver = webdriver.Chrome()
            self.driver = webdriver.Chrome(
                executable_path="/mnt/samba/share/Selenium_PhantomJS_Driver/Chrome_Driver_selenium/chromedriver_linux64/chromedriver")

        # 设置显示等待时间10秒
        # self.wait = WebDriverWait(self.browser, 10)

    def __enter_douban(self):
        # 打开百度首页
        self.driver.get("http://www.baidu.com")
        # 窗口最大化
        self.driver.maximize_window()
        # 百度首页输入框的元素表达式
        input_id = "kw"
        # 设置显性等待，等待百度首页输出框的出现
        WebDriverWait(self.driver, 3, 0.3).until(EC.visibility_of_element_located((By.ID, input_id)))
        # 定位百度输入框并输入豆瓣电影Top250
        self.driver.find_element_by_id(input_id).send_keys("豆瓣电影Top250")
        # 定位百度一下按钮并点击
        self.driver.find_element_by_id("su").click()
        # 第一条搜索结果的元素表达式
        top250_css = "div[id='1'] h3 a"
        # 设置显性等待，等待第一条搜索结果的出现
        WebDriverWait(self.driver, 5, 0.3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, top250_css)))
        # 获得当前浏览器的所有窗口句柄
        windows = self.driver.window_handles
        # 定位到第一条搜索结果并点击
        self.driver.find_element_by_css_selector(top250_css).click()
        # 设置显性等待，等待新窗口的出现
        WebDriverWait(self.driver, 10, 0.3).until(EC.new_window_is_opened(windows))
        # 获得当前浏览器的所有窗口句柄
        windows = self.driver.window_handles
        # 切换到新的窗口
        self.driver.switch_to.window(windows[-1])

    def __get_datas(self):
        if self.page_num == 1:
            # 得到标题
            title = self.driver.find_element_by_xpath("//div[@id='content']//h1").text
            # 打印标题
            print(title)
            self.fs.write(title + "\r\n")
        # 获得当前页面电影信息的元素对象的列表，总共有25条
        movies_list = self.driver.find_elements_by_xpath("//ol//li")
        for element in movies_list:
            print(element.text + "\n")
            self.fs.write(element.text + "\r\n")

    def get_all_pages(self):
        self.page_num = 1
        while self.page_num < 26:
            self.__get_datas()
            print("-------------第{0}页-----------\n".format(self.page_num))
            self.fs.write("-------------第{0}页-----------\n".format(self.page_num))
            self.page_num += 1
        # 关闭文件
        self.fs.close()


if __name__ == "__main__":
    douban_movies = DouBan_Movies()
    douban_movies.get_all_pages()
