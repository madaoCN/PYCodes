import codecs
from lxml import etree
import os
import xlwt

def createExcel(list):
    book = xlwt.Workbook(encoding = 'utf-8',style_compression = 0)
    sheet = book.add_sheet('path',cell_overwrite_ok = True)

    for index in range(len(list)):
	
	dict = list[index]
        name = dict.keys()[0]
        resu = dict.pop(name)
	
	sheet.write(index,0,name)
	for d in resu:
	    for key in d.keys():
		x = key[:-2]
		y = key[len(key) - 1 :]
		sheet.write(index,2 + int(x)*3+int(y),d.pop(key))

    book.save("count_0.xls")


def read_xml(in_path):
    #print in_path
    tree = etree.parse(in_path)
    return tree

def countItem(path):
    for root, dirs, files in os.walk(path):
       for file in  files :
          if file.startswith(".DS_Store"):
                   pass
          elif file.endswith("_base.xml"):
                   pass
          elif file.endswith("_ext.xml"):
                   pass
          else:
           if os.path.exists(path + "/" +file) and file.endswith(".xml"):
             tree = read_xml(path + "/" +file)
             inputs = tree.getroot().xpath("//*")

             news_tags = []

             for input in inputs:
                if input.tag not in news_tags:
                   news_tags.append(input.tag)

             return  set(news_tags)
           else:
	     return None


def classify(dict,path):
    realPath = path[2:]
    year = realPath.split('#')[0][:4]

    company_name = realPath.split('#')[1]

    if not dict.get(company_name) == None:
        dict.get(company_name).append(path)
    else:
        list = []
        list.append(path)
        dict[company_name] = list

def dealFile(key,list):

    result = []
    
    for index in  range(len(list) - 1):
        
        dic = {}
        if int(list[index][2:6]) + 1 == int(list[index + 1][2:6]) :

            key1 = 2016 - int(list[index + 1][2:6])
            
            setA = countItem(list[index + 1])
            setB = countItem(list[index])
            if setA != None and setB != None:

                dic[str(key1)+"_1"] = str(len(setA & setB))
                dic[str(key1) + "_2"] = str(len(setA - setB))
                dic[str(key1) + "_3"] = str(len(setB - setA))
	    else:
		dic[str(key1)+"_1"] = "-"
		dic[str(key1)+"_2"] = "-"
		dic[str(key1)+"_3"] = "-"
            result.append(dic)

    dict = {key: result}
    
    return  dict


if __name__ == "__main__":

    # find. - type d >> folder.txt
    fi = open("folder.txt")

    filePathlist = []
    result = {}
    while 1:
        line = fi.readline()
        if not line:
            break
        else:
            for root, dirs, files in os.walk(line[:-1]):
                for file in  files :
                   if file.endswith(".xml"):
                       filePathlist.append(line[:-1])
                       break
    fi.close()
    for index in range(len(filePathlist)):
        try:
            classify(result, filePathlist[index])
        except Exception,e:
            print filePathlist[index]
	    #print e
#    print  result
    i = 0 
    resultList = []
    print len(result.keys())
    for j in range(0,2500):
    #for k in result.keys():
        k = result.keys()[j]
        l = result.pop(k)
        if len(l) > 1:
           l.sort()
           #print l
           i = i + 1
	   print i
           resultList.append(dealFile(k,l))
        else:
            pass
    #print resultList    
    createExcel(resultList)
