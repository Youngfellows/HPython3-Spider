# coding=utf-8
import platform
from selenium import webdriver
import time


# 使用chrome浏览器内核
def chrome():
    system_type = platform.system()
    print("操作系统类型:{}".format(system_type))
    if system_type == "Windows":
        # browser = webdriver.Chrome()
        browser = webdriver.Chrome(
            executable_path="D:\Python\Chrome_Driver_selenium\chromedriver_win32\chromedriver.exe")
    elif system_type == "Linux":
        browser = webdriver.Chrome(
            executable_path="/mnt/samba/share/Selenium_PhantomJS_Driver/Chrome_Driver_selenium/chromedriver_linux64/chromedriver")
    # url = "http://www.baidu.com/"
    url = "https://www.douyu.com/directory/all"
    browser.get(url)

    # 休眠3秒
    time.sleep(3)

    # 向下滚动10000像素
    js = "document.body.scrollTop=10000"
    # js="var q=document.documentElement.scrollTop=10000"

    # 查看页面快照
    browser.save_screenshot("./screenshot/baidu.png")

    # 执行JS语句
    browser.execute_script(js)
    time.sleep(10)

    # 查看页面快照
    browser.save_screenshot("./screenshot/new_baidu.png")

    # 退出
    browser.quit()


# 使用firefox浏览器内核
def firefox():
    pass


if __name__ == "__main__":
    chrome()
    firefox()
