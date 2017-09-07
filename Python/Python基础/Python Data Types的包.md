# 数据结构
--- 
collections模块包含了多种数据结构的实现,扩展了其他模块中的向英杰结构. 例如Deque是双向队列,允许从任意一端增加或删除元素.

defaultdickt是一个字典, 如果找不到某个键, 它会相应一个默认值, 而是OrderDict会记住增加元素的序列.
namedtuple扩展了一般的tuple, 除了每个成员元素提供一个数值索引外还提供一个属性名称.

对于大量数据,array会比list更加高效的利用内存. 由于array仅限于一种数据类型

## collections 高性能容器数据类型
### Counter
Conuter作为一个容器, 可以跟踪相同的值增加的了多少次.
一个方便快速的方便的计数器
```
In [8]: cnt = Counter()
In [10]: for word in ['red', 'blue', 'red', 'green', 'blue', 'blue']:
    ...:     cnt[word] += 1
    ...:     

In [11]: cnt
Out[11]: Counter({'blue': 3, 'green': 1, 'red': 2})

```

### defaultdict
标准字典 包括了一个setdefault()方法来获取一个值,如果这个值不存在则建立一个默认值.

`d = defaultdict("None", foo='bar')`
`d['foo']`
`d['bar']`

### dequeue
双向队列, 支持从任意一端增加和删除元素. 更为常用的两种结构, 即栈和队列.

**旋转**
`d.rotate(2)`
```
In [2]: d = deque(range(10))

In [3]: d
Out[3]: deque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

In [4]: d.rotate(2)

In [5]: d
Out[5]: deque([8, 9, 0, 1, 2, 3, 4, 5, 6, 7])

In [9]: d.rotate(-2)

In [10]: d
Out[10]: deque([2, 3, 4, 5, 6, 7, 8, 9, 0, 1])

```

### namedtuple
```
In [12]: Person = namedtuple('Person', 'name age gender')

In [13]: print type(Person)
<type 'type'>

In [14]: bob = Person(name='Bob', age=30, gender='male')

In [15]: bob
Out[15]: Person(name='Bob', age=30, gender='male')

In [16]: bob.name
Out[16]: 'Bob'

In [17]: bob.age
Out[17]: 30

In [18]: bob.gender
Out[18]: 'male'
```

### OrderedDict
一个有序字典

## Array  固定类型的数据序列
类似于List, 但是存储的相同基本类型的对象.
```
from array import array
array('l')
array('c', "hello world")

In [14]: a.append(2)

In [15]: a.append(3)

In [16]: a
Out[16]: array('l', [2, 3])

In [17]: array('c', "hello world")
Out[17]: array('c', 'hello world')

```

`class array.array(typecode[, initializer])`

### 数组和文件
可以使用高效读写文件的专用的内置方法将数组的内容写入文件或者从文件读取.
使用`fromfile()`, `tofile()`

### 候选字节顺序
如果数组中的数据没有采用固定字节顺序, 或者在发送到一个采用不同字节顺序的系统(或者在网络上发送)之前需要做数据交换, 可以有Python转换整个数组而无需迭代处理每一个元素. 



## heapq--堆排序算法
这个模块提供了对队列算法的, 或者说是优先级队列算法.
heap是一个二叉树, 每一个节点都一个小于或者等于他的子节点.通常使用数组实现, 规则是虽有的元素K, 都会满足`heap[k]<= heap[2*k+1]` 和 `heap[k] < heap[2*k + 2]`, 常常最小的元素是第一个元素(k=0).

heapq的API通常的heap算法有两个不同:
1. 我们从0开始计数,这使得指数之间的关系为其孩子节点和索引稍微不那么明显,但更为合适,因为Python使用从零开始的索引.
2. `pop`操作返回的的是最小的一个


heapq中的heap可以使用`[]`, 你可以通过函数填充列表转换成一堆heapify()。

### 函数:
`heapq.heappush(heap, item)`: push 一个value到heap中, 保持heapq不变
`heapq.heappop(heap)`: pop和返回最小的元素从heap中. heap空触发`IndexError`
`heappushpop(heap, item)`: 先push一个item到heap中,然后pop,并返回最小的一个元素. 这个函数的效率比`push`和`pop`两个合起来操作高. 如果新加的是最小的会返回.
`heapq.heapfiy(x)`: 转换list x为heap队列形式
`heapq.heqpreplace(heap, item)`: pop,并返回最小的一个从heap, 然后push一个新的到heap中.
`heapq,merge(*iterable)`:  合并多个队列(比如按照时间合并日志), 返回一个迭代器, 不把他放在内存.
`heapq.nlargest(n, iterable[,key])`: 返回iterable最大的前n个. 如果指定key可以, 指定一个参数的函数, 进行比较每一个元素, 类似sorted等
`heapq.nsmallest(n, iterable[,key])`: 类似于上边

```python
def heapsort(iterable):
    h = []
    for value in iterable:
        heappush(h, value)
    return [ heappop(h) for i in range(len(h)) ]

>>> h = []
>>> heappush(h, (5, 'write code'))
>>> heappush(h, (7, 'release product'))
>>> heappush(h, (1, 'write spec'))
>>> heappush(h, (3, 'create tests'))
>>> heappop(h)
(1, 'write spec')
```

## bisect -- 维护有序列表
维护一个有序列表, 插入也是有序的
`bisect.bisect_left(a, x, lo=0, hi=len(a))`: 

## Queue线程安全的FIFO实现

### Queue
基本的先进先出队列 
**方法**:
`Queue(maxsize=0)`
`qsize()`
`full()`
`put(item[,block[,timeout]])`
`put_nowait(item)` == `put(item, False)`
`get([block[,timeout]])`
`get_nowait()`
`task_done()`: 表明队列已经完成. 用在队列的消费者线程端.  每一次`get()`后运行一个任务,  然后调用一下`task_done()`告诉队列已经处理完了. 如果一个`join()`正在执行阻塞队列,他可以使之重新执行.
`join()`: 阻塞知道队列中所有取走或者执行完. 队列put,会增加未完成的任务, `task_done`减少队列数. 如果`get`不调用`task_done()`后, 队列可能出现计数不准确的情况.

```python
def  worker():
    while True:
        item = q.get()
        q.task_done()
q = Queue()
for i in range(num_worker_threads):
    t = Thread(target= worker)
    t.start()

for item in source():
    q.put(item)
q.join() # 阻塞到所有的都执行完成.
```

### LifoQueue 后进先出

### PriorityQueue 优先队列


## weakref--对象的非永久引用
什么是弱引用?
维基:
> 在计算机程序设计中，弱引用与强引用相对，是指不能确保其引用的对象不会被垃圾回收器回收的引用。一个对象若只被弱引用所引用，则被认为是不可访问（或弱可访问）的，并因此可能在任何时刻被回收。一些配有垃圾回收机制的语言，如Java、C#、Python、Perl、Lisp等都在不同程度上支持弱引用。
> 


弱引用的主要用途是实现缓存或映射控股大型对象的需要,大对象不能存活仅仅因为它出现在一个缓存或映射。