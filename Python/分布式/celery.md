# celery
---

## 何为任务队列?
任务队列是一种在线程或者机器间分发任务的机制.
消息队列的输入是工作的一个单元, 称之为任务, 独立的Worker进程持续监视队列中是否有需要处理的新任务.

Celery 用消息通信, 通常使用 中间人(broker) 在客户端和Worker间斡旋. 这个过程从客户端向队列添加消息开始, 之后中间人把消息派送给worker

Celery 系统可包含多个Worker 和 中间人, 以此获得高可用性和横向扩展能力.


## 安装
```
pip intall -U celery

捆绑安装

$ pip install "celery[librabbitmq]"

$ pip install "celery[librabbitmq,redis,auth,msgpack]"
```

## Celery 组成介绍

### Broker(中间人)
用于与客户端传送消息的.
Celery 支持几种消息传输方式: RabbitMQ, Redis,

### RabbitMQ

RabbitMQ 是默认的代理方式, 因此不需要额外的依赖关系, 或者初始配置, 除了配置代理实例的URL 位置.
```
broker_url = 'amqp://myuser:mypassword@localhost:5672/myvhost'
```

设置 rabbitmq
```
$ sudo rabbitmqctl add_user myuser mypassword
$ sudo rabbitmqctl add_vhost myvhost
$ sudo rabbitmqctl set_user_tags myuser mytag
$ sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"
```

### 使用Redis

```shell
#捆绑安装

pip install -U "celery[redis]"

# 配置
app.conf.broker_url = 'redis://localhost:6379/0'
# redis://:password@hostname:port/db_number


# Results
app.conf.result_backend = 'redis://localhost:6379/0'

```

## 快速开始

###  选择一个Broker
使用redis

### 安装 celery

### 应用
首先 需要一个 Celery 实例. 我们称作 Celery application 或者 app. 由于此 Celery 实例用作想在 Celery 中执行的所有操作的入口, 例如创建任务和管理worker, 其他模块必须可以导入.

这个 教程中 我们保证每一个每一件事都放在一个的module 中,  但是在大的项目中需要编写单独的模块.

创建tasks.py
```py
from celery import Celery
BROKER_URL = 'redis://localhost:6379'
app = Celery('tasks', broker=BROKER_URL)

@app.task
def add(x, y): 
    return x + y
```
Celery 的第一个参数是用来定义当前模块名称的.
第二个参数 是 broker 的url

### 运行celery

`celery -A tasks worker  --loglevel=info`

### 调用 task
调用我们自定义的task 需要使用 delay()方法
这个是 apply_async() 方法的 缩写版

```
from tasks import add
add.delay(4, 4)
```
这个任务现在由你刚刚开始的worker处理。您可以通过查看worker的控制台输出来验证这一点。

调用这个 task 返回一个 AsyncResult 实例. 它可以检测task, 直到task运行完成, 或者取得 返回的结果.

默认情况下不启用结果。为了进行远程过程调用或跟踪数据库中的任务结果，您需要配置Celery以使用结果后端。这将在下一节中介绍。

### 保持结果
如果需要保持tasks状态, Celery 需要 存储或者发送状态到任何地方.
There are several built-in result backends to choose from: SQLAlchemy/Django ORM, Memcached, Redis, RPC (RabbitMQ/AMQP), and – or you can define your own.

对于这个例子，我们使用 rpc 结果后端，它将状态发回为短消息。
后端通过后台参数指定给 Celery（或通过result_backend设置，如果您选择使用配置模块）：
`app = Celery('tasks', backend='rpc://', broker='pyamqp://')`
或者你希望使用Redis 作为backend.

现在result后端保存已经配置, 再次执行以下. 现在
`>>> result = add.delay(4, 4)`

`ready()` 方法返回 任务是否处理完成
```
>>> result.ready()
False

```

你可以等待 result 完成, 但是很少使用它，因为它将异步调用转换为同步调用：
```
>>> result.get(timeout=1)
8
```

如果任务引发异常，get() 将重新引发异常，但是可以通过指定传播参数来覆盖它：
`>>> result.get(propagate=False)`

如果任务引发异常，您还可以访问原始的追溯：
`>>> result.traceback`

### 配置
可以直接或通过使用专用配置模块在应用程序上设置配置。例如，您可以通过更改task_serializer设置来配置用于序列化任务有效负载的默认序列化：
`app.conf.task_serializer = 'json`

可以这样更新配置
```
app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='Europe/Oslo',
    enable_utc=True,
)
```

单独配置实例

celeryconfig.py:
```py
broker_url = 'pyamqp://'
result_backend = 'rpc://'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Oslo'
enable_utc = True
```

`app.config_from_object('celeryconfig')`

` python -m celeryconfig`
