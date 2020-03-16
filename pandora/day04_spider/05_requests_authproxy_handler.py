# coding=utf-8
import requests

if __name__ == "__main__":
    url = "http://www.baidu.com"
    proxies = {'https': '218.249.45.162:35586'}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Connection": "keep-alive",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "BAIDUID=D17B34117C46D60C15B6A9AB4C625F68:FG=1; BIDUPSID=D17B34117C46D60C15B6A9AB4C625F68; PSTM=1576460924; BDUSS=kdLZGw4MFh4ZTIyVDVHRkM4cEN-c25YV09xcmhneUl3LWZTUzN-MDdZT2R4a2RlSVFBQUFBJCQAAAAAAAAAAAEAAACOSosns8K93DIwMTAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJ05IF6dOSBeQ; BD_UPN=12314753; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BD_HOME=1; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; BD_CK_SAM=1; PSINO=6; H_PS_PSSID=30975_1468_21087_30910_30999_30824_31086_26350; H_PS_645EC=f1ddzsxe1mE61NWdPoN5X4vLKD241%2BmMzzx1cug2Gr%2FYq6BvaWqdcsPIQVXmdiHvCDyV; sugstore=1"
    }

    response = requests.post(url, headers=headers, proxies=proxies, verify=False)  # verify是否验证服务器的SSL证书
    response.encoding = "utf-8"
    html = response.text
    print(html)
