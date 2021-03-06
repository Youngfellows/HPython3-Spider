# coding=utf-8
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import xlwt
import platform

# 无痕浏览器
# browser = webdriver.PhantomJS()

# 使用chrome浏览器
# browser = webdriver.Chrome()

system_type = platform.system()
print("操作系统类型:{}".format(system_type))

if system_type == "Windows":
    # driver = webdriver.Chrome()
    browser = webdriver.Chrome(
        executable_path=r"D:\Python\Chrome_Driver_selenium\chromedriver_win32\chromedriver.exe")
    # browser = webdriver.PhantomJS(executable_path=r"D:\Python\phantomjs-2.1.1-windows\bin\phantomjs.exe")

elif system_type == "Linux":
    # driver = webdriver.Chrome()
    browser = webdriver.Chrome(
        executable_path=r"/mnt/samba/share/Selenium_PhantomJS_Driver/Chrome_Driver_selenium/chromedriver_linux64/chromedriver")
    # browser = webdriver.PhantomJS(
    #   executable_path=r"/mnt/samba/share/Selenium_PhantomJS_Driver/phantomjs_Driver/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")

WAIT = WebDriverWait(browser, 10)
browser.set_window_size(1400, 900)

book = xlwt.Workbook(encoding='utf-8', style_compression=0)

sheet = book.add_sheet('蔡徐坤篮球', cell_overwrite_ok=True)
sheet.write(0, 0, '名称')
sheet.write(0, 1, '地址')
sheet.write(0, 2, '描述')
sheet.write(0, 3, '观看次数')
sheet.write(0, 4, '弹幕数')
sheet.write(0, 5, '发布时间')

n = 1


def search():
    try:
        print('开始访问b站....')
        browser.get("https://www.bilibili.com/")

        # 被那个破登录遮住了
        # index = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#primary_menu > ul > li.home > a")))
        # index.click()

        # 等待搜索框出现
        # input = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#nav_searchform > input")))
        input = WAIT.until(EC.presence_of_element_located((By.XPATH, '//form[@id="nav_searchform"]/input')))

        # submit = WAIT.until(EC.element_to_be_clickable(
        #     (By.XPATH, '/html/body/div[2]/div/div[1]/div[1]/div/div[2]/div/form/div/button')))
        submit = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//form[@id="nav_searchform"]/div/button')))

        input.send_keys('蔡徐坤 篮球')
        submit.click()

        # 跳转到新的窗口
        print('跳转到新窗口')
        all_h = browser.window_handles
        browser.switch_to.window(all_h[1])
        get_source()

        # total = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR,
        #                                                    "#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.last > button")))

        total = WAIT.until(EC.presence_of_element_located((By.XPATH,
                                                           '//div[@id="all-list"]/div[@class="flow-loader"]/div[@class="page-wrap"]/div[@class="pager"]/ul/li[@class="page-item last"]')))
        return int(total.text)
    except TimeoutException:
        return search()


def next_page(page_num):
    try:
        print('获取下一页数据,page_num = {}'.format(page_num))
        # next_btn = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
        #                                                   '#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.next > button')))
        next_btn = WAIT.until(EC.element_to_be_clickable((By.XPATH,
                                                          '//div[@id="all-list"]/div[@class="flow-loader"]/div[@class="page-wrap"]/div[@class="pager"]/ul/li[@class="page-item next"]')))
        next_btn.click()

        # 当前页数,判断某个元素中的 text 是否 包含 了预期的字符串
        # WAIT.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,
        #                                              '#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.active > button'),
        #                                             str(page_num)))
        WAIT.until(EC.text_to_be_present_in_element((By.XPATH,
                                                     '//div[@id="all-list"]/div[@class="flow-loader"]/div[@class="page-wrap"]/div[@class="pager"]/ul/li[@class="page-item active"]'),
                                                    str(page_num)))

        get_source()
    except TimeoutException:
        browser.refresh()
        return next_page(page_num)


def save_to_excel(soup):
    # list = soup.find(class_='video-list clearfix').find_all(class_='video-item matrix')
    # list = soup.find(name="ul", class_='video-list clearfix').find_all(class_='video-item matrix')
    # list = soup.find(name="ul", attrs={"class":"video-list clearfix"}).find_all(class_='video-item matrix')
    list = soup.find(name="ul", attrs={"class": "video-list clearfix"}).find_all(name="li", class_='video-item matrix')

    for item in list:
        item_title = item.find('a').get('title')
        item_link = item.find('a').get('href')
        item_dec = item.find(class_='des hide').text
        item_view = item.find(class_='so-icon watch-num').text
        item_biubiu = item.find(class_='so-icon hide').text
        item_date = item.find(class_='so-icon time').text

        print('爬取：' + item_title)

        global n

        sheet.write(n, 0, item_title)
        sheet.write(n, 1, item_link)
        sheet.write(n, 2, item_dec)
        sheet.write(n, 3, item_view)
        sheet.write(n, 4, item_biubiu)
        sheet.write(n, 5, item_date)

        n = n + 1


def get_source():
    # WAIT.until(EC.presence_of_element_located(
    #     (By.CSS_SELECTOR, '#all-list > div.flow-loader > div.filter-wrap')))
    WAIT.until(EC.presence_of_element_located(
        (By.XPATH, '//div[@id="all-list"]/div[@class="flow-loader"]/div[@class="filter-wrap"]')))

    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    print('到这')

    save_to_excel(soup)


def main():
    try:
        total = search()
        print(total)

        for i in range(2, int(total + 1)):
            next_page(i)

    finally:
        print("quit browser ...")
        browser.close()
        #browser.quit()


if __name__ == '__main__':
    main()
    book.save('./json/蔡徐坤篮球.xlsx')
