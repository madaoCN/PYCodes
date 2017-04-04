import gevent
from gevent.event import  Event

evt = Event()


def setter():
    print('A: hey wait for me, i have to do something')
    gevent.sleep(3)
    print('ok, i am done')
    evt.set()


def waiter():
    print('B:i will wait for you')
    evt.wait()
    print('it is about time')


gevent.joinall([
    gevent.spawn(setter),
    gevent.spawn(waiter),

])