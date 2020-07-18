# coding=utf-8
import matplotlib.pyplot as plt
import numpy as np


class MyGraph(object):
    """绘图测试"""

    def __init__(self):
        object.__init__(self)

    def test(self):
        # 开启一个窗口，num设置子图数量，这里如果在add_subplot里写了子图数量，num设置多少就没影响了
        # figsize设置窗口大小，dpi设置分辨率
        fig = plt.figure(num=2, figsize=(20, 8), dpi=80)
        fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')

        # 使用add_subplot在窗口加子图，其本质就是添加坐标系
        # 三个参数分别为：行数，列数，本子图是所有子图中的第几个，最后一个参数设置错了子图可能发生重叠
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)

        # 绘制曲线
        ax1.set_title("Open Google Map")
        ax1.set_xlabel("times")
        ax1.set_ylabel("confidence")
        ax1.plot(np.arange(0, 1, 0.1), range(0, 10, 1), color='g')
        # 同理，在同一个坐标系ax1上绘图，可以在ax1坐标系上画两条曲线，实现跟上一段代码一样的效果
        ax1.plot(np.arange(0, 1, 0.1), range(0, 20, 2), color='b')

        # 在第二个子图上画图
        ax2.set_title("Open Google Map")
        ax2.set_ylabel("scores")
        ax2.plot(np.arange(0, 1, 0.1), range(0, 20, 2), color='r')
        plt.show()
        plt.clf()

    def test2(self):
        fig = plt.figure(figsize=(20, 10), dpi=80)
        ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=1, colspan=1)
        plt.title("XXXX")
        plt.ylabel('H-L')
        plt.plot(np.arange(0, 1, 0.1), range(0, 10, 1), color='g')

        ax2 = plt.subplot2grid((6, 1), (1, 0), rowspan=4, colspan=1, sharex=ax1)
        plt.ylabel('Price')
        plt.plot(np.arange(0, 1, 0.1), range(0, 10, 1), color='g')

        ax3 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
        plt.ylabel('MAvgs')
        plt.plot(np.arange(0, 1, 0.1), range(0, 10, 1), color='g')
        plt.show()
        plt.clf()

    def draw_subgraph(self):
        """绘制子图"""
        data1 = [[0.3765, 0.3765, 0.3765, 0.3765, 0.3765], [0.3765, 0.3765, 0.3765, 0.3765, 0.3765],
                 [0.3765, 0.3765, 0.3765, 0.3765, 0.3765], [0.3765, 0.3765, 0.3765, 0.3765, 0.3765]]
        data2 = [[0.2985, 0.2268, 0.2985, 0.2996, 0.2985], [0.2022, 0.3203, 0.3141, 0.2926, 0.2681],
                 [0.2985, 0.2668, 0.2786, 0.2985, 0.2985], [0.2985, 0.2985, 0.2984, 0.2978, 0.2966]]
        data3 = [[0.7789, 0.7698, 0.6999, 0.7789, 0.7789], [0.7788, 0.7758, 0.7768, 0.7698, 0.8023],
                 [0.7789, 0.7781, 0.7789, 0.7789, 0.7789], [0.7789, 0.7782, 0.7752, 0.7852, 0.7654]]
        data4 = [[0.6688, 0.6688, 0.6688, 0.6981, 0.6618], [0.6688, 0.5644, 0.5769, 0.5858, 0.5882],
                 [0.6688, 0.6688, 0.6688, 0.6688, 0.6646],
                 [0.6688, 0.6646, 0.6646, 0.6688, 0.6746]]  # date1-date4均为我用到的数据，数据的形式等可自行更换。

        ##将4个图画在一张图上
        fig = plt.figure(figsize=(13, 11))
        ax1 = fig.add_subplot(2, 2, 1)  ##左右布局
        ax2 = fig.add_subplot(2, 2, 2)
        ax3 = fig.add_subplot(2, 2, 3)  ##上下布局
        ax4 = fig.add_subplot(2, 2, 4)

        plt.sca(ax1)
        labels = ['Today is Sunday', 'Today is Monday', 'Today is Tuesday', 'Today is Wednesday']  # 标签
        plt.boxplot(data1, labels=labels, boxprops={'linewidth': '2'}, capprops={'linewidth': '2'},
                    whiskerprops={'linewidth': '2'},
                    medianprops={
                        'linewidth': '2'})  # linewidth设置线条的粗细；boxprops、capprops、whiskerprops、medianprops表示盒图中各个线条的类型
        # ax1.set_xticklabels(
        #     ['Today is Sunday', '\n' + 'Today is Monday', 'Today is Tuesday', '\n' + 'Today is Wednesday'], fontsize=16)
        # ax1.set_xticklabels(['Today is Sunday', 'Today is Monday', 'Today is Tuesday', 'Today is Wednesday'],
        #                     fontsize=16, rotation=10)
        plt.ylabel('Today', fontsize=16)
        plt.xlabel('(a)', fontsize=16)

        plt.sca(ax2)
        labels = ['Today is Sunday', 'Today is Monday', 'Today is Tuesday', 'Today is Wednesday']
        plt.boxplot(data2, labels=labels, boxprops={'linewidth': '2'}, capprops={'linewidth': '2'},
                    whiskerprops={'linewidth': '2'}, medianprops={'linewidth': '2'})
        plt.xlabel('(b)', fontsize=16)

        plt.sca(ax3)
        labels = ['Today is Sunday', 'Today is Monday', 'Today is Tuesday', 'Today is Wednesday']
        plt.boxplot(data3, labels=labels, boxprops={'linewidth': '2'}, capprops={'linewidth': '2'},
                    whiskerprops={'linewidth': '2'}, medianprops={'linewidth': '2'})
        plt.ylabel('Today', fontsize=16)
        plt.xlabel('(c)', fontsize=16)

        plt.sca(ax4)
        labels = ['Today is Sunday', 'Today is Monday', 'Today is Tuesday', 'Today is Wednesday']
        plt.boxplot(data4, labels=labels, boxprops={'linewidth': '2'}, capprops={'linewidth': '2'},
                    whiskerprops={'linewidth': '2'}, medianprops={'linewidth': '2'})
        plt.xlabel('(d)', fontsize=16)
        plt.tight_layout()
        plt.show()
        plt.clf()  # 清除画布


if __name__ == "__main__":
    my_graph = MyGraph()
    my_graph.draw_subgraph()
    my_graph.test()
    my_graph.test2()
