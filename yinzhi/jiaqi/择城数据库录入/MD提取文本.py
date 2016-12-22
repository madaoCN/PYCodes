# coding=utf8
import os
import codecs
from bs4 import BeautifulSoup
import re
from multiprocessing import Pool

def getFileContent(filePath):
    '''
    遍历文件
    :param filePath: 文件路径
    :return: 句子列表
    '''
    with codecs.open(filePath, 'r', 'utf8') as file:
        return file.read()

    return None

def praseHTML(dire, fileName):
    # currentDIR = os.path.dirname(filePath)
    filePath = os.path.join(dire, fileName)
    resultDIR = os.path.join(os.path.expanduser('~'), 'Desktop','result/')
    # if not os.path.exists(resultDIR):
    #     os.makedirs(resultDIR)
    resultFile = codecs.open(os.path.join(resultDIR, fileName.replace('html', 'txt')),'w+', 'utf8')
    print os.path.join(resultDIR, fileName.replace('html', 'txt'))
    with codecs.open(filePath, encoding='utf8') as file:
        soup = BeautifulSoup(file, 'lxml')
        content = soup.find_all('div', {'class': 'para'})
        for div in content:
            divText = div.text.strip()
            spliteEnd = re.split(u'。|;|；', divText)
            for end in spliteEnd:
                # end = end.strip(u' {}[],.（）()\n\s\t\b ')
                end = "".join(end.split())
                if end != '' and end != ' ' and len(end) > 4:
                    resultFile.write(end + '\n')
    resultFile.close()


def main(dire, file):
    try:
        # contetnt = getFileContent(os.path.join(dire, file))
        praseHTML(dire, file)
    except Exception, e:
        print '**********' + file + '**********'
        print e


if __name__ == "__main__":

    pool = Pool(5)
    def funx(args, dire ,files):
        for file in files:
            if file.endswith('.html'):
                pool.apply_async(main, (dire, file))
                # main(dire, file)
    os.path.walk('/Users/liangxiansong/Desktop/baike', funx, ())
    pool.close()
    pool.join()