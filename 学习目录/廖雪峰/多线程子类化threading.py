#!encoding:utf-8
import Queue
import threading

class parent:
    link = []
    queue = Queue.Queue(0)

    def __init__(self):
        # self.MyThread(self.queue).start()
        pass

    def addLink(self, pid):
        self.queue.put(pid)
        self.MyThread(self.queue).start()

    class MyThread(threading.Thread):
        th_link = []
        th_queue = []

        def __init__(self, queue):
            self.th_queue = queue
            threading.Thread.__init__(self)

        def run(self):
            while True:
                if self.th_queue.qsize() > 0:
                    pid = self.th_queue.get()
                    m = False
                    a = utilQu()
                    while not m:
                        returnType = a.pidStatus(pid=pid)
                        if returnType == "commplate" :
                            print "%s结束了\n"%(pid)
                            break
                        else :
                            print "%s运行中....\n"%(pid)

                else:
                    self.th_queue.join()

import random
class utilQu:
    temp = ["running", "running", "running", "running", "running", "running", "running", "running", "running",
            "commplate"]

    def pidStatus(self, pid):
        num = len(self.temp)
        index = random.randint(0, num - 1)
        # print "utilQu中获取到的下标为:%s,值为%s" % (index, self.temp[index])
        return self.temp[index]


a = parent()
a.addLink("aaaaaaaaa")
a.addLink("bbbbbbbbb")
a.addLink("ccccccccc")
a.addLink("ddddddddd")
a.addLink("eeeeeeeee")
a.addLink("fffffffff")