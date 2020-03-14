# coding=utf-8
import platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


# 使用chrome浏览器内核
def chrome():
    system_type = platform.system()
    print("操作系统类型:{}".format(system_type))
    if system_type == "Windows":
        # browser = webdriver.Chrome()
        driver = webdriver.Chrome(
            executable_path="D:\Python\Chrome_Driver_selenium\chromedriver_win32\chromedriver.exe")
    elif system_type == "Linux":
        driver = webdriver.Chrome(
            executable_path="/mnt/samba/share/Selenium_PhantomJS_Driver/Chrome_Driver_selenium/chromedriver_linux64/chromedriver")
    url = "http://www.baidu.com"
    driver.get(url)
    # print(driver.title)
    assert "百度一下，你就知道" in driver.title
    elem = driver.find_element_by_name("wd")
    elem.send_keys("美女")
    elem.send_keys(Keys.RETURN)
    print(driver.page_source)

    # 休眠3*60秒
    time.sleep(30)


if __name__ == "__main__":
    chrome()
