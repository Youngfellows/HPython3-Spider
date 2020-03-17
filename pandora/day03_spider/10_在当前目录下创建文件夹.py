# coding=utf-8
import os
import time


class CreatePath:
    path = os.getcwd()
    path = path + "\\"

    print("cur_path = {}".format(path))

    # 写在这里是为了直观一点方便修改目录
    # windows
    # path = 'E:\\TempCode\\PythonCode\\PythonStudy\\study\day05\\'

    # linux
    # path='/root/dalu/'
    def mkdir(self):
        files = 'report_' + time.strftime('%Y-%m-%d', time.localtime(time.time()))
        path = self.path + files
        isExists = os.path.exists(path)
        print(path)
        print("isExists = {}".format(isExists))
        if not isExists:
            os.makedirs(path)
            print('创建成功:{}'.format(path))
        else:
            print(path + ' 目录已存在')
        return path


if __name__ == "__main__":
    create = CreatePath()
    create.mkdir()
