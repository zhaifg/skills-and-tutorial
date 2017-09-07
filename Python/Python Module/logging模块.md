# logging模块
---

Logger从来不直接实例化，经常通过logging模块级方法（Module-Level Function）logging.getLogger(name)来获得，其中如果name不给定就用root。名字是以点号分割的命名方式命名的(a.b.c)。对同一个名字的多个调用logging.getLogger()方法会返回同一个logger对象。这种命名方式里面，后面的loggers是前面logger的子logger，自动继承父loggers的log信息，正因为此,没有必要把一个应用的所有logger都配置一遍，只要把顶层的logger配置好了，然后子logger根据需要继承就行了


主要是总结python的logging的使用
python日志模块logging：从python2.3开始加入此模块，子模块包含loggers,handlers,filters和formatters。
 
## 一.  Loggers把应用需要直接调用的接口暴露出来。

Logger从来不直接实例化，经常通过logging模块级方法(Module-Level Function)logging.getLogger(name)来获得，其中如果name不给定就用root。名字是以点号分割的命名方式命名的(a.b.c)。对同一个名字的多个调用`logging.getLogger()`方法会返回同一个`logger对象`。这种命名方式里面，后面的loggers是前面logger的子logger，自动继承父loggers的log信息，正因为此,没有必要把一个应用的所有logger都配置一遍，只要把顶层的logger配置好了，然后子logger根据需要继承就行了。

**logging.Logger对象扮演了三重角色**:
1. 首先,它暴露给应用几个方法以便应用可以在运行时写log.
2. 其次,Logger对象按照log信息的严重程度或者根据filter对象来决定如何处理log信息(默认的过滤功能).
3. 最后,logger还负责把log信息传送给相关的handlers.

**部分具体方法**：
`setLevel(lvl)` : 定义处理log的最低等级，内建的级别为:`DEBUG`,`INFO`, `WARNING`, `ERROR`, `CRITICAL`

下图是级别对应数值
`debug`(log_message, [*args[, **kwargs]])
`info`(log_message, [*args[, **kwargs]])
`warning`(log_message, [*args[, **kwargs]])
`error`(log_message, [*args[, **kwargs]])
`critical`(log_message, [*args[, **kwargs]])
`exception`(message[, *args])和error()一样，多出一个stack trace用于转储，exception()方法只能从一个exception handler里面调用.

`log(log_level, log_message, [*args[, **kwargs]])`显式的带一个level参数,用这个可以得到比使用上面所列举的方法更为详细的log信息。
`addFilter()`和`removeFilter()`分别用于为handler增加一个filter和删除一个filter。
`addHandler(hdlr)`加入一个Handler。
 
## 二.  Handlers把Logger记录发到相应的目的地，也可认为是处理日志的方式。
对Logger对象通过addHandler()方法添加零个或多个handler对象到Logger中。

- 1. Handler不直接实例化，通过引用logging.Handler对象来实例化（如logging.FileHandler），Handler对象有以下几种：
 
StreamHandler      发送日志到流中                       核心logging模块中
FileHandler        发生日志到文件中                     核心logging模块中
NullHandler        无操作的日志处理类                   核心logging模块中，2.7版本新加

- 2. 以下Handler都定义在子模块logging.handlers中

`WatchedFileHandler` 是一个FileHandler，当日志文件改变后，文件会被关闭，并且使用同样的文件名再次打开。如果由于在运行的程序外部执行了日志备份操作, 从而导致日志文件已被删除或移动,这些变化可能就会发生。此处理器只能工作在UNIX系统上。

`RotatingFileHandler` 发送日志到文件，并且限制最大的日志文件大小，并适时轮徇。maxBytes单个文件的最大字节数；backupCount部分文件的个数，当文件超出maxBytes后会重新部分在心文件中，旧文件会以.1重新命名，最终备份文件数等于.backupCount
`TimedRotatingFileHandler`   发生日志到文件，并在适当的事件间隔进行轮徇
`SocketHandler`           日志通过TCP协议发送
`DatagramHandler`         日志通过UDP协议发送
`SysLogHandler`           发送日志到UNIX syslog服务，并支持远程syslog服务
`NTEventLogHandler`       发送日志到WindowsNT/2000/XP事件日志
`SMTPHandler`             通过SMTP协议发送日志
`MemoryHandler`           发送日志到内存中的缓冲区，并在达到特定条件时清空
`HTTPHandler`             通过GET或POST方法发送日志到HTTP服务器
  
- 3. 部分具体方法：

`setLevel()`方法跟logger对象里面的setLevel()一样，也是用于设定一个最低分发log信息的级别。

为什么有两个setLevel()呢？logger的严重等级用于决定那个级别的log信息可以分发到它的handlers。handler里面的level设置用于控制哪些个log信息是handler需要转寄的。
setFormatter()方法选定一个格式化对象给它自己用。
addFilter()和removeFilter()分别用于为handler增加一个filter和删除一个filter。
 
## 三.  Filters决定哪些记录需要发给Handlers。
Filters能够用在Loggers和Handlers上，可以实现比level更复杂的过滤。可以直接实例化。通过构造函数参数name可以过滤日志名称。
 
##四.  Formatters定义了Logger记录的输出格式。
定义了最终log信息的内容格式，应用可以直接实例化Foamatter类。信息格式字符串用`%(<dictionary key>)`s风格的字符串做替换。
属性名称
 
|      格式      |                      说明                      |
|----------------|:-----------------------------------------------|
|   name         |  %(name)s  日志的名称                          |
|  asctime       |  %(asctime)s 可读时间，默认格式‘2003-07-08 16:49:45,896’，逗号之后是毫秒 |
|  filename      |  %(filename)s 文件名，pathname的一部分  |
|  pathname      |  %(pathname)s 文件的全路径名称  |
|  funcName      |  %(funcName)s 调用日志多对应的方法名  |
|  levelname     |  %(levelname)s  日志的等级   |
|  levelno       |  %(levelno)s    数字化的日志等级  |
|  lineno        |  %(lineno)d  被记录日志在源码中的行数  |
|  module        |  %(module)s 模块名  |
|  msecs         |  %(msecs)d   时间中的毫秒部分  |
|  process       |  %(process)d  进程的ID  |
|  processName   |  %(processName)s 进程的名称  |
|  thread        |  %(thread)d 线程的ID  |
|  threadName    |  %(threadName)s 线程的名称 |
|  relativeCreated | %(relativeCreated)  d日志被创建的相对时间，以毫秒为单位  |


## 五.  模块级方法，以下模块级方法（Module-Level Function）中直接记录log信息针对的是名为root的logger对象，其默认level是warning。

`debug(log_message, [*args[, **kwargs]])`
`info(log_message, [*args[, **kwargs]])`
`warning(log_message, [*args[, **kwargs]])`
`error(log_message, [*args[, **kwargs]])`
`critical(log_message, [*args[, **kwargs]])`
`exception(message[, *args]) `         和error()一样，多出一个stack trace用于转储，exception()方法只能从一个exception handler里面调用.
log(log_level, log_message, [*args[, **kwargs]])   显式的带一个level参数,用这个可以得到比使用上面所列举的方法更为详细的log信息。

`addHandler()`  添加一个Handler对象
 
##  六.  日志配置，通过logging.config包进行相关处理。

-  1 文件配置方式
python可以通过配置文件来定义日志，配置文件的格式通过`logging.config.fileConfig()`此函数基于ConfigParser）来解析，`[loggers]` ,` [handlers]` 和 `[formatters]` ,用来标识文件定义的几种类型的实体。这价格标识必须包含在配置文件中。
[loggers]标识： 

关键字keys后通过=号指定对应logger实体的名称，而对具体的logger实体配置就在[logger_logger实体名]，如keys=root则对应详细配置在[logger_root]中。
详细配置如[logger_root] 中必须包含level和handlers，level值包含一中介绍的所以level信息；handlers包含一个或多个在[handlers]定义的值，多值用“，”分开。
还可能包括propagate和qualname，propagete项如果为1，则表示该logger必须处理它继承的父类logger的信息，如果为0则不必； qualname项表示logger的分层结构的上下文名称，应用程序中就是用这个名字结合logger实体名称来获得logger的全路径。

[handlers]标识： 与[loggers]类似，如keys=hand01则具体配置在[handler_hand01]。
详细配置如[handler_hand01]中包含class，level，formatter和args等关键字。
class值表示handlers的具体类；level是handler的日志级别；formatter表示用于此handler的格式，此处如果不为空必须在[formatters]总定义，如果为空则用默认的formatter(logging._defaultFormatter)；
args表示handler实例化时传给handler构造函数的参数，多个参数用“()”扩起来。
[formatters]标识： 同上，keys=format01则[formatter_format01]。
详细配置如[formatter_format01]中包含format，datefmt和class。
class可选，它指出了 formatter 的类名(模块名和类名通过点来分隔)；format定义格式字符串，方式如四中介绍；datefmt项可以接受跟strftime()函数兼容的时间/日期格式字符串。如果为空，则默认用ISO8601格式的日期/时间格式，其格式也定义了微秒，可以用一个逗号隔开添加到上面的格式字符串之后，ISO8601格式的一个示例是 2003-01-23 00:29:50,411。

**如下实例**：log配置
```     
[loggers]  
keys=root, demo1  
  
[handlers]  
keys=console, filehandler  
  
[formatters]  
keys=format1  
  
[logger_root]  
level=DEBUG  
handlers=console  
  
[logger_demo1]  
level=INFO  
handlers=filehandler  
propagate=0  
qualname=wjinfo  
  
[handler_console]  
class=StreamHandler  
level=DEBUG  
args=(sys.stdout,)  
formatter=format1  
  
[handler_filehandler]  
class=handlers.RotatingFileHandler  
level=INFO  
args=("F:/tmp/logdemo/a.log", 'a', 20480, 5)  
formatter=format1  
  
[formatter_format1]  
format=%(asctime)s-%(name)s-%(module)s-%(levelname)s: %(message)s  
class=logging.Formatter
```
```
import logging.config  
  
logging.config.fileConfig('./loginfo')  
  
logger1 = logging.getLogger()  
logger1.debug("nihao")  
  
logger2 = logging.getLogger('wjinfo.demo1')  
logger2.info("gunkai")  
logger2.info("gunkai2")  
```
 
- 2 字典配置方式
python可以通过字典的键值对应参数的方式配置日志。字典配置通过`logging.config.dictConfig(config)`来实现。

配置字典包含以下键：`version；formatters；filters；handlers；loggers；root；disable_existing_loggers`等。

## 设置实例
```
logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s - %(name)s -  %(levelname)s -' \
       ' %(message)s', filename='/mnt/xvdb1/yimilogs/apimonitor.log', filemode='a')
    # level=logging.DEBUG, format='%(asctime)s - %(funcName)s - %(name)s -
    # %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

```

## python logging的高级用法
[高级][1]
[2][2]


  [1]: http://python.jobbole.com/81132/
  [2]: http://python.jobbole.com/82221/
