# coding=utf-8
import re

str = "共12页: "
pattern = re.compile(r"(\d+)")
result = pattern.search(str)
print(result)
print(result.group(0))
print(result.groups())

# 首图url:
url = "https://www.tupianzj.com/meinv/20191115/198736.html"
index = url.rfind(".html")
print("index = {}".format(index))
pre_url = url[0:index]
print(pre_url)
