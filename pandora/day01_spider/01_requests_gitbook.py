# -*- coding:UTF-8 -*-

# requests网络请求库
import requests

if __name__ == "__main__":
    target = "https://gitbook.cn/"
    response = requests.get(url=target)

    # 响应文本
    html = response.text
    print(html)

    print("*" * 40)
    # 响应的头信息
    resopnse_head = requests.head(url=target)
    print("type(resopnse_head):{}".format(type(resopnse_head)))
    headers = resopnse_head.headers
    # print(headers)
    for key, value in headers.items():
        print("{}:{}".format(key, value))
