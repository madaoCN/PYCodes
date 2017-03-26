#coding=utf8
import re
import os
import codecs
from xlwt import Workbook
from xlwt import Worksheet
compiler = re.compile('(?<=charset=)(.+?)(?=>)')


def funx(args, dire, files):
    for file in files:
        if file.endswith('.html'):  # 获取要删除的文件名
            filePath = os.path.join(dire, file)
            # print filePath
            with codecs.open(filePath, 'r', 'utf8') as file:
                content = file.read()
                content = compiler.subn('UTF8" />', content)
                if content[-1] == 0:
                    print '未找到'
                    print filePath
                    # file.write(content)
                with codecs.open(filePath, 'w', 'utf8') as file:
                    file.write(content[0])

if __name__ == "__main__":
    filePath = os.path.join(os.path.expanduser('~'), 'Desktop', u'bills-data')
    os.path.walk(filePath, funx, ())





