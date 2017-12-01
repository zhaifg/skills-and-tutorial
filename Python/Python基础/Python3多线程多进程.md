# Python3 多线程 多进程技术
---

期物(期待操作的对象) 是concurrent.futures 和 asyncio 包的重要组件

concurrent.futures.Future 和 asyncio.Future 这两个类的作用相同: 两个 Future 类的实例都表示可能已经完成尚未完成的延迟计算.

期物封装待完成的操作, 可以放入队列, 完成的状态可以查询, 得到结果(或抛出异常)后可以获取结果(或异常).

通常情况下自己不应该创建期物, 而只能由并发框架(concurrent.futures 或 asyncio) 实例化. 原因很简单: 期物表示终将发生的事情, 而确定某件事会发生的唯一方式是执行的时间已经排定. 因此, 只有排定把某件事交给 concurrent.futures.Executor 子类处理时, 才会concurrent.futures.Future 实例. 例如, Executor.submit() 方法的参数是一个调用的对象, 调用这个方法后卫传入的可调用对象排期, 并返回一个期物.

客户端代码不应该改变期物的状态, 并发框架的在期物表示的延迟计算结束后会改变期物的状态, 而我们无法控制计算何时结束.

这两种期物都有 `.done()` 方法, 这个方法不阻塞, 返回布尔值, 指明期物链接的可调用对象是否已经执行. 客户端代码通常不会询问期物是否运行结束, 而是会等待通知. 因此, 两个Future 类都有 `.add_done_callback()` 方法: 这个方法只有一个参数, 类型是可调用对象, 期物运行结束后会调用指定的可调用对象.

此外, 还有`.result()`方法. 在期物运行结束后调用的话, 这个方法在两个Future 类中的作用相同: 返回可调用对象的结果, 或者重新抛出执行可调用的对象时抛出的异常. 可是, 如果期物没有运行结束, result 方法在两个Future 类中的行为相差很大. 对 concurrency.futures.Future 实例来说, 调用 `f.result()` 方法会阻塞调用方所在的线程, 知道有运行结果可返回. 此时, result 方法可以接受可选的timeout 参数, 如果在指定的 时间内期物没有运行完毕, 会抛出 TimeoutError 异常.  asyncio.Future.result 方法, 不支持设定超时时间, 在那个库中获取的结果最好使用 yield from结构.

## asyncio

* asyncio.Task 对象差不多与threading.Thread 对象等效.
* Task 对象用于驱动协程, Thread 对象用于调用可调用的对象.
* Task 对象 不由自己手动创建, 而是通过把协程传给loop.create_task(...)等方法获取
* 获取的Task 对象已经排定了运行时间(例如, 由 asyncio.async 函数排定); Thread 实例则必须调用start 方法, 名曲告知让它运行
* 线程版supervisor 函数中, slow_function 函数是普通的函数, 直接由线程调用. 在异步版 supervisor 函数中, slow_function 函数是协程, 由yield from/await 驱动
* 没有API能从外部终止线程, 因为线程随时可能被中断, 导致系统处于无效状态. 如果想终止任务, 可以使用 Task.cancel() 实例方法, 在协程内部抛出 CancelledError 异常. 协程可以在暂停的yield 处捕获这个异常, 处理终止请求
* superivsor 协程必须在 main 函数中由loop.run_until_complete 方法执行.

### asyncio.Future : 故意不阻塞
asyncio.Future 类与 concurrent.futures.Future 类接口基本一致, 不过实现方式不同, 不可以互换.


期物只是调度执行某物的结果. 在asyncio 包中, BaseEventLoop.create_task(...) 方法接收一个协程, 排定它的运行时间, 然后返回一个asyncio.Task 实例----也是asyncio.Future 类的实例, 因为 Task 是Future 的子类, 用于包装协协程. 这与调用 Executor.submit(...) 方法创建concurrent.futures.Future 实例是一个道理


与concurrent.futures.Future 类似, asyncio.Future 类也提供了 `.done()`, `.add_done_callback(...)` 和 `.result()` 等方法. 前两个方法的用法与 concurrent一样, 不过`.result()` 方法差别很大.

asyncio.Future 类的 `.result()`方法没有参数, 因此不能指定超时时间. 此外, 调用`.result()` 方法时期物还没完全运行完毕, 那么`.result()` 方法不会阻塞去等待结果, 而是抛出asyncio.InvalidStateError 异常.

然而, 获取asyncio.Future 对象等级过通常使用 await(yield from), 从中产出结果.

使用await (yield from) 处理期物, 等待期物运行完毕这一步无需我们关系, 而且不会阻塞事件循环, 因为在asyncio 包中, yield form(await) 的作用把控制权换给事件循环.

> 使用 await (yield from) 处理期物与使用add_done_callback 方法处理协程的作用一样: 延迟的操作结束后, 事件循环不会触发回调对象, 而是设置期物的返回值; 而 yield from(await) 表达式则在暂停的协程中生成返回值, 恢复执行协程.

总之, 因为 asyncio.Future 类的目的是与 yield from(await) 一起使用, 所以通常不需要使用一下方法
* 无需调用 my_future.add_done_callback(...), 因为可以直接把在期物运行结束后的操作放在协程中 yield from (await) my_future 表达式的后面. 这是协程一大优势: 协程是可以暂停的恢复的函数.
* 无需调用 my_future.result(), 因为, yield from (await) 从期物中产出的值就是结果 (例如, result = await my_future)

当然，有时也需要使用 .done()、.add_done_callback(...) 和
.result() 方法。但是一般情况下，asyncio.Future 对象由 yield
from 驱动，而不是靠调用这些方法驱动.

在 asyncio 包中, 期物和协程关系紧密, 因为可以使用 yield from 从asyncio.Future对象中产出结果. 这意味着, 如果 foo 是协程函数(调用后返回协程对象), 抑或是返回Future 或 Task 实例的普通函数, 那么可以这样写:
res = yield from foo(). 这是 asyncio 包的 API 中很多地方可以互换协程与期物的原因之一.

为了执行这些操作, 必须排定协程的运行时间, 然后使用asyncio.Task 对象包装协程. 对协程来说, 获取 Task对象有两种主要方式:

asyncio.async(coro_or_future, *, loop=None)

这个函数统一了协程和期物: 第一个参数可以是二者中的任何一个. 如果是Future 或者 Task对象, 那就原封不动的返回,. 如果是协程, 那么async 函数 会调用 loop.create_task(...) 方法创建 Task对象. loop= 关键字参数是可选的, 用于传入事件循环; 如果没有传入, 那么async 函数会通过调用asyncio.get_event_loop() 函数获取循环对象.

BaseEventLoop.create_task(coro)

这个方法排定协程的执行时间, 返回一个asyncio.Task对象. 如果在自定义的 BaseEventLoop 子类上调用, 返回的对象可能是外部库(Tornado)中与Task类兼容的某个类的实例.
> BaseEventLoop.crate_task(...)方法只在Python 3.4.2 以上版本中使用. 如果是 Python 3.3 或者Python 3.3 旧版本, 要使用 asyncio.async(...) 函数

asyncio包中有多个函数会自动(内部使用的是asyncio.async 函数)把参数指定的协程在asyncio.Task 对象中, 例如 BaseEventLoop.run_until_complete(...)方法.


asyncio.wait(...) 协程的参数是一个由期物或者西城构成的可迭代对象; wait 会分别把各个协程包装进一个Task 对象. 最终的结果是, wait 处理的所有对象都是通过某种方式编程Future类的实例. wait是协程函数, 因此返回的是一个协程或生成器对象; wait_coro 变量中存储的正式这种对象. 为了驱动协程, 我们把协程传递给 loop.run_until_complete(...)方法.

loop.run_until_complete(...) 方法的参数是一个期物或协程. 如果是协程, run_until_complete 方法与wait函数一样, 把协程包装进一个Task 对象中. 协程, 期物的任务都能由 yield from 驱动, 这正是 run_until_complete 方法对 wait 函数返回的 wait_coro 对象所做的事. wait_coro 运行结束后返回一个元组, 第一个元素是系列结束的期物, 第二个元素是一系列未结束的期物.


* 我们编写的协程链条始终通过把外层委派生成器传给 asyncio包中API中某个函数(如 loop.run_until_complete(...))驱动. 也就是说, 使用asyncio包时, 我们别的代码不通过调用next(...)函数或者`.send(...)`方法驱动协程---这一点由asyncio 包 实现的事件循环去做.
* 我们编写的协程链条最终通过 yield from 把职责委派给asyncio 包中的某个协程函数货协程方法, 或者其他库中实现高层协议的协程. 也就是说, 最内层的子生成器是库中真正执行I/O操作的函数, 而不是我们自己编写的函数.


在上面的实例中, 阻塞性函数是 save_flag. 这个脚本在线程版本中, save_flag函数会阻塞运行 download_one 函数的线程, 但是阻塞的只是众多工作线程中的一个. 阻塞型 I/O 调用的在背后会释放GIL, 因此另一个线程可以继续. 但是在flags2_asynico 脚本中, save_flag函数阻塞了客户代码与asyncio事件循环公用的唯一线程, 因此保存文件时, 整个应用程序都会冻结. 这个问题的解决方法是, 使用事件循环的 run_in_executor 方法.


asyncio 的事件循环在背后维护了一个 ThreadPoolExecutor 对象, 我们可以调用 run_in_executor 方法, 把可调用的对象发给它执行.
