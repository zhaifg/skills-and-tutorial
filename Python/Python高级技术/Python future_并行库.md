# concurrent.futures


```py
from  concurrent import futures

def download_one(cc):
    pass

def download_many(cc_list):
    with futures.ThreadExecutor(5) as executor:
        res = executor.map(download_one, cc_list)
    return len(list(res))
```

concurrent.futures 模块主要是特色是ThreadPoolExecutor 和 ProcessPoolExecutor  类, 这个两个类实现的接口能分别在不同下城或者进程中执行可调用对象. 这两个类内部维护者一个工作线程或工作进程池, 以及要执行的任务队列.

从Python3.4起, 标准库中有两个为Future的类: concurrent.futures.Future 和 asyncio.Future. 这两个类的实例都表示可能已完成或者尚未完成的延迟计算. 这与Twisted 引擎中的Deferred 类, Tornado 框架中的Future类, 一个多个Javascript库中的Promise对象类似.

要处理的对象装载完成的操作, 可以放入队列, 或者完成的状态可以查询, 得到结果(或者抛出异常)后可以获取结果(或异常)

通常情况下自己不应该创建 要处理的对象(期物), 而只能由并发框架(concurrent.futures或asyncio) 实例化. 原因很简单:  期物 表示终将发生的事情, 而确定某件事会发生的唯一方式是执行的时间已经排定. 因此. 只有排定把某件事交给concurrent.futures.Executor 子类处理时, 才会创建 concurrent.futures.Future 实例. 例, Executor.submit() 方法的参数是一个可调用的对象, 调用这个方法后会为传入的可调用对象排期, 并返回一个 期物.

客户端代买不应该改变期物的状态, 并发框架在期物表示的延迟计算结束后会改变期物的状态, 而我们无法控制计算何时结束

这两种期物的都有 .done() 方法, 这个方法不阻塞, 返回值是布尔值, 指明期物连接的可调用对象是否已经执行. 客户端代码通常不会询问期物是否运行结束, 而是会等待通知. 因此, 两个Future 类都有 .add_done_callback() 方法: 这个方法只有一个参数, 类型是可调用的对象, 期物运行结束后会调用指定的可调用对象.

此外, 还有 .result() 方法. 在期物运行结束后调用的话, 这个方法会在两个Future类中的作用相同: 返回可调用对象的结果, 或者重新抛出执行可调用的对象时抛出的异常. 可是, 如果期物没有运行结束, result 方法在两个 Future 类中的行为相差很大. 对 concurrency.futures.Future实例来说, 调用f.result() 方法会阻塞调用方所在的线程, 直到结果可返回. 此时, result方法可以接受可选的 timeout 参数, 如果在指定的时间内 期物没有运行完毕, 会抛出 TimeoutError 异常. asyncio.Future.result 方法不支持设定超时时间, 在那个库中获取期物的结果最好使用 yield from 结构. 不过, 对concurrent.futures.Future  实例不能这么做.

这两个库中有几个函数会返回期物, 其他函数则使用期物, 用户易于理解的方式实现自身. 如 Executor.map 方法输入后者: 返回值是一个迭代器, 迭代器的 `__next__` 方法调用各个期物的result 方法, 因此我们得到的是各个期物的结果, 而非期物本身.

为了从实用的角度理解期物, 我们可以谁可以使用 concurrent.futures.as_completed 函数. 可以使用 as_completed 重写上面的代码, 返回值是一个迭代对象, 在期物运行结束后产出期物.

为了使用 futures.as_completed 函数, 只需修改download_many 函数, 把较抽象的 executor.map 调用换成 两个for循环: 一个用于创建并排定期物, 另一个用于获取期物的结果.
```py
def  download_many(cc_list):
    cc_list = cc_list[:5]
    with futures.ThreadPoolExecutor(max_worker=4) as executor:
        to_do = []
        for cc in sorted(cc_list):
            future = executor.submit(download_one, cc) # 排定可调用对象的执行时间, 然后返回一个期物, 表示这个待执行的操作
            to_do.append(future)
            msg = 'Scheduled for {}: {}'
            print(msg.format(cc, future))

        results = []
        for future in futures.as_completed(to_do):
            res = future.result()
            msg = '{} result: {!r}'
            print(msg.format(future, res))
            results.append(res)

        return len(results)
```
