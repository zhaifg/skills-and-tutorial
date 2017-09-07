#Python的上下文管理器(with)
---

上下文管理器是Python 2.5开始支持的一种语法, 用于规定某个对象的使用范围. 一旦进入或者离开使用范围, 会有特殊操作被调用(比如对象分配或者释放内存). 语法形式`with ...as`.

例如：当需要操作文件或数据库的时候，首先需要获取文件句柄或者数据库连接对象，当执行完相应的操作后，需要执行释放文件句柄或者关闭数据库连接的动作。

又如，当多线程程序需要访问临界资源的时候，线程首先需要获取互斥锁，当执行完成并准备退出临界区的时候，需要释放互斥锁。

对于这些情况，Python中提供了上下文管理器（Context Manager）的概念，可以通过上下文管理器来定义/控制代码块执行前的准备动作，以及执行后的收尾动作。


## 上下文管理器的概念

**上下文管理协议**(context Manager Protocol): 包含方法`__enter__()` 和 `__exit__()`, 支持该协议的对象要要实现这个方法.

__上下文管理器__: 支持上下文管理协议的对象, 这种对象实现了`__enter__()`与`__exit__()`方法. 上下文管理器定义执行with语句时要建立的运行的上下文, 负责执行的with语句块上下文的进入和退出操作. 通常使用with 语句调用上下文管理器, 也可以通过直接调用其方法来使用.

__运行时上下文__: 由上下文管理器创建, 通过上下文管理器的`__enter__()`和`__exit__()`实现,`__enter__()` 方法在语句体执行之前进入运行时上下文，`__exit__()` 在
语句体执行完后从运行时上下文退出。with 语句支持运行时上下文这一概念。

__上下文表达式__ : with 语句中跟在关键字之后的表达式, 该表达式要返回一个上下文管理器对象.

__语句体__ :with 语句包括起来的代码, 在执行与举起之前会调用上下文管理器的`__enter__()`方法, 执行完语句后会执行`__exit__()`方法.


```
with context_expression [as target(s)]:
   with-body
```

## 怎么使用上下文管理器

如何使用上下文管理器？

看代码是最好的学习方式，来看看我们通常是如何打开一个文件并写入"Hello World"？

```
filename = "my_file.txt"
mode = "w" # Mode that allows to write to the file
writer = open(filename, mode)
writer.write("Hello ")
writer.write("World")
writer.close()
```
1-2行，我们指明文件名以及打开方式(写入)。

第3行，打开文件，4-5行写入"Hello world"，第6行关闭文件。

这样不就行了，为什么还需要上下文管理器？但是我们忽略了一个很小但是很重要的细节：如果我们没有机会到达第6行关闭文件，那会怎样？

举个例子，磁盘已满，因此我们在第4行尝试写入文件时就会抛出异常，而第6行则根本没有机会执行。

当然，我们可以使用try-finally语句块来进行包装：

```
writer = open(filename, mode)
try:
    writer.write("Hello ")
    writer.write("World")
finally:
    writer.close()
```
finally语句块中的代码无论try语句块中发生了什么都会执行。因此可以保证文件一定会关闭。这么做有什么问题么？当然没有，但当我们进行一些比写入`Hello world`更复杂的事情时，try-finally语句就会变得丑陋无比。例如我们要打开两个文件，一个读一个写，两个文件之间进行拷贝操作，那么通过with语句能够保证两者能够同时被关闭。

OK，让我们把事情分解一下：

首先，创建一个名为“writer”的文件变量。

然后，对writer执行一些操作。

最后，关闭writer。

这样是不是优雅多了？

```python
with open(filename, mode) as writer:
    writer.write("Hello") 
    writer.write("World")
```
让我们深入一点，`with`是一个新关键词，并且总是伴随着上下文管理器出现。`open(filename, mode)`曾经在之前的代码中出现。`as`是另一个关键词，它指代了从`open`函数返回的内容，并且把它赋值给了一个新的变量。`writer`是一个新的变量名。

2-3行，缩进开启一个新的代码块。在这个代码块中，我们能够对writer做任意操作。这样我们就使用了`open`上下文管理器，它保证我们的代码既优雅又安全。它出色的完成了try-finally的任务。

open函数既能够当做一个简单的函数使用，又能够作为上下文管理器。这是因为open函数返回了一个文件类型(file type)变量，而这个文件类型实现了我们之前用到的write方法，但是想要作为上下文管理器还必须实现一些特殊的方法，我会在接下来的小节中介绍


## 自定义上下文管理器


当一个对象被用作上下文管理器时：

`__enter__` 方法将在进入代码块前被调用。

`__exit__` 方法则在离开代码块之后被调用(即使在代码块中遇到了异常)。

下面是上下文管理器的一个例子，它分别进入和离开代码块时进行打印。

```python

class PypixContextManagerDemo:

    def __enter__(self):
        print "Entering the contextManager"

    def __exit__(self, *unused):
        print "Exiting the contextManager"


with PypixContextManagerDemo():
    print "In the block"
```

```
Entering the contextManager
In the block
Exiting the contextManager
[Finished in 0.3s]
```

注意一些东西：

1. 没有传递任何参数。
2. 在此没有使用“as”关键词。
3. 稍后我们将讨论__exit__方法的参数设置。

我们如何给一个类传递参数？其实在任何类中，都可以使用`__init__`方法，在此我们将重写它以接收两个必要参数(filename, mode)。

当我们进入语句块时，将会使用open函数，正如第一个例子中那样。而当我们离开语句块时，将关闭一切在__enter__函数中打开的东西。

```python
class PypixOpen:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

 def __enter__(self):
        self.openedFile = open(self.filename, self.mode)
        return self.openedFile
 
    def __exit__(self, *unused):
        self.openedFile.close()
 
with PypixOpen(filename, mode) as writer:
    writer.write("Hello World from our new Context Manager!")
```


3-5行，通过__init__接收了两个参数。
7-9行，打开文件并返回。
12行，当离开语句块时关闭文件。
14-15行，模仿open使用我们自己的上下文管理器。

除此之外，还有一些需要强调的事情：

__如何处理异常__

我们完全忽视了语句块内部可能出现的问题。

如果语句块内部发生了异常，`__exit__`方法将被调用，而异常将会被重新抛出(`re-raised`)。当处理文件写入操作时，大部分时间你肯定不希望隐藏这些异常，所以这是可以的。而对于不希望重新抛出的异常，我们可以让`__exit__`方法简单的返回True来忽略语句块中发生的所有异常(大部分情况下这都不是明智之举)。

我们可以在异常发生时了解到更多详细的信息，完备的`__exit__`函数签名应该是这样的：
```
def __exit__(self, exc_type, exc_val, exc_tb)
```

这样__exit__函数就能够拿到关于异常的所有信息(异常类型，异常值以及异常追踪信息)，这些信息将帮助异常处理操作。在这里我将不会详细讨论异常处理该如何写，以下是一个示例，只负责抛出SyntaxErrors异常。
```
class RaiseOnlyIfSyntaxError:
 
    def __enter__(self):
        pass
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        return SyntaxError != exc_type
```

实例
```
import time
 
class MyTimer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def __enter__(self):
        print "enter now"
        self.start = time.time()
        return self

    def __exit__(self, *unused):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000
        if self.verbose:
            print 'elapsed time: %f ms' % self.msecs


def fib(n):
    if n in [1, 2]:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


with MyTimer(True):
    print fib(30)
```

```
enter now
832040
elapsed time: 321.000099 ms
```


__异常处理和__exit__

在使用上下文管理器中，如果代码块 （with_suite）产生了异常，__exit__方法将被调用，而__exit__方法又会有不同的异常处理方式。

当`__exit__`方法退出当前运行时上下文时，会并返回一个布尔值，该布尔值表明了`如果代码块 （with_suite）执行中产生了异常，该异常是否须要被忽略`。

1.` __exit__`返回False，重新抛出(`re-raised`)异常到上层

修改前面的例子，在MyTimer类型中加入了一个参数`ignoreException`来表示上下文管理器是否会忽略代码块 （with_suite）中产生的异常。

```
import time
 
class MyTimer(object):
    def __init__(self, verbose = False, ignoreException = False):
        self.verbose = verbose
        self.ignoreException = ignoreException
 
    def __enter__(self):
        self.start = time.time()
        return self
 
    def __exit__(self, *unused):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000
        if self.verbose:
            print "elapsed time: %f ms" %self.msecs
        return self.ignoreException
 
try:        
    with MyTimer(True, False):
        raise Exception("Ex4Test")
except Exception, e:
    print "Exception (%s) was caught" %e
else:
    print "No Exception happened"
```

运行这段代码，会得到以下结果，由于__exit__方法返回False，所以代码块 （with_suite）中的异常会被继续抛到上层代码。
```
elapsed time: 0.000000 ms
Exception (Ex4Test) was caught
```

__exit__返回Ture，代码块 （with_suite）中的异常被忽略

将代码改为__exit__返回为True的情况：
```
try:        
    with MyTimer(True, True):
        raise Exception("Ex4Test")
except Exception, e:
    print "Exception (%s) was caught" %e
else:
    print "No Exception happened"
```

```
elapsed time: 0.000000 ms
No Exception happened
```

一定要小心使用`__exit__`返回Ture的情况，除非很清楚为什么这么做。

__通过__exit__函数完整的签名获取更多异常信息__

对于`__exit__`函数，它的完整签名如下，也就是说通过这个函数可以获得更多异常相关的信息。

`__exit__(self, exception_type, exception_value, traceback)`
继续修改上面例子中的__exit__函数如下：
```
def __exit__(self, exception_type, exception_value, traceback):
    self.end = time.time()
    self.secs = self.end - self.start
    self.msecs = self.secs * 1000
    if self.verbose:
        print "elapsed time: %f ms" %self.msecs
 
    print "exception_type: ", exception_type
    print "exception_value: ", exception_value
    print "traceback: ", traceback
 
    return self.ignoreException
```


本文介绍了Python中的上下文管理器，以及如何结合with语句来使用上下文管理器。

总结一下with 语句的执行流程：

1. 执行context_expr 以获取上下文管理器对象
2. 调用上下文管理器的 `__enter__()` 方法
  * 如果有 as var 从句，则将 `__enter__()` 方法的返回值赋给 var
3. 执行代码块 with_suite
4. 调用上下文管理器的 `__exit__()` 方法，如果 with_suite 产生异常，那么该异常的 type、value 和 traceback 会作为参数传给 `__exit__()`，否则传三个 None
  - 如果 with_suite 产生异常，并且 `__exit__()` 的返回值等于 False，那么这个异常将被重新抛出到上层
  - 如果 with_suite 产生异常，兵器 `__exit__()` 的返回值等于 True，那么这个异常就被忽略，继续执行后面的代码

## 上下文库(contextlib)

contextlib是一个Python模块，作用是提供更易用的上下文管理器。

### contextlib.closing

假设我们有一个创建数据库函数，它将返回一个数据库对象，并且在使用完之后关闭相关资源(数据库连接会话等)

我们可以像以往那样处理或是通过上下文管理器：

```
with contextlib.closing(CreateDatabase()) as database:
    database.query()
```

contextlib.closing方法将在语句块结束后调用数据库的关闭方法。

### contextlib.nested

另一个很cool的特性能够有效地帮助我们减少嵌套：

假设我们有两个文件，一个读一个写，需要进行拷贝。

以下是不提倡的：
```python
with open("toReadFile", "r") as reader:
    with open("toWriteFile", "w") as writer:
        writer.writer(reader.read())
```

可以通过contextlib.nested进行简化：
```python
with contextlib.nested(open("fileToRead.txt", "r"),
                       open("fileToWrite.txt", "w")) as (reader, writer):
    writer.write(reader.read())
```

在Python2.7中这种写法被一种新语法取代：
```python
with open("fileToRead.txt", "r") as reader, \
        open("fileToWrite.txt", "w") as writer:
        writer.write(reader.read())
```

### contextlib.contextmanager

对于Python高级玩家来说，任何能够被`yield`关键词分割成两部分的函数，`都能够通过装饰器装饰的上下文管理器来实现`。`任何在yield之前的内容都可以看做在代码块执行前的操作，而任何yield之后的操作都可以放在exit函数中`。

__这里我举一个线程锁的例子__：

锁机制保证两段代码在同时执行时不会互相干扰。例如我们有两块并行执行的代码同时写一个文件，那我们将得到一个混合两份输入的错误文件。但如果我们能有一个锁，任何想要写文件的代码都必须首先获得这个锁，那么事情就好办了。如果你想了解更多关于并发编程的内容，请参阅相关文献。

下面是线程安全写函数的例子：
```python
import threading

lock = threading.Lock()

def safeWriteToFile(openedFile, content):
    lock.acquire()
    openedFile.write(content)
    lock.release()
```
接下来，让我们用上下文管理器来实现，回想之前关于yield和contextlib的分析：

```python
@contextlib.contextmanager
def loudLock():
    print "Locking"
    lock.acquire()
    yield
    print "Releasing"
    lock.release()

with loudLock():
    print "Lock is locked: %s" % lock.locked()
    print "Doing something that needs locking"

#Output:
#Locking
#Lock is locked: True
#Doing something that needs locking
#Releasing
```
特别注意，这不是异常安全(exception safe)的写法。如果你想保证异常安全，请对yield使用try语句。幸运的是threading。lock已经是一个上下文管理器了，所以我们只需要简单地：

```python
@contextlib.contextmanager
def loudLock():
    print "Locking"
    with lock:
        yield
    print "Releasing"
```

因为`threading.lock`在异常发生时会通过`__exit__`函数返回`False`，这将在`yield被调用是被重新抛出`。这种情况下锁将被释放，但对于“print ‘Releasing’”的调用则不会被执行，除非我们重写try-finally。

如果你希望在上下文管理器中使用“as”关键字，那么就用yield返回你需要的值，它将通过as关键字赋值给新的变量。
