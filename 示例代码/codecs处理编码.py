#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Function:
【教程】用Python的codecs处理各种字符编码的字符串和文件
http://www.crifan.com/tutorial_python_codecs_process_file_char_encoding

Author:     Crifan Li
Version:    2013-10-20
Contact:    http://www.crifan.com/about/me
"""

import codecs;

def python_codecs_demo():
    """demo how to use codecs to handle file with specific encoding"""
    testStrUnicode = u"中文测试Unicode字符串";
    print "testStrUnicode=",testStrUnicode
    testStrUtf8 = testStrUnicode.encode("UTF-8");
    testStrGbk = testStrUnicode.encode("GBK");

    outputFilename = "outputFile.txt"

    # print "------------ 1.UTF-8 write and read ------------"
    # print "--- (1) write UTF-8 string into file ---"
    # # 'a+': read,write,append
    # # 'w' : clear before, then write
    # outputFp = codecs.open(outputFilename, 'w');
    # outputFp.write(testStrUtf8);
    # outputFp.flush();
    # outputFp.close();
    # print "--- (2) read out previously written UTF-8 content ---"
    # readoutFp = codecs.open(outputFilename, 'r', 'UTF-8');
    # #here already is unicode, for we have pass "UTF-8" to codecs.open
    # readOutStrUnicodeFromUtf8 = readoutFp.read()
    # readoutFp.close();
    # print "readOutStrUnicodeFromUtf8=",readOutStrUnicodeFromUtf8

    print "------------ 2.GBK write and read ------------"
    print "--- (1) write GBK string into file ---"
    # 'a+': read,write,append
    # 'w' : clear before, then write
    outputFp = codecs.open(outputFilename, 'w');
    outputFp.write(testStrGbk);
    outputFp.flush();
    outputFp.close();
    print "--- (2) read out previously written GBK content ---"
    readoutFp = codecs.open(outputFilename, 'r', 'GBK');
    #here already is unicode, for we have pass "GBK" to codecs.open
    readOutStrUnicodeFromGbk = readoutFp.read()
    readoutFp.close();
    print "readOutStrUnicodeFromGbk=",readOutStrUnicodeFromGbk

    print "Note: "
    print "1. more about encoding, please refer:"
    print u"【详解】python中的文件操作模式"
    print u"http://www.crifan.com/summary_python_file_operation_mode/"

if __name__ == "__main__":
    python_codecs_demo()