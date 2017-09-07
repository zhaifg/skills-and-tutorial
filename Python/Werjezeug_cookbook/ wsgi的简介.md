# WSGI的简介
---
## 什么是WSGI?


PEP333规定了WSGI的实现, 主要实现如下功能
1. WSGI应用是一个Python 对象, 并且这个对象可以是函数, 或者类(类必须重写`__call__`), 这个Python对象(函数, 或者`__call__`)必须有两个参数: 1)一个WSGI的环境变量的参数;2)必须是一个可以可以执行函数用来启动response的.
2. 应用必须有个启动一个response的函数, 函数返回一个可迭代的且可以writing和flushing.
3. WSGI环境变量像CGI的环境变量一样,仅仅提供一些额外的keys由server或者中间件提供
4. 可以使用中间件包装这个WSGI.



def application(environ, start_response)
environ: 包含有CGI式环境变量的字典, 由server负责提供内容
start_response:  由server提供的回调函数, 其作用是将状态码和响应头返回给Server


## 实现一个简单的Hello World的WSGI
```python
from cgi import parse_qs, escape
def hello_world(environ, start_response):
    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    if 'subject' in parameters:
        subject = escape(parameters['subject'][0])
    else:
        subject = 'World'
    start_response('200 OK', [('Content-Type', 'text/html')])
    # start_response 有两个参数,一个http的状态码, 一个header的元组列表
    return ['''Hello %(subject)s
    Hello %(subject)s!
''' % {'subject': subject}]
```
或者一个实现类,实现__call__
```
class Upperware:
   def __init__(self, app):
      self.wrapped_app = app

   def __call__(self, environ, start_response):
      for data in self.wrapped_app(environ, start_response):
         return data.upper()
```

[Getting Started with WSGI](http://lucumr.pocoo.org/2007/5/21/getting-started-with-wsgi/)
[pep3333](https://www.python.org/dev/peps/pep-3333/)
[](http://www.letiantian.me/2015-09-10-understand-python-wsgi/)