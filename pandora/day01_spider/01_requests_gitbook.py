# -*- coding:UTF-8 -*-

# requests网络请求库
import requests

if __name__ == "__main__":
    target = "https://gitbook.cn/"
    # 请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
    }
    # 网络请求
    requests.packages.urllib3.disable_warnings()  # 去除警告
    response = requests.get(url=target, headers=headers, verify=False)  # 忽略证书认证
    html = response.text
    print(html)

    print("*" * 40)
    # 响应的头信息
    resopnse_head = requests.head(url=target, headers=headers, verify=False)
    print("type(resopnse_head):{}".format(type(resopnse_head)))
    headers = resopnse_head.headers
    # print(headers)
    for key, value in headers.items():
        print("{}:{}".format(key, value))
