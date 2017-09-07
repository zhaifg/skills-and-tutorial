# tornado 入门
---

## 介绍
Tornado 是一个web 框架和异步网络库, 使用异步 I/O. 支持 long pooing , WebSockets

大致分为四个部分:
1. web 框架 (RequestHandler 子类创建 web 应用).
2. HTTP 的客户端和服务器端
3. 异步网络开发库, 包括IOLoop 和IOStream.
4. 协程库 (tornado.gen)


### 异步非阻塞 i/o

### 阻塞

### 异步

异步函数在完成之前返回，并且通常会在触发应用程序中的未来操作之前在后台进行一些工作（与正常的同步函数相反，这些功能在返回之前将执行所有操作）。
异步接口有很多样式:

* 回调参数
* 返回占位符 (Future, Promise, Deferred)
* 发送到队列
* 回调注册表（例如POSIX信号）

无论使用哪种类型的接口，定义的异步功能与其呼叫者的交互方式不同;没有任何自由的方式使同步功能以对其调用者透明的方式进行异步（像gevent这样的系统使用轻量级线程来提供与异步系统相当的性能，但实际上并不使事情异步）。

实例
一下是同步函数
```py
from  tornado.httpclient import HTTPClient

def synchronous_fetch(url):
    http_client = HTTPClient()
    response = http_client.fetch(url)
    return response.body

```

通过回调重写

```py
from torndao.httpclient import AsyncHTTPClient

def asynchronous_fetch(url, callback):
    http_client = AsyncHTTPClient()
    def handle_response(response):
        callback(response.body)
    http_client.fetch(url, callback=handle_response)
```

通过 Future 方式取代 回调

```py
from tornado.concurrent import Future

def async_fetch_future(url):
    http_client = AsyncHTTPClient()
    my_future = Future()
    fetch_future = http_client.fetch(url)
    fetch_future.add_done_callback(
        lambda f: my_furture.set_result(f.result())
        )
    return my_future
```

协程方式

```py
from tornado import gen

@gen.coroutine
def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    raise gen.Return(response.body)

```

## 协程
Tornado 推荐使用 协程来编写异步程序. 协程是用 yield 关键字 暂停和恢复执行来代替 回调方式. (合作的轻量级线程如Gevent这样的框架也被称为协程，但是在Tornado中，所有协同程序都使用显式上下文切换，称为异步函数)

协调程序几乎与同步代码一样简单，但不需要线程费用。它们还通过减少上下文切换可能发生的位置数量使并发更容易理解。

```
from tornado import gen
@gen.corotuine
def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    # In Python versions prior to 3.3, returning a value from
    # a generator is not allowed and you must use
    #   raise gen.Return(response.body)
    # instead.
    return response.body

```

###  Python 3.5 的 async 和 await

Py 3.5 添加了 async 和 await 关键字. 自Tornado 4.3 开始可以使用 async 和 await 来代替 yield 和 装饰器的形式. 上面的可以改写为
```py


async def f(url):
    http_client =  AsyncHTTPClient()
    response = await http_client.fetch(url)
    return response.body
```

await关键字不如yield关键字多功能。 yield 为基础的协程可以 yield 一个list 的Future, 在 py 3.5 中必须使用 `tornado.gen.multi`  进行包装, 以消除对 `concurrent.futures` 的整合. 您可以使用 `tornado.gen.convert_yielded` 将任何可以与 `yield` 一起工作的内容转换成可与 `await` 一起工作的表单：
```py

async def f():
    executor = concurrent.futures.ThreadPoolExecutor()
    await tornado.gen.convert_yielded.submit(executor.submit(g))

```


Tornado 的协程程序可以接收 其他的框架的 协程来执行; asynci 不支持. 建议使用 tornado runner 结合多个框架的应用程序.

使用 `Tornado.platform.asyncio.to_asyncio_future` 适配器，在已经使用 asyncio 转换程序的协同程序中使用Tornado运行程序调用协同程序。

### 如何工作

### 如何调用协程
协调程序不会以正常方式提出异常：他们提出的任何异常将被困在 Future 直到 yield。这意味着以正确的方式调用协同程序很重要，否则可能会出现不被忽视的错误：

```py

@gen.coroutine
def divide(x, y):
    return x/y

def bad_call():
     #  会触发zeroDivisionError, 但是  它不是协程不正确执行的原因
    divide(1, 0)
```

在几乎所有情况下，任何调用协同程序的函数都必须是协同程序本身，并在调用中使用yield关键字。当您覆盖超类中定义的方法时，请参阅文档以查看是否允许协程（文档应该说该方法“可能是协程”或“可能会返回Future”）:

```py
@gen.coroutine
def good_call():
    # yield will unwrap the Future returned by divide() and raise
    # the exception.
    yield divide(1, 0)
```

有时候，你可能想要“开火忘记”一个协议，而不用等待其结果。在这种情况下，建议使用`IOLoop.spawn_callback`，这将使`IOLoop`负责该调用。如果失败，`IOLoop`将记录堆栈跟踪：
```py
# The IOLoop will catch the exception and print a stack trace in
# the logs. Note that this doesn't look like a normal call, since
# we pass the function object to be called by the IOLoop.
IOLoop.current().spawn_callback(divide, 1, 0)
```

对于使用`@ gen.coroutine`的函数，建议以这种方式使用`IOLoop.spawn_callback`，但是使用`async def`的函数需要使用（否则协同程序运行程序将无法启动）。

最后，在程序的顶层，如果 IOLoop 尚未运行，可以启动 IOLoop ，运行协同程序，然后使用 `IOLoop.run_sync` 方法停止IOLoop。这通常用于启动面向批处理程序的主要功能：
```py
# run_sync() doesn't take arguments, so we must wrap the
# call in a lambda.
IOLoop.current().run_sync(lambda: divide(1, 0))
```

### 协程模式

#### 与回调整合
使用 callback 来代替 Future, 并把其包装成 Task . 这将为您添加回调参数，并返回一个可以产生的Future：
```py
@gen.coroutine
def call_task():
    # Note that there are no parens on some_function.
    # This will be translated by Task into
    #   some_function(other_args, callback=callback)
    yield gen.Task(some_function, other_args)
```

#### 调用 阻塞函数

协程调用阻塞函数的最简单的方式是使用 ThreadPoolExecutor, 让其返回Furtures
```py
thread_pool = ThreadPoolExecutor(4)

@gen.coroutine
def call_blocking():
    yield thread_pool.submit(blocking_func, args)
```

#### 并行方式
协程装饰器 师承认价值为Future的list和字典，并且并行等待所有这些Future：
```py
@gen.coroutine
def parallel_fetch(url1, url2):
    resp1, resp2 = yield [http_client.fetch(url1),
                          http_client.fetch(url2)]

@gen.coroutine
def parallel_fetch_many(urls):
    responses = yield [http_client.fetch(url) for url in urls]
    # responses is a list of HTTPResponses in the same order

@gen.coroutine
def parallel_fetch_dict(urls):
    responses = yield {url: http_client.fetch(url)
                        for url in urls}
    # responses is a dict {url: HTTPResponse}
```

#### 交错
有时候，保存一个Future而不是立即使用它是有用的，所以你可以在等待之前启动另一个操作：
```py
@gen.coroutine
def get(self):
    fetch_future = self.fetch_next_chunk()
    while True:
        chunk = yield fetch_future
        if chunk is None: break
        self.write(chunk)
        fetch_future = self.fetch_next_chunk()
        yield self.flush()

```

这个模式最适用于`@gen.coroutine`. 如果fetch_next_chunk()使用`async def`，则必须将其调用为`fetch_future = tornado.gen.convert_yielded（self.fetch_next_chunk()` 以开始后台处理。

#### Looping
循环与协同程序是棘手的，因为Python中没有办法在for或while循环的每次迭代中产生，并捕获yield的结果。
相反，您需要将循环条件与访问结果进行分离，如`Motor`所示：

```py
import motor
db = motor.MotorClient().test

@gen.coroutine
def loop_example(collection):
    cursor = db.collection.find()
    while (yield cursor.fetch_next):
        doc = cursor.next_object()
```

#### 在后台运行
`PeriodicCallback` 通常不用于协同程序。相反，协程可以包含一个True：循环，并使用`tornado.gen.sleep`：
```py
@gen.coroutine
def minute_loop():
    while True:
        yield do_something()
        yield gen.sleep(60)

# Coroutines that loop forever are generally started with
# spawn_callback().
IOLoop.current().spawn_callback(minute_loop)

```

有时可能需要更复杂的循环。例如，前一个循环每60+N秒运行一次，其中N是 do_something() 的运行时间。要每60秒运行一次，请使用上面的交错模式：
```py
@gen.coroutine
def minute_loop2():
    while True:
        nxt = gen.sleep(60)   # Start the clock.
        yield do_something()  # Run while the clock is ticking.
        yield nxt             # Wait for the timer to run out

```


## Main event loop: Tornado.ioloop

### class tornado.ioloop.IOLoop
水平触发的

### 运行一个 IOLoop
`static IOLoop.current(instance=True)`
返回 当前的线程的 IOLoop.
如果IOLoop正在运行或已被`make_current`标记为current，则返回该实例。如果没有当前IOLoop，则返回`IOLoop.instance()`(即主线程的IOLoop，如果需要，则创建一个)。

一般来说，您应该在构造异步对象时使用 `IOLoop.current` 作为默认值，并在使用`IOLoop.instance`表示与其他主线程通信时使用`IOLoop.instance`。

`IOLoop.make_current()`
Makes this the IOLoop for the current thread.

`static IOLoop.instance()`
返回全局的IOLoop 实例

`static IOLoop.initialized()`

`IOLoop.install()`

`static IOLoop.clear_instance()`

`IOLoop.start()`

`IOLoop.stop()`

`IOLoop.run_sync(func, timeout=None)`

`IOLoop.close(all_fds=False)`

### I/O events
`IOLoop.add_handler(fd, handler, events)`: 

`IOLoop.update_handler(fd, events)`

`IOLoop.remove_handler(fd)`


### Callbacks and timeouts
`IOLoop.add_callback(callback, *args, **kwargs)`

`IOLoop.add_callback_from_signal(callback, *args, **kwargs)`

`IOLoop.add_future(future, callback)`

`IOLoop.add_timeout(deadline, callback, *args, **kwargs)`

`IOLoop.call_at(when, callback, *args, **kwargs)`

`IOLoop.call_later(delay, callback, *args, **kwargs)`

`IOLoop.remove_timeout(timeout)`

`IOLoop.spawn_callback(callback, *args, **kwargs)`

`IOLoop.time()`

`class tornado.ioloop.PeriodicCallback(callback, callback_time, io_loop=None)`:
   `start()`
   `stop()`
   `is_running()`

### Debugging and error handling



## tornado.iostream — Convenient wrappers for non-blocking sockets

用于写入和读取非阻塞文件和套接字的实用程序类:

1. BaseIOStream
2. IOStream
3. SSLIOStream
4. PipeIOStream

### Base class

`class tornado.iostream.BaseIOStream(io_loop=None, max_buffer_size=None, read_chunk_size=None, max_write_buffer_size=None)`:
用于写入和读取非阻塞文件或套接字的实用程序类。

我们支持非阻塞 `write()` 和一系列 `read_*()` 方法。所有这些方法都采用可选的 回调参数 ，只有在没有 回调 给定的情况下才返回一个 Future。当操作完成时，回调 将被运行，或者 Future 将通过读取的数据（或对于None  write()）来解析。当流关闭时，所有未完成的 Future 将解决 `StreamClosedError`;回调接口的用户将通过`BaseIOStream.set_close_callback`通知。

当流由于错误而关闭时，IOStream的错误属性包含异常对象。
子类必须实现 fileno，close_fd，write_to_fd，read_from_fd和 可选的 get_fd_error。

参数:
  * io_loop: 4.1 之后被放弃
  * `max_buffer_size`:  最大读入的换组 默认100M
  * `read_chunk_size`:  从底层运输一次读取的数据量;默认为64KB.
  * `max_write_buffer_size`:  默认无限制
  * 

### Main interface
`BaseIOStream.write(data, callback=None)`:
Asynchronously write the given data to this stream.

>The **data** argument may be of type **bytes** or **memoryview**.

`BaseIOStream.read_bytes(num_bytes, callback=None, streaming_callback=None, partial=False)`:

Asynchronously read a number of bytes.

如果给出了一个streaming_callback，它将在数据可用时被调用，最终结果将为空。否则，结果是所有读取的数据。如果给出回调，它将以数据作为参数运行;如果没有，这个方法返回一个Future。
如果 partial是真的，一旦我们有任何字节返回（但从不超过num_bytes），回调就会运行.

`BaseIOStream.read_until(delimiter, callback=None, max_bytes=None)`:
Asynchronously read until we have found the given delimiter.

结果包括所有读取的数据，包括分隔符。如果给出回调，它将以数据作为参数运行;如果没有，这个方法返回一个Future。
如果max_bytes不为None，则如果已读取超过max_bytes个字节并且未找到分隔符，则连接将关闭。

`BaseIOStream.read_until_regex(regex, callback=None, max_bytes=None)`

`BaseIOStream.read_until_close(callback=None, streaming_callback=None)`

`BaseIOStream.close(exc_info=False)`

`BaseIOStream.set_close_callback(callback)`

`BaseIOStream.closed()`

`BaseIOStream.reading()`

`BaseIOStream.writing()`

`BaseIOStream.set_nodelay(value)`

### Methods for subclasses
`BaseIOStream.fileno()`
`BaseIOStream.close_fd()`
`BaseIOStream.write_to_fd(data)`
`BaseIOStream.read_from_fd()`
`BaseIOStream.get_fd_error()`

### 实现
#### `class tornado.iostream.IOStream(socket, *args, **kwargs)`
基于套接字的IOStream实现。

这个类支持从BaseIOStream读取和写入方法加上一个connect方法。
套接字参数可能连接或未连接。对于服务器操作，套接字是调用`socket.accept`的结果。对于客户端操作，套接字是用s`ocket.socket`创建的，可以在将其传递到`IOStream`或与`IOStream.connect`连接之前连接。

A very simple (and broken) HTTP client using this class:
```py
import tornado.ioloop
import tornado.iostream
import socket

def send_request():
    stream.write(b"GET / HTTP/1.0\r\nHost: friendfeed.com\r\n\r\n")
    stream.read_until(b"\r\n\r\n", on_headers)

def on_headers(data):
    headers = {}
    for line in data.split(b"\r\n"):
       parts = line.split(b":")
       if len(parts) == 2:
           headers[parts[0].strip()] = parts[1].strip()
    stream.read_bytes(int(headers[b"Content-Length"]), on_body)

def on_body(data):
    print(data)
    stream.close()
    tornado.ioloop.IOLoop.current().stop()

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    stream = tornado.iostream.IOStream(s)
    stream.connect(("friendfeed.com", 80), send_request)
    tornado.ioloop.IOLoop.current().start()
```

`connect(address, callback=None, server_hostname=None)`
Connects the socket to a remote address without blocking.

address = (ip, port)


`start_tls(server_side, ssl_options=None, server_hostname=None)`
Convert this IOStream to an SSLIOStream.

#### class tornado.iostream.SSLIOStream(*args, **kwargs)
ssl.wrap_socket(sock, do_handshake_on_connect=False, **kwargs)
wait_for_handshake(callback=None)


#### class tornado.iostream.PipeIOStream(fd, *args, **kwargs)

### Exceptions
`exception tornado.iostream.StreamBufferFullError[so`
`exception tornado.iostream.StreamClosedError(real_error=None)`
`exception tornado.iostream.UnsatisfiableReadError`
