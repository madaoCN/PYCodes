import gevent

from gevent import Timeout
seconds = 6
timeout = Timeout(seconds)
timeout.start()

def wait():
    gevent.sleep(5)
    print('success')


try:
    gevent.spawn(wait).join()
except Timeout:
    print('Could not complete')


############ style 2
import gevent
from gevent import Timeout

time_to_wait = 5 # seconds

class TooLong(Exception):
    pass

with Timeout(time_to_wait, TooLong):
    gevent.sleep(10)


############ style 3
import gevent
from gevent import Timeout
def wait():
    gevent.sleep(2)
timer = Timeout(1).start()

thread1 = gevent.spawn(wait)

try:
    thread1.join(timeout=timer)
except Timeout:
    print('Thread 1 timed out')

timer = Timeout.start_new(1)
thread2 = gevent.spawn(wait)
try:
    thread2.get(timeout=timer)
except Timeout:
    print('Thread 2 timed out')
# --
try:
    gevent.with_timeout(1, wait)
except Timeout:
    print('Thread 3 timed out')