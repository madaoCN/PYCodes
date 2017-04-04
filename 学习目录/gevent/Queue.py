import gevent
from gevent.queue import Queue


tasks = Queue()

def worker(n):
    while not tasks.empty():
        task = tasks.get()
        print("work {} got task {}".format(n , task))
        gevent.sleep(0)

    print('Qutting time!')


def boss():
    for i in range(1, 10):
        tasks.put_nowait(i)

gevent.spawn(boss).join()

gevent.joinall([
    gevent.spawn(worker, 'steve'),
    gevent.spawn(worker, 'jack')
])