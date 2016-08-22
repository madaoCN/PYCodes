#coding=utf8
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def praseXML(path):
    tree = ET.parse(path)
    root = tree.getroot()
    try:
        txt = tree.find('.//Text').text
        print txt
        #栈
        stack = Stack()
        #变量数组
        vars = []

        for char in txt:
            if stack.empty():
                stack.push(char)
            elif stack.top() == '#':
                stack.push(char)
            elif char != '#' and stack.top() != '#':
                stack.push(char)
            elif char == '#' and stack.top() != '#':
                var = ''
                while stack.top() != '#':
                    var = stack.pop() + var
                vars.append(var)
                print var

        print vars
    except Exception, e:
        print e

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def clear(self):
        del self.items[:]

    def empty(self):
        return self.size() == 0

    def size(self):
        return len(self.items)

    def top(self):
        return self.items[self.size()-1]


if __name__ == "__main__":
    praseXML('/Users/liangxiansong/Desktop/编制记账凭证_收到固定资产捐赠_工业企业.xml')
