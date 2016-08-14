#coding=utf8
import os


def getDirOrFile(dir, isDir = 'yes'):
    '''
    获取目录下html文档路径
    :param dir: 路径
    :return: 文档路径集合
    '''
    fileList = []
    list = os.listdir(dir)
    if len(list) > 0:
        for file in list:
            filePath = os.path.join(dir, file)
            if isDir == 'yes' or isDir == 'YES':
                if  os.path.isdir(filePath):  # 如果是目录
                    fileList.append(filePath)
            elif isDir == 'no' or isDir == 'NO':
                if  os.path.isfile(filePath):  # 如果是文件
                    fileList.append(filePath)

    return fileList

if __name__ == "__main__":
    print getDirOrFile(os.path.join(os.path.expanduser("~"), 'Desktop'), isDir='no')