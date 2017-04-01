import gevent
from gevent.event import AsyncResult

a = AsyncResult()


def setter():
    print('A: hey wait for me, i have to do something')
    gevent.sleep(3)
    print('ok, i am done')
    a.set('surprise!')


def waiter():
    print('B:i will wait for you')
    print(a.get())
    print('it is about time')


gevent.joinall([
    gevent.spawn(setter),
    gevent.spawn(waiter),

])