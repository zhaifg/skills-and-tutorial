# Python multiprocessing 模块
----
multiprocessing是一个类似于threading的模块.为了解决GIL锁问题,高效的利用多核cpu而设计的.但它不是多线程而是多进程.

## 快速入门
multiprocessing的快速使用多核的方式:

```python
from multiprocessing import Pool
def f(x):
return x*x

if  __name__ == "__main__":
    p = Pool(5) # 声明使用5个进程同时进行
    print(p.map(f, [1,2,3,4]))

    # p.map类似于map函数,单它可以把程序分布到各个cpu 上执行
    ```


## Process
multiprocessing的执行过程催生了Process,通过Process的start()方法启动进程, 使用的方式类似于`threading.Thread`;
```python
from multiprocessing import Process

def f(name):
print "hello", name

if __name__ == '__main__':
p = Process(target=f, args=('zhaifg',))
p.start()
p.join()
```

可以看一下Process一些相关信息
```python
from multiprocessing import Pool
from multiprocessing import Process

import os


def info(title):
print title
print "module name", __name__

if hasattr(os, 'getppid'):
print "parent process", os.getppid()

print "process ID:", os.getpid()


def f(name):
info("function f")
print "hello ", name


if __name__ == '__main__':
info("main line")
print "======"
p = Process(target=f, args=('zhaifg',))
p.start()
p.join()

```

```
main line
module name __main__
parent process 3455
process ID: 3720
======
function f
module name __main__
parent process 3720
process ID: 3721
hello  zhaifg
```

##进程之间的数据的交换
一个父进程生成一个进程时,会复制一份父进程的变量给子进程,各个进程之间的变量等不是共享,而是独自独立于各个进程里的(不像多线程可以共享变量等).这样当进程之间需要交互时需要第三方的渠道进行交互.

- 1. 使用multiprocessing的中Queue的进程数据交互
```python
from multiprocessing import Process, Queue


def f(q, name):
q.put(name)
    # q.put([42, None, 'hello'])

if __name__ == '__main__':
    q = Queue()
    for i in range(10):
    p = Process(target=f, args=(q, i))
    p.start()
    p.join()
    for i in range(q.qsize()):
        print q.get()
```

 - 2. 使用Pipes进行数据交互
    Pipe产生两个连接对象, 对象都有 `send()`与`recv()`方法.
    ```python
    from multiprocessing import Process, Pipe


    def f(conn):
    conn.send([42, None, 'Hello'])
    conn.close()

    if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()
    print parent_conn.recv()
    p.join()
    ```


##　进程间的同步
`multiprocessing`中的同步原语与threading中相同,
```python
from multiprocessing import Process, Lock

def f(l, i):
l.acquire()
print 'Hello world', i
l.release()

if __name__ == '__main__':
lock = Lock()

for num in range(10):
Process(target=f, args=(lock, num,)).start()
```

## 进程之间使用共享状态

### 共享内存
共享内存是通过multiprocessing的中Value和Array类实现的.
`Value`: `multiprocessing.Value(typecode_or_type, *args[, lock])` 
返回一个内存中的`ctypes`对象, 返回的对象的类型是由`typecode_or_type` 决定的

`Array`: `multiprocessing.Array(typecode_or_type, size_or_initializer, *, lock=True)` 返回一个内存分配好的ctypes arrary.

```python
from multiprocessing import Process, Value, Array

def f(n, a):
n.value = 3.1415826
for i in range(len(a)):
a[i] = - a[i]


if __name__ == '__main__':
num = Value('d', 0.0)
arr = Array('i', range(10))

p = Process(target=f, args=(num, arr,))
p.start()
p.join()

print num.value
print arr[:]
```

```
3.1415927
[0, -1, -2, -3, -4, -5, -6, -7, -8, -9]
```


## 通过Manager方式管理Process
Manager对象可以通过Manager()管理一个服务器进程,控制其他的进程的运行.

manager 可以支持的类型有 `list`, `dict`, `Namespace`, `Lock`, `RLock`, `Semaphore`, `BoundedSemaphore`, `Condition`, `Event`, `Queue`, `Value` and `Array`.

```python
from multiprocessing import Process, Manager

def f(d, l):
d[1] = '1'
d['2'] = 2
d[0.25] = None
l.reverse()

if __name__ == '__main__':
manager = Manager()
d = manager.dict()
l = manager.list(range(10))

p = Process(target=f, args=(d, l))
p.start()
p.join()

print d
print l
```
通过manager的管理的dict()与list()共享信息.
```
{0.25: None, 1: '1', '2': 2}
[9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
```
- [] da

## 使用pool进程池

```python
from multiprocessing import Pool, TimeoutError
import time
import os


def f(x):
return x * x

if __name__ == '__main__':
pool = Pool(processes=4)

print pool.map(f, range(10))

for i in pool.imap_unordered(f, range(10)):
print i

res = pool.apply_async(f, (20,))
print res.get(timeout=1)

res = pool.apply_async(os.getpid, ())
print res.get(timeout=1)

multiple_results = [pool.apply_async(os.getpid, ()) for i in range(4)]
print [res.get(timeout=1) for res in multiple_results]

res = pool.apply_async(time.sleep, (10,))

try:
print res.get(timeout=1)
except TimeoutError, e:
print "We lacked patience and got a multiprocessing. timeouterr"

```

```
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
0
1
4
9
16
25
36
49
64
81
400
6584
[6584, 6584, 6584, 6584]


```

```bash
>>> from multiprocessing import Pool
>>> p = Pool(5)
>>> def f(x):
...     return x*x
...
>>> p.map(f, [1,2,3])
Process PoolWorker-1:
Process PoolWorker-2:
Process PoolWorker-3:
Traceback (most recent call last):
AttributeError: 'module' object has no attribute 'f'
AttributeError: 'module' object has no attribute 'f'
AttributeError: 'module' object has no attribute 'f'
```

## Process
`class multiprocessing.Process(group=None, target=None, name=None, args=(), kwargs={})`

## Connection Objects

### Pipe

## Synchronization primitives 同步原语
参见threading.
同步原语有Lock, 信号量,[Condition, Event, Lock, RLock, Semaphore]

##  Shared ctypes Objects
1. Value
2. Array
3. RawArray
4. RawValue
5. ...

## Managers
本地,远程方式, 代理模式

## 进程池

`class multiprocessing.Pool([processes[, initializer[, initargs[, maxtasksperchild]]]])`:  一个进程池对象, 它控制可以提交作业, 它支持超时和回调的异步结果, 并具有并行映射实现.

`processes`: 要使用的进程池的大小. 如果不指定则使用cpu的数量.如果初始化不是None,俺么每个工作进程在启动时都会调用  `initializer(*initargs)`.

`maxtasksperchild` 2.7版本实现, 工作进程在完全退出并被新工作进程替换之前可以完成的任务数, 一边释放未使用的资源. 默认为None.

`apply(func[, args[, kwds]])`:相同于内置的`apply`函数. 它会阻塞直到结果就绪.`appley_async()`是更好的实现. func必须只能运行在一个pool中

`apply_async(func[, args[, kwds[, callback]]])`: apply的一个变体,返回结果对象(AsyncResult)
* callback函数是一个有一个参数(执行的结果)的函数. 当job的结果结算就绪时, callback会被执行(除非job执行错误). callback应该立即完成, 否则处理结果的线程会被阻塞.

`map(func, iterable[, chunksize])`: 并行的内置函数`map`.此方法将iterable切成多个块，将其作为单独的任务提交到进程池。 这些块的（近似）大小可以通过将chunksize设置为正整数来指定。

`map_async(func, iterable[, chunksize[, callback]])`:
`imap(func, iterable[, chunksize])`
`imap_unordered(func, iterable[, chunksize])`: 结果排序的map函数.
`close()`防止任何更多的任务被提交到池中。一旦所有的任务已经完成了工作进程退出。
`terminate()`:立即停止工作进程没有完成出色的工作。当连接池对象被垃圾收集()将立即终止
`join()`:等待 工作进程退出.调用之前波裇调用close()或者terminate()

### class multiprocessing.pool.AsyncResult
这个类是`apply_async` 和 `map_async()`的返回的结果类

`get([timeout])`: 当job执行完成时,返回这个这个对象.  `multiprocessing.TimeoutError `

`wait([timeout])`: 等待指导有结果或者超时
`ready()`: 返回是否完成
`successful()`: 返回是否执行完成并成功, 是否触发异常.
```python
from multiprocessing import Pool

def f(x):
    return x*x

if __name__ == '__main__':
    pool = Pool(processes=4)              # start 4 worker processes

    result = pool.apply_async(f, (10,))    # evaluate "f(10)" asynchronously
    print result.get(timeout=1)           # prints "100" unless your computer is *very* slow

    print pool.map(f, range(10))          # prints "[0, 1, 4,..., 81]"

    it = pool.imap(f, range(10))
    print it.next()                       # prints "0"
    print it.next()                       # prints "1"
    print it.next(timeout=1)              # prints "4" unless your computer is *very* slow

    import time
    result = pool.apply_async(time.sleep, (10,))
    print result.get(timeout=1) 
```

```python
import multiprocessing as mp
import time

def foo_pool(x):
    time.sleep(2)
    return x*x

result_list = []
def log_result(result):
    # This is called whenever foo_pool(i) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    result_list.append(result)

def apply_async_with_callback():
    pool = mp.Pool()
    for i in range(10):
        pool.apply_async(foo_pool, args = (i, ), callback = log_result)
    pool.close()
    pool.join()
    print(result_list)

if __name__ == '__main__':
    apply_async_with_callback()
```
[Who runs the callback when using apply_async method of a multiprocessing pool?](http://stackoverflow.com/questions/24770934/who-runs-the-callback-when-using-apply-async-method-of-a-multiprocessing-pool)
## Listeners and Clients

## Logging
`multiprocessing.get_logger()`:返回logger对象
第一次创建日志级别是`logging.NOTSET`, 以及没有默认的logger handler. 日志会传播到root logger

`multiprocessing.log_to_stderr()`:发送到错误日志中．默认格式`'[%(levelname)s/%(processName)s] %(message)s'.`
```python
>>> import multiprocessing, logging
>>> logger = multiprocessing.log_to_stderr()
>>> logger.setLevel(logging.INFO)
>>> logger.warning('doomed')
[WARNING/MainProcess] doomed
>>> m = multiprocessing.Manager()
[INFO/SyncManager-...] child process calling self.run()
[INFO/SyncManager-...] created temp directory /.../pymp-...
[INFO/SyncManager-...] manager serving at '/.../listener-...'
>>> del m
[INFO/MainProcess] sending shutdown message to manager
[INFO/SyncManager-...] manager exiting with exitcode 0

```

## Example
