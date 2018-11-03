# futures 
---

`class concurrent.futures.Executor`:
提供异步执行调用的方法的抽象类。
- `submit(fn, *args, **kwargs)`: 计划调度执行 fn函数，执行方式 fn(*args, **kwargs), 返回一个可以执行 Future 对象。
```
with ThreadPoolExecutor(max_worker=1) as executor:
    future = executor.submit(pow, 323, 1235)
    print(future.result())
```

- map(func, *iterable, timeout=None, chunksize=1): 
相当于 map(func, *iterable),除了这个函数是异步执行，多次调用函数可以同时。返回的迭代器 会抛出一个  concureent.futures.TimeoutError 如果`__next__()` 如果 执行时间超时的话。 `timeout` 是一个 int 或者float; 如果 timeout 没有被指定， 就是不限制等待时间。很长的可迭代对象，采用大值分片能明显比1的默认大小提高性能。用线程池，分片大小没有影响。

- shutdown(wait=True): 


Deadlocks can occur when the callable associated with a Future waits on the results of another Future. For example:

`class concurrent.futures.ThreadPoolExecutor(max_workers=None, thread_name_prefix='')`


`ProcessPoolExecutor(max_workers=None)`

`class concurrent.futures.Future`:
- cancel()
- cancelled()
- running()
- done()
- result(timeout=None)
- exception(timeout=None)
- add_done_callback(fn)
- set_running_or_notify_cancel()
- set_result(result)
- set_exception(exception)

## 模块方法
- concurrent.futures.wait(fs, timeout=None, return_when=ALL_COMPLETED)
- concurrent.futures.as_completed(fs, timeout=None)


exception concurrent.futures.CancelledError
exception concurrent.futures.TimeoutError
exception concurrent.futures.process.BrokenProcessPool