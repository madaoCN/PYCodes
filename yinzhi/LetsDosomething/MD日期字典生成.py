#coding=utf8




if __name__ == '__main__':
    import codecs
    import os
    filePath = os.path.join(os.path.expanduser('~'), 'Desktop', 'timeDic.txt')

    file = codecs.open(filePath, 'a', encoding='utf8')
    for year in range(1900, 2016):
        for month in range(1, 13):
            if month < 10:
                content = unicode(year) + u'.' + '0'+unicode(month)
            else:
                content = unicode(year) + u'.' + unicode(month)
            print content
            try:
                file.write(content)
                file.write('\n')
            except Exception, e:
                print e
            # for day in range(1, 32):
            #     content = unicode(year) + u'年' + unicode(month)+ u'月' + unicode(day) + u'日'
            #     print content
            #     try:
            #         file.write(content)
            #         file.write('\n')
            #     except Exception,e:
            #         print e