#Python多线程
---
## 介绍

Python多线程的有两个相关模块:thread与threading.
thread的是底层的实现,一般不使用. 通常情况下使用threading模块,
threading模块是对thread的进行高级封装.

##  Global Interpreter Lock
在Python中提到多线程就不得不提到GIL(Global Interpreter Lock),GIL的存在让python的多线程多少有点鸡肋了。Cpython的线程是操作系统原生的线程在解释器解释执行任何Python代码时，都需要先获得这把锁才行，在遇到 I/O 操作时会释放这把锁。因为python的进程做为一个整体，解释器进程内只有一个线程在执行，其它的线程都处于等待状态等着GIL的释放。

在官方文档中提高,如果想写更好性能的程序,可以用多进程模块multiprocessing.

## 线程的介绍
创建线程之后，线程并不是始终保持一个状态。其状态大概如下：

- New 创建。
- Runnable 就绪。等待调度
- Running 运行。
- Blocked 阻塞。阻塞可能在 Wait Locked Sleeping
- Dead 消亡
这些状态之间是可以相互转换的，一图胜千颜色：
![](img/thread_state.jpg)


**线程中执行到阻塞,可能有三种情况**:
> 1. 同步:线程中获取同步锁,但是资源已经被其他线程锁定时, 进入Locked状态,直到该资源可获取(获取的顺序由Lock列控制).
> 2. 睡眠: 线程运行sleep()或者join()方法后,线程进入sleeping状态.区别在于sleep等待固定的时间, 而join()是等待子线程执行完.当然join()可以指定一个超时时间. 从语义讲,如果两个线程a,b,在a调用b.join(),相当于合并(join)成一个线程.最常见情况是主线程中join()的所有子线程.
> 3.等待: 线程中执行wait()方法后, 线程进入wating状态,等待其他线程的通知(notify).

## 线程类型

线程有着不同的状态，也有不同的类型。大致可分为：

1. 主线程
2. 子线程
3. 守护线程（后台线程）
4. 前台线程

## 线程创建
一般是用threading来创建多线程,threading的创建多线程有两种方式:
1. 实例化一个threading.Thread实例.
2. 继承threading.Thread类.

### 实例化一个threading.Thread实例.

```python
from threading import  Thread
import time

def f(name):
    print name

if __name__ == "__main__":
    threadlist = []
    for i in range(5):
        t = Thread(target=f, args=(i,))
        threadlist.append(t)

    for t in threadlist:
        t.start()
    #for t in threadlist:
       #t.join()

```


### 继承threading.Thread类

```python
from threading import  Thread
import time

class MyThread(Thread):
    def run(self):
        for i in range(5):
            print 'thread {0}, @number: {0}'.format(self.name, i)
            time.sleep(1)

def main():
    print "Start main threading"
    threads = [MyThread() for i in range(3)]

    for t in threads:
        t.start()
    print "End Main threading."

if __name__ == '__main__':
    main()

```

```
Start main threading
thread Thread-1, @number: 0
thread Thread-2, @number: 0
End Main threading.
thread Thread-3, @number: 0
thread Thread-1, @number: 1
thread Thread-2, @number: 1
thread Thread-3, @number: 1
thread Thread-1, @number: 2
thread Thread-2, @number: 2
thread Thread-3, @number: 2
thread Thread-1, @number: 3
thread Thread-2, @number: 3
thread Thread-3, @number: 3
thread Thread-1, @number: 4
thread Thread-2, @number: 4
thread Thread-3, @number: 4

```

每个线程都依次打印 0 – 3 三个数字，可是从输出的结果观察，线程并不是顺序的执行，而是三个线程之间相互交替执行。此外，我们的主线程执行结束，将会打印 End Main threading。从输出结果可以知道，主线程结束后，新建的线程还在运行。


## 线程合并（join方法）
上述的例子中, 主线程结束了,子线程还在运行.如果需要主线程等待子线程执行完毕再退出, 可以使用线程join()法官法.
>join(timeout)方法将会等待直到线程结束。这将阻塞正在调用的线程，直到被调用join()方法的线程结束。

主线程或者某个函数如果创建了子线程,只要调用了子线程的join()方法,那么主线程就会被子线程所阻塞,直到子线程执行完毕再轮到主线程执行.其结果就是所有子线程执行完毕,才打印`Eed Main threading`.

```python
def main():
    print "Start main threading"
    threads = [MyThread() for i in range(3)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()
    print "End Main threading."
```

```
Start main threading
thread Thread-1, @number: 0
thread Thread-2, @number: 0
thread Thread-3, @number: 0
thread Thread-1, @number: 1
thread Thread-2, @number: 1
thread Thread-3, @number: 1
thread Thread-1, @number: 2
thread Thread-2, @number: 2
thread Thread-3, @number: 2
thread Thread-1, @number: 3
thread Thread-2, @number: 3
thread Thread-3, @number: 3
thread Thread-1, @number: 4
thread Thread-2, @number: 4
thread Thread-3, @number: 4
End Main threading.

```
所有子线程结束了才会执行也行print "End Main threading"。有人会这么想，如果在 t.start()之后join会怎么样？结果也能阻塞主线程，但是每个线程都是依次执行，变得有顺序了。其实join很好理解，就字面上的意思就是子线程 “加入”（join）主线程嘛。在CPU执行时间片段上“等于”主线程的一部分。在start之后join，也就是每个子线程由被后来新建的子线程给阻塞了，因此线程之间变得有顺序了。


**借用moxie的总结**：
> 1. join方法的作用是阻塞主进程(挡住,无法执行join()以后的语句), 专注执行多线程.
> 2. 多线程多join的情况下, 一次执行各个线程的join方法,前头一个结束了才能执行后面一个.
> 3. 无参数,则等待到该线程结束, 才开始执行下一个线程join.
> 4. 设置参数后,则等待该线程设置的参数的时间(秒), 不管线程有没有结束都继续后面的程序.

## 线程同步和互斥锁
线程之所以比进程轻量，其中一个原因就是他们共享内存。也就是各个线程可以平等的访问内存的数据，如果在短时间“同时并行”读取修改内存的数据，很可能造成数据不同步。例如下面的例子：
```python 
class MyThread(Thread):
    def run(self):
        global count
        time.sleep(1)
        for i in range(100):
            count += 1
        print 'thread {0} add 1, count is {1}'.format(self.name, count)


def main():
    print "Start main threading"
    for i in range(10):
        MyThread().start()

    print "End Main threading"

if __name__ == '__main__':
    main()
```
输出结果如下,10个线程,如果每个线程增加100, 运算结果应该是1000
```
Start main threading
End Main threading
thread Thread-1 add 1, count is 124thread Thread-2 add 1, count is 124
 thread Thread-4 add 1, count is 272thread Thread-3 add 1, count is 272
thread Thread-5 add 1, count is 272

thread Thread-7 add 1, count is 560thread Thread-6 add 1, count is 560thread Thread-10 add 1, count is 526thread Thread-8 add 1, count is 562


 thread Thread-9 add 1, count is 562
```

为了避免线程不同步造成是数据不同步,可以对资源进行加锁.也是访问资源的线程需要获得锁,才能访问.threading的提供了Lock功能, 代码修改如下
```python
from threading import Lock
count = 0
lock = Lock()


class MyThread(Thread):
    def run(self):
        global count
        time.sleep(1)
        if lock.acquire():
            for i in range(100):
                count += 1
            print 'thread {0} add 1, count is {1}'.format(self.name, count)
            lock.release()


def main():
    print "Start main threading"
    for i in range(10):
        MyThread().start()

    print "End Main threading"

if __name__ == '__main__':
    main()
```

```
Start main threading
End Main threading
thread Thread-1 add 1, count is 100
thread Thread-7 add 1, count is 200
thread Thread-6 add 1, count is 300
thread Thread-5 add 1, count is 400
thread Thread-4 add 1, count is 500
thread Thread-2 add 1, count is 600
thread Thread-3 add 1, count is 700
thread Thread-9 add 1, count is 800
thread Thread-8 add 1, count is 900
thread Thread-10 add 1, count is 1000
```

## 死锁
有所就可以方便的处理线程同步问题, 可是多线程的复杂度和难以调试的根源也来自于线程的锁.利用不当,甚至会带来更多问题.比如死锁就是需要避免的问题.

```python
mutex_a = threading.Lock()
mutex_b = threading.Lock()

mutex_a = Lock()
mutex_b = Lock()


class MyThread(Thread):
    def task_a(self):
        if mutex_a.acquire():
            print "thread {0} get mutex a".format(self.name)
            time.sleep(1)
            if mutex_b.acquire():
                print "thread {0} get mutex b".format(self.name)
                mutex_b.release()
            mutex_a.release()

    def task_b(self):
        if mutex_b.acquire():
            print "thread {0} get mutex b".format(self.name)
            time.sleep(1)
            if mutex_a.acquire():
                print "thread {0} get mutex a".format(self.name)
                mutex_a.release()
            mutex_b.release()

    def run(self):
        self.task_a()
        self.task_b()


def main():
    print "Start main threading"

    threads = [MyThread() for i in range(2)]

    for t in threads:
        t.start()
    print "End main threading"


if __name__ == '__main__':
    main()

```
线程需要执行两个任务，两个任务都需要获取锁，然而两个任务先得到锁后，就需要等另外锁释放。

## 可重入锁
为了支持在同一线程中多次请求同一资源, python提供了可重入锁(RLock).RLock内部维护着一个Lock和counter变量, counter记录了acquire的次数,从而使得资源可以多次require.直到一个线程所有的acquire都变成release,其他的线程才能获得资源.

```python
from threading import RLock

mutex = RLock()
class MyThread(Thread):

    def run(self):
        if mutex.acquire(1):
            print "thread {0} get mutex".format(self.name)
            time.sleep(1)
            mutex.acquire()
            mutex.release()
            mutex.release()

def main():
    print "Start main Thread"
    threads = [ MyThread()  for i in range(2) ]

    for t in threads:
        t.start()

    print "End main threading"


if __name__ == '__main__':
    main()

```

```
Start main Thread
thread Thread-1 get mutex
End main threading
thread Thread-2 get mutex
```

## 条件变量
实用锁可以达到线程同步,当前的互斥锁就是这种机制.更复杂的环境,需要针对锁进行一些条件判断.Python提供Condition对象.它除了具有acquire和release方法之外,还提供了wait和notify方法.线程首先acquire一个条件变量锁. 如果条件不足,则线程wai, 如果满足条件就执行线程, 甚至可以notify其他线程.其他处于wait状态的线程接到通知后重新判断条件.

条件变量可以看成不同的线程先后acquire的获得锁, 如果不满足条件, 可以理解为被扔到一个(Lock或RLock)的waiting池. 直到其他线程notify之后再重新判断条件.该模式常用于生产者消费者模式.
```python
from threading import Condition
from random import randrange, random
queue = []
con = Condition()


class Producer(Thread):

    def run(self):
        while True:
            if con.acquire():
                if len(queue) > 1:
                    con.wait()
                else:
                    elem = randrange(100)
                    queue.append(elem)
                    print 'Producer a elem {0}, Now size is {1}'.format(elem, len(queue))
                    time.sleep(random())

                    con.notify()
                con.release()


class Consumer(Thread):
    def run(self):
        while True:
            if con.acquire():
                if len(queue) == 0:
                    con.wait()
                else:
                    elem = queue.pop()
                    print "Consumer a elem {0}. Now queue size {1}".format(elem, len(queue))
                    time.sleep(random())
                    con.notify()
                con.release()


def main():
    for i in range(3):
        Producer().start()

    for i in range(2):
        Consumer().start()

if __name__ == '__main__':
    main()
```

```
Producer a elem 57, Now size is 1
Producer a elem 69, Now size is 2
Consumer a elem 69. Now queue size 1
Consumer a elem 57. Now queue size 0
Producer a elem 18, Now size is 1
Producer a elem 58, Now size is 2
Consumer a elem 58. Now queue size 1
Consumer a elem 18. Now queue size 0
Producer a elem 36, Now size is 1
Producer a elem 32, Now size is 2
Consumer a elem 32. Now queue size 1
Consumer a elem 36. Now queue size 0
Producer a elem 78, Now size is 1
Producer a elem 15, Now size is 2
Consumer a elem 15. Now queue size 1
Consumer a elem 78. Now queue size 0
Producer a elem 41, Now size is 1
Producer a elem 78, Now size is 2
Consumer a elem 78. Now queue size 1
Consumer a elem 41. Now queue size 0
Producer a elem 61, Now size is 1
Producer a elem 26, Now size is 2
```

上述就是一个简单的生产者消费者模型, 先看生产者, 生产者条件变量锁之后就检查条件, 如果不符合条件则wait, wait的时候会释放锁. 如果条件符合, 则往队列列添加元素, 然后会notify其他进程. 注意生产者调用了condition的notify()方法后, 消费者则被唤醒, 但是唤醒不意味着可以开始运行, notify() 并不释放lock, 调用notify()后, lock依然被生产者持有. 生产者通过con.release()显式释放lock. 消费者再次开始运行, 获得条件锁后判断执行.

##　队列
生产者消费者模型主要是对队列操作, Python实现了一个队列结构, 队列内部实现了锁的相关设置. 可以用队列重写生产者消费者模型.

```python
import Queue

queue = Queue.Queue(10)


class Producer(Thread):

    def run(self):
        while True:
            elem = randrange(100)
            queue.put(elem)
            print "Producer a elem {0}, Now size is {1}".format(elem, queue.qsize())
            time.sleep(random())


class Consumer(Thread):

    def run(self):
        while True:
            elem = queue.get()
            queue.task_done()
            print 'Consumer a elem  {0}. Now size is {1}'.format(elem, queue.qsize())
            time.sleep(random())


def main():
    for i in range(3):
        Producer().start()
    for i in range(2):
        Consumer().start()

if __name__ == '__main__':
    main()
```

```
Producer a elem 54, Now size is 1
Producer a elem 94, Now size is 2
Producer a elem 12, Now size is 3
Consumer a elem  54. Now size is 2
Consumer a elem  94. Now size is 1
Consumer a elem  12. Now size is 0
Producer a elem 61, Now size is 1
Producer a elem 26, Now size is 2
Consumer a elem  61. Now size is 1
Producer a elem 35, Now size is 2
Consumer a elem  26. Now size is 1
Producer a elem 96, Now size is 2
Producer a elem 76, Now size is 3
Producer a elem 51, Now size is 4
```
queue 内部实现了相关的锁, 如果queue为空, 则get元素的时候会被阻塞, 直到队列里面的被其他线程写入数据. 同理, 当写入数据的时候, 如果元素的个数大于队列的长度, 也会被阻塞, 也就是在put或者get的时候都会获得Lock.

## 线程通信
线程可以读取共享的内存, 通过内存对一些数据处理. 这就是线程通信的一种, Python还提供了更加高级的线程通信接口. Event对象可以用来进行线程通信, 调用event对象的wait方法, 线程则会阻塞等待, 直到别的线程set之后, 才会被唤醒.
```python

from threading import Event


class MyThread(Thread):
    def __init__(self, event):
        super(MyThread, self).__init__()
        self.event = event

    def run(self):
        print "thread {0} is ready".format(self.name)
        self.event.wait()
        print "thread {0} run".format(self.name)

signal = Event()


def main():
    start = time.time()
    for i in range(3):
        t = MyThread(signal)
        t.start()
    time.sleep(3)
    print 'after {0}s'.format(time.time() - start)
    signal.set()
if __name__ == '__main__':
    main()
```
上面的例子创建了3个线程, 调用线程后, 线程将会被阻塞, sleep 3秒后, 才会被唤醒执行.
```
thread Thread-1 is ready
thread Thread-2 is ready
thread Thread-3 is ready
after 3.00199985504s
thread Thread-1 run
thread Thread-2 run
thread Thread-3 run
```

## 后台线程
默认情况下, 主线程退出之后, 即使子线程没有join(). 那么主线程结束后, 子线程也依然会执行. 如果希望主线程退出后, 其子线程也退出而不再执行, 则需要设置子线程为后台线程. Python提供了setDaemon方法.
```python
class MyThread(Thread):
    def run(self):
        wait_time = randrange(1, 10)
        print "thread {0} will wait {1}s".format(self.name, wait_time)
        time.sleep(wait_time)
        print "thread {0} finished".format(self.name)


def main():
    print "Start main threading"

#    threads = []
    for i in range(5):
        t = MyThread()
        t.setDaemon(True)
#        threads.append(t)
        t.start()

#    for t in threads:
#        t.join()   不会退出
    print "End Main threading"
if __name__ == '__main__':
    main()
```

```
Start main threading
thread Thread-1 will wait 4s
thread Thread-2 will wait 4s
thread Thread-3 will wait 1s
thread Thread-4 will wait 3s
thread Thread-5 will wait 3s
End Main threading
```
每个线程都应该等待sleep几秒，可是主线程很快就执行完了，子线程因为设置了后台线程，所以也跟着主线程退出了。

关于Python多线程的介绍暂且就这些，多线程用于并发任务。对于并发模型，Python还有比线程更好的方法。同样设计任务的时候，也需要考虑是计算密集型还是IO密集型。针对不同的场景，设计不同的程式系统。

[参考](http://python.jobbole.com/85177/)
