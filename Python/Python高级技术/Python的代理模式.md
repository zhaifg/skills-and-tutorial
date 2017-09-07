# Python的代理模式
---
## 什么是代理模式?
代理模式(Proxy Pattern)是程序设计中的一种设计模式.
所谓的代理者是指一个类别可以作为其他东西的接口. 代理者可以作为任何东西的接口:网络连接,存储器中的大对象, 文件或其他昂贵或者无法复制到资源.

## 面向过程的实现
```
def hello():
    print 'hi, i am hello'

def proxy():
    print 'prepare....'
    hello()
    print 'finish....'

if __name__ == '__main__':
    proxy()
```

## 面向对象的实现
```python
class AbstractSubject(object):

    def __init__(self):
        pass

    def request(self):
        pass

class RealSubject(AbstractSubject):

    def __init__(self):
        pass
    def request(self):
        print 'hi, i am RealSubject'

class ProxySubject(AbstractSubject):

    def __init__(self):
        self.__rs = RealSubject()

    def request(self):
        self.__beforeRequest()
        self.__rs.request()
        self.__afterRequest()

    def __beforeRequest(self):
        print 'prepare....'

    def __afterRequest(self):
        print 'finish....'

if __name__ == '__main__':
    subject = ProxySubject()
    subject.request()
```

如果`RealSubject`的初始函数`__init__`有参数, 代理类ProxySubject可以作两种方式的修改:
### 第一种
`ProxySubject`的`__init__`的方法同样有参数, 初始化代理类的时候将初始化参数传递给`RealSubject`.

### 第二种
将`ProxySubject`的`__init__`的方法修改为:
```
def __init__(self):
    self.__rs = None
```
将ProxySubject的request方法改为:
```
def request(self, *args, **kwargs):
    if self.__rs is None:
        self.__rs = RealSubject(*args, *kwargs)
    self.__beforeRequest()
    self.__rs.request()
    self.__afterRequest()
```




()[http://www.letiantian.me/2014-01-01-proxy-pattern-with-python/]
