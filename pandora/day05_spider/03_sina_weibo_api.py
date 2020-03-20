# coding=utf-8
import json
import requests
import sys
import traceback
from collections import OrderedDict
from datetime import date, datetime, timedelta
from time import sleep
import os
import tqdm
import math
from lxml import etree
from requests.adapters import HTTPAdapter
import urllib


class WeiBoAPI(object):
    """
    测试新浪微博api接口
    """

    def __init__(self, user_config):
        """构造函数"""
        self.user_config = user_config
        self.cookie = {
            "Cookie": "_T_WM=17987859486; SCF=ApV_4nOagHHSD5qQrZGtiLOf-214psdlRVx6Jc5aD7Iq4F57vTnTJnrVSohmv1KUmiXnpT4pYaSGeaPe0LZ5bFI.; MLOGIN=1; XSRF-TOKEN=8d60d8; SUB=_2A25zcGp7DeRhGeFK6lQR9C3IyT6IHXVQm3YzrDV6PUJbkdAKLUvNkW1NQ5gAUiiAWUVHAs4_h-xi7mxnGSTKJwAm; SUHB=0ftpOYAi2YfhnB; SSOLoginState=1584667179", }  # 微博cookie，可填可不填
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
            "Cookie": "_T_WM=17987859486; SCF=ApV_4nOagHHSD5qQrZGtiLOf-214psdlRVx6Jc5aD7Iq4F57vTnTJnrVSohmv1KUmiXnpT4pYaSGeaPe0LZ5bFI.; MLOGIN=1; XSRF-TOKEN=8d60d8; SUB=_2A25zcGp7DeRhGeFK6lQR9C3IyT6IHXVQm3YzrDV6PUJbkdAKLUvNkW1NQ5gAUiiAWUVHAs4_h-xi7mxnGSTKJwAm; SUHB=0ftpOYAi2YfhnB; SSOLoginState=1584667179",
        }

    def get_json(self, params):
        """获取网页中json数据"""
        url = 'https://m.weibo.cn/api/container/getIndex?'
        # r = requests.get(url, params=params, cookies=self.cookie)
        r = requests.get(url, params=params, headers=self.headers)
        # 将获取的json数据转换为pythond对象(字典)
        return r.json()

    def get_weibo_json(self, page):
        """获取网页中微博json数据"""
        params = {
            'containerid': '107603' + str(self.user_config['user_id']),
            'page': page
        }
        js = self.get_json(params)
        return js

    def read2json(self, file_name):
        """读取json文件,并转换为字典/列表"""
        with open(file_name, "r", encoding="utf-8") as fp:
            chapters = json.load(fp)
        print(chapters)
        return chapters

    def writer2json(self, file_name, dict):
        """将列表保存为json"""
        # 删除旧文件
        if file_name in os.listdir():
            os.remove(file_name)

        # dumps()默认中文为ascii编码格式，ensure_ascii默认为Ture
        # 禁用ascii编码格式，返回的Unicode字符串，方便使用
        json_str = json.dumps(dict, ensure_ascii=False)
        with open(file_name, "wb") as fp:
            fp.write(json_str.encode('utf-8'))

    def standardize_info(self, weibo):
        """标准化信息，去除乱码"""
        for k, v in weibo.items():
            if 'bool' not in str(type(v)) and 'int' not in str(
                    type(v)) and 'list' not in str(
                type(v)) and 'long' not in str(type(v)):
                weibo[k] = v.replace(u"\u200b", "").encode(
                    sys.stdout.encoding, "ignore").decode(sys.stdout.encoding)
        return weibo

    def get_user_info(self):
        """获取用户信息"""
        params = {'containerid': '100505' + str(self.user_config['user_id'])}
        print(params)
        js = self.get_json(params)
        self.writer2json("./json/weibo_user_info.json", js)
        # print("获取的用户信息: {}".format(js))

        if js['ok']:
            info = js['data']['userInfo']
            user_info = OrderedDict()
            user_info['id'] = self.user_config['user_id']
            user_info['screen_name'] = info.get('screen_name', '')
            user_info['gender'] = info.get('gender', '')
            params = {
                'containerid':
                    '230283' + str(self.user_config['user_id']) + '_-_INFO'
            }
            zh_list = [
                u'生日', u'所在地', u'小学', u'初中', u'高中', u'大学', u'公司', u'注册时间',
                u'阳光信用'
            ]
            en_list = [
                'birthday', 'location', 'education', 'education', 'education',
                'education', 'company', 'registration_time', 'sunshine'
            ]
            for i in en_list:
                user_info[i] = ''
            js = self.get_json(params)
            self.writer2json("./json/weibo_user_info_detail.json", js)

            if js['ok']:
                cards = js['data']['cards']
                if isinstance(cards, list) and len(cards) > 1:
                    card_list = cards[0]['card_group'] + cards[1]['card_group']
                    for card in card_list:
                        if card.get('item_name') in zh_list:
                            user_info[en_list[zh_list.index(
                                card.get('item_name'))]] = card.get(
                                'item_content', '')
            user_info['statuses_count'] = info.get('statuses_count', 0)
            user_info['followers_count'] = info.get('followers_count', 0)
            user_info['follow_count'] = info.get('follow_count', 0)
            user_info['description'] = info.get('description', '')
            user_info['profile_url'] = info.get('profile_url', '')
            user_info['profile_image_url'] = info.get('profile_image_url', '')
            user_info['avatar_hd'] = info.get('avatar_hd', '')
            user_info['urank'] = info.get('urank', 0)
            user_info['mbrank'] = info.get('mbrank', 0)
            user_info['verified'] = info.get('verified', False)
            user_info['verified_type'] = info.get('verified_type', 0)
            user_info['verified_reason'] = info.get('verified_reason', '')
            user = self.standardize_info(user_info)
            # print(user)
            self.writer2json("./json/user.json", user)
            self.user = user
            return user

    def print_user_info(self):
        """打印用户信息"""
        print('+' * 100)
        print(u'用户信息')
        print(u'用户id：%s' % self.user['id'])
        print(u'用户昵称：%s' % self.user['screen_name'])
        gender = u'女' if self.user['gender'] == 'f' else u'男'
        print(u'性别：%s' % gender)
        print(u'生日：%s' % self.user['birthday'])
        print(u'所在地：%s' % self.user['location'])
        print(u'教育经历：%s' % self.user['education'])
        print(u'公司：%s' % self.user['company'])
        print(u'阳光信用：%s' % self.user['sunshine'])
        print(u'注册时间：%s' % self.user['registration_time'])
        print(u'微博数：%d' % self.user['statuses_count'])
        print(u'粉丝数：%d' % self.user['followers_count'])
        print(u'关注数：%d' % self.user['follow_count'])
        print(u'url：https://m.weibo.cn/profile/%s' % self.user['id'])
        if self.user.get('verified_reason'):
            print(self.user['verified_reason'])
        print(self.user['description'])
        print('+' * 100)

    def get_page_count(self):
        """获取微博页数"""
        try:
            weibo_count = self.user['statuses_count']
            page_count = int(math.ceil(weibo_count / 10.0))
            return page_count
        except KeyError:
            print(u'程序出错，错误原因可能为以下两者：\n'
                  u'1.user_id不正确；\n'
                  u'2.此用户微博可能需要设置cookie才能爬取。\n'
                  u'解决方案：\n'
                  u'请参考\n'
                  u'https://github.com/dataabc/weibo-crawler#如何获取user_id\n'
                  u'获取正确的user_id；\n'
                  u'或者参考\n'
                  u'https://github.com/dataabc/weibo-crawler#3程序设置\n'
                  u'中的“设置cookie”部分设置cookie信息')

    def get_at_users(self, selector):
        """获取@用户"""
        a_list = selector.xpath('//a')
        at_users = ''
        at_list = []
        print("a.xpath('@href')[0] = {}".format(a_list[0].xpath('@href')[0]))
        print("a.xpath('@href')[1] = {}".format(a_list[1].xpath('@href')[0]))
        print("a.xpath('string(.)') = {}".format(a_list[0].xpath('string(.)')))
        print("a.xpath('string(.)') = {}".format(a_list[1].xpath('string(.)')))
        # 获取列表节点的属性和内容
        for a in a_list:
            if '@' + a.xpath('@href')[0][3:] == a.xpath('string(.)'):
                # if '@' + a.xpath('@href')[0][3:] == a.text:
                at_list.append(a.xpath('string(.)')[1:])
        if at_list:
            at_users = ','.join(at_list)
        return at_users

    def download_one_file(self, url, file_path, type, weibo_id):
        """下载单个文件(图片/视频)"""
        try:
            if not os.path.isfile(file_path):
                s = requests.Session()
                s.mount(url, HTTPAdapter(max_retries=5))
                downloaded = s.get(url, cookies=self.cookie, timeout=(5, 10))
                # downloaded = s.get(url, headers=self.headers, timeout=(5, 10))
                # downloaded = requests.get(url, headers=self.headers)
                with open(file_path, 'wb') as f:
                    f.write(downloaded.content)
        except Exception as e:
            error_file = './json/not_downloaded.txt'
            with open(error_file, 'ab') as f:
                url = type + ":" + str(weibo_id) + ':' + url + '\n'
                f.write(url.encode(sys.stdout.encoding))
            print('Error: ', e)
            traceback.print_exc()


if __name__ == "__main__":
    """测试新浪微博api接口"""

    # 古力娜扎
    user_config = {"user_id": 1350995007, "since_date": "2019-10-01"}
    weibo = WeiBoAPI(user_config)

    # 获取用户信息
    weibo.get_user_info()

    # 打印信息
    weibo.print_user_info()

    # 获取微博页数
    page_count = weibo.get_page_count()
    print("微博页数: {}".format(page_count))

    since_date = datetime.strptime("2018-07-26", '%Y-%m-%d')
    today = datetime.strptime(str(date.today()), '%Y-%m-%d')
    start_date = datetime.now().strftime('%Y-%m-%d')
    print(since_date)
    print(today)
    print(start_date)

    # 测试tqdm
    for page in tqdm.tqdm(range(1, page_count + 1), desc="Progress"):
        print("{}*******".format(page))

    # 获取@信息
    text = '''在线复工！Hi，我是<a  href="https://m.weibo.cn/search?containerid=231522type%3D1%26t%3D10%26q%3D%23%E9%A3%9E%E5%88%A9%E6%B5%A6%E7%BE%8E%E5%8F%91%E4%BB%A3%E8%A8%80%E4%BA%BA%E5%A8%9C%E6%89%8E%23&extparam=%23%E9%A3%9E%E5%88%A9%E6%B5%A6%E7%BE%8E%E5%8F%91%E4%BB%A3%E8%A8%80%E4%BA%BA%E5%A8%9C%E6%89%8E%23&luicode=10000011&lfid=1076031350995007" data-hide=""><span class="surl-text">#飞利浦美发代言人娜扎#</span></a>  ，很高兴被<a href='/n/飞利浦健康科技'>@飞利浦健康科技</a> 邀请，成为首位美发代言人。<br />对自己女王般的宠爱，要从“头”开始。心里有光，发丝也要美到发光✨相信春意和阳光很快如约而至，期待和你们见面的那天！ '''
    selector = etree.HTML(text)
    at_users = weibo.get_at_users(selector)
    print("at_users: {}".format(at_users))

    # 将列表转换为字符串
    at_list = ["夏明", "赵敏", "小龙女"]
    at_user = ",".join(at_list)
    print("at_users: {}".format(at_user))

    # 测试下载图片
    pic_url = "http://wx3.sinaimg.cn/large/a306ef6dly1gcx4u5itwvj20ts1hak6g.jpg"

    # 测试下载视频
    video_url = "http://f.video.weibocdn.com/EQ8nlZxSlx07BrpGp9gc010412007iHQ0E010.mp4?label=mp4_hd&template=640x368.25.0&trans_finger=62b30a3f061b162e421008955c73f536&Expires=1584688710&ssig=cH%2BN%2F6Vurp&KID=unistore,video"
    video_ur2 = "http://f.video.weibocdn.com/howH57STlx07BrpGms64010412006qw00E010.mp4?label=mp4_ld&template=624x360.25.0&trans_finger=40a32e8439c5409a63ccf853562a60ef&Expires=1584688710&ssig=OOtOatvJs4&KID=unistore,video"

    weibo.download_one_file(url=pic_url, file_path="./images/1.jpg", type="img", weibo_id=123455)
    weibo.download_one_file(url=video_url, file_path="./video/test_1.mp4", type="video", weibo_id=654321)
    weibo.download_one_file(url=video_ur2, file_path="./video/test_2.mp4", type="video", weibo_id=654321)
