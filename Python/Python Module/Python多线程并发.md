# Python 并发编程---线程篇
---

## Semaphore 信号量
信号量同步基于内部计数器, 每调用一次acquire(), 计数器减1; 每次调用release(), 计数器为0时, acquire()调用被阻塞.
```python
import  time
from random import random
from threading import Thread, Semaphore

sema = Semaphore(3)

def foo(tid):
    with sema:
        print '{} acquire seam'.format(tid)
        wt = random() * 2
        time.sleep(wt)
    print '{} release sema'.format(tid)

threads = []
for i in range(5):
    t = Thread(target=foo, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

```

## Lock(锁)
锁相当于信号量为1
```python
import time
from threading import Thread

value = 0

def getlock():
    global value
    value = value + 1
    time.sleep(0.1)
   

threads = []
for i in range(100):
    t = Thread(target=getlock)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print value # 可能等于16
```

yong锁
```python
import time
from threading import Thread, Lock
lock = Lock()

value = 0

def getlock():
    global value
    with  lock:
        value = value + 1
        time.sleep(0.1)
   

threads = []
for i in range(100):
    t = Thread(target=getlock)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print value # 可能等于16
```

## RLock可重入锁
`acquire()` 能够不被阻塞的被同一线程调用多次. 但是要注意的是 `release() `需要调用与`acquire()`相同的次数才能释放锁.

## Condtion(条件)
一个线程等待特定条件, 而另一个线程发出特定条件满足的信号. 最好说明的例子就是`生产者/消费者`模型
```python
import time
import threading

def consumer(cond):
    t = threading.currentThread()
    with cond:
        cond.wait() # wai() 方法创建了一个名为waiter的锁, 并且设置锁的状态为locked. 这个waiter锁用于线程间的通讯
        print '{}: Resource ius avaiable to consumer'.format(t.name)

def producer(cond):
    t = threading.currentThread()
    with cond:
        print '{}:makring resource'.format(t.name)
        cond.notfiyAll() # 释放waiter锁, 唤醒消费者

condition = threading.Condition()
c1 = threading.Thread(name='c1', target=consumer, args=(condition, ))
c1 = threading.Thread(name='c2', target=consumer, args=(condition, ))
p1 = threading.Thread(name='p1', target=consumer, args=(condition, ))

c1.start()
tim.sleep(1)
c2.start()
time.sleep(1)
p1.start()

#c1.join()
#c2.join()
#p1.join()
```

## Event
一个线程发送/传递时间, 另外的线程等待事件的触发. 我们同样的用[生产者消费者]模型
```python
import  time
import threading
from random import randint

TIMEOUT = 2

def consumer(event, l):
    t = threading.currentThread()
    while l:
        event_is_set = event.wait(TIMEOUT)
        if event_is_set:
            try:
                integer = l.pop()
                print  '{} popped from list by {}'.format(integer, t.name)
                event.clear() # 重置事件状态
            except IndexError:
                pass

def producer(event, l):
    t = threading.currentThread()
    while l:
        integer = randint(10, 100)
        l.append(integer)
        print '{} appended to list by {}'.format(integer, t.name)
        event.set()
        time.sleep(1)


event = threading.Event()
l = []
threads = []

for name in ('consumer1', 'consumer2'):
    t = threading.Thread(name=name, target=consumer, args=(event,l))
    t.start()
    threads.append(t)

p = threading.Thread(name='producer1', target=producer, args=(event, l))
p.start()
threads.append(p)

for t in threads:
    t.join()
```

## Queue
队列再并发开发中最常用的. 我们借助"生产者消费者"模式来理解L
注意四个方法:
1. put: 相对列添加一个消息
2. get: 从队列中删除并返回一个消息
3. task_done: 当某项任务完成时调用
4. join:阻塞直到所有项目都被处理完成.

```python
import time
import threading
from random import random
from Queue import Queue

q = Queue()

def double(n):
    return n * 2

def producer():
    while l:
        wt = random()
        time.sleep(wt)
        q.put((double, wt))

def consumer():
    while 1:
        task, args = q.get()
        print args, task(args)
        q.task_done()

for target in (producer, consumer):
    t = threading.Thread(target=target)
    t.start()

```

Queue 模块还带了 `PriorityQueue`(带有优先级)和 LifoQueue的2中特殊队列. 我们这里展示下线程安全的优先级队列的用法.

PriorityQueue 要求我们put的数据的格式是: `(poriorty_number, data)`

```python

import time
import threading
from random import randint
from Queue import PriorityQueue

q = PriorityQueue()

def double(n):
    return n * 2

def producer():
    count = 0 
    while 1:
        if count > 5:
            break
        pri = randint(0, 200)
        print 'put: {}'.format(pri)
        q.put((pri, dulble, pri)) # (priority, func, args)
        count += 1

def consumer():
    while 1:
        if q.empty():
            break
        pri, task, arg = q.get()
        print '[PRI:{}] {} * 2'.format(pri, arg, task(arg))
        q.task_done()
        time.sleep(0.1)

t = threading.Thread(target=producer)
t.start()

t = threading.Thread(target=consumer)
t.start()
```

## 线程池
面向对象开发中,创建和销毁对象很耗费时间,因为创建一个对象要获取内存资源或者其他更多的资源.无节制的创建和销毁线程是一种极大的浪费. 我们可以使用完成任务而不销毁重复利用.
如`from multiprocessing.pool import ThreadPool`

```
from multiprocessing.pool import ThreadPool

pool = ThreadPool()
pool.map(io_heavy_work, data_in_shared_memory)
```

### 自定义实现一
```python
import  time
import  threading
from random import random
from Queue import Queue

def double(m):
    return m * 2

class Worker(threading.Thread):
    def __init__(self, queue):
        super(Woker, self).__init__()
        self._q = queue
        self.daemon = True
        self.start()

    def run(self):
        while 1:
            f, args, kwargs = self._q.get()
            try:
                print 'USE: {}'.format(self.name)
                print f(*args, **kwargs)
            except Exception as e:
                print e
            self._q.task_done()


class ThreadPool(object):
    def __init__(self, num_t = 5):
        self._q = Queue(num_t)
        for _ in range(num_t):
            Woker(self._q)

    def add_task(self, f, *args, **kwargs):
        self._q.put((f, args, kwargs))

    def wait_complete(self):
        self._q.join()

pool = ThreadPool()
for _ in range(8):
    wt = random()
    pool.add_task(double, wt)
    time.sleep(wt)

pool.wait_complete()


```
