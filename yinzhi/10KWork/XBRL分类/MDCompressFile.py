#!/usr/bin/env python
#coding=utf8
import gzip
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO


def gzip_compress(raw_data):
    buf = StringIO()
    f = gzip.GzipFile(mode='wb', fileobj=buf, compresslevel=9)
    try:
        f.write(raw_data)
    finally:
        f.close()
    return buf.getvalue()

def gzip_uncompress(c_data):
    buf = StringIO(c_data)
    f = gzip.GzipFile(mode = 'rb', fileobj = buf)
    try:
        r_data = f.read()
    finally:
        f.close()
    return r_data

def uncompress_file(file_in):
    f_n = gzip.open(file_in, 'rb')
    file_content = f_n.read()
    f_n.flush()
    f_n.close()
    return file_content

# def compress_file(fn_in, fn_out):
#     f_in = open(fn_in, 'rb')
#     f_out = gzip.open(fn_out, 'wb')
#     f_out.writelines(f_in)
#     f_out.close()
#     f_in.close()
#
#
# def uncompress_file(fn_in, fn_out):
#     f_in = gzip.open(fn_in, 'rb')
#     f_out = open(fn_out, 'wb')
#     file_content = f_in.read()
#     f_out.write(file_content)
#     f_out.close()
#     f_in.close()

if __name__ == "__main__":
    print uncompress_file(r'/Users/liangxiansong/Desktop/XBRLTestData/20121217172421#0001368637/bbls-20120930_ext.xml')



