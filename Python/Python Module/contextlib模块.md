# contextlib模块.md
---
```
import threading
lock = threading.Lock()

lock.acquire()
try:
    my_list.append(item)
finally:
    lock.release()
# 相当于
with lock:
    my_list.append(item)
```

使用contextlib写上下文管理器
```
@contextlib.contextmanager
def some_generator(<argument>):
    <setup>
    try:
        yield <value>
    finally:
        <cleanup>

with some_generator(<arguments>) as <variable>:
    <body>
```


```
from contextlib import contextmanager

@contextmanager
def make_open_context(filename, mode):
    fp = open(filename, mode)
    try:
        yield fp
    finally:
        fp.close()

with make_open_context('tmp.txt', 'a') as f:
    f.write("ssss")

# 多个上下文, 通常需要嵌套
@contextmanager
def make_context(*args):
    print args
    yield

with make_context(1, 2) as A:
    with make_context(3, 4) as B:
        print 'In the context'

# 在py2.7中with语句不需要嵌套
with make_context(1, 2) as A, make_context(3, 4) as B:
    print "In the context"
```

```
>>> lock = threading.Lock()
>>> @contextmanager
... def openlock():
...     print('Acquire')
...     lock.acquire()
...     yield
...     print('Releasing')
...     lock.release()
... 
>>> with openlock():
...     print('Lock is locked: {}'.format(lock.locked()))
...     print 'Do some stuff'
... 
Acquire
Lock is locked: True
Do some stuff
Releasing
```

```
>>> @contextmanager
... def openlock2():
...     print('Acquire')
...     with lock: # threading.Lock其实就是个with的上下文管理器.
...         # __enter__ = acquire
...         yield
...     print('Releasing')
... 
>>> with openlock2():
...     print('Lock is locked: {}'.format(lock.locked()))
...     print 'Do some stuff'
... 
Acquire
Lock is locked: True
Do some stuff
Releasing
```

```
>>> @contextmanager
... def operation(database, host='localhost', 
                  port=27017):
...     db = pymongo.MongoClient(host, port)[database]
...     yield db
...     db.connection.disconnect()
... 
>>> import pymongo
>>> with operation('test') as db:
...     print(db.test.find_one())
... 
{u'a': 0.9075717522597431, u'_id': 
```