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

## Listeners and Clients

## Logging

## Example
