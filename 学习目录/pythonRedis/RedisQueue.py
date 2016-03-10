#_*_coding=utf8_*_

import redis
class RedisQueue(object):
    def __init__(self, name, namespace='queue', **redis_kwrags):
        self.__db = redis.Redis(host='192.168.1.105', port=6375, db=0)
        self.key = '%s:%s' %(namespace, name)

    def qsize(self):
        return self.__db.llen(self.key)
    def empty(self):
        return self.qsize() == 0
    def put(self, item):
        self.__db.rpush(self.key, item)
    def get(self, block=True, timeout = None):
        '''If optional args block is true and timeout is None (the default), block
        if necessary until an item is available.'''
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)
        if item:
            item = item[1]
        return item
    def get_nowait(self):
        return self.get(False)