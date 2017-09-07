# 属性描述
---

描述符是对多个属性运用相同存取逻辑的一种方式. 例如, Django ORM 和 SQLAlchemy 等 ORM 中的字段类型是描述符, 把数据库记录中字段的数据与Python对象的属性对应起来.

描述符是实现了特定协议的类, 这个协议包括 `__get__`, `__set__`, `__delete__` 方法. property 类实现了完整的描述符协议.


## 描述符示例: 验证属性
实现了 `__get__`, `___set__` 或 `__delete__` 方法的类是描述类. 描述类的用法是, 创建一个实例, 作为另一个类的类属性.

我们将定义一个 Quantity 描述符, LineItem 类会用到两个 Quantity 实例: 一个用于管理 weight 属性, 一个用于管理 price 属性. 

Quantiy                                 LineItem
storage_name        <--weight--       weight {storage}
`__init__`         ---->  <-price--   price {storage}
`__set__`                             `__init__`, subtotal

weight, price 出现了两次, 因为其实两个不同的属性都叫 weight, 一个是LineItem的类属性, 另一个是各个LineItem对象的实例属性. price 也是.

从现在开始使用下述定义:
**描述符类**: 实现描述符协议的类, 如Quantity类
**托管类**: 把描述符实例声明为类属性的类, LineItem
**描述符实例**: 描述符类的各个实例, 声明为托管类的类属性.
**托管实例**: 托管类的实例, LineItem 的实例
**存储属性**: 托管实例中存储自身托管属性的属性. LineItem 实例的weight 和 price 属性是存储属性.
**托管属性**: 托管类中由描述符实例处理的公开属性, 值存储在存储属性中. 也就是说, 描述符实例和存储属性为托管属性建立了基础.

```py
class Quantity:
    def __init__(self, storage_name):
        self.storage_name = storage_name

    def __set__(self, instance, value):
        if value > 0:
            instance.__dict__[self.storage_name] = value # 是托管类LineItem 类的实例
        else:
            raise ValueError('value must be > 0')


class LineItem:
    weight = Quantity('weight')
    price = Quantity('price')

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
```

编写`__set__` 方法时, 要记住self 和 instance 参数的意思:
> self 是描述符实例, instance 是托管实例. 管理实例属性的描述符应该把值存储在托管实例中. 因此, Python 才会为描述符中的那个方法提供了 instance 参数.

可以想想 `__set__` 方法前两个参数(self 和 instance)的意思. 这里, self 是描述符实例. 它其实是托管类的类属性. 同一刻, 内存中可能有几千个 LineItem 实例, 不过只会有两个描述符实例: LineItem.weight 和 LineItem.price. 因此, 存储在描述符实例中的数据, 其实会变成 LineItem 类的类属性, 从而由全部 LineItem 实例共享.
