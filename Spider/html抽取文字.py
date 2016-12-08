#coding=utf-8
import re
import chardet
import codecs
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

##过滤HTML中的标签
# 将HTML中标签等信息去掉
# @param htmlstr HTML字符串.
def filter_tags(htmlstr):
    # 先过滤CDATA
    re_cdata = re.compile('//<!CDATA\[[ >]∗ //\] > ',re.I) #匹配CDATA
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)
    # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)
    # style
    re_br = re.compile('<br\s*?/?>')
    # 处理换行
    re_h = re.compile('</?\w+[^>]*>')
    # HTML标签
    re_comment = re.compile('<!--[^>]*-->')
    # HTML注释
    s = re_cdata.sub('', htmlstr)
    # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)
    # 去掉style
    s = re_br.sub('', s)
    # 将br转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)
    # 去掉HTML注释
    # 去掉多余的空行
    blank_line = re.compile('\n+')
    s = blank_line.sub('', s)
    blank_line_l = re.compile('\n')
    s = blank_line_l.sub('', s)
    blank_kon = re.compile('\t')
    s = blank_kon.sub('', s)
    blank_one = re.compile('\r\n')
    s = blank_one.sub('', s)
    blank_two = re.compile('\r')
    s = blank_two.sub('', s)
    blank_three = re.compile(' ')
    s = blank_three.sub('', s)
    s = replaceCharEntity(s)  # 替换实体
    return s


##替换常用HTML字符实体.
# 使用正常的字符替换HTML中特殊的字符实体.
# 你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
# @param htmlstr HTML字符串.
def replaceCharEntity(htmlstr):
    CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"''"', '34': '"',}

    re_charEntity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charEntity.search(htmlstr)
    while sz:
        entity = sz.group()  # entity全称，如>
        key = sz.group('name')  # 去除&;后entity,如>为gt
        try:
            htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
        except KeyError:
            # 以空串代替
            htmlstr = re_charEntity.sub('', htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
    return htmlstr


def repalce(s, re_exp, repl_string):
    return re_exp.sub(repl_string,s)



if __name__ == '__main__':

    with codecs.open('/Users/liangxiansong/Desktop/test.txt', encoding='utf8') as file:
        contents = file.read()
        contents = filter_tags(contents)
        contents = replaceCharEntity(contents)
        print contents

        fileCopy = codecs.open('/Users/liangxiansong/Desktop/test_1.txt','w+', encoding='utf8')
        fileCopy.write(contents)

