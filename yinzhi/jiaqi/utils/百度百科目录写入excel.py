#coding=utf8
import re
import os
import codecs
from xlwt import Workbook
from xlwt import Worksheet


if __name__ == "__main__":
    # content = get_html()
    filePath = 'folder.txt'
    book = Workbook()
    sheet = book.add_sheet('sheets0', cell_overwrite_ok=True)
    row = 0
    with codecs.open(filePath, 'r', 'utf8') as file:
        for line in file.readlines():
            line = line.strip('./\n.html')
            list = line.split('/')
            lastItem = list.pop()
            list.extend(lastItem.split('_')[-1: -3: -1])
            sheet.write(row, 3, list[-2])
            sheet.write(row, 4, list[-1])
            sheet.write(row, 0, list[0])
            if len(list) == 4:
                sheet.write(row, 1, list[1])
            elif len(list) == 3:
                pass
            # for idx in range(len(list)):
            #     sheet.write(row, idx, list[idx])
            row = row + 1
    book.save('guanyuan.xls')
