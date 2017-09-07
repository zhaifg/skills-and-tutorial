# Python生成器
---

## generator与yield

来理解generator与yield将会事半功倍.

首先先理清几个概念:

> `generator`: A function which returns a generator iterator. It looks like a normal function except that it contains yield expressions for producing a series of values usable in a for-loop or that can be retrieved one at a time with the next() function.
`generator iterator`: An object created by a generator funcion.
`generator expression`: An expression that returns an iterator.


以上定义来自Python官方文档. 可见我们常说的`生成器`,就是带有`yield`的函数,而`generator iterator`则是`generator function`的返回值, 即一个`generator`对象,而形如`(elem for elem in range(3))`的表达式,称为`generator expression`, 实际使用与`generator`无异.

```python
a = (elem for elem in range(3))
<generator object <genexpr> at 0x7f774c0e2cd0>

def fib():
    a, b = 0,1
    while True:
        yield  b
        a,b =b, a+b
fib
<function __main__.fib>

b=fib()
<generator object fib at 0x15da140>

```
其实,说白了,`generator`就是`iterator`的一种, 以更优雅的方式实现的`iterator`.

>Python’s generators provide a convenient way to implement the iterator protocol.

你完全可以像使用`iterator`一样使用`generator`,当然除了定义.定义一个`iterator`,你需要分别实现`__iter__()`方法和`__next__()`方法,但`generator`只需要一个小小的`yield`(好吧,`generator expression`的使用比较简单,就不展开讲了.)

前文讲到`iterator`通过`__next__()`方法实现了每次调用,返回一个单一值的功能.而`yield`就是实现`generator`的`__next__()`方法的关键!先来看一个最简单的例子:

```python
n [8]: def g():
   ...:     print "1 is"
   ...:     yield 1
   ...:     print "2 is"
   ...:     yield 2
   ...:     print "3 is"
   ...:     yield 3
   ...:     

In [9]: z = g()

In [10]: next(z)
1 is
Out[10]: 1

In [11]: next(z)
2 is
Out[11]: 2

In [12]: next(z)
3 is
Out[12]: 3

In [13]: next(z)
---------------------------------------------------------------------------
StopIteration                             Traceback (most recent call last)
<ipython-input-13-7b32f85a2b4e> in <module>()
----> 1 next(z)

StopIteration:

```


第一次调用`next()`方法时,函数似乎执行到`yield 1`,就暂停了.然后再次调用`next()`时,函数从`yield 1`之后开始执行的,并再次暂停.第三次调用`next()`,从第二次暂停的地方开始执行.第四次,抛出`StopIteration`异常.

事实上,`generator`确实在遇到`yield`之后暂停了,确切点说,是先返回了`yield`表达式的值,再暂停的.当再次调用`next()`时,从先前暂停的地方开始执行,直到遇到下一个`yield`.这与上文介绍的对`iterator`调用`next()`方法,执行原理一般无二.

有些教程里说`generator`保存的是算法,
而我觉得用`中断服务子程序`来描述`generator`或许能更好理解,这样你就能将`yield`理解成一个中断服务子程序的断点,没错,是中断服务子程序的断点.我们每次对一个`generator`对象调用`next()`时,函数内部代码执行到`”断点`”`yield`,然后返回这一部分的结果,并保存上下文环境,”中断”返回.

怎么样,是不是瞬间就明白了`yield`的用法?

我们再来看另一段代码:

```python
In [25]: def gen():
   ....:     while True:
   ....:         s = yield
   ....:         print s
   ....:         

In [26]: g = gen()

In [27]: g.send("sss")
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-27-c3cf34a27543> in <module>()
----> 1 g.send("sss")

TypeError: can't send non-None value to a just-started generator

In [28]: next(g)

In [29]: g.send("xxxx")
xxxx

In [30]: g.send("xxxx")
xxxx

In [31]: next(g)
None

```

`genera`有两种调用方法(恢复执行),集通过`send(value)`方法将`value`作为`yield`表达式的当前值,你可以用该值再对其他变量进行赋值,这段代码就很好理解了. 当我们调用`send(value)`方法时, `generator`正由于`yield`的缘故被暂停了. 此时,`send(value)`方法传入的值作为`yield`表达式的值,函数中又将该值赋给变量`s`,然后`print`打印, 循环在遇到`yield`,暂停返回.

调用`send(value)`时需要注意,确保`generator`是在`yield`处被暂停.如此才能想`yield`表达式传值,否则将会报错(如上所示), 可以通过`next()`方法或者`send(None)`使`generator`执行到`yield`.

再来看一段`yield`更复杂的用法,或许能加深你对`generator`的`next()`与`send(value)`的理解.

```python
In [43]: def echo(value=None):
   ....:     while 1:
   ....:         value = (yield value)
   ....:         print "The value is", value
   ....:         if value:
   ....:             value +=1
   ....:             

In [44]: g=echo(1)

In [45]: next(g)
Out[45]: 1

In [46]: g.send(2)
The value is 2
Out[46]: 3

In [47]: g.send(5)
The value is 5
Out[47]: 6

In [48]: next(g)
The value is None
```

上述代码既有yield value的形式,又有value = yield形式, 看起来有点复杂.但以yield分离代码进行解读, 就不太难了. 第一次调用next()方法,执行到`yield value`表达式,保存上下文环境暂停返回1; 第二次调用`send(value`方法,从`value = yield`开始,打印,再次遇到`yield value`暂停返回,后续调用`send(value)`或者`next()`.

这里引出了另一个问题,`yield`作为暂停恢复的点,代码从`yield`处恢复, 又在下一个`yield`处暂停. 可见,在一次`next()`(非首次)或`send(value)`调用过程中,实际上存在两个`yield`, 一个作为恢复点的`yield`与另一个作为暂停点的`yield`.因此,也就有两个`yield`表达式.`send(value)`方法是将值传给恢复点的`yield`;调用`next()`表达式的值时, 其恢复点`yield`的值总是`None`, 而将暂停点的`yield`表达式值返回.为方便记忆,可以将此处的恢复点记作当前的 (current), 而将暂停点记作下一次的(next),这样就与next()方法匹配起来了.

`generator`还实现了另外两个方法`throw(type[,value,[traceack]])`与`close()`;前者用于抛出异常,后者用于关闭`generator`.不过这2个方法似乎很少被直接用到,本文就不再多说了.

### throw(type[,value,[traceack]])
```python
def mygen():
  try:
    yield 'something'
  except ValueError:
    print 'clean'

gg=mygen()
print gg.next()
print gg.throw(ValueError)
```

调用gg.next很明显此时输出‘something’,并在yield ‘something’暂停，此时向gg发送ValueError异常，恢复执行环境，except  将会捕捉，并输出信息。

理解了这些，我们就可以向协同程序发起攻击了，所谓协同程序也就是是可以挂起，恢复，有多个进入点。其实说白了，也就是说多个函数可以同时进行，可以相互之间发送消息等。

这里有必要说一下multitask模块(不是标准库中的),看一段multitask使用的简单代码：
```python
def tt():
  for x in xrange(4):
    print 'tt'+str(x)
    yield

def gg():
  for x in xrange(4):
    print 'xx' +  str(x)
    yield

t = multitask.TaskManager()
t.add(tt())
t.add(gg())
t.run()

```

```
tt0
xx0
tt1
xx1
tt2
xx2
tt3
xx3
```
如果不是使用生成器，那么要实现上面现象，即函数交错输出，那么只能使用线程了，所以生成器给我们提供了更广阔的前景

如果仅仅是实现上面的效果，其实很简单，我们可以自己写一个。主要思路就是将生成器对象放入队列，执行send(None)后，如果没有抛出StopIteration,将该生成器对象再加入队列。
```python
class Task():
    def __init__(self):
        self._queue = Queue.Queue()

    def add(self,gen):
        self._queue.put(gen)

    def run(self):
        while not self._queue.empty():
            for i in xrange(self._queue.qsize()):
                try:
                    gen= self._queue.get()
                    gen.send(None)
                except StopIteration:
                    pass
                else:
                    self._queue.put(gen)

t=Task()
t.add(tt())
t.add(gg())
t.run()

```

当然，multitask实现的肯定不止这个功能，有兴趣的童鞋可以看下源码，还是比较简单易懂的。




面试Python时遇到这么一道题目：

```python
def thread1():
    for x in range(4):
        yield  x


def thread2():
    for x in range(4,8):
        yield  x


threads=[]
threads.append(thread1())
threads.append(thread2())


def run(threads): #写这个函数，模拟线程并发
    pass

run(threads)
```




如果上面class Task看懂了，那么这题很简单，其实就是考你用yield模拟线程调度，解决如下：

```python
def run(threads):
    for t in threads:
        try:
            print t.next()
        except StopIteration:
            pass
        else:
            threads.append(t)

```

## 迭代器和生成器小结

![ddd](img/iterators-generators-iterables.png)

1. 可迭代对象(Iterable)是实现了`__iter__()`方法的对象,通过调用`iter()`方法可以获得一个迭代器(Iterator)
2. 迭代器(Iterator)是实现了`__iter__()`和`__next__()`的对象
3. `for ... in ...`的迭代,实际是将可迭代对象转换成迭代器,再重复调用`next()`方法实现的
4. 生成器(generator)是一个特殊的迭代器,它的实现更简单优雅.
5. `yield`是生成器实现`__next__()`方法的关键.它作为生成器执行的暂停恢复点,可以对`yield`表达式进行赋值,也可以将yield表达式的值返回.

## 应该阅读的文档

https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do-in-python
