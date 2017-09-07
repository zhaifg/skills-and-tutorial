# Python functools 包偏函数
---
通过设定参数的默认值, 可以降低函数调用的难度.
当一个函数有很多参数时, 调用者就需要提供多个参数, 如果减少参数个数, 就可以简化调用者的负担.
比如int()函数可以把字符串转换成整数, 默认为10进制的转换, 如果base参数设置N则为N进制的转换.

```
In [9]: int('223344', base=8)
Out[9]: 75492

In [10]: int('223344', 8)
Out[10]: 75492

In [11]: int('223344', 16)
Out[11]: 2241348

In [13]: int('100110111', 2)
Out[13]: 311

```
现在有大量的二进制的字符串要转换, 每次传入int(x, base=2)非常麻烦, 于是想到可以定义一个int2()的函数, 默认值base=2
```
def int2(x, base=2):
    return int(x, base)
# 于是
int2('11110000')

```
functools.partial就是帮助我们创建一个偏函数的, 不需要我们自己定义int2()函数, 直接使用下面的代码创建新的int2:
```
In [14]: int2 = functools.partial(int, base=2)

In [15]: int2('111100110011')
Out[15]: 3891

```
所以, function.partial可以把一个参数多的函数变成一个函数参数少的新函数, 少的参数的函数需要在创建时指定默认值, 这样,新函数调用的难度就降低了.

## 例子
我们在sorted这个高阶函数中传入自定义排序函数就可以实现忽略大小写排序。请用functools.partial把这个复杂调用变成一个简单的函数：
```
import functools
sorted_ignore_case = functools.partial(sorted, key=str.upper)
print sorted_ignore_case(['bob', 'about', 'Zoo', 'Credit'])
#=====
['about', 'bob', 'Credit', 'Zoo']
```

## update_wrapper(wrapper, wrapped[, assigned][, updated])
看这个函数的源代码发现，它就是把被封装的函数的 module, name, doc 和 dict 复制到封装的函数中去，源码如下，很简单的几句：
```

WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__doc__')
WRAPPER_UPDATES = ('__dict__',)
def update_wrapper(wrapper,
                   wrapped,
                   assigned = WRAPPER_ASSIGNMENTS,
                   updated = WRAPPER_UPDATES):
    for attr in assigned:
        setattr(wrapper, attr, getattr(wrapped, attr))
    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
    return wrapper
```

## functools.wraps(wrapped[, assigned][, updated])
This is a convenience function for invoking update_wrapper() as a function decorator when defining a wrapper function. It is equivalent to partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated). For example:
```

>>> from functools import wraps
>>> def my_decorator(f):
...     @wraps(f)
...     def wrapper(*args, **kwds):
...         print 'Calling decorated function'
...         return f(*args, **kwds)
...     return wrapper
...
>>> @my_decorator
... def example():
...     """Docstring"""
...     print 'Called example function'
...
>>> example()
Calling decorated function
Called example function
>>> example.__name__
'example'
>>> example.__doc__
'Docstring'
```
