# -*- coding: UTF-8 -*-

"""
获取百度翻译请求
    百度翻译: https://fanyi.baidu.com/
    post请求: https://fanyi.baidu.com/v2transapi?from=zh&to=en

    请求Headers:
        POST https://fanyi.baidu.com/v2transapi?from=zh&to=en HTTP/1.1
        Host: fanyi.baidu.com
        Connection: keep-alive
        Content-Length: 129
        Accept: */*
        Sec-Fetch-Dest: empty
        X-Requested-With: XMLHttpRequest
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36
        Content-Type: application/x-www-form-urlencoded; charset=UTF-8
        Origin: https://fanyi.baidu.com
        Sec-Fetch-Site: same-origin
        Sec-Fetch-Mode: cors
        Referer: https://fanyi.baidu.com/
        Accept-Encoding: gzip, deflate, br
        Accept-Language: zh-CN,zh;q=0.9
        Cookie: BAIDUID=D17B34117C46D60C15B6A9AB4C625F68:FG=1; BIDUPSID=D17B34117C46D60C15B6A9AB4C625F68; PSTM=1576460924; BDUSS=kdLZGw4MFh4ZTIyVDVHRkM4cEN-c25YV09xcmhneUl3LWZTUzN-MDdZT2R4a2RlSVFBQUFBJCQAAAAAAAAAAAEAAACOSosns8K93DIwMTAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJ05IF6dOSBeQ; FANYI_WORD_SWITCH=1; REALTIME_TRANS_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1582882623,1583119627,1583997471; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=30975_1468_21087_30910_30999_30824_31086_26350; delPer=0; PSINO=6; yjs_js_security_passport=a97990e3525b5c1f7e5e62c01b98854f136bb962_1584090199_js; from_lang_often=%5B%7B%22value%22%3A%22it%22%2C%22text%22%3A%22%u610F%u5927%u5229%u8BED%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; to_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1584092503; __yjsv5_shitong=1.0_7_3e150a289ef69c2d127f2a67baa9fd9ab2a0_300_1584092502819_119.139.196.224_76b744c2

        from=zh&to=en&query=%E7%81%AB%E7%AE%AD&simple_means_flag=3&sign=59704.264713&token=b486e2974261429a363a52bcf57e1b4f&domain=common

    请求body:
        from:zh
        to:en
        query:火箭
        simple_means_flag:3
        sign:59704.264713
        token:b486e2974261429a363a52bcf57e1b4f
        domain:common

"""
from urllib import request
import requests
import json

if __name__ == "__main__":
    # hanzi = input("请输入要翻译的汉字:")
    hanzi = "火箭"

    # post请求的url
    target = "https://fanyi.baidu.com/v2transapi?from=zh&to=en"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        "Host": "fanyi.baidu.com",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://fanyi.baidu.com",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "BAIDUID=D17B34117C46D60C15B6A9AB4C625F68:FG=1; BIDUPSID=D17B34117C46D60C15B6A9AB4C625F68; PSTM=1576460924; BDUSS=kdLZGw4MFh4ZTIyVDVHRkM4cEN-c25YV09xcmhneUl3LWZTUzN-MDdZT2R4a2RlSVFBQUFBJCQAAAAAAAAAAAEAAACOSosns8K93DIwMTAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJ05IF6dOSBeQ; FANYI_WORD_SWITCH=1; REALTIME_TRANS_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1582882623,1583119627,1583997471; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=30975_1468_21087_30910_30999_30824_31086_26350; delPer=0; PSINO=6; yjs_js_security_passport=a97990e3525b5c1f7e5e62c01b98854f136bb962_1584090199_js; from_lang_often=%5B%7B%22value%22%3A%22it%22%2C%22text%22%3A%22%u610F%u5927%u5229%u8BED%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; to_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1584092503; __yjsv5_shitong=1.0_7_3e150a289ef69c2d127f2a67baa9fd9ab2a0_300_1584092502819_119.139.196.224_76b744c2",
    }

    # 创建form表单
    form_data = {
        "from": "zh",
        "to": "en",
        "query": hanzi,
        "simple_means_flag": "3",
        "sign": "59704.264713",
        "token": "b486e2974261429a363a52bcf57e1b4f",
        "domain": "common",
    }
    requests.packages.urllib3.disable_warnings()  # 去除警告
    response = requests.get(url=target, headers=headers, params=form_data, verify=False)
    # 方式1: 解决中文乱码问题
    html = response.content
    html = html.decode('utf-8', 'ignore')
    # html = html.decode('gbk', 'ignore')

    # 方式2: 解决中文乱码问题
    # response.encoding = "utf-8"
    # response.encoding = "gbk"
    # html = response.text
    print(html)
    # dataJsonStr = html.replace("\\n", "")

    # 使用JSON
    translate_results = json.loads(html)
    print(translate_results)
    print("翻译结果:{} --- >>>  {}".format(translate_results["trans_result"]["data"][0]["src"],
                                       translate_results["trans_result"]["data"][0]["dst"]))
