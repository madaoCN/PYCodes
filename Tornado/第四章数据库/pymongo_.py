#coding=utf8
import pymongo
from pymongo import MongoClient
import pprint


conn = MongoClient()
db = conn['bookstore']

resule = db.test.find()
for doc in  resule:
    del resule["_id"]
import json
print json.dumps(resule)

# db.books.insert({
#     "title":"Programming Collective Intelligence",
#    "subtitle": "Building Smart Web 2.0 Applications",
#     "image":"/static/images/collective_intelligence.gif",
#     "author": "Toby Segaran",
#     "date_added":1310248056,
#    "date_released": "August 2007",
#    "isbn":"978-0-596-52932-1",
#   "description":"<p>[...]</p>"
# })
# db.books.insert({
#   "title":"RESTful Web Services",
#   "subtitle": "Web services for the real world",
#   "image":"/static/images/restful_web_services.gif",
#     "author": "Leonard Richardson, Sam Ruby",
#   "date_released": "May 2007",
#     "isbn":"978-0-596-52926-0",
#     "description":"<p>[...]>/p>"
# })

# conn = pymongo.Connection("localhost", 27017)
# conn = pymongo.Connection( "mongodb://user:password@staff.mongohq.com:10066/your_mongohq_db")db
# # 创建数据库
# db = conn.example
# # 创建表
# widgets = db.widgets
# widgets.insert({"foo": "bar"})
# # 输出所有表
# print db.collection_names()

# # 插入数据
# widgets.insert({"name": "flibnip", "description": "grade-A industrial flibnip", "quantity": 3})

# 查找数据
# print widgets.find_one({"name": "flibnip"})

# words = db.words
# words.insert({"definition": "Bother, unsettle, modify", "word": "perturb"})
# # 迭代获取数据
# for doc in widgets.find():
#     print doc