# asyncio 模块应用
---

## 多任务和协程

### 开始一个协程
```py
# asyncio_coroutine.py
import asyncio


async def coroutine():
    print('in coroutine')


event_loop = asyncio.get_event_loop()
try:
    print('starting coroutine')
    coro = coroutine()
    print('entering event loop')
    event_loop.run_until_complete(coro)
finally:
    print('closing event loop')
    event_loop.close()
```

```
$ python3 asyncio_coroutine.py

starting coroutine
entering event loop
in coroutine
closing event loop
```
### 协程的返回值
```py

# asyncio_coroutine_return.py
import asyncio


async def coroutine():
    print('in coroutine')
    return 'result'


event_loop = asyncio.get_event_loop()
try:
    return_value = event_loop.run_until_complete(
        coroutine()
    )
    print('it returned: {!r}'.format(return_value))
finally:
    event_loop.close()

```

```
python3 asyncio_coroutine_return.py

in coroutine
it returned: 'result
```

### 链协程
一个协程里包含其他的协程, 协程调用其他协程

```py
asyncio_coroutine_chain.py
import asyncio


async def outer():
    print('in outer')
    print('waiting for result1')
    result1 = await phase1()
    print('waiting for result2')
    result2 = await phase2(result1)
    return (result1, result2)


async def phase1():
    print('in phase1')
    return 'result1'


async def phase2(arg):
    print('in phase2')
    return 'result2 derived from {}'.format(arg)


event_loop = asyncio.get_event_loop()
try:
    return_value = event_loop.run_until_complete(outer())
    print('return value: {!r}'.format(return_value))
finally:
    event_loop.close()

```

```
$ python3 asyncio_coroutine_chain.py

in outer
waiting for result1
in phase1
waiting for result2
in phase2
return value: ('result1', 'result2 derived from result1')
```

##  调用普通函数为协程

### call_soon

```py

# asyncio_call_soon.py
import asyncio
import functools


def callback(arg, *, kwarg='default'):
    print('callback invoked with {} and {}'.format(arg, kwarg))


async def main(loop):
    print('registering callbacks')
    loop.call_soon(callback, 1)
    wrapped = functools.partial(callback, kwarg='not default')
    loop.call_soon(wrapped, 2)

    await asyncio.sleep(0.1)


event_loop = asyncio.get_event_loop()
try:
    print('entering event loop')
    event_loop.run_until_complete(main(event_loop))
finally:
    print('closing event loop')
    event_loop.close()
```

```
$ python3 asyncio_call_soon.py

entering event loop
registering callbacks
callback invoked with 1 and default
callback invoked with 2 and not default
closing event loop
```

### 延迟调用 call_later

```py
asyncio_call_later.py
import asyncio


def callback(n):
    print('callback {} invoked'.format(n))


async def main(loop):
    print('registering callbacks')
    loop.call_later(0.2, callback, 1)
    loop.call_later(0.1, callback, 2)
    loop.call_soon(callback, 3)

    await asyncio.sleep(0.4)


event_loop = asyncio.get_event_loop()
try:
    print('entering event loop')
    event_loop.run_until_complete(main(event_loop))
finally:
    print('closing event loop')
    event_loop.close()
```

```
python3 asyncio_call_later.py

entering event loop
registering callbacks
callback 3 invoked
callback 2 invoked
callback 1 invoked
closing event loop
```

### 指定时间的调用 call_at

```py
# asyncio_call_at.py
import asyncio
import time


def callback(n, loop):
    print('callback {} invoked at {}'.format(n, loop.time()))


async def main(loop):
    now = loop.time()
    print('clock time: {}'.format(time.time()))
    print('loop  time: {}'.format(now))

    print('registering callbacks')
    loop.call_at(now + 0.2, callback, 1, loop)
    loop.call_at(now + 0.1, callback, 2, loop)
    loop.call_soon(callback, 3, loop)

    await asyncio.sleep(1)


event_loop = asyncio.get_event_loop()
try:
    print('entering event loop')
    event_loop.run_until_complete(main(event_loop))
finally:
    print('closing event loop')
    event_loop.close()
```

```
$ python3 asyncio_call_at.py

entering event loop
clock time: 1479050248.66192
loop  time: 1008846.13856885
registering callbacks
callback 3 invoked at 1008846.13867956
callback 2 invoked at 1008846.239931555
callback 1 invoked at 1008846.343480996
closing event loop
```

## 异步生成结果 (Future)
```py
#asyncio_future_event_loop.py
import asyncio


def mark_done(future, result):
    print('setting future result to {!r}'.format(result))
    future.set_result(result)


event_loop = asyncio.get_event_loop()
try:
    all_done = asyncio.Future()

    print('scheduling mark_done')
    event_loop.call_soon(mark_done, all_done, 'the result')

    print('entering event loop')
    result = event_loop.run_until_complete(all_done)
    print('returned result: {!r}'.format(result))
finally:
    print('closing event loop')
    event_loop.close()

print('future result: {!r}'.format(all_done.result()))

```

```
$ python3 asyncio_future_event_loop.py

scheduling mark_done
entering event loop
setting future result to 'the result'
returned result: 'the result'
closing event loop
future result: 'the result'
```

future 带有 await
```py
#asyncio_future_await.py
import asyncio


def mark_done(future, result):
    print('setting future result to {!r}'.format(result))
    future.set_result(result)


async def main(loop):
    all_done = asyncio.Future()

    print('scheduling mark_done')
    loop.call_soon(mark_done, all_done, 'the result')

    result = await all_done
    print('returned result: {!r}'.format(result))


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()

```

```
python3 asyncio_future_await.py

scheduling mark_done
setting future result to 'the result'
returned result: 'the result'
```

### Future 回调
```py
#asyncio_future_callback.py
import asyncio
import functools


def callback(future, n):
    print('{}: future done: {}'.format(n, future.result()))


async def register_callbacks(all_done):
    print('registering callbacks on future')
    all_done.add_done_callback(functools.partial(callback, n=1))
    all_done.add_done_callback(functools.partial(callback, n=2))


async def main(all_done):
    await register_callbacks(all_done)
    print('setting result of future')
    all_done.set_result('the result')


event_loop = asyncio.get_event_loop()
try:
    all_done = asyncio.Future()
    event_loop.run_until_complete(main(all_done))
finally:
    event_loop.close()

```

```
$ python3 asyncio_future_callback.py

registering callbacks on future
setting result of future
1: future done: the result
2: future done: the result
```

## 同步执行任务 Task
task 是与事件循环交互的主要方式之一.
task 包装 协同程序，并在完成后跟踪. task 是Future的子类，所以其他协程程序可以等待它们，每个都有一个可以在任务完成后被检索的结果。

###  开始一个 Task
通过 create_task() 创建一个 Task 实例. 
只要循环正在运行并且协程没有返回，结果任务将作为事件循环管理的并发操作的一部分运行。

```py
#asyncio_create_task.py
import asyncio


async def task_func():
    print('in task_func')
    return 'the result'


async def main(loop):
    print('creating task')
    task = loop.create_task(task_func())
    print('waiting for {!r}'.format(task))
    return_value = await task
    print('task completed {!r}'.format(task))
    print('return value: {!r}'.format(return_value))


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()
```

```
$ python3 asyncio_create_task.py

creating task
waiting for <Task pending coro=<task_func() running at
asyncio_create_task.py:12>>
in task_func
task completed <Task finished coro=<task_func() done, defined at
asyncio_create_task.py:12> result='the result'>
return value: 'the result'
```

### 取消 Task
可以在完成任务之前取消任务的操作
```python
#asyncio_cancel_task.py
import asyncio


async def task_func():
    print('in task_func')
    return 'the result'


async def main(loop):
    print('creating task')
    task = loop.create_task(task_func())

    print('canceling task')
    task.cancel()

    print('canceled task {!r}'.format(task))
    try:
        await task
    except asyncio.CancelledError:
        print('caught error from canceled task')
    else:
        print('task result: {!r}'.format(task.result()))


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()

```

```
$ python3 asyncio_cancel_task.py

creating task
canceling task
canceled task <Task cancelling coro=<task_func() running at
asyncio_cancel_task.py:12>>
caught error from canceled task
```

如果task在等待另一个并发操作时被取消，则通过在其等待的时刻引发 CancelledError异常 来通知其取消该任务.

```python
#asyncio_cancel_task2.py
import asyncio


async def task_func():
    print('in task_func, sleeping')
    try:
        await asyncio.sleep(1)
    except asyncio.CancelledError:
        print('task_func was canceled')
        raise
    return 'the result'


def task_canceller(t):
    print('in task_canceller')
    t.cancel()
    print('canceled the task')


async def main(loop):
    print('creating task')
    task = loop.create_task(task_func())
    loop.call_soon(task_canceller, task)
    try:
        await task
    except asyncio.CancelledError:
        print('main() also sees task as canceled')


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()

```

```
$ python3 asyncio_cancel_task2.py

creating task
in task_func, sleeping
in task_canceller
canceled the task
task_func was canceled
main() also sees task as canceled
```


### 从协程 创建一个 task
ensure_future() 函数返回一个绑定到协同程序执行的任务. 然后，该任务实例可以传递给其他代码，可以等待它，而不知道如何构造或调用原始协同程序。


```py
#asyncio_ensure_future.py
import asyncio


async def wrapped():
    print('wrapped')
    return 'result'


async def inner(task):
    print('inner: starting')
    print('inner: waiting for {!r}'.format(task))
    result = await task
    print('inner: task returned {!r}'.format(result))


async def starter():
    print('starter: creating task')
    task = asyncio.ensure_future(wrapped())
    print('starter: waiting for inner')
    await inner(task)
    print('starter: inner returned')


event_loop = asyncio.get_event_loop()
try:
    print('entering event loop')
    result = event_loop.run_until_complete(starter())
finally:
    event_loop.close()
```

```
$ python3 asyncio_ensure_future.py

entering event loop
starter: creating task
starter: waiting for inner
inner: starting
inner: waiting for <Task pending coro=<wrapped() running at
asyncio_ensure_future.py:12>>
wrapped
inner: task returned 'result'
starter: inner returned
```

## 协程的控制结构和组合
### 等待多个协程
将一个操作分成许多部分并分别执行是非常有用的.  比如在下载几个远程资源.

在执行顺序无关紧要的情况下，可能会有任意数量的操作，wait()可以用于暂停一个协程，直到其他后台操作完成。

```py
#asyncio_wait.py
import asyncio


async def phase(i):
    print('in phase {}'.format(i))
    await asyncio.sleep(0.1 * i)
    print('done with phase {}'.format(i))
    return 'phase {} result'.format(i)


async def main(num_phases):
    print('starting main')
    phases = [
        phase(i)
        for i in range(num_phases)
    ]
    print('waiting for phases to complete')
    completed, pending = await asyncio.wait(phases)
    results = [t.result() for t in completed]
    print('results: {!r}'.format(results))


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(3))
finally:
    event_loop.close()
```
在内部，wait() 使用一个集合来保存它创建的Task实例。这导致他们以不可预测的顺序开始和结束。来自wait()的返回值是一个包含两个集合的元组(completed, pending)，包含已完成和挂起的任务。
```
$ python3 asyncio_wait.py

starting main
waiting for phases to complete
in phase 0
in phase 1
in phase 2
done with phase 0
done with phase 1
done with phase 2
results: ['phase 1 result', 'phase 0 result', 'phase 2 result']
```
如果wait()与timeout 一起使用，则只剩下待处理的操作。
```py
# asyncio_wait_timeout.py
import asyncio


async def phase(i):
    print('in phase {}'.format(i))
    try:
        await asyncio.sleep(0.1 * i)
    except asyncio.CancelledError:
        print('phase {} canceled'.format(i))
        raise
    else:
        print('done with phase {}'.format(i))
        return 'phase {} result'.format(i)


async def main(num_phases):
    print('starting main')
    phases = [
        phase(i)
        for i in range(num_phases)
    ]
    print('waiting 0.1 for phases to complete')
    completed, pending = await asyncio.wait(phases, timeout=0.1)
    print('{} completed and {} pending'.format(
        len(completed), len(pending),
    ))
    # Cancel remaining tasks so they do not generate errors
    # as we exit without finishing them.
    if pending:
        print('canceling tasks')
        for t in pending:
            t.cancel()
    print('exiting main')


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(3))
finally:
    event_loop.close()
```
那些剩下的后台操作应该通过等待它们来取消或完成.在事件循环继续的情况下将它们悬挂下来将使它们进一步执行，如果整个操作被认为是中断，这可能是不可取的。在过程结束时将其悬空将导致报告。
```
$ python3 asyncio_wait_timeout.py

starting main
waiting 0.1 for phases to complete
in phase 1
in phase 0
in phase 2
done with phase 0
1 completed and 2 pending
cancelling tasks
exiting main
phase 1 cancelled
phase 2 cancelled
```

### 汇总协程的结果
```py
#asyncio_gather.py
import asyncio


async def phase1():
    print('in phase1')
    await asyncio.sleep(2)
    print('done with phase1')
    return 'phase1 result'


async def phase2():
    print('in phase2')
    await asyncio.sleep(1)
    print('done with phase2')
    return 'phase2 result'


async def main():
    print('starting main')
    print('waiting for phases to complete')
    results = await asyncio.gather(
        phase1(),
        phase2(),
    )
    print('results: {!r}'.format(results))


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main())
finally:
    event_loop.close()

```
通过收集创建的任务不会公开，所以不能取消。返回值是与传递给gather()的参数的顺序相同的结果列表，而不管后台操作实际完成的顺序如何。
```
$ python3 asyncio_gather.py

starting main
waiting for phases to complete
in phase2
in phase1
done with phase2
done with phase1
results: ['phase1 result', 'phase2 result']
```

### 处理后台操作

as_completed()是一个生成器，用于管理赋予它的协同程序列表的执行，并在运行结果时一次生成一个结果。与wait()一样，命令不受as_completed()的保证，但在执行其他操作之前，不必等待所有后台操作完成。
```py
#asyncio_as_completed.py
import asyncio


async def phase(i):
    print('in phase {}'.format(i))
    await asyncio.sleep(0.5 - (0.1 * i))
    print('done with phase {}'.format(i))
    return 'phase {} result'.format(i)


async def main(num_phases):
    print('starting main')
    phases = [
        phase(i)
        for i in range(num_phases)
    ]
    print('waiting for phases to complete')
    results = []
    for next_to_complete in asyncio.as_completed(phases):
        answer = await next_to_complete
        print('received answer {!r}'.format(answer))
        results.append(answer)
    print('results: {!r}'.format(results))
    return results


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(3))
finally:
    event_loop.close()
```

```
$ python3 asyncio_as_completed.py

starting main
waiting for phases to complete
in phase 0
in phase 2
in phase 1
done with phase 2
received answer 'phase 2 result'
done with phase 1
received answer 'phase 1 result'
done with phase 0
received answer 'phase 0 result'
results: ['phase 2 result', 'phase 1 result', 'phase 0 result']
```
此示例启动几个后台phase ，以相反的顺序完成它们的启动。当生成器被消耗时，循环等待协调的结果等待

##  同步原语

### Locks

```py
#asyncio_lock.py
import asyncio
import functools


def unlock(lock):
    print('callback releasing lock')
    lock.release()


async def coro1(lock):
    print('coro1 waiting for the lock')
    with await lock:
        print('coro1 acquired lock')
    print('coro1 released lock')


async def coro2(lock):
    print('coro2 waiting for the lock')
    await lock
    try:
        print('coro2 acquired lock')
    finally:
        print('coro2 released lock')
        lock.release()


async def main(loop):
    # 创建并取得共享锁
    lock = asyncio.Lock()
    print('acquiring the lock before starting coroutines')
    await lock.acquire()
    print('lock acquired: {}'.format(lock.locked()))

    # 0.1 秒后执行 释放锁 .
    loop.call_later(0.1, functools.partial(unlock, lock))

    # 执行协程, 并等待释放锁 取得所得使用权.
    print('waiting for coroutines')
    await asyncio.wait([coro1(lock), coro2(lock)]),


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()

```

```
$ python3 asyncio_lock.py

acquiring the lock before starting coroutines
lock acquired: True
waiting for coroutines
coro1 waiting for the lock
coro2 waiting for the lock
callback releasing lock
coro1 acquired lock
coro1 released lock
coro2 acquired lock
coro2 released lock
```

### Events
一个asyncio.Event是基于threading.Event，并且用于允许多个消费者等待某事发生，而不寻找与该通知相关联的特定值。

```py
#asyncio_event.py
import asyncio
import functools


def set_event(event):
    print('setting event in callback')
    event.set()


async def coro1(event):
    print('coro1 waiting for event')
    await event.wait()
    print('coro1 triggered')


async def coro2(event):
    print('coro2 waiting for event')
    await event.wait()
    print('coro2 triggered')


async def main(loop):
    # Create a shared event
    event = asyncio.Event()
    print('event start state: {}'.format(event.is_set()))

    loop.call_later(
        0.1, functools.partial(set_event, event)
    )

    await asyncio.wait([coro1(event), coro2(event)])
    print('event end state: {}'.format(event.is_set()))


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()

```

```
$ python3 asyncio_event.py

event start state: False
coro2 waiting for event
coro1 waiting for event
setting event in callback
coro2 triggered
coro1 triggered
event end state: True
```

### Conditions

```py
asyncio_condition.py
import asyncio


async def consumer(condition, n):
    with await condition:
        print('consumer {} is waiting'.format(n))
        await condition.wait()
        print('consumer {} triggered'.format(n))
    print('ending consumer {}'.format(n))


async def manipulate_condition(condition):
    print('starting manipulate_condition')

    # pause to let consumers start
    await asyncio.sleep(0.1)

    for i in range(1, 3):
        with await condition:
            print('notifying {} consumers'.format(i))
            condition.notify(n=i)
        await asyncio.sleep(0.1)

    with await condition:
        print('notifying remaining consumers')
        condition.notify_all()

    print('ending manipulate_condition')


async def main(loop):
    # Create a condition
    condition = asyncio.Condition()

    # Set up tasks watching the condition
    consumers = [
        consumer(condition, i)
        for i in range(5)
    ]

    # Schedule a task to manipulate the condition variable
    loop.create_task(manipulate_condition(condition))

    # Wait for the consumers to be done
    await asyncio.wait(consumers)


event_loop = asyncio.get_event_loop()
try:
    result = event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()
```

```
$ python3 asyncio_condition.py

starting manipulate_condition
consumer 3 is waiting
consumer 1 is waiting
consumer 2 is waiting
consumer 0 is waiting
consumer 4 is waiting
notifying 1 consumers
consumer 3 triggered
ending consumer 3
notifying 2 consumers
consumer 1 triggered
ending consumer 1
consumer 2 triggered
ending consumer 2
notifying remaining consumers
ending manipulate_condition
consumer 0 triggered
ending consumer 0
consumer 4 triggered
ending consumer 4
```

### Queue
```py
# asyncio_queue.py
import asyncio


async def consumer(n, q):
    print('consumer {}: starting'.format(n))
    while True:
        print('consumer {}: waiting for item'.format(n))
        item = await q.get()
        print('consumer {}: has item {}'.format(n, item))
        if item is None:
            # None is the signal to stop.
            q.task_done()
            break
        else:
            await asyncio.sleep(0.01 * item)
            q.task_done()
    print('consumer {}: ending'.format(n))


async def producer(q, num_workers):
    print('producer: starting')
    # Add some numbers to the queue to simulate jobs
    for i in range(num_workers * 3):
        await q.put(i)
        print('producer: added task {} to the queue'.format(i))
    # Add None entries in the queue
    # to signal the consumers to exit
    print('producer: adding stop signals to the queue')
    for i in range(num_workers):
        await q.put(None)
    print('producer: waiting for queue to empty')
    await q.join()
    print('producer: ending')


async def main(loop, num_consumers):
    # Create the queue with a fixed size so the producer
    # will block until the consumers pull some items out.
    q = asyncio.Queue(maxsize=num_consumers)

    # Scheduled the consumer tasks.
    consumers = [
        loop.create_task(consumer(i, q))
        for i in range(num_consumers)
    ]

    # Schedule the producer task.
    prod = loop.create_task(producer(q, num_consumers))

    # Wait for all of the coroutines to finish.
    await asyncio.wait(consumers + [prod])


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop, 2))
finally:
    event_loop.close()

```

```
 python3 asyncio_queue.py

consumer 0: starting
consumer 0: waiting for item
consumer 1: starting
consumer 1: waiting for item
producer: starting
producer: added task 0 to the queue
producer: added task 1 to the queue
consumer 0: has item 0
consumer 1: has item 1
producer: added task 2 to the queue
producer: added task 3 to the queue
consumer 0: waiting for item
consumer 0: has item 2
producer: added task 4 to the queue
consumer 1: waiting for item
consumer 1: has item 3
producer: added task 5 to the queue
producer: adding stop signals to the queue
consumer 0: waiting for item
consumer 0: has item 4
consumer 1: waiting for item
consumer 1: has item 5
producer: waiting for queue to empty
consumer 0: waiting for item
consumer 0: has item None
consumer 0: ending
consumer 1: waiting for item
consumer 1: has item None
consumer 1: ending
producer: ending
```


## 具有协议类抽象的异步I/ O

```py
#!/usr/bin/env python
# @author: zhaifengguo@gmail.com
# encoding:utf-8

import asyncio
import logging
import sys

SERVER_ADDRESS = ('localhost', 10000)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr
)
log = logging.getLogger('main')

loop = asyncio.get_event_loop()


class EchoServer(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport
        self.address = self.transport.get_extra_info('peername')
        self.log = logging.getLogger(
        'EchoServer_{}_{}'.format(*self.address)
        )
        self.log.debug('connection acceped')

    def data_received(self, data):
        self.log.debug('received {!r}'.format(data))
        self.transport.write(data)
        self.log.debug('sent {!r}'.format(data))

    def eof_received(self):
        self.log.debug('received EOF')
        if self.transport.can_write_eof():
            self.transport.write_eof()

    def connection_lost(self, error):
        if error:
            self.logger.error('ERROR: {}'.format(error))
        else:
            self.log.debug('closing')
        super().connection_lost(error)


factory = loop.create_server(EchoServer, *SERVER_ADDRESS)
server = loop.run_until_complete(factory)

log.debug('starting up on {} port {}'.format(*SERVER_ADDRESS))

try:
    loop.run_forever()
finally:
    log.debug('closing server')
    server.close()
    loop.run_until_complete(server.wait_closed())
    log.debug('closing event loop')
    loop.close()
```


```py
import asyncio
import functools
import logging
import sys

MESSAGES = [
    b'This is the message. ',
    b'It will be sent ',
    b'in parts.',
]
SERVER_ADDRESS = ('localhost', 10000)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr,
)
log = logging.getLogger('main')

event_loop = asyncio.get_event_loop()


class EchoClient(asyncio.Protocol):

    def __init__(self, messages, future):
        super().__init__()
        self.messages = messages
        self.log = logging.getLogger('EchoClient')
        self.f = future

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.log.debug(
            'connecting to {} port {}'.format(*self.address)
        )

        for msg in self.messages:
            transport.write(msg)
            self.log.debug('sending {!r}'.format(msg))
        if transport.can_write_eof():
            transport.write_eof()

    def data_received(self, data):
        self.log.debug('received {!r}'.format(data))

    def eof_received(self):
        self.log.debug('received EOF')
        self.transport.close()
        if not self.f.done():
            self.f.set_result(True)

    def connection_lost(self, exc):
        self.log.debug('server closed connection')
        self.transport.close()
        if not self.f.done():
            self.f.set_result(True)
        super().connection_lost(exc)


client_completed = asyncio.Future()

client_factory = functools.partial(
    EchoClient,
    messages=MESSAGES,
    future=client_completed
)

factory_coroutine = event_loop.create_connection(client_factory,
                                                 *SERVER_ADDRESS)

log.debug('waiting for client to complete')
try:
    event_loop.run_until_complete(factory_coroutine)
    event_loop.run_until_complete(client_completed)
finally:
    log.debug('closing event loop')
    event_loop.close()
```

## 使用协程和流的异步I /O
```py
import asyncio
import logging
import sys

SERVER_ADDRESS = ('127.0.0.1', 10000)
logging.basicConfig(
    level = logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr
)
log = logging.getLogger('main')

loop = asyncio.get_event_loop()


async def echo(reader, writer):
    address = writer.get_extra_info('peername')
    log = logging.getLogger('echo_{}_{}'.format(*address))
    log.debug("connection accepted")

    while True:
        data = await reader.read(128)

        if data:
            log.debug('received {!r}'.format(data))
            writer.write(data)
            await writer.drain()
            log.debug('sent {!r}'.format(data))
        else:
            log.debug('closing')
            writer.close()
            return

factory = asyncio.start_server(echo, *SERVER_ADDRESS)
server = loop.run_until_complete(factory)
log.debug('starting up on {} port {}'.format(*SERVER_ADDRESS))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    log.debug('closing server')
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()



```

```py
import asyncio
import logging
import sys

MESSAGES = [
    b'This is the message.',
    b'It will be sent',
    b'in parts.'
]

SERVER_ADDRESS = ('localhost', 10000)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr,
)
log = logging.getLogger('main')

event_loop = asyncio.get_event_loop()


async def echo_client(address, messages):
    log = logging.getLogger('echo_client')
    log.debug('connecting to {} port {}'.format(*address))
    reader, writer = await asyncio.open_connection(*address)

    for msg in  messages:
        writer.write(msg)
        log.debug('sending {!r}'.format(msg))
    if writer.can_write_eof():
        writer.write_eof()
    await writer.drain()

    log.debug('waiting for response')
    while True:
        data = await reader.read(128)
        if data:
            log.debug('received {!r}'.format(data))
        else:
            log.debug('closing')
            writer.close()
            return


try:
    event_loop.run_until_complete(echo_client(SERVER_ADDRESS, MESSAGES))
finally:
    log.debug('closing event loop')
    event_loop.close()
```


## Using SSL

`openssl req -newkey rsa:2048 -nodes -keyout pymotw.key \                  
-x509 -days 365 -out pymotw.crt`

```py
import asyncio
import logging
import sys
import ssl


SERVER_ADDRESS = ('127.0.0.1', 10000)
logging.basicConfig(
    level = logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr
)
log = logging.getLogger('main')

loop = asyncio.get_event_loop()

ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.check_hostname = False
ssl_context.load_cert_chain('pymotw.crt', 'pymotw.key')

async def echo(reader, writer):
    address = writer.get_extra_info('peername')
    log = logging.getLogger('echo_{}_{}'.format(*address))
    log.debug("connection accepted")

    while True:
        data = await reader.read(128)

        if data:
            log.debug('received {!r}'.format(data))
            writer.write(data)
            await writer.drain()
            log.debug('sent {!r}'.format(data))
        else:
            log.debug('closing')
            writer.close()
            return

factory = asyncio.start_server(echo, *SERVER_ADDRESS, ssl=ssl_context)
server = loop.run_until_complete(factory)
log.debug('starting up on {} port {}'.format(*SERVER_ADDRESS))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    log.debug('closing server')
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

```

```py
import asyncio
import logging
import sys
import ssl


MESSAGES = [
    b'This is the message.',
    b'It will be sent',
    b'in parts.'
]

SERVER_ADDRESS = ('localhost', 10000)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr,
)
log = logging.getLogger('main')

event_loop = asyncio.get_event_loop()

ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.check_hostname = False
ssl_context.load_verify_locations('pymotw.crt')

async def echo_client(address, messages):
    log = logging.getLogger('echo_client')
    log.debug('connecting to {} port {}'.format(*address))
    reader, writer = await asyncio.open_connection(*address, ssl=ssl_context)

    for msg in  messages:
        writer.write(msg)
        log.debug('sending {!r}'.format(msg))
    writer.write(b'\x00')
    if writer.can_write_eof():
        writer.write_eof()
    await writer.drain()

    log.debug('waiting for response')
    while True:
        data = await reader.read(128)
        if data:
            log.debug('received {!r}'.format(data))
        else:
            log.debug('closing')
            writer.close()
            return



try:
    event_loop.run_until_complete(echo_client(SERVER_ADDRESS, MESSAGES))
finally:
    log.debug('closing event loop')
    event_loop.close()
        

```
## 与域名服务交互

```py
import asyncio
import logging
import socket
import sys

TARGETS = [
    ('pymotw.com', 'https'),
    ('doughellmann.com', 'https'),
    ('python.org', 'https'),
    ('www.baidu.com', 'https')
]

async def main(loop, targets):
    for target in targets:
        info = await loop.getaddrinfo(
            *target,
            proto=socket.IPPROTO_TCP,
        )

        for host in info:
            print('{:20}: {}'.format(target[0], host[4][0]))


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main(loop, TARGETS))
finally:
    loop.close()

```

```
python asyncio_getaddrinfo.py       
pymotw.com          : 66.33.211.242
doughellmann.com    : 66.33.211.240
python.org          : 23.253.135.79
python.org          : 2001:4802:7901:0:e60a:1375:0:6
www.baidu.com       : 180.97.33.107
www.baidu.com       : 180.97.33.108

```


```py
import asyncio
import logging
import socket
import sys


TARGETS = [
    ('66.33.211.242', 443),
    ('104.130.43.121', 443),
]


async def main(loop, targets):
    for target in targets:
        info = await loop.getnameinfo(target)
        print('{:15}: {} {}'.format(target[0], *info))


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop, TARGETS))
finally:
    event_loop.close()

```

```
 python  asyncio_getnameinfo.py          
66.33.211.242  : apache2-zoo.george-washington.dreamhost.com https
104.130.43.121 : 104.130.43.121 https

```

## Working with Subprocesses
### Using the Protocol Abstraction with Subprocesses
```py
# asyncio_subprocess_protocol.py
import asyncio
import functools


async def run_df(loop):
    print('in run_df')
    cmd_done = asyncio.Future()
    factory = functools.partial(DFProtocol, cmd_done)
    proc = loop.subprocess_exec(
        factory,
        'df', '-hl',
        stdin=None,
        stderr=None,
    )

    try:
        print("launching process")
        transport, protocol = await proc
        print("waiting for process to complete")
        await cmd_done
    finally:
        transport.close()
    return cmd_done.result()


class DFProtocol(asyncio.SubprocessProtocol):
    FD_NAMES = ['stdin', 'stdout', 'stderr']

    def __init__(self, done_future):
        self.done = done_future
        self.buffer = bytearray()
        super().__init__()

    def connection_made(self, transport):
        print("process started {}".format(transport.get_pid()))
        self.transport = transport


    def pipe_data_received(self, fd, data):
        print('read {} bytes from {}'.format(len(data), self.FD_NAMES[fd]))
        
        if fd == 1:
            self.buffer.extend(data)

    def process_exited(self):
        print("process exited")
        return_code = self.transport.get_returncode()
        print('return code {}'.format(return_code))
        if not return_code:
            cmd_output = bytes(self.buffer).decode()
            results = self._parse_results(cmd_output)
        else:
            results = []
        self.done.set_result((return_code, results))

    def _parse_results(self, output):
        print("parsing results")

        if not output:
            return []
        lines = output.splitlines()
        headers = lines[0].split()
        device = lines[1:]
        results = [
            dict(zip(headers, line.split()))
            for line in device
        ]
        return results


event_loop = asyncio.get_event_loop()
try:
    return_code, results = event_loop.run_until_complete(
        run_df(event_loop)
    )
finally:
    event_loop.close()

if return_code:
    print("error exit {}".format(return_code))
else:
    print("\nFree space:")
    for r in results:
        print("{Mounted:25}: {Avail}".format(**r))

```

```
in run_df
launching process
process started 37211
waiting for process to complete
read 537 bytes from stdout
process exited
return code 0
parsing results

Free space:
/dev                     : 2.0G
/run                     : 354M
/                        : 3.7G
/dev/shm                 : 2.0G
/run/lock                : 5.0M
/sys/fs/cgroup           : 2.0G
/boot                    : 242M
/run/user/1000           : 395M

```

### Calling Subprocesses with Coroutines and Streams
```py
# asyncio_subprocess_coroutine.py
import asyncio.subprocess

def _parse_results(output):
        print('parsing results')
        # Output has one row of headers, all single words.  The
        # remaining rows are one per filesystem, with columns
        # matching the headers (assuming that none of the
        # mount points have whitespace in the names).
        if not output:
            return []
        lines = output.splitlines()
        headers = lines[0].split()
        devices = lines[1:]
        results = [
            dict(zip(headers, line.split()))
            for line in devices
        ]
        return results

async def run_df():
    print('in run_df')

    buffer = bytearray()

    create = asyncio.create_subprocess_exec(
        'df', '-hl',
        stdout=asyncio.subprocess.PIPE,
    )
    print("launching process")
    proc = await create
    print("prcess started {}".format(proc.pid))
    while True:
        line = await proc.stdout.readline()
        print('read {!r}'.format(line))
        if not line:
            print("no more output from command")
            break
        buffer.extend(line)

        print("waiting for process to complete")
        await proc.wait()

        return_code = proc.returncode
        print("return code {}".format(return_code))
        if not return_code:
            cmd_output = bytes(buffer).decode()
            results = _parse_results(cmd_output)
        else:
            results =  []
        return (return_code, results)

event_loop = asyncio.get_event_loop()
try:
    return_code, results = event_loop.run_until_complete(
        run_df()
    )
finally:
    event_loop.close()

if return_code:
    print('error exit {}'.format(return_code))
else:
    print('\nFree space:')
    for r in results:
        print('{Mounted:25}: {Avail}'.format(**r))

```


### Sending Data to a Subprocess

```py
# asyncio_subprocess_coroutine_write.py
import asyncio
import asyncio.subprocess

async def to_upper(input):
    print("in to_upper")

    create = asyncio.create_subprocess_exec(
        'tr', '[:lower:]', '[:upper:]',
        stdout=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.PIPE
    )
    print("launching process")
    proc = await create
    print('pid {}'.format(proc.pid))

    print("communicating with process")
    stdout, stderr = await proc.communicate(input.encode())
    print("waiting for process to complete")
    await proc.wait()

    return_code = proc.returncode
    print("return code {}".format(return_code))
    if not return_code:
        results = bytes(stdout).decode()
    else:
        results = ''
    return(return_code, results)

MESSAGE = """
This message will converted to all caps.

"""

event_loop = asyncio.get_event_loop()
try:
    return_code, results = event_loop.run_until_complete(
        to_upper(MESSAGE)
    )
finally:
    event_loop.close()

if return_code:
    print('error exit {}'.format(return_code))
else:
    print('Original: {!r}'.format(MESSAGE))
    print('Changed : {!r}'.format(results))
```

```
in to_upper
launching process
pid 37237
communicating with process
waiting for process to complete
return code 0
Original: '\nThis message will converted to all caps.\n\n'
Changed : '\nTHIS MESSAGE WILL CONVERTED TO ALL CAPS.\n\n'
```
## Receiving Unix Signals



## 将协程与线程和进程相结合

很多现有的库都没有准备好与异步本地使用。它们可能阻止或依赖于通过该模块不可用的并发功能。通过使用`concurrent.futures`的执行程序在单独的线程或单独的进程中运行代码，仍然可以在基于asyncio的应用程序中使用这些库。

### Threads
事件循环的`run_in_executor()`方法会执行一个执行器实例，一个可调用的常规调用，以及要传递给可调用的任何参数. 它返回一个可以用于等待功能完成其工作并返回某些东西的Future。如果没有传递执行executor，则创建一个ThreadPoolExecutor。此示例显式创建一个执行器来限制它将可用的工作线程数。

ThreadPoolExecutor启动其工作线程，然后在线程中调用每个提供的函数一次。
此示例显示如何组合run_in_executor()和wait()以在事件循环中具有协同工作收益控制，同时阻止在单独的线程中运行的函数，然后在这些函数完成时将其唤醒。
```py
#asyncio_executor_thread.py
import asyncio
import concurrent.futures
import logging
import sys
import time


def blocks(n):
    log = logging.getLogger('blocks({})'.format(n))
    log.info('running')
    time.sleep(0.1)
    log.info('done')
    return n ** 2


async def run_blocking_tasks(executor):
    log = logging.getLogger('run_blocking_tasks')
    log.info('starting')

    log.info('creating executor tasks')
    loop = asyncio.get_event_loop()
    blocking_tasks = [
        loop.run_in_executor(executor, blocks, i)
        for i in range(6)
    ]
    log.info('waiting for executor tasks')
    completed, pending = await asyncio.wait(blocking_tasks)
    results = [t.result() for t in completed]
    log.info('results: {!r}'.format(results))

    log.info('exiting')


if __name__ == '__main__':
    # Configure logging to show the name of the thread
    # where the log message originates.
    logging.basicConfig(
        level=logging.INFO,
        format='%(threadName)10s %(name)18s: %(message)s',
        stream=sys.stderr,
    )

    # Create a limited thread pool.
    executor = concurrent.futures.ThreadPoolExecutor(
        max_workers=3,
    )

    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(
            run_blocking_tasks(executor)
        )
    finally:
        event_loop.close()

```

```
$ python3 asyncio_executor_thread.py

MainThread run_blocking_tasks: starting
MainThread run_blocking_tasks: creating executor tasks
  Thread-1          blocks(0): running
  Thread-2          blocks(1): running
  Thread-3          blocks(2): running
MainThread run_blocking_tasks: waiting for executor tasks
  Thread-1          blocks(0): done
  Thread-3          blocks(2): done
  Thread-1          blocks(3): running
  Thread-2          blocks(1): done
  Thread-3          blocks(4): running
  Thread-2          blocks(5): running
  Thread-1          blocks(3): done
  Thread-2          blocks(5): done
  Thread-3          blocks(4): done
MainThread run_blocking_tasks: results: [16, 4, 1, 0, 25, 9]
MainThread run_blocking_tasks: exiting
```

### Processes

```py
# asyncio_executor_process.py
# changes from asyncio_executor_thread.py

if __name__ == '__main__':
    # Configure logging to show the id of the process
    # where the log message originates.
    logging.basicConfig(
        level=logging.INFO,
        format='PID %(process)5s %(name)18s: %(message)s',
        stream=sys.stderr,
    )

    # Create a limited process pool.
    executor = concurrent.futures.ProcessPoolExecutor(
        max_workers=3,
    )

    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(
            run_blocking_tasks(executor)
        )
    finally:
        event_loop.close()
```

```
python3 asyncio_executor_process.py

PID 16429 run_blocking_tasks: starting
PID 16429 run_blocking_tasks: creating executor tasks
PID 16429 run_blocking_tasks: waiting for executor tasks
PID 16430          blocks(0): running
PID 16431          blocks(1): running
PID 16432          blocks(2): running
PID 16430          blocks(0): done
PID 16432          blocks(2): done
PID 16431          blocks(1): done
PID 16430          blocks(3): running
PID 16432          blocks(4): running
PID 16431          blocks(5): running
PID 16431          blocks(5): done
PID 16432          blocks(4): done
PID 16430          blocks(3): done
PID 16429 run_blocking_tasks: results: [4, 0, 16, 1, 9, 25]
PID 16429 run_blocking_tasks: exiting
```

## Debugging with asyncio
