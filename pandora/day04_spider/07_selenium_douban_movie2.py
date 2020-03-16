# coding=utf-8
"""
豆瓣电影爬虫
"""
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

url = 'https://movie.douban.com/'


# 获取电影详情地址以及电影的名称
def get_datail_url_and_movie_name(movie_count):
    # 定位“选电影”
    driver_info.get(url)
    WebDriverWait(driver_info, 15).until(
        #lambda driver_info: driver_info.find_elements_by_css_selector('.nav-items a')[1]).click()
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
        for x in range(1, open_more + 1):
            WebDriverWait(driver_info, 10).until(
                lambda driver_info: driver_info.find_element_by_css_selector('.more')).click()
            # 提取电影名称
            title_list = driver_info.find_elements_by_css_selector('.list a')
            for a in title_list:
                #//div[@class="list"]/a[@class="item"]/@href
                print
                u'电影地址:' + a.get_attribute('href')
                # //div[@class="list"]/a[@class="item"]//p/text()
                print
                u'电影名称:' + a.text
                # 根据电影详情URL下载热门评论
                get_detail_info(a.get_attribute('href'))


def get_detail_info(url):
    driver_detail.get(url)
    div = WebDriverWait(driver_detail, 10).until(
        lambda driver_detail: driver_detail.find_element_by_css_selector('#hot-comments'))
    comments_list = div.find_elements_by_class_name('comment-item')
    # 获取前15条热门评论
    for comment in comments_list[:15]:
        # 在comment这个对象的基础上继续定位p标签
        p = comment.find_element_by_tag_name('p').text
        print
        u'热门评论：' + p


if __name__ == '__main__':
    # 创建连个PhantomJS浏览器对象，一个用于解析列表页，一个用于解析详情页的
    # 热门评论
    driver_info = webdriver.PhantomJS(executable_path=r"H:\Python\phantomjs-2.1.1-windows\bin\phantomjs.exe")
    driver_detail = webdriver.PhantomJS(executable_path=r"H:\Python\phantomjs-2.1.1-windows\bin\phantomjs.exe")
    # 输入需要下载的数量
    number = int(input('请输入下载总数：'))
    get_datail_url_and_movie_name(number)
