# Python 面向对象
---
## 新式类与经典类
新式类与经典类的声明最大不同在于, 所有新式类必须继承至少一个父类;object是所有类的父类, 如果没有类继承时, 将object作为基类. 如果你没有直接或者间接的子类化一个对象, 那么定义就是经蛋类.
```
class A:
    pass
```


## 方法:
定义

## 类属性
类属性仅与其被定义的类绑定的,与实例无关,或者说属于全部实例的. 并且因为实力对象在日常OOP中用的最多,

## 多继承

## 静态方法和类方法

### 静态方法
静态方法的定义时, 不能有参数,

```
class C:
    @staticmethod
    def f():
        pass
```
经常有一些跟类有关系的功能但在运行时又不需要实例和类参与的情况下需要用到静态方法. 比如更改环境变量或者修改其他类的属性等能用到静态方法. 这种情况可以直接用函数解决, 但这样同样会扩散类内部的代码，造成维护困难.

即静态方法,主要处理与这个类的逻辑关联, 如验证数据;

### 类方法
类方法的定义,第一个参数必须是代表类本身的cls参数.
```
class C:
    @classmethod
    def f(cls, arg1, arg2...):
        pass
```

更关注于从类中调用方法, 而不是在实例中调用方法, 如构造重载;

### 静态方法和类方法的异同

1. 相同点:
  都不能访问实例属性和实例变量  

2. 不不同点:
  1. 类方法可以访问类变量.
  2. 类方法的参数第一个必须是代表本类的cls, 静态方法不能有参数.


### 具体应用
比如日期的方法, 可以通过实例化(__init__)进行数据输出;
可以通过类方法(@classmethod)进行数据转换;
可以通过静态方法(@staticmethod)进行数据验证;
```
class Date(object):  
  
    day = 0  
    month = 0  
    year = 0  
  
    def __init__(self, day=0, month=0, year=0):  
        self.day = day  
        self.month = month  
        self.year = year  
          
    def display(self):  
        return "{0}*{1}*{2}".format(self.day, self.month, self.year)  
     
    @classmethod  
    def from_string(cls, date_as_string):  
        day, month, year = map(int, date_as_string.split('-'))  
        date1 = cls(day, month, year)  
        return date1  
     
    @staticmethod  
    def is_date_valid(date_as_string):  
        day, month, year = map(int, date_as_string.split('-'))  
        return day <= 31 and month <= 12 and year <= 3999  
      
date1 = Date('12', '11', '2014')  
date2 = Date.from_string('11-13-2014')  
print(date1.display())  
print(date2.display())  
print(date2.is_date_valid('11-13-2014'))  
print(Date.is_date_valid('11-13-2014'))  
```

## 类的内建方法
`__doc__`
`__bases__`
`__dict__`
`__module__`
`__class__`

`__init__`
`__new__`
`__del__`


dir()返回的近视对象的属性的一个名字列表.

hasattr()
getattr()
setattr()
delattr()
## 定制类

[参考](http://stackoverflow.com/questions/12179271/python-classmethod-and-staticmethod-for-beginner)
[知乎](https://www.zhihu.com/question/20021164)
