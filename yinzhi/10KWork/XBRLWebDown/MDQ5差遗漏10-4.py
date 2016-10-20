#coding=utf8
#!/usr/bin/python
import codecs
import os

if __name__ == "__main__":
	DIC = {}
	desktopPath = os.path.join(os.path.expanduser('~'), 'Desktop')
#	with codecs.open(os.path.join(desktopPath, 'q5.txt'), 'r') as q5File:
#		for line in q5File.readlines():
##			print line.strip()
#			DIC.update({line.strip():[]}) 

	with codecs.open(os.path.join(desktopPath, 'all.txt'), 'r') as resultFile:
		for line in resultFile.readlines():
			lt = line.strip().split('#')
			cik = lt[-1]
			year = lt[0][2:6]
			if DIC.has_key(cik):
				DIC[cik].append(year)
			else:
				DIC[cik] = [year]
				
	for key in DIC.keys():
		DIC[key].sort()
	
	resultDIC = {}
	for key in DIC.keys():
		arr = DIC[key]
		unTrackedYearArr = []
		
		anchor = arr[0]
		for idx in range(int(anchor), 2017):
			unTrackedYearArr.append(unicode(idx))
		for item in arr:
			if item in unTrackedYearArr:
				unTrackedYearArr.remove(item)
		resultDIC.update({key:unTrackedYearArr})
	
	with codecs.open(os.path.join(desktopPath, 'target.txt'), 'a') as targetFile:
		for key in resultDIC.keys():
			print key
			map(lambda year:targetFile.write(key+'#'+year+'\n') , resultDIC[key])
			 