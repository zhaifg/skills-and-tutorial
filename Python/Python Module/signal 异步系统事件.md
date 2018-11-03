#signal 异步系统事件
---

信号是操作系统特性, 它提供了一个痛经可以通知程序发生了一个事件并异步处理这个事
件. 信号可以由系统本身生成,也可以从一个进程发送到另一个进程. 由于信号会中断程序
的正常控制流, 如果在中间接收到信号,有些操作(特别是I/O操作)可能会产生错误.


## 接收信号
与其他形式基于事件的编程一样,要通过建立一个回调函数来处理信号, 这个回调函数称为
信号处理程序(signal handler),她会在出现信号时调用. 信号处理程序的参数包括信号编
号以及程序被信号中断那一时刻的栈帧.

```py
import signal
import os
import time

def receive_signal(signum, stack):
    print 'Recevied: ', signum


# 注册信号处理处理程序

signal.signal(signal.SIGUSR1, receive_signal)
signal.signal(signal.SIGUSR2, receive_signal)

print "Mypid:" os.getpid()

while True:
    print "Waiting..."
    time.sleep(3)
```

```
python signal_signal.py

```

    kill -USR1 pid
    kill -USR2 pid
    kill -INT pid

## 获取注册程序
要查看为一个信号注册了哪些信号处理程序,可以使用`getsignal()`. 要将信号编号作为
参数传入. 返回值是已注册的处理程序, 或者是以下某个特殊值: `SIG_IGN`(如果信号被
忽略),`SIG_DFL`(如果使用默认行为)或None(如果从C而不是从Python注册现有信号处理程
序).

```
import signal

def alarm_received(n, stack):
    return

signal.signal(signal.SIGALRM, alarm_received)

signals_to_names = dict(
       (getattr(signal, n), n)
       for n in dir(signal)
       if n.startswith('SIG') and '_' not in n
    )
#{0: 'SIG_DFL', 1: 'SIG_IGN'}
for s, name in sorted(signals_to_names.items()):
    handler = signal.getsignal(s)
    if handler is signal.SIG_DFL:
        handler = 'SIG_DFL'
    elif handler is signal.SIG_IGN:
        handler = 'SIG_IGN'
    print '%-10s (%2d):' %(name, s), handler
```

```
[root@yimi devops]# python signal_01.py 
SIGHUP     ( 1): SIG_DFL
SIGINT     ( 2): <built-in function default_int_handler>
SIGQUIT    ( 3): SIG_DFL
SIGILL     ( 4): SIG_DFL
SIGTRAP    ( 5): SIG_DFL
SIGIOT     ( 6): SIG_DFL
SIGBUS     ( 7): SIG_DFL
SIGFPE     ( 8): SIG_DFL
SIGKILL    ( 9): SIG_DFL
SIGUSR1    (10): SIG_DFL
SIGSEGV    (11): SIG_DFL
SIGUSR2    (12): SIG_DFL
SIGPIPE    (13): SIG_IGN
SIGALRM    (14): <function alarm_received at 0x7f9e88956b90>
SIGTERM    (15): SIG_DFL
SIGCLD     (17): SIG_DFL
SIGCONT    (18): SIG_DFL
SIGSTOP    (19): SIG_DFL
SIGTSTP    (20): SIG_DFL
SIGTTIN    (21): SIG_DFL
SIGTTOU    (22): SIG_DFL
SIGURG     (23): SIG_DFL
SIGXCPU    (24): SIG_DFL
SIGXFSZ    (25): SIG_IGN
SIGVTALRM  (26): SIG_DFL
SIGPROF    (27): SIG_DFL
SIGWINCH   (28): SIG_DFL
SIGPOLL    (29): SIG_DFL
SIGPWR     (30): SIG_DFL
SIGSYS     (31): SIG_DFL
SIGRTMIN   (34): SIG_DFL
SIGRTMAX   (64): SIG_DFL
```

## 发送信号

os.kill()

## 闹铃
闹铃(ALarm) 是一种特殊的信号, 程序要求操作系统在过去一段时间之后再发出这个信号
通知. os的标注模块文档指出, 这对于避免一个I/O操作或其他系统调用无限阻塞很有用.
```
import signal
import time

def receive_alarm(signum, stack):
    print "Alarm :", time.ctime()

# 2秒钟引发闹铃
signal.signal(signal.SIGALRM, receive_alarm)
signal.alarm(2)

print 'Before:', time.ctime()
time.sleep(4)
print 'After : ', time.ctime()
```

```
[root@yimi devops]# python signal_alarm.py 
Before: Fri Jan  1 09:26:08 2016
Alarm : Fri Jan  1 09:26:10 2016
After :  Fri Jan  1 09:26:10 2016
[root@yimi devops]# 

```
## 忽略信号
要忽略一个信号,需要注册SIG_IGN作为处理程序.下面这个脚本将SIGINT的默认处理程序替
换为SIG_IGN, 并为SIGUSR1注册一个程序. 然后使用signal.pause()等待接收一个信号.

```
import signal
import os
import time
def do_exit(sig, stack):
    raise SystemExit('Exiting')

signal.signal(signal.SIGINT, signal.SIG_IGN)  # 忽略信号
signal.signal(signal.SIGUSR1, do_exit)

print 'My pid: ', os.getpid()
signal.pause()
```
```
[root@yimi devops]# python signal_ignore.py 
My pid:  25449
^C^C^C^CExiting

# other tamernial
kill -USR1 25449
```
正常情况下,SIGINT(用户按下Ctrl+C时shell会向程序发送这个信号)会产生
KeyboardInterrupt. 这个例子将忽略SIGINT, 并发现SIGUSR1时产生一个Systemexit. 输出中的每个^C表示每一次尝试使用Cr-c从终端结束脚本. 从另一个终端使用kill -USR1 pid才会推出程序.

## 信号和线程
信号和线程通常不能很好的结合,因为只有进程的主线程可以接收信号. 下面的例子建立了
一个信号处理程序. 他在一个线程中等待信号,而从另一个线程发送信号.

```py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-12-31 21:40:45
# @Author  : Zhaifg (zhaifengguo@foxmail.com)
# @Link    : http://htop.me
# @Version : $Id$

import signal
import threading
import os
import time

def signal_handler(num, stack):
    print "Received signal  %d in %s" % (num, threading.currentThread().name)

signal.signal(signal.SIGUSR1, signal_handler)


def wait_for_signal():
    print "Waiting for signal in", threading.currentThread().name
    signal.pause()
    print "Done waiting"

receiver = threading.Thread(target=wait_for_signal, name='receiver')
receiver.start()
time.sleep(0.1)

def send_signal():
    print "Sending signal in", threading.currentThread().name()
    os.kill(os.gitpid(), signal.SIGUSR1)

sender = threading.Thread(target=send_signal, name="sender")
sender.start()
sender.join()

print "Waiting for", receiver.name
signal.alarm(2)
receiver.join()



```

```
[root@yimi devops]# python signal_threads.py 
Waiting for signal in receiver
Sending signal in sender
Received signal  10 in MainThread
Waiting for receiver
Alarm clock

```
信号处理程序都在主线程中注册, 因为这个signal模块Python实现的一个要求, 不论底层平台对于结合线程和信号提供怎样的支持都有这个要求. 尽管接收者线程调用了signal.pause(), 但它不会接收信号.这个例子接近结束时的signal.alarm()调用避免了无限阻塞,因为接收者永远不会退出.

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-01-01 08:25:08
# @Author  : Zhaifg (zhaifengguo@foxmail.com)
# @Link    : http://htop.me
# @Version : $Id$

import signal
import time
import threading

def signal_handler(num, stack):
    print time.ctime(), "Alarm in", threading.currentThread().name

signal.signal(signal.SIGALRM, signal_handler)

def use_alarm():
    t_name = threading.currentThread().name
    print time.ctime(), 'Setting alarm in', t_name
    signal.alarm(1)
    print time.ctime(), 'Sleeping in', t_name
    time.sleep(3)
    print time.ctime(), 'Done with sleep in', t_name

# start a thread that will not receive the signal

alarm_thread = thread.Thread(target=use_alarm, name='alarm_thread')

alarm_thread.start()
time.sleep(0.1)

# Wait for the thread to see the signal (not going to happen!)
alarm_thread.join()

print time.ctime(), 'Exiting normally'
```

```
[root@yimi devops]# vim signal_threads_alarm.py
[root@yimi devops]# python signal_threads_alarm.py 
Fri Jan  1 09:33:30 2016 Setting alarm in alarm_thread
Fri Jan  1 09:33:30 2016 Sleeping in alarm_thread
Fri Jan  1 09:33:33 2016 Done with sleep in alarm_thread
Fri Jan  1 09:33:33 2016 Alarm in MainThread
Fri Jan  1 09:33:33 2016 Exiting normally

```


当handler为signal.SIG_IGN时，信号被无视(ignore)。当handler为singal.SIG_DFL，进程采取默认操作(default)。当handler为一个函数名时，进程采取函数中定义的操作。


```
import signal
# Define signal handler function
def myHandler(signum, frame):
    print('I received: ', signum)

# register signal.SIGTSTP's handler 
signal.signal(signal.SIGTSTP, myHandler)
signal.pause()
print('End of Signal Demo')
```

在主程序中，我们首先使用signal.signal()函数来预设信号处理函数。然后我们执行signal.pause()来让该进程暂停以等待信号，以等待信号。当信号SIGUSR1被传递给该进程时，进程从暂停中恢复，并根据预设，执行SIGTSTP的信号处理函数myHandler()。myHandler的两个参数一个用来识别信号(signum)，另一个用来获得信号发生时，进程栈的状况(stack frame)。这两个参数都是由signal.singnal()函数来传递的。


http://blog.csdn.net/jhonguy/article/details/7716257
