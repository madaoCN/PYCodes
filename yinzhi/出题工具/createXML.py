#!/usr/bin/env python
#coding=utf8
import xml.dom.minidom as Dom

# FILE = '/Users/lixiaorong/Desktop/'

def initalXML(formData, xmlData, moreTag):
    doc = Dom.Document()
    #生成根节点
    root_node = doc.createElement('TQuestion')
    doc.appendChild(root_node)
    #生成title和variables节点
    title = doc.createElement('Title')
    variables = doc.createElement('Variables')
    entry = doc.createElement('Entry')

    # entry属性
    entry.setAttribute("entryTime", 'yewushijian')
    entry.setAttribute("name", 'yewuming')
    entry.setAttribute("type", 'readonly')

    root_node.appendChild(title)
    root_node.appendChild(variables)
    title.appendChild(entry)

    #form节点
    length = len(formData)
    for form in formData:
        f = doc.createElement('form')
        f.setAttribute('formID', form)
        f.setAttribute('name', formData[form])
        f.setAttribute('order',form.replace('T', ''))
        if form == 'T1':
            f.setAttribute('type', '1')
        elif form == 'T'+str(length):
            f.setAttribute('type', '3')
        else:
            f.setAttribute('type', '2')
        entry.appendChild(f)

    #c节点
    for xml in xmlData:
        c = doc.createElement('C')
        if xmlData[xml] == '##':
            c.setAttribute('expr', 'null')
        else:
            c.setAttribute('expr', 'equalTo(%s)' % xmlData[xml])
        c.setAttribute('type', 'T')
        c.setAttribute('name', xml)

        variables.appendChild(c)
    #T1节点
    for xml in moreTag:
        name = xml.getAttribute('name')
        xml.setAttribute('name', 'T1_'+name)
        variables.appendChild(xml)

    return doc

def writeXML(path, xml):
    '''创建xml'''
    currentDirName = path.split('/')[-1]
    print '当前目录名称',currentDirName
    print path
    try:
        file = open(path+'/%s.xml' % (currentDirName), mode='w')
        file.write(xml.toprettyxml(indent = "\t", newl = "\n", encoding = "utf-8"))
        file.close()
        print '文件目录', path + '/%s.xml' % (currentDirName)
        print '生成xml成功。。'

    except Exception, e:
        print e
