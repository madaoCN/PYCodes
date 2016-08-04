#!/usr/bin/env python
# -*- coding:utf-8 -*-
import threading
import time
import Queue
SHARE_Q = Queue.Queue()  #构造一个不限制大小的的队列
_WORKER_THREAD_NUM = 3  #设置线程的个数

class MyThread(threading.Thread) :
    """
    doc of class
    Attributess:
        func: 线程函数逻辑
    """
    def __init__(self, func) :
        super(MyThread, self).__init__()  #调用父类的构造函数
        self.func = func  #传入线程函数逻辑
    def run(self) :
        """
        重写基类的run方法
        """
        self.func()
def do_something(item) :
    """
    运行逻辑, 比如抓站
    """
    print item
def worker() :
    """
    主要用来写工作逻辑, 只要队列不空持续处理
    队列为空时, 检查队列, 由于Queue中已经包含了wait,
    notify和锁, 所以不需要在取任务或者放任务的时候加锁解锁
    """
    global SHARE_Q
    while True :
        if not SHARE_Q.empty():
            item = SHARE_Q.get() #获得任务
            do_something(item)
            time.sleep(1)
            SHARE_Q.task_done()
def main() :
    global SHARE_Q
    threads = []
    #向队列中放入任务, 真正使用时, 应该设置为可持续的放入任务
    for task in xrange(5) :
        SHARE_Q.put(task)
    #开启_WORKER_THREAD_NUM个线程
    for i in xrange(_WORKER_THREAD_NUM) :
        thread = MyThread(worker)
        thread.start()  #线程开始处理任务
        threads.append(thread)
    for thread in threads :
        thread.join()
    #等待所有任务完成
    SHARE_Q.join()
if __name__ == '__main__':
    main()