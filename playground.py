#!/usr/bin/python
#coding=utf-8
import math
import random
from random import randrange
import math as myMath
import types
import logging
import logging.config


# #Python内置的sorted()函数就可以对list进行排序：
# print sorted([5, 3, 6, 2, 1])

# def reversed_cmp(x, y):
#     if x > y:
#         return -1
#     if x < y:
#         return 1
#     return 0
# print sorted([36, 5, 12, 9, 21], reversed_cmp)
#
# print sorted([36, 5, 12, 9, 21], lambda x, y : -1 if x > y else 1)





class Animal(object):
    def run(self):
        print 'Animal is running...'

class Dog(Animal):
    def run(self):
        print 'Dog is running...'
 

class Cat(Animal):
    def run(self):
        super(Cat, self).run()
        print 'And it is a cat!'

dog = Dog()
cat = Cat()
dog.run()
cat.run()


a = list() # a是list类型
b = Animal() # b是Animal类型
c = Dog() # c是Dog类型

print isinstance(c, Dog)
print isinstance(b, Animal)
print isinstance(c, Dog)
print isinstance(c, Animal)








