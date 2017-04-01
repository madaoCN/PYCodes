import gevent
from gevent.queue import Queue, Empty


tasks = Queue(maxsize=3)

def worker(n):
    try:
        while True:
            task = tasks.get(timeout=1)
            print("work {} got task {}".format(n, task))
            gevent.sleep(0)
    except Empty:
        print('Quitting')

def boss():
    for i in range(1, 10):
        tasks.put(i)
    print('Assigned all work in iteration 1')

    for i in range(1, 10):
        tasks.put(i)
    print('Assigned all work in iteration 2')


gevent.joinall([
    gevent.spawn(boss),
    gevent.spawn(worker, 'steve'),
    gevent.spawn(worker, 'jack')
])