#coding=utf8
import pymongo
from pymongo import MongoClient
import pprint


conn = MongoClient()
# conn = pymongo.Connection("localhost", 27017)
# conn = pymongo.Connection( "mongodb://user:password@staff.mongohq.com:10066/your_mongohq_db")db
# 创建数据库
db = conn.example
# 创建表
widgets = db.widgets
widgets.insert({"foo": "bar"})
# 输出所有表
print db.collection_names()

# # 插入数据
# widgets.insert({"name": "flibnip", "description": "grade-A industrial flibnip", "quantity": 3})

# 查找数据
# print widgets.find_one({"name": "flibnip"})

words = db.words
words.insert({"definition": "Bother, unsettle, modify", "word": "perturb"})
# 迭代获取数据
for doc in widgets.find():
    print doc