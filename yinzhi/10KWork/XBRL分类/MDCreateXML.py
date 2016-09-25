#!/usr/bin/env python
#coding=utf8
import xml.dom.minidom as Dom
import MDCompressFile

# FILE = '/Users/lixiaorong/Desktop/'

def initalXML(nameSpace, tags):
    doc = Dom.Document()


    # 获取当前使用到的tag值
    try:
        # 生成根节点
        root_node = doc.createElement('xbrl')
        for name in nameSpace:
            if name == None:
                root_node.setAttribute('xmlns', nameSpace[None])
            else:
                root_node.setAttribute('xmlns'+':'+name, nameSpace[name])
    except Exception, e:
        print e
        return

    doc.appendChild(root_node)
    #生成实例文档节点
    try:
        for dic in tags:
            #读取tag
            for tag in dic:
                if tag == 'categoryTag':
                    continue
                item = doc.createElement(tag)
                #设置属性和内容
                for secTag in dic[tag]:
                    if secTag == 'CONTENTTEXT':#设置内容
                        try:
                            if dic[tag]['CONTENTTEXT'] == None:
                                content = doc.createTextNode(' ')
                                item.appendChild(content)
                            else:
                                content = doc.createTextNode(dic[tag]['CONTENTTEXT'])
                                item.appendChild(content)
                        except Exception, e:
                            print e
                            print 'initalXML + 29 '
                    else:#设置属性
                        item.setAttribute(secTag, dic[tag][secTag])
                root_node.appendChild(item)
    except Exception, e:
        print e
    return doc

def writeXML(path, xml):
    '''创建xml'''
    currentDirName = path.split('/')[-1]
    print '当前目录名称============='
    print path
    try:
        file = open(path, mode='w')
        file.write(MDCompressFile.gzip_compress(xml.toprettyxml(indent = "\t", newl = "\n", encoding = "utf-8")))
#        file.write(xml.toprettyxml(indent = "\t", newl = "\n", encoding = "utf-8"))
        file.close()
        print '文件目录', path
        print '生成xml成功。。'

    except Exception, e:
        print e


if __name__ == "__main__":
    doc = initalXML({'None':'http://www/baidu.com','iso4217': 'http://www.xbrl.org/2003/iso4217', 'cvx': 'http://xbrl.chevron.com/20081231', 'xlink': 'http://www.w3.org/1999/xlink', 'us-gaap': 'http://xbrl.us/us-gaap/2008-03-31', 'dei': 'http://xbrl.us/dei/2008-03-31', 'link': 'http://www.xbrl.org/2003/linkbase','xbrli': 'http://www.xbrl.org/2003/instance', 'xbrldi': 'http://xbrl.org/2006/xbrldi'}
, [{'gaap:OtherNonoperatingIncome':{'decimals': '-5', 'CONTENTTEXT':'66666666'}}, {'xlink:PaymentsForProceedsFromBusinessesAndInterestInAffiliates':{'decimals': '-6', 'CONTENTTEXT':'66666666'}}])
    writeXML('/Users/lixiaorong/Desktop/test.xml',doc)
