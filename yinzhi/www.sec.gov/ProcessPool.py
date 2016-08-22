#coding=utf8
from multiprocessing import Pool,Process
import GetDirFile
import PraseXML

def process(file):
    PraseXML.praseXML(file)

files = GetDirFile.getDirFile('/Users/lixiaorong/Desktop/xmls')

pool = Pool(1)
for file in files:
    print file
    pool.apply_async(process, args=(file,))
pool.close()
pool.join()
