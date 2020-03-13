"""
python 删除字符串多余空格及删除多余的空格与空行
"""


# 通过字符串的 replace
def methon1():
    test = 'I love python'
    print(test.replace(' ', ''))


# 通过字符串的 replace
def methon2():
    test = 'I love Java'
    test = test.split(' ')  # 这里变成了 list ['I','love','python']
    test = ''.join(test)  # list 拼接成 str,'Ilovepython'
    print(test)


# 使用 python 的正则表达式 re
def methon3():
    import re
    test = 'I love Android'
    pattenr = re.compile(' ')
    test = pattenr.sub('', test)
    print(test)


# 删除文字中多余的空格和空行
def methon4():
    import re
    test = """第一章 他叫白小纯
帽儿山，位于东林山脉中，山下有一个村子，民风淳朴，以耕田为生，与世隔绝。

清晨，村庄的大门前，整个村子里的乡亲，正为一个十五六岁少年送别，这少年瘦弱，但却白白净净，看起来很是乖巧，衣着尽管是寻常的青衫，可却洗的泛白，穿在这少年的身上，与他目中的纯净搭配在一起，透出一股子灵动。

他叫白小纯。

“父老乡亲们，我要去修仙了，可我舍不得你们啊。”少年满脸不舍，原本就乖巧的样子，此刻看起来更为纯朴。

四周的乡亲，面面相觑，顿时摆出难舍之色。

“小纯，你爹娘走的早，你是个……好孩子！！难道你不想长生了么，成为仙人就可以长生，能活的很久很久，走吧，雏鹰长大，总有飞出去的那一天。”人群内走出一个头发花白的老者，说道好孩子三个字时，他顿了一下。

“在外面遇到任何事情，都要坚持下去，走出村子，就不要回来，因为你的路在前方！”老人神色慈祥，拍了拍少年的肩膀。

“长生……”白小纯身体一震，目中慢慢坚定起来，在老者以及四周乡亲鼓励的目光下，他重重的点了点头，深深的看了一眼四周的乡亲，转身迈着大步，渐渐走出了村子。

眼看少年的身影远去，村中的众人，一个个都激动起来，目中的难舍刹那就被喜悦代替，那之前满脸慈祥的老者，此刻也在颤抖，眼中流下泪水。"""
    print(test)
    test = re.sub('[\n]+', '\n', test)
    print("*" * 50)
    print(test)


if __name__ == "__main__":
    methon1()
    methon2()
    methon3()
    methon4()
