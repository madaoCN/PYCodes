#coding=utf8
import codecs
import os
import json
from bs4 import BeautifulSoup
import bs4

def read(filePath):
    with codecs.open(filePath) as f:
        jsonData = json.load(f)
        return jsonData["RECORDS"]

def getLayer(jsonArr):


    with codecs.open(os.path.expanduser('~') + '/Desktop/result.txt', 'w') as file:
        for json in jsonArr:
            fId = json["f_id"]
            print fId
            html = json["f_html_text"]
            soup = BeautifulSoup(html, "lxml")
            file.write(fId + '|')
            try:
                for child in soup.body.descendants:
                    if isinstance(child, bs4.element.NavigableString):
                        continue
                    print child.name, child.attrs

                    content = child.name + '##' + str(child.attrs)
                    file.write(content.strip() + '|')
                    # if child.name == 'table' or child.name == 'input' or child.name == 'textarea':
                    if child.name == 'table':
                        break
                print '=============='
                file.write('\n')
            except Exception, e:
                print e








if __name__ == "__main__":
    desktopPath = os.path.join(os.path.expanduser('~'), 'Desktop')
    jsonArr = read(desktopPath + "/onlineclass_bill_form.json")
    getLayer(jsonArr)