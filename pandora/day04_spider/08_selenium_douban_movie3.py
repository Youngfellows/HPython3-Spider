# coding=utf-8
"""
豆瓣电影爬虫
"""
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import platform
from lxml import etree

url = 'https://movie.douban.com/'


# 获取电影详情地址以及电影的名称
def get_datail_url_and_movie_name(movie_count):
    # 定位“选电影”
    driver_info.get(url)
    WebDriverWait(driver_info, 15).until(
        # lambda driver_info: driver_info.find_elements_by_css_selector('.nav-items a')[1]).click()
        lambda driver_info: driver_info.find_elements_by_css_selector('.nav-items a')[1]).click()
    # 定位"按评价排序"
    WebDriverWait(driver_info, 10).until(
        # lambda driver_info: driver_info.find_elements_by_css_selector('.tag-list label')[4]).click()
        lambda driver_info: driver_info.find_elements_by_css_selector('.sort label')[2]).click()

    # 需要根据电影总数量来计算需要点击几次‘加载更多’，
    # open_more变量用与记录点击次数
    if movie_count == 20:
        pass

    else:
        open_more = int(movie_count / 20 - 1)
        print("open_more: {}".format(open_more))

        # 定位加载更多
        # for x in range(1, open_more + 1):
        more = WebDriverWait(driver_info, 10).until(
            lambda driver_info: driver_info.find_element_by_css_selector('.more'))

        # 等待电影列表加载完成
        WebDriverWait(driver_info, 15).until(
            lambda driver_info: driver_info.find_element_by_css_selector('.list'))

        # 设置显性等待，等待第一条搜索结果的出现
        # 搜索结果的元素表达式
        # list_css = "div[id='1'] h3 a"
        # '//div[@class="list"]/a/p'
        list_css = "div[class='list'] a p"
        WebDriverWait(driver_info, 15, 0.3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, list_css)))

        html = driver_info.page_source
        print(html)

        # 提取电影名称
        # title_list = driver_info.find_elements_by_css_selector('.list a')
        # title_list = driver_info.find_elements_by_xpath('//div[@class="list"]/a')

        # 解析html
        dom_tree = etree.HTML(html)
        title_list = dom_tree.xpath('//div[@class="list"]/a/p/text()')
        link_list = dom_tree.xpath('//div[@class="list"]/a/@href')

        print("*" * 60)
        new_titles = []
        for title in title_list:
            title = title.strip()
            # print("title: {}-->>>size(): {}".format(title, len(title)))
            if len(title) != 0:
                new_titles.append(title)  # 去出空格

        print("title_list.size(): {},{}".format(len(title_list), title_list))
        print("new_titles.size(): {},{}".format(len(new_titles), new_titles))
        print("link_list.size(): {},{}".format(len(link_list), link_list))

        for title, link in zip(new_titles, link_list):
            print("=" * 60)
            print("电影名: {}".format(title))
            print("详  情: {}".format(link))
            get_detail_info(link)

        """
        如果没有最多的时候,退出爬取
        """
        # 点击更多
        more.click()


def get_detail_info(url):
    # driver_detail.get(url)
    # div = WebDriverWait(driver_detail, 10).until(
    #     lambda driver_detail: driver_detail.find_element_by_css_selector('#hot-comments'))

    driver_info.get(url)
    div = WebDriverWait(driver_info, 10).until(
        lambda driver_detail: driver_detail.find_element_by_css_selector('#hot-comments'))
    comments_list = div.find_elements_by_class_name('comment-item')
    # print(comments_list)

    # 获取前15条热门评论
    for comment in comments_list[:15]:
        # 在comment这个对象的基础上继续定位p标签
        p = comment.find_element_by_tag_name('p').text
        print("热门评论：{}".format(p))


if __name__ == '__main__':
    # 创建连个PhantomJS浏览器对象，一个用于解析列表页，一个用于解析详情页的
    # 热门评论
    # driver_info = webdriver.PhantomJS(executable_path=r"H:\Python\phantomjs-2.1.1-windows\bin\phantomjs.exe")
    # driver_detail = webdriver.PhantomJS(executable_path=r"H:\Python\phantomjs-2.1.1-windows\bin\phantomjs.exe")

    system_type = platform.system()
    print("操作系统类型:{}".format(system_type))
    if system_type == "Windows":
        # driver = webdriver.Chrome()
        driver_info = webdriver.Chrome(
            executable_path="D:\Python\Chrome_Driver_selenium\chromedriver_win32\chromedriver.exe")
        # driver_detail = webdriver.Chrome(
        #     executable_path="D:\Python\Chrome_Driver_selenium\chromedriver_win32\chromedriver.exe")
    elif system_type == "Linux":
        # driver = webdriver.Chrome()
        driver_info = webdriver.Chrome(
            executable_path="/mnt/samba/share/Selenium_PhantomJS_Driver/Chrome_Driver_selenium/chromedriver_linux64/chromedriver")
        # driver_detail = webdriver.Chrome(
        #     executable_path="/mnt/samba/share/Selenium_PhantomJS_Driver/Chrome_Driver_selenium/chromedriver_linux64/chromedriver")

    # 输入需要下载的数量
    number = int(input('请输入下载总数：'))
    get_datail_url_and_movie_name(number)
