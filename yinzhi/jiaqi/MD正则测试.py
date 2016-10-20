#!/usr/bin/python
# coding=utf8
import re
import string


def dealFliter(sentence):
    delset = '''\!"#$%&'()\*\+,-./:;<=>?@[\]\^_`{|}~;,。、'''
    ST = sentence
    result = re.search('[^%s]省委' % delset, ST)
    if result:
        temp = result.group(0).replace('省委', '省省委')
        ST = ST.replace(result.group(0), temp)

    result = re.search('[^%s]市委' % delset, ST)
    if result:
        temp = result.group(0).replace('市委', '市市委')
        ST = ST.replace(result.group(0), temp)

    result = re.search('[^%s]区委' % delset, ST)
    if result:
        temp = result.group(0).replace('区委', '区区委')
        ST = ST.replace(result.group(0), temp)

    result = re.search('[^%s]县委' % delset, ST)
    if result:
        temp = result.group(0).replace('县委', '县县委')
        ST = ST.replace(result.group(0), temp)
    return ST

    result = re.search('[^%s]洲委' % delset, ST)
    if result:
        temp = result.group(0).replace('洲委', '洲委')
        ST = ST.replace(result.group(0), temp)
    return ST


print dealFliter('中共广东,省委')
print dealFliter('1989年3月任吉林省委常委省委组织部部长（')

print dealFliter('1956年7月至1961年6月任中共广东,县委常委')
print dealFliter('1956年7月至1961年6月任中共广东市委常委')
print dealFliter('1956年7月至1961年6月任中共广东区委常委')