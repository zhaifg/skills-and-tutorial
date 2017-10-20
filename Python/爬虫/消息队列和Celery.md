# 消息队列和Celery
---
消息队列(Message Queue)提供异步通信协议, 可以实现进程间通信或者同一进程的不同线程的通信. 其中"消息"是指包含必要信息的数据. 消息的发送者发送完成后立即返回, 消息存储在进程队列中, 对这个消息感兴趣的订阅者会订阅消息并接收和处理他.

好处:
1. 应用解耦
2. 异步通信
3. 数据持久化. 未完成的消息不会因为某些故障而丢失.
4. 送达保证.

## Beanstalkd
Beanstalkd是消息队列的后起之秀, 高性能轻量级的分布式内存队列系统
特点:
1. 可持久化. Beanstalkd 运行使用内存, 但提供了持久支持. 在启动的时候使用-b参数指定持久化目录, 它会将所有的任务写入binlog文件. 断电重启后, 同样参数重启后, 将恢复binlog中内容.
2. 支持任务优先级
3. 任务超时重发.
4. 支持任务预留. 如果任务因为某些原因无法执行, 消费者可以把任务置为buried状态保留这些任务.
5. 支持分布式
6. 灵活的任务过期和TTR时间

job就是待异步执行的任务, 也就是消息, 是Beanstalkd中基本单元. 一个job通过使用put命令时创建, 然后被放在一个管道(tube)中. job有四个状态:
  1. ready: 等待取出并处理
  2. reserved: 如果job被消费这(worker)去除, 将被此消息预定, 消费者将执行此job.
  3. delayed: 等待特定时间后, 状态再改为ready
  4. bured: 等待被唤醒, 通常在job处理失败时, 会改变这个状态
  5. 


## 深入理解 RabbitMQ
RabbitMQ是一个实现了AMQP协议标准的开源消息代理和队列服务器. 和Beanstalkd不同的是, 他是企业级消息系统, 自带了集群,管理,插件系统等待特性,在高可用, 可扩展性, 易用性等方面的做得很好.
```
sudo apt-get install rabbitmq-server -yq
# python 客户端
pip install pika
```

### AMQP
AMQP(Advaced Message Queuing Protocol, 高级消息队列协议)是一个异步消息传递所使用的应用层协议规范. 它的设计初衷是为了摆脱商业MQ高额费用和不同MQ供应商的接口不统一的问题, 所以一开始就设计成开放标砖, 已解决企业复杂的消息队列需求问题.

几个概念:
1. 消息(Message). 消息实际包含两部分内容:
  * 有效载荷(Payload), 也就是要传输的数据, 数据类型可以是纯文本也可以是JSON.
  * 标签(Label), 它包含交换机的名字和可选的主题(topic)标记等. AMQP仅仅描述了标签, 而RabbitMQ决定了把这个消息发给哪个消费者.
2. 发布者(Productor): 也就是生产者, 它创建消息并且设置标签
3. 消费者(Consumer): 消费者连接到代理服务器上, 接收消息的有效载荷(注意消费者并不需要消息中的标签)

AMQP的工作流程:

发布者(Publisher) --> 交换机 --> 队列 <---> 消息订阅者

为了保证消息被正确的取出并执行, 消息投递失败后会重发, AMQP模块包含了一个消息确认的概念: 当一个消息从队列中投递给消费者后,消费者会通知消息代理(也就是常说的Broker), 这个通知可以是自动完成的, 也可是由处理消息的应用来指定. 当消息确认(ack)被启用的时候, 消息代理不会完全将消息从队列中删除, 除非收到来自消费者确认回执.

交换机拿到一个消息之后会将他路由给队列. 他使用哪种路由算法是由交换机类型和被称作"绑定"(queue_bind)的规则所决定的. 目前RabbitMQ提供了如下四种交换机.

1. 直连交换机(direct exchange):根据消息所携带的路由键（routing key)将消息投递给对应队列. 将一个队列绑定到某一个交换机的同时赋予该绑定一个路由键, 顶一个携带着路由键为XXX的消息被发送给智联交换机时, 交换机会把它路由给绑定值同样为XXX的队列. 直连交换机用来处理消息的单播路由.
2. 主题交换机(topic exchange):通过对消息的路由键和队列到交换机的绑定模式之间的匹配，将消息路由给一个或多个队列．　主题交换机通常用来实现消息的多播路由．发送到主题交换机的消息的路由键，　必须是一个由"."分割的词语列表,这些词语应该和对应的业务相关联, 词语的个数可以随意, 但是不要超过255字节. 绑定键支持通配符: "*"用来表示一个单词;"#"用来表示任意数量(零个或多个)单词.
3. 扇型交换机(fanout exchange): 将消息路由给绑定到他身上的所有队列, 且不理会绑定的路由键. 扇型交换机用来处理消息广播路由. 扇型交互及非常有用,因为它允许你对单挑消息做不通的处理, web开发中一个操作可能要做多个连带工作, 比如用户床架一篇闲的日记, 需要更新用户创建的日记数, 清楚相关缓存, 给关注这个用户等其他用户推送消息,日记审核后台, 日记进最新日鸡翅等等, 可以使用扇型交换机把一个消息分发给多个任务队列,执行不一样的工作. 尤其是当业务改变时, 使用扇型交换机直接为新的消费者添加声明并绑定进来就可以了. 否则需要修改发送方的代码添加接收方. 所以,使用扇型交换机可以有效地解耦发布者和消费者.
4. 头交换机(headers exchange): 允许匹配AMQP的头而非路由键, 其实收银起来和直接交换机差不多, 但是性能缺差的很多, 一般用不到这种类型.

### 简单的生产者消费者的例子
producter
```python
import sys 
import pika
# %2F是被转义的"/", 是这里使用了默认的虚拟主机和默认的用户和密码
parameters = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F')
connection = pika.BlockingConnection(parameters) # connection就是所谓的消息代理
channel = connection.channel() # 获得信道

# 声明交换机, 指定交换机类型为直连交换机. 最后两个参数表示想要持久化的交换机, 其中durable为True表示RabbitMQ在崩溃重启之后会重建队列和交换机
channel.exchange_declare(exchange='web_devlop', exchange_type='direct', 
                        passive=False, durable=True, auto_delete=False)

if len(sys.argv) !=1:
    msg = sys.argv[1] # 使用命令行作为消息体
else:
    msg = 'hah'

# 创建一个消息, delivery_mode为2表示让这个小消息持久化, 重启RabbitMQ也不会丢失. 使用持久化需要考虑为此付出的性能成本, 如果开启此功能, 强烈建议把小夏存储在SSD上.
props = pika.BasicProperties(content_type='text/plain', delivery_mode=2)

# basic_public表示发送路由键为xxx_routing_key, 消息体为hah的消息给web_devlop这个交换机.
channel.basic_publish('web_devlop', 'xxx_routing_key', msg, properties = props)
connection.close() # 关闭连接
```

若支持: json application/json, 

```python

import pika

# 处理接收到的消息的回调函数
# method_frame携带了投递标记, header_frame表示AMQP信息头的对象
# body为消息实体
def on_message(channel, method_frame, header_frame, body):
    # 消息确认, 确认之后才会删除消息并给消费者发送新的消息
    channel.basic_ack(delivery_tag = method_frame.delivery_tag)
    print body

parameters = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
# 接收确认消息
# channel.confirm_delivery()
channel.exchange_declare(exchange = 'web_devlop', exchange_type='direct',
                         passive = False, durable = True, auto_delete = False)

# 声明队列, 如果没有就创建
channel.queue_declare(queue='standard', auto_delete= True)
# 通过路由键将队列和交换机绑定    
channel.queue_bind(queue='standard', exchange='web_devlop', 
                   routing_key='xxx_routing_key')

channel.basic_consume(on_message, 'standard')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop()

connection.close()

```

### 虚拟主机 
RabbitMQ服务器可以创建虚拟主机, 他拥有自己的队列,绑定和交换机, 就像一个自己的权限机制的迷你版RabbitMQ. 不同的虚拟主机之间的完全隔离, 还可以有效避免命名冲突. 上面的例子都基于默认的虚拟主机"/".

管理RabbitMQ一般般都是通过rabbitmqctl命令来完成
```
sudo  rabbitmqctl add_user zhaifg 123456
sudo  rabbitmqctl add_vhost web_develop 
sudo  rabbitmqctl set_permission -p web_develop zhaifg ".*" ".*" ".*"
sudo  rabbitmqctl list_vhosts
sudo  rabbitmqctl list_queues -p zhaifg
sudo  rabbitmqctl list_users
```

解释AMQP, 深入理解RabbitMQ, 

## 使用celery
Celery是一个专注于实时处理和人物调度的分布式任务队列. 所谓的任务就是消息, 消息中的有效载荷中包含要执行任务需要的全部数据.

使用场景:
1. web 应用. 较长时间的, 交给后台执行
2. 定时任务
3. 其他可以可以异步的任务.

Celery提供的特性:
1. 方便产看任务执行情况, 是否成功, 当前状态, 执行任务花费的时间
2. 可以使用功能齐备的管理后台或命令行添加, 更新, 删除任务.
3. 方便把任务和配置管理相关联
4. 可选多进程, Eventlet和 Gevent 三种模式并发执行
5. 提供错误处理机制
6. 提供多种任务原语, 方便实现任务分组, 拆分, 和调用连
7. 支持多种消息代理和后端存储

Celery的架构:
- Celery Beat: 任务调度器, Beat进程会读取配置文件的内容, 周期性的将配置中到期的需要执行的任务发送给任务队列
- Celery Worker: 执行任务的消费之, 通常会在多台服务器运行多个消费者来提高执行效率
- Broker:消息代理，　或者叫做消息中间件, 接受任务生产者发送过来的任务消息, 存在队列再按照次序发给任务消费者(通常是消息队列或者数据库)
- Producer: 调用了Celery提供的API, 函数或者装饰器而产生的任务并交给任务队列处理的都是任务生产者.
- Result Backed: 任务处理完成后保存状态信息和结果, 以供查询. Celery默认一直吃Redis, RabbitMQ, MongoDB, DangjoORM, SQLAlchemy等.

## Celery序列化
在客户端和消费者之间传输数据需要序列化和反序列化. Celery支持如表所示的序列化方案:
`pickle`: pickle是Python标准库中的一个模块, 支持Python内置的数据结构, 但是它是Python的专有协议. 从Celery 3.2开始, 由于安全性等原因Celery将拒绝pickle这个方案
`json`: json支持多种语言, 可用于跨语言方案.
`yaml`: yaml的表达能力强, 支持的数据类型比json多, 但是Python客户端的性能不如JSON.
`msgpack`: msgpack是一个二进制的类json的序列化方案, 但是比json的数据结构更小, 更快.

安装配置Celery
`pip install "celery[]librabbitmq, redis, msgpack]"`

### 简单示例
```
proj
|--celeryconfig.py
|--celery.py
|--__init__.py
|__tasks.py
```
celery.py
```
from __future__ import absolute_import

from celery import Celery

app = Celery('proj1', include=['proj1.tasks'])
app.config_from_object('proj1.celeryconfig')

if __name__ == "__main__":
    app.start()

```

celeryconfig.py
```
BROKER_URL = 'amqp://zhaifg:123456@localhost:5672/web_develop'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_SERIALIZER = 'json'
#CELERY_TASK_SERIALIZER = 'msgpack'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_EXPIRES = 60 * 60 * 24
CELERY_ACCEPT_CONTENT = ['json', 'msgpack']
```
tasks.py
```
from __future__ import absolute_import
from proj1.celery import app 

@app.task
def add(x, y): 
    return x + y 
```

运行
```
# A
celery -A  proj worker -l info
In [1]: from proj1.tasks import add

In [2]: r = add.delay(1,3)

In [3]: r.result
Out[3]: 4

In [4]: r.successful
Out[4]: <bound method AsyncResult.successful of <AsyncResult: 19c2bb9a-0220-4ad2-85d0-0e99732e86e6>>

In [5]: r.status
Out[5]: u'SUCCESS'

In [6]: r.successful()
Out[6]: True

In [7]: r.backend
Out[7]: <celery.backends.redis.RedisBackend at 0x7f00b1aca2d0>


In [10]: task_id = '19c2bb9a-0220-4ad2-85d0-0e99732e86e6'

In [11]: add.AsyncResult(task_id).get()
Out[11]: 4

In [12]: from celery.result import AsyncResult

In [13]: AsyncResult(task_id).get()

```

### 指定队列
Celery非常容易设置和运行, 通常它会使用默认的名字为celery的队列(可以使用CELERY_DEFAULT_QUEUE修改)用来存放任务.
基于proj目录下的源码创建一个projq, 对celeryconfig.py添加以下设置
```
from kombu import Queue

CELERY_QUEUES = ( 
    # 定义任务队列
    Queue('default', routing_key="task.#"), # 路由键以"task.",
    # 开头的消息都进default队列. 

    Queue('web_tasks', routing_key='web.#'), #
    # 路由键以"web."开头的都进web_tasks队列
)

CELERY_DEFAULT_EXCHANGE = 'tasks'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = 'task.default'
CELERY_ROUTES = { 
    'projq.tasks.add': { # tasks.add 的消息会进入web_tasks队列
            'queue': 'web_tasks',
            'routing_key': 'web.add',
   }   
}

```
`celery -Aprojq woker -Q web_tasks -l info` 

### 使用任务调度器BEAT
以proj为模板创建projb

`celeryconfig.py`
```
from datetime import timedelta

CELERYBEAT_SCHEDULE = { 
    'add': {
        'task': 'projb.tasks.add',
        'schedule': timedelta(seconds=10),
        'args': (16,16)
    }   
}
```
CELERYBEAT_SCHEDULE中指定了tasks.add这个任务,每10秒钟跑一次, 执行的参数是16,16
启动:
`celery beat -A projb` 
然后启动Worker进程
`celery -A projb worker -l info`

一起启动的方式:
`celery -B -A projb worker -l info`
使用Djanog可以通过django-celery实现在管理后台创建, 删除,更新任务, 是因为他使用了自定义的调度管理类djcelery.schedulers.DatabaseScheduler, 我们可以参考实现. 使用自定义调度类可以实现动态的添加任务.

###  任务绑定, 记录日志和重试

任务绑定, 记录日志和重试是Celery常用的3个高级属性. 现在修改proj/tasks文件. 添加div函数用于演示:
```
from celery.utils import get_task_logger

logger = get_task_logger(__name__)


@app.task(bind=True)
def div(self, x, y): 
    logger.info(('Excuting task id {0.id}, args: {0.args!r}'
                 'kwargs: {0.kwargs!r}').format(self.request))
    try:
        result  = x/y 
    except ZeroDivisionError as e:
        raise self.retry(exc=e, countdown=5, max_retries = 3)
    return result

```
当使用bind = True后, 函数的参数发生变化, 多出了参数self(第一个参数), 相当于把div编程了一个以绑定的方法, 通过self可以获得任务的上下文.
 
 可以发现每个5秒钟重试一次, 一共尝试3次, 然后抛出异常

### 在flask应用中使用Celery
