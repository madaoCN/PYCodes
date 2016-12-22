#coding= utf8

import codecs
import os
import re
from multiprocessing import Pool

def replaceItem(content):
    print re.findall('.{1}[\d{1,4}]{1,4}.{1}', content)
    return re.findall('.{1}[\d{1,4}]{1,4}.{1}', content)

def doSomething(dirPath, filePath):

    if filePath.endswith(".txt"):
        print os.path.join(dirPath, filePath)
        with codecs.open(os.path.join(dirPath, filePath), 'r', 'utf8') as resultFile:
            content = resultFile.read()
            list = replaceItem(content)
            with codecs.open(os.path.join(dirPath, '../','target.txt'), 'a', 'utf8') as modifyFile:
                for item in list:
                    modifyFile.write(item)
                    # modifyFile.write('\s\s\s\s' + filePath)
                    modifyFile.write('\n')
if __name__ == "__main__":

    # resultPath = os.path.join(os.path.expanduser("~"), "Desktop", 'sentences', 'result.txt')
    # dirPath = os.path.join(os.path.expanduser("~"), "Desktop", 'sentences')
    #
    # # resultPath = os.path.join(os.path.expanduser("~"), "Desktop", 'test', 'result.txt')
    # # dirPath = os.path.join(os.path.expanduser("~"), "Desktop", 'test')
    #
    # doSomething(resultPath, dirPath)

    pool = Pool(5)
    def funx(args, dire, files):
        for file in files:
            if file.endswith('.txt'):
                pool.apply_async(doSomething, (dire, file))
                # main(dire, file)


    os.path.walk('/Users/liangxiansong/Desktop/sentences', funx, ())
    pool.close()
    pool.join()