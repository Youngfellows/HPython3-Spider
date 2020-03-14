# -*- coding: utf-8 -*-
import requests

# python2 和 python3的兼容代码
try:
    # python2 中
    import cookielib

    print(f"user cookielib in python2.")
except:
    # python3 中
    import http.cookiejar as cookielib

    print(f"user cookielib in python3.")

"""
使用cookie登录马蜂窝
    Request URL: https://passport.mafengwo.cn/login/
    Request Method: POST

headers头信息
	Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
	Accept-Encoding: gzip, deflate, br
	Accept-Language: zh-CN,zh;q=0.9
	Cache-Control: max-age=0
	Connection: keep-alive
	Content-Length: 36
	Content-Type: application/x-www-form-urlencoded
	Cookie: mfw_uuid=5e6c2e34-83e5-982d-ae52-c054b963e739; oad_n=a%3A3%3A%7Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222020-03-14+09%3A07%3A00%22%3B%7D; __mfwc=direct; __mfwlv=1584148021; __mfwvn=1; Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0=1584148022; UM_distinctid=170d694841586f-0585f7f4cd0b7e-4313f6a-144000-170d69484167cf; uva=s%3A91%3A%22a%3A3%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1584148022%3Bs%3A10%3A%22last_refer%22%3Bs%3A23%3A%22http%3A%2F%2Fwww.mafengwo.cn%2F%22%3Bs%3A5%3A%22rhost%22%3BN%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1584148022%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=5e6c2e34-83e5-982d-ae52-c054b963e739; __mfwa=1584148021275.86732.2.1584148021275.1584151738572; __jsluid_s=23eab2ffa92741453d0c1be13607d97b; uol_throttle=89605988; __omc_chl=; __omc_r=; CNZZDATA30065558=cnzz_eid%3D2011005706-1584148567-null%26ntime%3D1584148567; bottom_ad_status=0; mfw_passport_redirect=https%3A%2F%2Fwww.mafengwo.cn%2F; PHPSESSID=p8sid94dk4b572rmcniaguu011; __mfwb=b3d3566cd07c.23.direct; __mfwlt=1584152432; Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0=1584152433; _fmdata=eaB5TkFUz8i5pqH%2Bqmqx%2Fe2eqMctmiJUMt0kjLJDP1cX86%2FCQtROhoKplAWMlVmNDUIpWfV5bqGXbDjY4aCxIIG9CAk3gj0ssXSgDAIskKE%3D
	Host: passport.mafengwo.cn
	Origin: https://passport.mafengwo.cn
	Referer: https://passport.mafengwo.cn/
	Sec-Fetch-Dest: document
	Sec-Fetch-Mode: navigate
	Sec-Fetch-Site: same-origin
	Sec-Fetch-User: ?1
	Upgrade-Insecure-Requests: 1
	User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Mobile Safari/537.36

from_body请求体
    passport: 13699847981
    password: abcddf

登录成功后的个人页面
    #我的路线
	http://www.mafengwo.cn/plan/route.php
	
	我的收藏url
    http://www.mafengwo.cn/plan/fav_type.php 
"""


class Mafenwo(object):

    # 构造函数
    def __init__(self, account, password):
        object.__init__(self)
        requests.packages.urllib3.disable_warnings()  # 去除警告
        self.__login_url = "https://passport.mafengwo.cn/login/"  # 登录url
        self.__route_url = "http://www.mafengwo.cn/plan/route.php"  # 我的路线url
        self.__fav_url = "http://www.mafengwo.cn/plan/fav_type.php"  # 我的收藏url
        self._file_name = "./cookie/mafengwoCookies.txt"
        self.__mafengwo_session = requests.session()  # session代表某一次连接
        # 因为原始的session.cookies 没有save()方法，所以需要用到cookielib中的方法LWPCookieJar，
        # 这个类实例化的cookie对象，就可以直接调用save方法。
        self.__mafengwo_session.cookies = cookielib.LWPCookieJar(filename=self._file_name)
        self.__header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "passport.mafengwo.cn",
            "Origin": "https://passport.mafengwo.cn",
            "Referer": "https://passport.mafengwo.cn/",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Mobile Safari/537.36"
        }
        self.__form_data = {"passport": account, "password": password}  # post请求体

    # 加载已经存在的cookie
    def __load_cookie(self):
        try:
            # 第一步：尝试使用已有的cookie登录
            self.__mafengwo_session.cookies.load()
        except FileNotFoundError as e:
            print(e)
            print(f"cookie不存在,账号密码登录...")

    # 登录马蜂窝
    def __login(self):
        print("开始模拟登录马蜂窝")
        # 使用session直接post请求
        response = self.__mafengwo_session.post(url=self.__login_url, headers=self.__header,
                                                data=self.__form_data, verify=False)
        # 无论是否登录成功，状态码一般都是 statusCode = 200
        html = response.text
        print(f"login status code = {response.status_code}")
        # print(f"__login html = {html}")

        # 登录成功之后，将cookie保存在本地文件中，好处是，以后再去获取马蜂窝首页的时候，
        # 就不需要再走mafengwoLogin的流程了，因为已经从文件中拿到cookie了
        self.__mafengwo_session.cookies.save()

    # 通过访问个人中心页面的返回状态码来判断是否为登录状态
    def __is_login_state(self):
        # 下面有两个关键点
        # 第一个是header，如果不设置，会返回500的错误
        # 第二个是allow_redirects，如果不设置，session访问时，服务器返回302，
        # 然后session会自动重定向到登录页面，获取到登录页面之后，变成200的状态码
        # allow_redirects = False  就是不允许重定向
        response = self.__mafengwo_session.post(url=self.__route_url, headers=self.__header,
                                                allow_redirects=False, verify=False)
        code = response.status_code
        print(f"cookie login state = {code}")
        if code == 200:
            return True
        else:
            return False

    # 获取我的收藏页面信息
    def get_myfav(self):
        self.__load_cookie()  # 加载已经存在的cookie
        login = self.__is_login_state()  # 是否处于登录状态
        if login == False:
            # 第二步：如果cookie已经失效了，那就尝试用帐号登录
            print(f"cookie已经失效了,尝试用帐号登录...")
            self.__login()

        # 获取我的收藏页面信息
        response = self.__mafengwo_session.get(url=self.__fav_url, headers=self.__header, allow_redirects=False)
        state_code = response.status_code
        html = response.text
        print(f"fav page response, state code = {state_code}")
        # print(html)
        return html


if __name__ == "__main__":
    account = input("请输入马蜂窝用户名:")
    password = input("请输入马蜂窝密  码:")
    mafenwo = Mafenwo(account, password)
    mafenwo.get_myfav()  # 获取个人中心我的收藏信息
