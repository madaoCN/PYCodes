#!/usr/bin/python
#coding=utf8
import os
import re

def renameFunc(filePath, forStr, sufStr):
	print '当前处理文件路径', filePath, forStr, sufStr
	if not os.path.exists(filePath):
		return
	fileName = os.path.basename(filePath).lower()
	extName = os.path.splitext(fileName)[-1]
	dirName = os.path.dirname(filePath)
	targetName = fileName
#	result = re.search('\d+.+\d+.+\d+', fileName)
	
	left = re.search('\d{5}', fileName)
	mid = re.search('[^0-9]+\d+[^0-9]+', fileName)
	right = re.search('[^0-9]+\d+\.', fileName)
	if left and mid and right:
		leftStr = left.group(0)#左侧数字
		midStr = mid.group(0)#中间数字
		rightStr = right.group(0)#右边数字
		targetName.replace(leftStr, forStr)
		
		#获取左侧符号
		leftCharRes = re.search('[^0-9]\d', midStr)
		#获取右侧符号
		rightCharRes = re.search('\d[^0-9]', midStr)
		
		if not leftCharRes and not rightCharRes:
			print "hhhhhhhhh, %s ,格式不太对哦" % fileName
			return
		else:
			leftChar = leftCharRes.group(0).strip('0123456789')
			rightChar = rightCharRes.group(0).strip('0123456789')
			midStr = midStr.strip(leftChar).strip(rightChar)
			rightStr = rightStr.strip('.').strip(rightChar)
			targetName = "%s%s%s%s%s%s" % (forStr, '_', sufStr, '_', rightStr, extName)
			print targetName
			print "原始文件：", filePath
			print "=====>>重命名为", os.path.join(dirName, targetName)
			os.rename(filePath, os.path.join(dirName, targetName))
	else:
		print "hhhhhhhhh, %s ,格式不太对哦" % fileName


	
def reverseDIR(args,dire,files):
	for fileName in files:
		if fileName.endswith('.DS_Store'):
			continue
		if not dire.split('/')[-1].isdigit():
			continue
		numricDIR = int(dire.split('/')[-1])
		stringDIR = None
		if numricDIR < 10:
			renameFunc(os.path.join(dire, fileName), args[0], '0%d' % numricDIR)
		else:
			renameFunc(os.path.join(dire, fileName), args[0], dire.split('/')[-1])


if __name__ == "__main__":
	targetDIR = raw_input("请输出目标文件夹路径：")
	if not os.path.exists(targetDIR):
		print "hhhhhhhhhhh,你输的路径不太对, byebye~"
		exit(0)
	forStr = raw_input("请输入前缀：")
#	sufStr = raw_input("请输入后缀：")

#	targetDIR = '/Users/liangxiansong/Desktop/test'
#	forStr = '11111'
#	sufStr = '999'
	
	os.path.walk(targetDIR, reverseDIR, (forStr,))
	
	
		
	

