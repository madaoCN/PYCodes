# coding=utf8
import os
import lxml
from bs4 import BeautifulSoup
import codecs
from multiprocessing import Pool, Process
# from bs4 import BeautifulSoup
import re


def main(path):
    '''
    函数入口
    :return:
    '''
    print 'start processing ... '
    print 'and path is:', path

    fileRead = open(path, 'rb')
    content = fileRead.read()
    fileRead.close()
    # html = re.search('<html([\s\S]*)+</html>', content)
    html = re.search('<html[\s\S]+</html>', content)
    del content
    if html:
        print 'hey man,I got it!!!!!!!'
        with codecs.open(path, 'wb+') as tragetFile:
            tragetFile.write(html.group(0))
        tragetFile.close()
    else:
        print 'sorry, cant find what you want...'


    #soup
    # try:
    #     with codecs.open(path, 'rb', encoding='utf8') as fileRead:
    #         content = fileRead.read()
    #         soup = BeautifulSoup(content, 'lxml')
    #         soupContent = soup.html
    #     fileRead.close()
    # except Exception, e:
    #     print e
    #
    # if soupContent:
    #     try:
    #         with codecs.open(path, 'w+', encoding='utf8') as tragetFile:
    #             tragetFile.write(soupContent.prettify())
    #             print 'writing....'
    #     except Exception as e:
    #         print e
    #         raise e
    #     tragetFile.close()


if __name__ == '__main__':
    DIR = os.path.join(os.path.expanduser('~'),'Desktop', 'test02')

    # pool = Pool(1)
    def func(args, dire, files):
        for file in files:
            if file.endswith('.html'):
                # pool.apply_async(main, args=(os.path.join(dire, file),))
                main(os.path.join(dire, file))
    os.path.walk(DIR, func, ())
    # pool.close()
    # pool.join()
    print 'processed....'











