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

system_type = platform.system()
print("操作系统类型:{}".format(system_type))
if system_type == "Windows":
    # browser = webdriver.Chrome()
    browser = webdriver.Chrome(
        executable_path="D:\Python\Chrome_Driver_selenium\chromedriver_win32\chromedriver.exe")
elif system_type == "Linux":
    # browser = webdriver.Chrome()
    browser = webdriver.Chrome(
        executable_path="/mnt/samba/share/Selenium_PhantomJS_Driver/Chrome_Driver_selenium/chromedriver_linux64/chromedriver")

# 设置显示等待时间10秒
wait = WebDriverWait(browser, 10)

# 保存新闻连接的列表
sina_news_list = []


# 进入爬取页面
def search():
    try:
        url = 'https://news.sina.com.cn/roll/#pageid=153&lid=2509&k=&num=50&page=1'
        browser.get(url)
        wait.until(EC.presence_of_element_located((By.ID, 'pL_Main')))
        getDetail()
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#d_list > div > span:nth-child(14) > a')))
        return total.text
    except TimeoutError:
        return search()


# 得到具体信息
def getDetail():
    global sina_news_list
    html = pq(browser.page_source, parser="html")
    content = html.find('#d_list')
    uls = content.find('ul').items()
    for ul in uls:
        lis = ul('li').items()
        for li in lis:
            news = {
                'title': li.find('.c_tit a').text(),
                'href': li.find('.c_tit a').attr('href'),
                'time': li.find('.c_time').text()
            }
            sina_news_list.append(news)
            print(news)


# 爬取下一页
def next_detail(page_number):
    try:
        nextBotton = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#d_list > div > span:last-child > a')))
        nextBotton.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#d_list > div > span.pagebox_num_nonce'),
                                                    str(page_number)))
        getDetail()
    except TimeoutException:
        next_detail(page_number)


def main():
    try:
        total = search()
        total = int(total)
        print(total)
        for i in range(2, total + 1):
            next_detail(i)
    except Exception:
        print(Exception)
    finally:
        browser.close()


def writer2json():
    global sina_news_list
    file_name = "./json/sina_news.json"
    # 删除旧文件
    if file_name in os.listdir():
        os.remove(file_name)

    # dumps()默认中文为ascii编码格式，ensure_ascii默认为Ture
    # 禁用ascii编码格式，返回的Unicode字符串，方便使用
    json_str = json.dumps(sina_news_list, ensure_ascii=False)
    with open(file_name, "wb") as fp:
        fp.write(json_str.encode('utf-8'))


if __name__ == '__main__':
    main()
    print("*" * 50)
    # writer2json()
    print("恭喜您爬取新浪新闻成功...")
