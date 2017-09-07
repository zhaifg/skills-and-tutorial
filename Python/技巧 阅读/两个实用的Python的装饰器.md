# 两个实用的Python的装饰器
---

## 超时函数
这个函数的作用在于可以给任意可能会hang住的函数添加超时功能，这个功能在编写外部API调用 、网络爬虫、数据库查询的时候特别有用
```python
import signal, functools

class TimeoutError(Exception): pass

def timeout(seconds, error_message = "Function call time out"):
    def decorated(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        @functools.wraps
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _hendle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wrapper
```

```
@timeout(5)
def slowfunc(sleep_time):
    import time
    time.sleep(sleep_time)

slowfunc(4)
slowfunc(7)
```

## trace 函数
有时候处于演示的目的或者调试的目的, 我们需要程序运行的时候打印出每一步运行顺序 和调用逻辑, 类似bash -x功能.

```python
import sys, os, linecache

def trace(f):
    def globaltrace(frame, why, arg):
        if why == "call":
            return localtrace
        return None

    def localtrace(frame, why, arg):
        if why == 'line':
            filename = frame.f_code.co_filename
            lineno = frame.f_lineno
            bname = os.path.basename(filename)
            print "{}({})".format(bname, lineno,
                        linecache.getline(filename, lineno).strip('\r\n'))
        return localtrace

    def _f(*args, **kwargs):
        sys.settrace(globaltrace)
        result = f(*args, **kwargs)
        sys.settrace(None)
        return result
    return _f

@trace
def main():
    print 1
    print "xxxx"
```


https://zhuanlan.zhihu.com/p/20175869?columnSlug=auxten
