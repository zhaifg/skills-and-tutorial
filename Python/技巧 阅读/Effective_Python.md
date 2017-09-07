# 函数部分
---
## 尽量用异常表示特殊情况,而不要返回None.
None表示特殊意义的函数, 很容易使调用者犯错, 因为None,0以及空格之类的字符串的值,在if里都是False.

## 了解如何在闭包里使用外围作用中的变量.
假如有一份列表,其中的元素都是数字, 现在要对其排序,但排序时, 要把出现在某个群组内的数字, 放在群组外的数字的前面. (优先级).

实现该动能的常见做法, 是在调用列表的sort方法是, 把辅助函数传给key参数. 这个辅助函数的返回值, 将会用来 确定列表中各个元素的顺序. 辅助函数可以判断受测元素是否处在重要的群组中, 并据此返回相应的排序关键字(sort key)

```
def sort_priority(values, group):
    def helper(x):
        if x in group:
            return (0, x)
        return (1, x)
    values.sort(key=helper)

numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = [2, 3, 5, 7]
sort_priority(numbers, group)
print numbers

### 
[2, 3, 5, 7, 1, 4, 6, 8]
```
- Python支持闭包,: 闭包是一种定义在某个作用域中的函数, 这种函数引用了那个作用的变量. helper函数之所以能够访问sort_priority的group参数,原因就在于它是闭包.
- Python的函数是一级对象(first-class object), 也就是说我们可以直接引用函数,把函数赋给变量,把函数当成参数传给其他函数, 并通过表达式以及if语句对其进行比较判断, 等等. 于是我们可以把helper这个闭包函数,
传递给sort方法的key参数.
- Python使用特殊的规则来比较两个元组. 它首先比较各个元组中下表为0的对应的元素, 如果相等,则比较下标为1的元素,以此类推.

这个sort_priority函数如果能够改进一下, 它应该返回一个值, 用来表示用户界面是否出现了优先级较高的原件, 是的该函数的调用者, 可以根据这个返回值做出相应的处理. 该函数里的闭包函数, 能够判断受测数字是否处于群组内, 那么不妨在发现优先级较高的原件时, 从闭包函数中翻转某个标志变量,然后令sort_priority函数把经过闭包修改的那个标志变量,返回给调用者.

先使用简单的方式:
```
def sort_priority2(numbers, group):
    found = False

    def helper(x):
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found
## 
False
[2, 3, 5, 7, 1, 4, 6, 8]
```
排序结果是对的, 但是found值不对:
在表达式中引用变量时, Python解释器将如下顺序遍历各个作用域, 已解析该引用:
1. 当前函数的作用域.
2. 任何外围作用域(例如,包含当前函数的其他函数.)
3. 包含当前代码的那个模块的作用域(也叫全局作用域, global space).
4. 内置作用域(也就是包含len以及str等函数的那个作用域.).

如果以上方面都没有定义过名称的变量时, 就抛出`NameError`

给变量赋值时, 规则有所不同. 如果当前作用域内已经定义了这个变量, 那么该变量就具备新值. 若当前作用域内没有定义此变量时, 则会这次赋值当成定义变量.
而新定义的这个变量, 其作用域就是包含赋值操作的这个函数.

上面的sort_prority2中helper的found=True,相当于在helper内部重新定义了一个found变
量, 值为True. 

### 获取闭包内数据
Python3中有一个特殊写法, 能够获取闭包内的数据. 可以使用nonlocal来表明用途.
也就是:给相关变量赋值的时候, 应该在上层作用域中查找该变量. nonlocal的唯一的限制
在于不能延伸到模块级别, 这是为了防止对全局的作用域的污染.

```
def sort_priority2(numbers, group):
    found = False

    def helper(x):
        nonlocal found
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found
```

防止对nonlocal滥用, 建议只在简单函数的函数作用域中使用.
在复杂的环境下,应该写成辅助类来使用.

```
class Sorter(object):
    def __init__(self, group):
        self.group = group
        self.found =  False
    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)
        return (1, x)
sorter = Sorter(group)
numbers.sort(sorter)
assert sortter.found  is True
```


### Python2的实现
Python2 不支持nonlocal关键字, 为了实现类似功能, 需要利用Python的作用域规则来
解决, 虽然不太优雅, 但是成了Python编程的习惯.
```
def sort_priority2(numbers, group):
    found = [False]

    def helper(x):
        if x in group:
            found[0] = True
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found[0]
```

> 1.对于定义在某作用域的闭包来说, 他可以引用这些作用域的变量.
> 2. 使用默认方式对闭包变量赋值时, 不会影响外围作用域中同名变量.
> 3. Python3中, 程序可以在闭包中使用nonlocal语句来修饰某个名称, 使改闭包能够修改外围作用域中的同名变量.
> 4. Python2中, 可以使用可变值(例如, 包含打个元素的列表)来实现与nonlocal语句相仿的机制.
> 5. 除了比较简单的函数, 尽量不要用nonlocal语句.

## 考虑用生成器来改写直接返回列表的函数P35
生成器是使用yield表达式的函数.调用生成器函数时, 他并不会真的运行,而是返回一个迭代器. 每次在这个迭代器上调用内置的next函数时, 迭代器会把生成器推进到下一个yield表达式里.生成器传给yield每一个值,都会由迭代器返回给调用者.

1. 使用生成器比把收集到结果放入列表返回给调用者更加清晰.
2. 由生成器函数所返回的那个迭代器,可以把生成器函数体中, 传给yield表达式的那些值,逐次产生出来.
3. 无论输入量有多大,生成器都能产生一系列输出, 因为这些输入量和输出量,都不会影响它在执行时所消耗的内存.

```
def index_file(handle):
    offset = 0
    for line in handle:
        if line:
            yield offset
        for letter in line:
            if letter == ' ':
                yield offset

with open('/tmp/address.txt', 'r') as f:
    it = index_file(f)
    results = islice(it, 0,3)
    print(list(results))
```

## 在参数上面迭代时,要多加小心.ddd


## 用数量可变的位置参数减少视觉杂讯(函数) *arg
1. 在def语句中使用 *args, 即可令函数接受数量可变的位置参数
2. 调用函数式, 可以采用* 操作符,把序列中的元素当成位置参数, 传给该函数.
3. 对生成器使用*操作符, 可能导致程序耗尽内存并崩溃.
4. 在已经接受*args参数的函数上继续添加位置参数, 可能会产生难以排查的bug.

## 用关键字参数来表达可选行为(函数)

* 函数参数可以按位置或者关键字来指定.
* 使用位置参数来调用函数, 可能会导致这些参数值的含义不够明确, 而关键字参数则能够阐明每个参数的意图.
* 给函数添加新的行为时,可以使用带默认值的关键字参数, 以便与原有的函数调用代码保持兼容.
* 可选的关键字参数, 总是应该以关键字形式来指定, 而不应该以位置参数形式来指定.

## 用None和文档字符串来描述具有动态默认值的参数(函数)

1. 参数默认值, 只会在程序加载模块并读取到本函数的定义时评估一次.对于{}或者[]等动态的值, 可能会导致奇怪的行为.
2. 对于以动态值作为实际默认值的关键字参数来说, 应该把形式上的默认值写为None, 并在函数文档字符串里面描述该默认值所对应的实际行为.


