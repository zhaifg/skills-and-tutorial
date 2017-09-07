# Python super 的应用
---

1. 提供使用案例
2. 给出一个清晰的工作模型



```python
class LoggingDict(dict):
    def __setitem__(self, key, value):
        print "Settingto %s: %s" % (key, value)
        super(self.__class__, self).__setitem__(key, value)

ld = LoggingDict()
ld['a'] = 'a'
```

使用super的好处可以动态调用基类的方法, 当修改子类的基类时, 子类引用父类的方法不用修改代码. 如上面的例子,
如果我们不使用super()时
```python
class LoggingDict(dict): # Adict
    def __setitem__(self, key, value):
        print "Settingto %s: %s" % (key, value)
        dict.__setitem__(key, value) #   Adict.__setitem__(key, value)
```

## 菱形继承的MRO顺序

```
class LoggingOD(LoggingDict, collections.OrderedDict):
    pass
```
上面的MRO顺序:
1. LoggingOD的方法优先级大于父类, LoggingDict和OrdereDicty
2. LoggingDict的优先级大于OrdereDict, 因为 LoggingOD.__bases__ is (LoggingDict, OrderedDict)
3. LoggingDict优先级大于他的父类dict
4. dict优先级大于object


## 使用建议

super()在将方法调用委托给实例的祖先树中的某个类的业务中。
对于可重排序的方法调用来工作，类需要被协同设计。
这提出了三个容易解决的实际问题：
1. super()调用的父类对象需要存在
2. 调用者和被调用者需要具有匹配的参数(参数个数等要匹配)
3. 需要每次调用时用super 调用

### 调用者与被调用者匹配方法的参数列表
当的子类的要调用父类的时, 参数不定时, 可以使用**kw 字来处理.

```python
class Shape:
    def __init__(self, shapename, **kwds):
        self.shapename = shapename
        super(self.__class__, self).__init__(**kwds)        

class ColoredShape(Shape):
    def __init__(self, color, **kwds):
        self.color = color
        super(self.__class__, self).__init__(**kwds)

cs = ColoredShape(color='red', shapename='circle')
```

### super()调用的父类方法必须存在
```
class Root:
    def draw(self):
        # the delegation chain stops here
        assert not hasattr(super(), 'draw')

class Shape(Root):
    def __init__(self, shapename, **kwds):
        self.shapename = shapename
        super().__init__(**kwds)
    def draw(self):
        print('Drawing.  Setting shape to:', self.shapename)
        super().draw()

class ColoredShape(Shape):
    def __init__(self, color, **kwds):
        self.color = color
        super().__init__(**kwds)
    def draw(self):
        print('Drawing.  Setting color to:', self.color)
        super().draw()

cs = ColoredShape(color='blue', shapename='square')
cs.draw()
```

## 整合多继承
偶尔，一个子类可能想要使用多重继承技术并需要一个不是为它设计的第三方类（也许感兴趣他的的方法,而不使用super()或者不希望从这个类做继承）。这种情况很容易通过创建由具有此功能的适配器类来做。

比如下面的Moveable类不会使用super()方法, 而且`__init__`方法是自定义的, 不会继承object类.
```python
class Moveable:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def draw(self):
        print('Drawing at position:', self.x, self.y)
```
如果我们需要用这个类与我们自己设计的`ColoredShape`, 我们需要编写一个适配器来适配.
```python 
class MoveableAdapter(Root):
    def __init__(self, x, y, **kwds):
        self.movable = Moveable(x, y)
        super(self.__class__, self).__init__(**kwds)

    def draw(self):
        self.movable.draw()
        super(self.__class__, self).draw()

class MovableColoredShape(ColoredShape, MoveableAdapter):
    pass

MovableColoredShape(color='red', shapename='triangle',
                    x=10, y=20).draw()
```

## 完整的例子
在Python 2.7和3.
```python
from collections import Counter, OrderedDict

class OrderedCounter(Counter, OrderedDict):
     'Counter that remembers the order elements are first seen'
     def __repr__(self):
         return '%s(%r)' % (self.__class__.__name__,
                            OrderedDict(self))
     def __reduce__(self):
         return self.__class__, (OrderedDict(self),)

oc = OrderedCounter('abracadabra')
```
