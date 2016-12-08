# -*- coding:utf-8 -*-
# @Date    : 2016-07-13 14:47:56
# @Function: 把Excel表单转化为json文件
# @Author  : JennyZhang

import xlrd
import json
import codecs
import os


# 把excel表格中指定sheet转为json
def Excel2Json(file_path):
    # 打开excel文件
    if get_data(file_path) is not None:
        book = get_data(file_path)
        # 抓取所有sheet页的名称
        worksheets = book.sheet_names()
        print "该Excel包含的表单列表为：\n"
        for sheet in worksheets:
            print ('%s,%s' % (worksheets.index(sheet), sheet))
        inp = raw_input(u'请输入表单名对应的编号，对应表单将自动转为json:\n')
        sheet = book.sheet_by_index(int(inp))
        row_0 = sheet.row(0)  # 第一行是表单标题
        nrows = sheet.nrows  # 行号
        ncols = sheet.ncols  # 列号

        result = {}  # 定义json对象
        result["title"] = file_path  # 表单标题
        result["rows"] = nrows  # 行号
        result["items"] = {}  # 每一行作为数组的一项
        # 遍历所有行，将excel转化为json对象
        for i in range(nrows):
            tmp = {}
            tmpArr = []
            tempKey = None
            # 遍历当前行所有列
            for j in range(ncols):
                if j == 0:#第一列为key
                    tempKey = sheet.row_values(i)[0]
                    continue

                # 获取单元格的值
                cellValue = sheet.row_values(i)[j]
                if cellValue == None or cellValue == "":
                    continue
                tmpArr.append(cellValue)
            # tmp[tempKey] = tmpArr
            result["items"][tempKey] = tmpArr
        json_data = json.dumps(result, indent=4, sort_keys=True).decode('unicode_escape')

        # saveFile(os.getcwd(), worksheets[int(inp)], json_data)
        print json_data


# 获取excel数据源
def get_data(file_path):
    """获取excel数据源"""
    try:
        data = xlrd.open_workbook(file_path)
        return data
    except Exception, e:
        print u'excel表格读取失败：%s' % e
        return None


def saveFile(file_path, file_name, data):
    output = codecs.open(file_path + "/" + file_name + ".txt", 'w', "utf-8")
    output.write(data)
    output.close()


if __name__ == '__main__':
    file_path = raw_input(u'请输入excel文件路径：\n')
    json_data = Excel2Json(file_path)