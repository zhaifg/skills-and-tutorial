# Blinker信号的使用
---

## 什么信号

## 使用信号的好处
Blinker 提供一个简单快速的 对象-to-对象以及广播的python对象

Blinker的核心相当小, 但是具有强大的功能:
1. 命名信号的全局注册
2. 匿名信号
3. 自定义信号注册
4. 永久或临时连接的接收器
5. ...

## 信号的执行过程
信号的应用中,分为三种角色:signal, receiver, sender.

- signal: 是指一个信号的本身, 只是连接receiver和sender的信息连接信号
- receiver: 即为一个可以执行的对象, 通常是一个函数(至少有一个位置参数第一个位置参数就是send第一个位置参数传送来的对象, 通常为发送者的对象). 当接收到信号的时候会根据信号的内容进行执行处理程序.一个信号可以有多可receiver, 一个receiver可以注册到多个信号中.
- sender: 信号的发送者, 发送信号会触发订阅在信号的上receiver执行.



例如给add(x, y)函数传递一个信号'sum'信号的过程
```
sum = signal('sum')
def  add(sender, x=0, y=0):
    #print sender
    return int(x) + int(y)

@sum.connect
def  mul(sender, x=0, y=0):
    print sender
    return int(x) * int(y)

sum.connect(add)
result = sum.send(x=1,y=2)
print result

```
1. 定义一个账号: sum = signal('sum')
2. 第一个add函数
3. 定义mul函数并注册一sum信号
4. 注册add到sum信号
5. 发送一个信号.
6. receiver: add和mul接收一个,发送者为None并带有两个参数值的信号,然后执行add, mul之后返回给result一个列表.
```
[(<function mul at 0x000000000374F588>, 2), (<function add at 0x000000000374F518>, 3)]
```

## 信号去除耦合

使用命名信号
```
from blinker import signal
initalized = signal('initalized')
initalized is signal('initalized') # True
```
每个对`signal（'name'）`的调用都返回相同的信号对象，允许不连接的代码部分（不同的模块，插件，任何东西）都使用相同的信号，而不需要任何代码共享或特殊的导入。

## 订阅信号
通过`Signal.connect()` 注册一个函数, 在每次发送信号时都调用这个函数. 连接的函数总是传递注册这个函数的对象, 

```python
def subscriber(sender):
    print "Got a signal send by  %r"% sender

ready = signal('ready')
ready.connect(subscriber) #在信号ready注册一个函数
# <function __main__.subscriber>

# 发送信号
ready.send("s")
# Got a signal send by 's' 
```

## 发送信号
通过Signal.send()向所有连接到这个信号的对象发送信号.(既是执行所有连接到这个信号的对象.)

一个简单的例子, Processor类当开始执行某些东西时,发送一个`ready`信号; 当执行完成是发送一个`complete`信号. 它将self传递给send()方法, 表示特定实例负责发出信号.

```python
from blinker import signal

def subscriber(sender):
    print "Got a signal send by  %r"% sender

ready = signal('ready')
ready.connect(subscriber)

class Processor:
    def __init__(self, name):
        self.name = name
    
    def go(self):
        ready = signal('ready')
        ready.send(self)
        print "Processing ..."
        complete = signal('complete')
        complete.send(self)
    
    def __repr__(self):
        return "<Processor %s> "%self.name

processor_a = Processor('a')
processor_a.go()
```
out
```
Got a signal send by  <Processor a> 
Processing ...
```
注意go()中的`complete`信号？没有接收器去连接`complete`，这是一个确定。在没有接收器的信号上调用send()将导致不发送通知，并且这些无操作发送被优化为尽可能廉价。

## 订阅特定的发送者
无论何时sender发送它时，到信号的默认连接调用接收器功能。`Signal.connect()`函数接受一个可选参数，以限制发送给一个特定订阅对象的：

```
def b_subscriber(sender):
    print "Caught signal from process processor_b."
    assert sender.name == 'b'

processor_b = Processor('b')
ready.connect(b_subscriber, sender=processor_b)
```
b_subscriber此函数已订阅到ready上，但仅当由processor_b发送时
```
processor_a.go()
#Got a signal send by  <Processor a> 
#Processing ...

```

```
processor_b.go()
#Got a signal send by  <Processor b> 
#Caught signal from process processor_b.
#Processing ..
```

## 通过信号发送和接收数据
可以通过传递额外的参数给send(), send()传递这些参数到订阅函数.

```
send_data = signal('send-data')

@send_data.connect
def receive_data(sender, **kw):
    print "Caught signal from %r, data %r" %(sender, kw)
    return "received"

result = send_data.send('anonymous', abc=123)
print result
```

```
Caught signal from 'anonymous', data {'abc': 123}
[(<function receive_data at 0x00000000038AE278>, 'received')]
```
send()的返回值, 是一个收集了每一个注册函数的返回值列表:`[(receiver function, return value),...]`
```
print result[0][0].__name__
receive_data
```

## 匿名信号
信号不需要命名。 Signal构造函数在每次被调用时创建一个唯一的信号。例如，来自上面的Processor的替代实现可以提供处理信号作为类属性：

```
>>> from blinker import Signal
>>> class AltProcessor:
...    on_ready = Signal()
...    on_complete = Signal()
...
...    def __init__(self, name):
...        self.name = name
...
...    def go(self):
...        self.on_ready.send(self)
...        print("Alternate processing.")
...        self.on_complete.send(self)
...
...    def __repr__(self):
...        return '<AltProcessor %s>' % self.name
```

## 使用connect的装饰器连接
```
apc = AltProcessor('c')
@apc.on_complete.connect
def completed(sender):
    print "AltProcessor %s completed!" %self.name


apc.go()

```

虽然方便，但不幸的是，这种形式不允许为连接的函数定制sender或弱参数。为此，可以使用connect_via()：

```
dice_roll = signal('dice_roll')
>>> @dice_roll.connect_via(1)
... @dice_roll.connect_via(3)
... @dice_roll.connect_via(5)
... def odd_subscriber(sender):
...     print("Observed dice roll %r." % sender)
...
>>> result = dice_roll.send(3)
Observed dice roll 3.
```

## 优化信号发送
信号被优化以非常快地发送，无论接收机是否连接。如果要与信号一起发送的关键字数据计算起来很昂贵，则通过测试receiver属性可以更有效地检查是否有任何接收器先连接：
```
bool(signal('ready').receivers)

True
>>> bool(signal('complete').receivers)
False
>>> bool(AltProcessor.on_complete.receivers)
True

```

检查接收器侦听特定发送者也是可能的：
```
>>> signal('ready').has_receivers_for(processor_a)
True
```

## API
### Basic Signals
1. blinker.base.ANY = ANY
2. blinker.base.receiver_connected 
3. class blinker.base.Signal(doc=None)
  - doc – optional. If provided, will be assigned to the signal’s` __doc__` attribute.
  - ANY = ANY
  - ...

### Named Signals
1. `blinker.base.signal(name, doc=None)`: Return the NamedSignal name, creating it if required.
2. `class blinker.base.NamedSignal(name, doc=None):` Bases: blinker.base.Signal
3. `class blinker.base.Namespace`:Bases: dict
  - signal(name, doc=None): Return the NamedSignal name, creating it if required.
4. class blinker.base.WeakNamespace(*args, **kw): Bases: weakref.WeakValueDictionary
  - signal(name, doc=None)

### signal对象常用的函数和属性
- 属性:
  1. receivers : A mapping of connected receivers.

- 函数
  1.` connect(receiver, sender=ANY, weak=True)`: Connect receiver to signal events sent by sender.
    - receiver: 可以调用的注册对象, 可以用send()的sender参数调用和提供给调用send（）的任何** kwarg。
    - sender: 任何对象或者ANY(default): 将传送到receiver的通知限制为仅由sender发送的那些sender. 仅接受sender发送的信息. 如果是ANY则是传递给所有的订阅的对象,
    - weak: 
  2. connect_via(sender, weak=False): 装饰器形式的connect
    - sender: 类似connect的sender
    - weak
  3. connected_to(*args, **kwds): 执行块，信号临时连接到接收器。
  4. send(*sender, **kwargs): 发送这个信号:
    - *sender:  Any object or None. If omitted, synonymous with None. Only accepts one positional argument.
    - * kwds: Data to be sent to receivers
  5. receivers_for(sender)
  6. has_receivers_for(sender)

()[https://pythonhosted.org/blinker/]
