# Python 高阶函数
---


在Python3 中map 和 filter 都返回一个生成器, Python2 中reduce 在内置函数中, 到了Python3 中 放到了 functools 模块中.


## map

## filter

## reduce

## apply(Python3 已删除)

## all
all(iterable): 如果iterable 的每个元素都是真值, 返回True; `all([])` 返回True

## any(iterable)
只要 iterable 中有元素是真值, 就返回True; `any([])` 返回 False

## lambda
匿名函数
lambda 只是语法糖, 跟def 语句一样,  lambda 表达式会创建函数对象. 

## 可调用对象
除了 用户定义的函数, 调用运算符即`()` 还可以应用到其他对象上. 如果想判断对象是否调用, 可以使用内置的 `callable()` 函数.

### 类的实例
如果类定义了 `__call__` 方法, 那么它的实例可以用作为函数调用

## 函数内省
