# asyncio 的异步操作-协程
---

## 常用术语

`event_loop`: 事件循环, 程序开启一个无限的循环, 程序员汇报一些函数注册到事件循环上. 当满足事件发生的时候, 调用相应的协程函数

`coroutine`协程: 协程对象, 指一个使用async关键字定义的函数, 它的调用不会立即执行函数,而是返回一个协程对象. 协程对象需要注册到事件循环, 由事件循环调用.

`task`任务, 一个协程对象就是一个原生可以挂起的函数, 任务则是对协程进一步封装, 其中包含任务的各种状态

`future`: 代表将来执行或者没有执行的任务的结果, 它和task 上没有本质的区别

`async/await`: 关键字, python 3.5 用于定义协程的关键字, async 定义一个协程, await 用于挂起阻塞的异步调用接口


## 官方文档

事件循环
### Base Event Loop
事件循环是由asyncio提供的中央执行设备。它提供多种设施，包括：
1. 注册, 执行和取消延迟 调用
2. 为各种通信 创建客户端和服务器传输
3. 启动子程序和相关联的传输以与外部程序进行通信。
4. 将昂贵的函数调用委托给一个线程池。

### class asyncio.BaseEventLoop 
它是AbstractEventLoop的子类，可能是asyncio中的一个具体事件循环实现的基类。
不应该直接使用;改用AbstractEventLoop。 BaseEventLoop不应该被第三方代码子类化;内部接口不稳定。

### class asyncio.AbstractEventLoop
是抽象类, 是所有event loop的. 不是线程安全的

### 运行一个事件循环

`AbstractEventLoop.run_forever()`: 一直运行直到执行 stop() ;如果在调用run_forever（）之前调用stop（），则轮询I / O选择器一次超时值为零，运行所有响应I / O事件（以及已安排的回调）的回调，然后退出。

`AbstractEventLoop.run_until_complete(future)`:  运行到 Future 执行完
如果参数是一个coutine对象，那么它将被ensure_future（）包装。Return the Future’s result, or raise its exception.

`AbstractEventLoop.is_running()`: Returns running status of event loop.
`AbstractEventLoop.stop()`:Stop running the event loop.

`AbstractEventLoop.is_closed()`: Returns True if the event loop was closed.

`AbstractEventLoop.close()`: 关闭事件循环, 时间循环中的必须没有正在运行的, pending 状态的回调会丢失.  会清零队列和干掉执行的, 但是不会等待正在执行的完成

`coroutine AbstractEventLoop.shutdown_asyncgens()`: 安排所有当前打开的异步生成器对象以使用aclose（）调用关闭。调用此方法后，事件循环将在每次迭代新的异步发生器时发出警告。应该用于可靠地完成所有调度的异步发电机。例：
```
try:
    loop.run_forever()
finally:
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()
```

```py
import asyncio

def hello_world(loop):
    print('Hello World')
    loop.stop()

loop = asyncio.get_event_loop()

# Schedule a call to hello_world()
loop.call_soon(hello_world, loop)

# Blocking call interrupted by loop.stop()
loop.run_forever()
loop.close()
```

### Calls 
大多数 asyncio 函数 不会接受关键字参数. 如果想要通过关键字进行回调时, 应该使用`functools.partial()`. 比如:
`loop.call_soon(functools.partial(print, 'Hello', flush=True))` 会被执行 `print("Hello", flush=True)`
>  functools.partial() 比 lambda 更好, 因为 asyncio 可以在debug模式下使检查 functools.partial() 对象 参数

`AbstractEventLoop.call_soon(callback, *args)`: 安排一个回调，尽快被调用。 回调函数在 call_soon() 返回之后, 当事件返回时.  这个操作类似于  FIFO, 执行顺序 是注册顺序, 只会执行一次. 返回一个asyncio.Handle的实例，可以用来取消回调。

`AbstractEventLoop.call_soon_threadsafe(callback, *args)`: like call_soon()

### Delayed calls 延迟调用
事件循环有自己的内部时钟用于计算超时
`AbstractEventLoop.call_later(delay, callback, *args)`: 在给定的延迟秒（无论是int还是浮动）之后安排回调被调用。返回一个asyncio.Handle的实例，可以用来取消回调.

`AbstractEventLoop.call_at(when, callback, *args)`
使用与AbstractEventLoop.time（）相同的时间引用（int或float）将给定的绝对时间戳调用回调。

`AbstractEventLoop.time()`: Return the current time, as a float value, according to the event loop’s internal clock.

```py
import asyncio
import datetime

def display_date(end_time, loop):
    print(datetime.datetime.now())
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1, display_date, end_time, loop)
    else:
        loop.stop()

loop = asyncio.get_event_loop()

# Schedule the first call to display_date()
end_time = loop.time() + 5.0
loop.call_soon(display_date, end_time, loop)

# Blocking call interrupted by loop.stop()
loop.run_forever()
loop.close()
```

### Futures
`AbstractEventLoop.create_future()`:  Create an asyncio.Future object attached to the loop. 
这是在asyncio中创建Future的首选方式，因为事件循环实现可以提供Future类的替代实现（具有更好的性能或工具）。

### Tasks
`AbstractEventLoop.create_task(coro)`:  安排cooutine对象的执行：将来包装它。返回一个Task对象。第三方事件循环可以使用他们自己的Task的子类来实现互操作性。在这种情况下，结果类型是Task的子类。此方法在Python 3.4.2中添加。使用async（）函数来支持较旧的Python版本。

`AbstractEventLoop.set_task_factory(factory)`:  Set a task factory that will be used by AbstractEventLoop.create_task().
If factory is None the default task factory will be set.
如果工厂是可调用的，它应该有一个签名匹配（loop，coro），其中loop将是对活动事件循环的引用，coro将是一个协同对象。 callable必须返回一个asyncio.Future兼容的对象。

`AbstractEventLoop.get_task_factory()`
Return a task factory, or None if the default one is in use.

### Creating connections 创建连接
`coroutine AbstractEventLoop.create_connection(protocol_factory, host=None, port=None, *, ssl=None, family=0, proto=0, flags=0, sock=None, local_addr=None, server_hostname=None)`:

创建到给定Internet主机和端口的流传输连接：socket family 是 AF_INET AF_INET
6  SOCK_STREAM的类型

这个方法在后台返回一个连接协程对象, 如果 成功, 返回(transport, protocol) 对
基本操作的时间序列概要如下：
1. 建立连接，创建传输来表示它。
2. protocol_factory无参数调用，必须返回一个协议实例。
3. 协议实例绑定到transport，并调用其connection_made（）方法。
4. 协调程序使用(transport, protocol) 对成功返回

`coroutine AbstractEventLoop.create_datagram_endpoint(protocol_factory, local_addr=None, remote_addr=None, *, family=0, proto=0, flags=0, reuse_address=None, reuse_port=None, allow_broadcast=None, sock=None)`

`coroutine AbstractEventLoop.create_unix_connection(protocol_factory, path, *, ssl=None, sock=None, server_hostname=None)`

###  Creating listening connections 创建服务端连接
`coroutine AbstractEventLoop.create_server(protocol_factory, host=None, port=None, *, family=socket.AF_UNSPEC, flags=socket.AI_PASSIVE, sock=None, backlog=100, ssl=None, reuse_address=None, reuse_port=None)`:
创建 一个 TCP server端 对象,  This method is a coroutine.

`coroutine AbstractEventLoop.create_unix_server(protocol_factory, path=None, *, sock=None, backlog=100, ssl=None)`

`coroutine BaseEventLoop.connect_accepted_socket(protocol_factory, sock, *, ssl=None)`

###  Watch file descriptors
`AbstractEventLoop.add_reader(fd, callback, *args)`: 开始观看文件描述符以获取可用性，然后使用指定的参数调用回调。
`AbstractEventLoop.remove_reader(fd)`: 停止观看文件描述符以查看可用性。

`AbstractEventLoop.add_writer(fd, callback, *args)`:
`AbstractEventLoop.remove_writer(fd)¶`

```py
import asyncio
try:
    from socket import socketpair
except ImportError:
    from asyncio.windows_utils import socketpair

# Create a pair of connected file descriptors
rsock, wsock = socketpair()
loop = asyncio.get_event_loop()

def reader():
    data = rsock.recv(100)
    print("Received:", data.decode())
    # We are done: unregister the file descriptor
    loop.remove_reader(rsock)
    # Stop the event loop
    loop.stop()

# Register the file descriptor for read event
loop.add_reader(rsock, reader)

# Simulate the reception of data from the network
loop.call_soon(wsock.send, 'abc'.encode())

# Run the event loop
loop.run_forever()

# We are done, close sockets and the event loop
rsock.close()
wsock.close()
loop.close()
```

### Low-level socket operations 
`coroutine AbstractEventLoop.sock_recv(sock, nbytes)`

`coroutine AbstractEventLoop.sock_sendall(sock, data)`

`coroutine AbstractEventLoop.sock_connect(sock, address)`

`coroutine AbstractEventLoop.sock_accept(sock)`

...

### UNIX signals
`AbstractEventLoop.add_signal_handler(signum, callback, *args)`
    Add a handler for a signal.

Raise `ValueError` if the signal number is invalid or uncatchable. `Raise RuntimeError` if there is a problem setting up the handler.

Use `functools.partial` to pass keywords to the callback.

`AbstractEventLoop.remove_signal_handler(sig)`
  Remove a handler for a signal.

Return True if a signal handler was removed, False if not.

```py
import asyncio
import functools
import os
import signal

def ask_exit(signame):
    print("got signal %s: exit" % signame)
    loop.stop()

loop = asyncio.get_event_loop()
for signame in ('SIGINT', 'SIGTERM'):
    loop.add_signal_handler(getattr(signal, signame),
                            functools.partial(ask_exit, signame))

print("Event loop running forever, press Ctrl+C to interrupt.")
print("pid %s: send SIGINT or SIGTERM to exit." % os.getpid())
try:
    loop.run_forever()
finally:
    loop.close()
```

### Server

`class asyncio.Server`
  Server listening on sockets.

Object created by the `AbstractEventLoop.create_server()` method and the `start_server()` function. Don’t instantiate the class directly.

`close()`
  Stop serving: close listening sockets and set the sockets attribute to None.

The sockets that represent existing incoming client connections are left open.

The server is closed asynchronously, use the wait_closed() coroutine to wait until the server is closed.

`coroutine wait_closed()`
Wait until the close() method completes.

This method is a coroutine.

`sockets`
List of socket.socket objects the server is listening to, or None if the server is closed.

### Handle
`class asyncio.Handle`
A callback wrapper object returned by `AbstractEventLoop.call_soon()`, `AbstractEventLoop.call_soon_threadsafe()`, `AbstractEventLoop.call_later()`, and` AbstractEventLoop.call_at()`.

`cancel()`
Cancel the call. If the callback is already canceled or executed, this method has no effect.

### Event loop functions
`asyncio.get_event_loop()`
Equivalent to calling `get_event_loop_policy().get_event_loop()`.

`asyncio.set_event_loop(loop)`
Equivalent to calling `get_event_loop_policy().set_event_loop(loop)`.

`asyncio.new_event_loop()¶`
Equivalent to calling `get_event_loop_policy().new_event_loop()`.


## Tasks and coroutines
(coroutines)  asyncio 协程是使用 async def 语句或者是 生成器.

coroutines 使用 @asyncio.coroutine  或者  async def 定义的

coroutines 类似于 生成器, 有两点不同:
1. 定义协同程序的函数（使用async def的函数定义或使用@ asyncio.coroutine进行装饰）.如果需要消歧，我们将其称为协同函数（iscoroutinefunction() 返回True）。
2. 通过调用协同函数获得的对象。该对象表示将最终完成的计算或 I/O 操作(通常是组合)。如果需要消歧，我们将其称为协同对象（iscoroutine（）返回True）。

协程可以做到事情:

* `result = await future` or `result = yield from future`: 暂停协程直到future完成，然后返回future的结果，或引发异常，这将被传播. (如果future被取消，它将引发CancelledError异常.)请注意，任务是futures，关于futures的一切都适用于任务。
* `result = await coroutine` or `result = yield from coroutine `: 等待另一个协同程序产生结果（或引发异常，这将被传播）。协调表达式必须是对另一个协同程序的调用。
* `return expression` 使用await或yield from 等待该协议的协同结果。
* `raise exception` 在协调中引发异常，正在等待这个异常使用等待或收益。

调用协同程序不会启动其代码运行 - 调用返回的协同程序对象在执行计划之前不会执行任何操作. 启动运行有两种基本方法:
`await coroutine` or `yield from coroutine` 让出执行权获得. 或者 使用 `ensure_future()` 和 `AbstractEventLoop.create_task()`, 调度取得.

> 协调程序（和任务）只能在事件循环运行时运行。

### @asyncio.coroutine
Decorator to mark generator-based coroutines. This enables the generator use yield from to call async def coroutines, and also enables the generator to be called by async def coroutines, for instance using an await expression.

- 1.实例1
```py
import asyncio

async def hello_world():
    print("Hello World!")

loop = asyncio.get_event_loop()
# Blocking call which returns when the hello_world() coroutine is done
loop.run_until_complete(hello_world())
loop.close()
```
- 2.
```py
import asyncio
import datetime

async def display_date(loop):
    end_time = loop.time() + 5.0
    while True:
        print(datetime.datetime.now())
        if (loop.time() + 1.0) >= end_time:
            break
        await asyncio.sleep(1)

loop = asyncio.get_event_loop()
# Blocking call which returns when the display_date() coroutine is done
loop.run_until_complete(display_date(loop))
loop.close()
```

- 3.协程链
```py
import asyncio

async def compute(x, y):
    print("Compute %s + %s ..." % (x, y))
    await asyncio.sleep(1.0)
    return x + y

async def print_sum(x, y):
    result = await compute(x, y)
    print("%s + %s = %s" % (x, y, result))

loop = asyncio.get_event_loop()
loop.run_until_complete(print_sum(1, 2))
loop.close()
```

compute()被链接到print_sum()：print_sum()coroutine等待直到compute()完成，然后返回其结果。

![../img/tulip_coro.png](dd)

### InvalidStateError
`exception asyncio.InvalidStateError`
The operation is not allowed in this state.

### TimeoutError
`exception asyncio.TimeoutError`
The operation exceeded the given deadline.

### Future
`class asyncio.Future(*, loop=None)`
This class is almost compatible with `concurrent.futures.Future`.

与 concurrent.futures.Future 不同点:
1. result()和exception()不需要超时参数，并且在未来尚未完成时引发异常。
2. 使用add_done_callback()注册的回调函数始终通过事件循环的call_soon_threadsafe()调用。
3. 该类与concurrent.futures包中的wait()和as_completed()函数不兼容

### method
`cancel()`
取消 future, 并安排 callbacks()
If the future is already done or cancelled, return False. Otherwise, change the future’s state to cancelled, schedule the callbacks and return True.

`cancelled()`
Return True if the future was cancelled.

`done()`
Return True if the future is done.
完成意味着结果/异常可用，或者将来被取消。
`result()`
Return the result this future represents.

If the future has been cancelled, raises CancelledError. If the future’s result isn’t yet available, raises InvalidStateError. If the future is done and has an exception set, this exception is raised.

`exception()`
Return the exception that was set on this future.

The exception (or None if no exception was set) is returned only if the future is done. If the future has been cancelled, raises CancelledError. If the future isn’t done yet, raises InvalidStateError.


`add_done_callback(fn)`
Add a callback to be run when the future becomes done.

使用单个参数（future对象）调用回调。如果future在调用此函数时已经完成，则调用call_soon()来调度回调。

`remove_done_callback(fn)`
Remove all instances of a callback from the “call when done” list.

Returns the number of callbacks removed.

`set_result(result)`
Mark the future done and set its result.

If the future is already done when this method is called, raises InvalidStateError.

`set_exception(exception)`
Mark the future done and set an exception.

If the future is already done when this method is called, raises InvalidStateError.

```py
import asyncio

async def slow_operation(future):
    await asyncio.sleep(1)
    future.set_result('Future is done!')

loop = asyncio.get_event_loop()
future = asyncio.Future()
asyncio.ensure_future(slow_operation(future))
loop.run_until_complete(future)
print(future.result())
loop.close()
```

```py
import asyncio

async def slow_operation(future):
    await asyncio.sleep(1)
    future.set_result('Future is done!')

def got_result(future):
    print(future.result())
    loop.stop()

loop = asyncio.get_event_loop()
future = asyncio.Future()
asyncio.ensure_future(slow_operation(future))
future.add_done_callback(got_result)
try:
    loop.run_forever()
finally:
    loop.close()
```

### Task
`class asyncio.Task(coro, *, loop=None)`:
安排协同程序的执行：将来包装它。Task是Future的一个子类。

task 负责在事件循环中执行协程对象. 如果 包装的协程对象来自于另一个协程对象, 那么这个协程对象会停止执行, 等待另一个的完成. 当这个 future 执行完, 包装的协程会重新启动执行 获得其结果或者异常,.

事件循环使用协调调度:  同一时间只有一个 协程在运行. 其他的任务可以并行运行, 在其他事件循环 运行在别的线程中. 当task等待完成 future 时，事件循环执行一个新的task。

协程 task 的取消跟 future 的取消不同. 调用 cancel() 后会抛出 CanceledError 异常. cancelled() 仅仅返回 True, 不会抓取 CancelledError 异常 或者触发CancelledError异常.

如果待处理的task被销毁，则其包装的协同程序的执行未完成。

> Don’t directly create Task instances: `use the ensure_future()` function or the `AbstractEventLoop.create_task()` method.


这个 Task 不是线程 安全的


`classmethod all_tasks(loop=None)`
Return a set of all tasks for an event loop.

By default all tasks for the current event loop are returned.

`classmethod current_task(loop=None)`
Return the currently running task in an event loop or `None`.
By default the current task for the current event loop is returned.
`None` is returned when called not in the context of a Task.

`cancel()`
Request that this task cancel itself.

这将安排一个 CancelledError 通过事件循环在下一个循环中被引入到包装的协同程序中。然后协调程序有机会使用try / except / finally清理甚至拒绝该请求。
与 Future.cancel() 不同，这并不能保证任务被取消：异常可能会被捕获并被执行，延迟取消任务或者完全阻止取消。该任务也可能返回值或引发不同的异常。

`get_stack(*, limit=None)`
Return the list of stack frames for this task’s coroutine.
返回task协程对象的堆栈列表
如果协同程序没有完成，这将返回它被挂起的堆栈。如果协同程序已成功完成或已取消，则返回一个空列表。如果协同程序被异常终止，则返回回溯帧列表。

框架总是从最旧到最新的顺序排列。

可选限制给出返回的最大帧数;默认情况下，返回所有可用帧。它的含义取决于是否返回堆栈或回溯：返回堆栈的最新帧，但是返回追溯的最旧帧。 （这与追溯模块的行为相匹配。）由于我们无法控制的原因，对于挂起的协调程序，只返回一个堆栈帧。

`print_stack(*, limit=None, file=None)`:
Print the stack or traceback for this task’s coroutine.

#### 实例, 并行执行 tasks

```py
import asyncio
import time

async def factorial(name, number):
    f = 1 
    for i in range(2, number+1):
        print("Task %s: Compute factorial(%s)..." % (name, i)) 
        await asyncio.sleep(1)
        f *= i
    print("Task %s: factorial(%s) = %s" % (name, number, f)) 

start = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(
    asyncio.gather(
        factorial("A", 2), 
        factorial("B", 3), 
        factorial("C", 4)
    )   
)
print("Elpasd %s" % (time.time() - start))
```

```
Task A: Compute factorial(2)...
Task B: Compute factorial(2)...
Task C: Compute factorial(2)...
Task A: factorial(2) = 2
Task B: Compute factorial(3)...
Task C: Compute factorial(3)...
Task B: factorial(3) = 6
Task C: Compute factorial(4)...
Task C: factorial(4) = 24
Elpasd 3.0085246562957764
```

### Task functions
>在下面的函数中，可选的循环参数允许显式设置底层任务或协程使用的事件循环对象。如果没有提供，则使用默认事件循环。

`asyncio.as_completed(fs, *, loop=None, timeout=None)`
Return an iterator whose values, when waited for, are Future instances.
返回一个 Future 对象的迭代器.

Raises asyncio.TimeoutError if the timeout occurs before all Futures are done.

Example:
```
for f in as_completed(fs):
    result = yield from f  # The 'yield from' may raise
    # Use result
```

`asyncio.ensure_future(coro_or_future, *, loop=None)`
安排cooutine对象的执行: 包装到一个future。返回一个Task对象。

如果是 参数是 future, 则直接返回

`asyncio.wrap_future(future, *, loop=None)`
Wrap a concurrent.futures.Future object in a Future object.

`asyncio.gather(*coros_or_futures, loop=None, return_exceptions=False)`
从给定的 协调对象 或 futures 中返回future的汇总结果
Return a future aggregating results from the given coroutine objects or futures.

所有future必须共享相同的事件循环.如果所有的task 都成功完成，返回的future的结果是结果列表（按原始顺序的顺序，不一定是结果到达的顺序).如果return_exceptions为true，则任务中的异常与成功结果相同，并在结果列表中收集;否则，第一个提出的异常将立即传播到返回的未来。

取消：如果外部未来被取消，所有的孩子（尚未完成）也被取消。如果任何孩子被取消，这被视为提高了CancelledError  - 在这种情况下外部未来未被取消。 （这是为了防止一个孩子被取消，导致其他孩子被取消）


`asyncio.iscoroutine(obj)`:
Return True if obj is a coroutine object, which may be based on a generator or an async def coroutine.

`asyncio.iscoroutinefunction(func)`
Return True if func is determined to be a coroutine function, which may be a decorated generator function or an async def function.

`asyncio.run_coroutine_threadsafe(coro, loop)`
Submit a coroutine object to a given event loop

Return a concurrent.futures.Future to access the result.

`coroutine asyncio.sleep(delay, result=None, *, loop=None)`
Create a coroutine that completes after a given time (in seconds). If `result` is provided, it is produced to the caller when the coroutine completes.

`asyncio.shield(arg, *, loop=None)`
Wait for a future, shielding(屏蔽) it from cancellation.

`coroutine asyncio.wait(futures, *, loop=None, timeout=None, return_when=ALL_COMPLETED)`
Wait for the Futures and coroutine objects given by the sequence futures to complete. Coroutines will be wrapped in Tasks. Returns two sets of Future: (done, pending).
等待序列 future 提供的 future 和 future 对象完成。协程将被包裹在task中。返回两组Future:(done，pending).

The sequence futures must not be empty.


`coroutine asyncio.wait_for(fut, timeout, *, loop=None)`
Wait for the single `Future` or `coroutine object` to complete with timeout. If `timeout` is None, block until the future completes.

Coroutine will be wrapped in Task.

Returns result of the Future or coroutine. When a timeout occurs, it cancels the task and raises `asyncio.TimeoutError`. To avoid the task cancellation, wrap it in `shield()`.

If the wait is cancelled, the future fut is also cancelled.

This function is a coroutine, usage:

`result = yield from asyncio.wait_for(fut, 60.0)`

## Transports and protocols (callback based API)
### Transports
传输是由asyncio提供的类，以便抽象各种通信信道。你通常不会自己实例化运输;相反，您将调用一个AbstractEventLoop方法，该方法将创建传输并尝试启动基础通信通道，当成功时回叫。
一旦建立通信信道，传输总是与协议实例配对。然后，协议可以将传输的方法称为各种目的。
asyncio目前实现TCP，UDP，SSL和子流程管道的传输。交通工具上的方法取决于运输方式。传输类不是线程安全的。

### BaseTransport

`class asyncio.BaseTransport`
Base class for transports

`close()`:
Close the transport

`is_closing()`

`get_extra_info(name, default=None)`:
Return optional transport information.  `name` 是字符串.
name是表示要获取的传输特定信息的字符串，如果信息不存在，则默认为返回的值
name的类型有:
* socket
  - `peername`:  the remote address to which the socket is connected, result of `socket.socket.getpeername()` (None on error)
  - `sokcet`: `socket.socket` 实例
  - `sockname`:  the socket’s own address, result of `socket.socket.getsockname()`
* SSL socket
  - `compression`: 
  - `cipher`:
  - `peercert`:
  - `sslcontext`:
  - `ssl_object`: 
* pipe:
  - `pipe`
* subprocess:
  - `subprocess`: `subprocess.Popen` instance


`set_protocol(protocol)`:
设置一个新的协议. 
Set a new protocol. Switching protocol should only be done when both protocols are documented to support the switch.

`get_protocol()`
Return the current protocol.


### ReadTransport
`class asyncio.ReadTransport`
Interface for read-only transports
`pause_reading()`:  Pause the receiving end of the transport.
`resume_reading()`
Resume the receiving end. The protocol’s` data_received()` method will be called once again if some data is available for reading.

### WriteTransport
`class asyncio.WriteTransport`
Interface for write-only transports.
`abort()`
`can_write_eof()`
`get_write_buffer_size()`
`get_write_buffer_limits()`
`set_write_buffer_limits(high=None, low=None)`
`write(data)`
`writelines(list_of_data)`
`write_eof()`


### DatagramTransport
`DatagramTransport.sendto(data, addr=None)`

`DatagramTransport.abort()`

### BaseSubprocessTransport
`class asyncio.BaseSubprocessTransport`
`get_pid()`
Return the subprocess process id as an integer.

`get_pipe_transport(fd)`
Return the transport for the communication pipe corresponding to the integer file descriptor fd:

* 0: readable streaming transport of the standard input (stdin), or `None` if the subprocess was not created with `stdin=PIPE`
* 1: writable streaming transport of the standard output (stdout), or `None` if the subprocess was not created with `stdout=PIPE`
* 2: writable streaming transport of the standard error (stderr), or `None` if the subprocess was not created with `stderr=PIPE`
* other fd: `None`

`get_returncode()`:

`kill()`
`send_signal(signal)`
`terminate()`
`close()`

### Protocols
asyncio提供了可以子类化实现您的网络协议的基类。这些类与传输结合使用（见下文）：协议解析输入数据并要求写出传出数据，而传输负责实际的I / O和缓冲。

在对类协议进行子类化时，建议您覆盖某些方法。这些方法是回调：它们将在某些事件上由传输器调用（例如当接收到某些数据时）;你不应该自己打电话，除非你正在实施运输。

> 所有回调都具有默认实现，这些实现是空的。因此，您只需要为感兴趣的事件实现回调。
> 

#### Protocol classes
`class asyncio.Protocol`
The base class for implementing streaming protocols (for use with e.g. TCP and SSL transports).

`class asyncio.DatagramProtocol`
The base class for implementing datagram protocols (for use with e.g. UDP transports).

`class asyncio.SubprocessProtocol`
The base class for implementing protocols communicating with child processes (through a set of unidirectional pipes).

#### Connection callbacks [TCP]
可以在 `Protocol`, `DatagramProtocol` `和SubprocessProtocol` 实例上调用这些回调函数：

`BaseProtocol.connection_made(transport)`
Called when a connection is made. 当建立连接是调用

`BaseProtocol.connection_lost(exc)`:
当连接关闭或者丢失时.

参数是 Exception对象或None。后者意味着接收到常规EOF，或者该连接的该端被中止或关闭。connection_made()和connection_lost()每次成功连接时都要精确调用一次。所有其他回调将在这两种方法之间进行调用，这样可以在协议实现中更容易地进行资源管理。

`SubprocessProtocol.pipe_data_received(fd, data)`
Called when the child process writes data into its stdout or stderr pipe. fd is the integer file descriptor of the pipe. data is a non-empty bytes object containing the data.

`SubprocessProtocol.pipe_connection_lost(fd, exc)`
Called when one of the pipes communicating with the child process is closed. fd is the integer file descriptor that was closed.

`SubprocessProtocol.process_exited()`
Called when the child process has exited.

#### Streaming protocols 流式协议
协议实例调用以下回调：
`Protocol.data_received(data)`
Called when some data is received. data is a non-empty bytes object containing the incoming data.

`Protocol.eof_received()`
Called when the other end signals it won’t send any more data (for example by calling `write_eof()`, if the other end also uses `asyncio`).

This method may return a false value (including `None`), in which case the transport will close itself. Conversely, if this method returns a true value, closing the transport is up to the protocol. Since the default implementation returns `None`, it implicitly closes the connection.

在连接期间可以调用data_received()任意次数。然而，eof_received()最多被调用一次，如果被调用，它将不会被调用data_received()。
```
start -> connection_made() [-> data_received() *] [-> eof_received() ?] -> connection_lost() -> end
```

#### Datagram protocols
`DatagramProtocol.datagram_received(data, addr)`
Called when a datagram is received. data is a bytes object containing the incoming data. addr is the address of the peer sending the data; the exact format depends on the transport.

`DatagramProtocol.error_received(exc)`
Called when a previous send or receive operation raises an OSError. exc is the OSError instance.


####  Flow control callbacks¶
hese callbacks may be called on Protocol, DatagramProtocol and SubprocessProtocol instances:

`BaseProtocol.pause_writing()`
Called when the transport’s buffer goes over the high-water mark.

`BaseProtocol.resume_writing()`
Called when the transport’s buffer drains below the low-water mark.

### Protocol examples

- 1. tcp echo client
```py
import asyncio

class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()


loop = asyncio.get_event_loop()

coro = loop.create_server(EchoServerClientProtocol, '127.0.0.1', 7878)
server = loop.run_until_complete(coro)

print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()

```

tcp echo sever
```py
import asyncio

class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()

loop = asyncio.get_event_loop()
# Each client connection will create a new protocol instance
coro = loop.create_server(EchoServerClientProtocol, '127.0.0.1', 7878)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
```

- 2 UDP echo client
```py
import asyncio

class EchoClientProtocol:
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print('Send:', self.message)
        self.transport.sendto(self.message.encode())

    def datagram_received(self, data, addr):
        print("Received:", data.decode())

        print("Close the socket")
        self.transport.close()

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print("Socket closed, stop the event loop")
        loop = asyncio.get_event_loop()
        loop.stop()

loop = asyncio.get_event_loop()
message = "Hello World!"
connect = loop.create_datagram_endpoint(
    lambda: EchoClientProtocol(message, loop),
    remote_addr=('127.0.0.1', 9999))
transport, protocol = loop.run_until_complete(connect)
loop.run_forever()
transport.close()
loop.close()
```

udp echo server
```py
import asyncio

class EchoServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = data.decode()
        print('Received %r from %s' % (message, addr))
        print('Send %r to %s' % (message, addr))
        self.transport.sendto(data, addr)

loop = asyncio.get_event_loop()
print("Starting UDP server")
# One protocol instance will be created to serve all client requests
listen = loop.create_datagram_endpoint(
    EchoServerProtocol, local_addr=('127.0.0.1', 9999))
transport, protocol = loop.run_until_complete(listen)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

transport.close()
loop.close()
```


- 3 Register an open socket to wait for data using a protocol
```py
import asyncio
try:
    from socket import socketpair
except ImportError:
    from asyncio.windows_utils import socketpair

# Create a pair of connected sockets
rsock, wsock = socketpair()
loop = asyncio.get_event_loop()

class MyProtocol(asyncio.Protocol):
    transport = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        print("Received:", data.decode())

        # We are done: close the transport (it will call connection_lost())
        self.transport.close()

    def connection_lost(self, exc):
        # The socket has been closed, stop the event loop
        loop.stop()

# Register the socket to wait for data
connect_coro = loop.create_connection(MyProtocol, sock=rsock)
transport, protocol = loop.run_until_complete(connect_coro)

# Simulate the reception of data from the network
loop.call_soon(wsock.send, 'abc'.encode())

# Run the event loop
loop.run_forever()

# We are done, close sockets and the event loop
rsock.close()
wsock.close()
loop.close()
```

## Streams (coroutine based API)
### Stream functions

`coroutine asyncio.open_connection(host=None, port=None, *, loop=None, limit=None, **kwds)`
A wrapper for create_connection() returning a (reader, writer) pair.

The reader returned is a StreamReader instance; the writer is a StreamWriter instance.

`coroutine asyncio.start_server(client_connected_cb, host=None, port=None, *, loop=None, limit=None, **kwds)`
Start a socket server, with a callback for each client connected. The return value is the same as `create_server()`.

The `client_connected_cb parameter` is **called** with two parameters: **client_reader**, **client_writer**. *client_reader* is a *StreamReader* object, while _client_writer_ is a _StreamWriter_ object. 

`coroutine asyncio.open_unix_connection(path=None, *, loop=None, limit=None, **kwds)`

`coroutine asyncio.start_unix_server(client_connected_cb, path=None, *, loop=None, limit=None, **kwds)`

### StreamReader
`class asyncio.StreamReader(limit=None, loop=None)`

`exception()`
`feed_eof()`
`feed_data()`
`set_exception(exc)`
`set_transport(transport)`

`coroutine read(n=-1)`: 
Read up to n bytes. If n is not provided, or set to -1, read until EOF and return all read bytes.

If the EOF was received and the internal buffer is empty, return an empty bytes object.

`coroutine readline()`

`coroutine readexactly(n)`

`coroutine readuntil(separator=b'\n')`

### StreamWriter
`class asyncio.StreamWriter(transport, protocol, reader, loop)`
Wraps a Transport.

This exposes `write()`, `writelines()`, `can_write_eof()`,` write_eof()`, `get_extra_info()` and `close()`. It adds drain() which returns an optional Future on which you can wait for flow control. It also adds a transport attribute which references the Transport directly.

`transport`
Transport.

`can_write_eof()`
Return True if the transport supports write_eof(), False if not. See WriteTransport.can_write_eof().

`close()`
Close the transport: see BaseTransport.close().

`coroutine drain()`
Let the write buffer of the underlying transport a chance to be flushed.

The intended use is to write:
```
w.write(data)
yield from w.drain()
```

`get_extra_info(name, default=None)`
Return optional transport information: see BaseTransport.get_extra_info().

`write(data)`
Write some data bytes to the transport: see WriteTransport.write().

`writelines(data)`
Write a list (or any iterable) of data bytes to the transport: see WriteTransport.writelines().

`write_eof()`
Close the write end of the transport after flushing buffered data: see WriteTransport.write_eof().

### StreamReaderProtocol
`class asyncio.StreamReaderProtocol(stream_reader, client_connected_cb=None, loop=None)`

### `exception asyncio.IncompleteReadError`
### `LimitOverrunError`
