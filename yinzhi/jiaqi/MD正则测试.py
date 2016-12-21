#!/usr/bin/python
# coding=utf8
import re
import string


def fliter(sentence):
    delset = u'''\!"#$%&'()\*\+,-./:;<=>?@[\]\^_`{|}~;,。、'''
    sentence = re.sub(u'(?<![%s区省市区县州洲])(?P<name>[省市区县州洲])(?P<suff>[委长])' % delset,
                      '\g<name>\g<name>\g<suff>', sentence)
    return sentence

def dealFliter(sentence):
    delset = '''\!"#$%&'()\*\+,-./:;<=>?@[\]\^_`{|}~;,。、'''
    ST = sentence
    result = re.search(u'[^%s]省委' % delset, ST)
    if result:
        temp = result.group(0).replace('省委', '省省委')
        ST = ST.replace(result.group(0), temp)

    result = re.search(u'[^%s]市委' % delset, ST)
    if result:
        temp = result.group(0).replace('市委', '市市委')
        ST = ST.replace(result.group(0), temp)

    result = re.search(u'[^%s]区委' % delset, ST)
    if result:
        temp = result.group(0).replace('区委', '区区委')
        ST = ST.replace(result.group(0), temp)

    result = re.search(u'[^%s]县委' % delset, ST)
    if result:
        temp = result.group(0).replace('县委', '县县委')
        ST = ST.replace(result.group(0), temp)
    return ST

    result = re.search(u'[^%s]洲委' % delset, ST)
    if result:
        temp = result.group(0).replace('洲委', '洲委')
        ST = ST.replace(result.group(0), temp)

    result = re.search(u'[^%s]州委' % delset, ST)
    if result:
        temp = result.group(0).replace('州委', '州委')
        ST = ST.replace(result.group(0), temp)

    return ST

# print fliter(u'1956年7月至1961年6月任中共广东,县委常委')
# print fliter(u'1956年7月至1961年6月任中共广东区委常委')
# print dealFliter('中共广东,省委')
# print dealFliter('1989年3月任吉林省委常委省委组织部部长（')
#
# print dealFliter('1956年7月至1961年6月任中共广东,县委常委')
# print dealFliter('1956年7月至1961年6月任中共广东市委常委')
# print dealFliter('1956年7月至1961年6月任中共广东区委常委')
# print dealFliter('1956年7月至1961年6月任中共广东州委常委')