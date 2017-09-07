# Python的迭代器
---

## 什么是迭代
> 迭代是重复反馈过程的活动, 其目的通常是为了接近并达到所需的目标或者结果.每一次对过程的重复被称之为一次*迭代*,而每一次迭代得到的结果会被用来作为下次迭代的初始值.

## 迭代对象(iterable)

在python中,迭代通常是通过`for ... in ...`来完成的,而且只要是可迭代对象(`iterable`),都能进行迭代.这里简单讲下`iterable`与`iterator`的区别:

> `iterable`是实现了`__iter__()`方法的对象.更确切的说,是`container.__iter__()`方法,该方法返回的是的一个`iterator`对象,因此`iterable`是你可以从其获得`iterator`的对象.使用`iterable`时,将一次性返回所有结果,都存放在内存中,并且这些值都能重复使用.



> `iterator`是实现了`itetor.__iter__()`和`iterator.__next__()`方法的对象.`iterator.__iter__()`方法返回的是`iterator`对象本身.根据官方的说法,正是这个方法,实现了`for ... in ...`语句.而`iterator.__next__()`是iterator区别于iterable的关键了.当调用next()方法时,实际上产生了2个操作:

1. 更新iterator状态, 令其指向后一项, 以便下次调用
2. 返回当前结果.

正是`__next__()`,使得`iterator`能在每次被调用时,返回一个单一的值(有些教程里,称为一边循环,一边计算,我觉得这个说法不是太准确.但如果这样的说法有助于你的理解,我建议你就这样记),从而极大的节省了内存资源.另一点需要格外注意的是,`iterator`是消耗型的,即每一个值被使用过后,就消失了.因此,你可以将以上的操作2理解成`pop`.对`iterator`进行遍历之后,其就变成了一个空的容器了,但不等于`None`哦.因此,若要重复使用`iterator`,利用`list()`方法将其结果保存起来是一个不错的选择.


```python
>>> from collections import Iterable, Iterator
>>> a = [1,2,3]   # 众所周知,list是一个iterable
>>> b = iter(a)   # 通过iter()方法,得到iterator,iter()实际上调用了__iter__(),此后不再多说
>>> isinstance(a, Iterable)
True
>>> isinstance(a, Iterator)
False
>>> isinstance(b, Iterable)
True
>>> isinstance(b, Iterator)
True
# 可见,iterable是iterator,但iterator不一定是iterable

# iterator是消耗型的,用一次少一次.对iterator进行变量,iterator就空了!
>>> c = list(b)
>>> c
[1, 2, 3]
>>> d = list(b)
>>> d
[]


# 空的iterator并不等于None.
>>> if b:
...   print(1)
...
1
>>> if b == None:
...   print(1)
...

# 再来感受一下next()
>>> e = iter(a)
>>> next(e)     #next()实际调用了__next__()方法,此后不再多说
1
>>> next(e)
2

```

既然提到了`for ... in ...`语句,我们再来简单讲下其工作原理吧,或许能帮助理解以上所讲的内容.

```python
>>> x = [1, 2, 3]
>>> for i in x:
...     ...
```

我们对一个`iterable`用`for ... in ...`进行迭代时,实际是先通过调用`iter()`方法得到一个`iterator`,假设叫做X.然后循环地调用X的`next()`方法取得每一次的值,直到`iterator`为空,返回的S`topIteration`作为循环结束的标志.`for ... in ... `会自动处理`StopIteration`异常,从而避免了抛出异常而使程序中断.如图所示
![f ](img/for-in.png)

## 迭代器的优点
迭代器最大的好处是定义了统一的访问容器（或集合）的统一接口，所以程序员可以随时定义自己的迭代器，只要实现了迭代器协议就可以。除此之外，迭代器还有惰性求值的特性，它仅可以在迭代至当前元素时才计算（或读取）该元素的值，在此之前可以不存在，在此之后可以销毁，也就是说不需要在遍历之前事先准备好整个迭代过程中的所有元素，所以非常适合遍历无穷个元素的集合（如斐波那契数列）或巨大的事物（如文件）。

```python
class Fib(object):
    def __init__(self):
        self._a = 0
        self._b = 0

    def __iter__(self):
        return self

    def next(self):
        self._a, self._b = self._b, self._a + self._b
        return self._a


for i, f in enumerate(Fib()):
    print f
    if i > 10:
       break
```
