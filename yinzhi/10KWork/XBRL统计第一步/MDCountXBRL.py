#coding=utf8
import codecs
from lxml import etree
import os
from os.path import getsize
import xlwt
import MDCompressFile
try:
	from cStringIO import StringIO
except:
	from StringIO import StringIO

def createExcel(list):
	book = xlwt.Workbook(encoding = 'utf-8',style_compression = 0)
	sheet = book.add_sheet('path',cell_overwrite_ok = True)

	sepIndex = 0
	excelNum = 0
	for index in range(len(list)):
		if sepIndex > 60000:
			book.save("resultcount_%s.xls" % excelNum)
			del book
			del sheet
			sepIndex = 0
			excelNum += 1
			book = xlwt.Workbook(encoding='utf-8', style_compression=0)
			sheet = book.add_sheet('path', cell_overwrite_ok=True)
		sheet.write(sepIndex,0,list[index].pop("aacceptanceDateTime",' '))
		sheet.write(sepIndex,1,list[index].pop("cik",' '))
		sheet.write(sepIndex, 2, list[index].pop("originSize", ' '))
		sheet.write(sepIndex, 3, list[index].pop("baseSize", ' '))
		sheet.write(sepIndex, 4, list[index].pop("extSize", ' '))
		sheet.write(sepIndex, 5, list[index].pop("count", ' '))
		sheet.write(sepIndex, 6, list[index].pop("tag_count", ' '))
		sheet.write(sepIndex, 7, list[index].pop("base_count", ' '))
		sheet.write(sepIndex, 8, list[index].pop("base_tag_count", ' '))
		sheet.write(sepIndex, 9, list[index].pop("ext_count", ' '))
		sheet.write(sepIndex, 10, list[index].pop("ext_tag_count", ' '))
		sepIndex += 1
	book.save("resultcount_%s.xls" % excelNum)

def read_xml(in_path):
#	f = codecs.open(in_path,"r", )
#	content = f.read()
#	f.flush()
#	f.close()
	content = MDCompressFile.uncompress_file(in_path)
	tree = etree.parse(StringIO(content), parser=etree.XMLParser(huge_tree=True))
	return tree

def countItem(path):

	print path
	tree = read_xml(path)
	inputs = tree.getroot().xpath("//*")

	# print  inputs
	news_tags = []

	for input in inputs:
		if input.tag not in news_tags:
			news_tags.append(input.tag)
	del tree
	result = []
	result.append(str(len(inputs)))
	result.append(str(len(news_tags)))

	return  result

def dealFile(path):
	dict = {}
	if not os.path.exists(path):
		return None
		
	for root, dire, files in os.walk(path):
		for file in files :
			if file.startswith(".DS_Store"):
				pass

			elif file.endswith("_base.xml"):

				list = countItem(path + "/"+file)
				try:
					dict.update({'baseSize':getsize(path + "/"+ file)})
				except Exception, e:
					dict.update({'baseSize': '0'})
				dict.update({"base_count": list[0]})
				dict.update({"base_tag_count": list[1]})

			elif file.endswith("_ext.xml"):
				list = countItem(path + "/"+file)
				try:
					dict.update({'extSize':getsize(path + "/"+ file)})
				except Exception, e:
					dict.update({'extSize':'0'})
				dict.update({"ext_count": list[0]})
				dict.update({"ext_tag_count": list[1]})
			else:
				sp = root.split('#')
				dict.update({"aacceptanceDateTime": sp[0].strip('./')})
				dict.update({'cik':sp[-1]})
				try:
					dict.update({'originSize':getsize(path + "/"+ file)})
				except Exception, e:
					dict.update({'originSize':'0'})
				list = countItem(path + "/"+ file)
				dict.update({"count": list[0]})
				dict.update({"tag_count": list[1]})
				# print dict

	return  dict

if __name__ == "__main__":

	# find. - type d >> folder.txt
	file = open("folder.txt")
	list = []
	while 1:
		line = file.readline()
		if not line:
			break
		else:
			try:
			   	item =  dealFile(line[:-1])
			   	if item != None:
					list.append(item)
			   # print dealFile(line[:-1])
			except Exception, e:
				print 'error..', e
				pass
		# print list
	file.close()
	createExcel(list)