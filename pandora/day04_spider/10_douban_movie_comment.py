# from bs4 import BeautifulSoup
import re, csv, urllib.request, urllib.parse, time, json, pickle, random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import platform

""""
心得：
     1.采用selenium由于涉及到加载数据，比较缓慢，容易超时，一定要采用try语句，
     2.使用的xpath搜索时，容易找不到所要的路径，需要简洁化，否认则会出现假死机现象
     3.采用selenium爬虫，由于涉及到页面加载，十分缓慢，个人倾向于ajax技术。
     4.由于豆瓣信息中需要获取的信息是静态的，所以可以直接使用bs4模块进行获取，不必采用selenium
"""


class managerurl(object):
    def __init__(self):
        self.oldurls = set()
        self.newurls = set()

    def add_newurls(self, urls):
        if urls:
            for i in urls:
                self.add_newurl(i)

    def add_newurl(self, url):
        if url not in self.newurls and url not in self.oldurls:
            self.newurls.add(url)

    def has_newurls(self):
        url = self.newurls.pop()
        self.oldurls.add(url)
        return url


class data_get(object):
    def __init__(self):
        self.manaurl = managerurl()

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

    def data_gain(self, url):
        data = []
        num = 0
        # driver = webdriver.Firefox()
        self.initChrome()

        self.manaurl.add_newurl(url)
        while 1:
            if len(self.manaurl.newurls):
                url1 = self.manaurl.has_newurls()
                self.driver.get(url1)
                try:
                    timeout = WebDriverWait(self.driver, 15)
                    moviescore = timeout.until(
                        EC.presence_of_element_located((By.XPATH, "//strong[@class='ll rating_num']")))  # 获取电影评分
                    othermovies = timeout.until(EC.presence_of_element_located(
                        (By.XPATH, "//div[@class='recommendations-bd']")))  # xpath语句一定要简洁化，可以考虑多次使用该函数见变量othermovie
                    moviename = timeout.until(
                        EC.presence_of_element_located((By.XPATH, "//span[@property='v:itemreviewed']")))  # 获取电影名字
                except:  # 超时时，关闭driver，重新打开
                    print(url1, 'is timeout')
                    self.driver.close()
                    # driver = webdriver.Firefox()
                    self.initChrome()
                    continue
                othermovie = othermovies.find_elements_by_xpath("//dd/a[@class='']")  # 获取同类电影列表
                print(moviename.text, num)
                for i in othermovie:
                    self.manaurl.add_newurl(i.get_attribute('href'))
                data.append({'moviename': moviename.text, 'score': moviescore.text})
                num += 1
            if num > 50:
                self.driver.close()
                print(data)
                break


if __name__ == "__main__":
    b = data_get()
    url = 'https://movie.douban.com/subject/27663742/'
    b.data_gain(url)
