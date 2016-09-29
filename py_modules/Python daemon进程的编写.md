# Linux下的Python daemon进程编写
---

## 了解 PEP 3143 中对 daemon行为的描述

[PEP143](http://www.python.org/dev/peps/pep-3143/#correct-daemon-behaviour)

- Close all open file descriptors.              （关闭所有打开的文件描述符。）
- Change current working directory.       （改变当前工作目录。）
- Reset the file access creation mask.   （重设文件访问创建掩码。）
- Run in the background.                         （在后台运行。）
- Disassociate from process group.       （脱离进程组。）
- Ignore terminal I/O signals.                  （忽略终端I / O信号。）
- Disassociate from control terminal.     （脱离控制终端。）
- Don’t reacquire a control terminal.       （不要重新获得一个控制终端。）

- Correctly handle the following circumstances:      （正确处理好以下情况：）
-- Started by System V init process.                （开始由System V init进程。）
-- Daemon termination by SIGTERM signal.   （SIGTERM信号守护程序终止。）
-- Children generate SIGCLD signal.               （子进程产生SIGCLD信号。）


## 使用python_daemon模块来快速写一个daemon

```
pip install python_daemon
```

```python

#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from time import sleep, asctime
from daemon.runner import *

class myDaemon(object):

    def __init__(self):
        self.name = 'myDaemon'
        self.working_directory = 
        self.stdin_path  = os.devnull
        self.stdout_path = os.path.join('daemon.log')
        self.stderr_path = os.path.join('daemon.log')
        self.pidfile_path = "var/run/myDaemon.pid"
        self.pidfile_timeout = 120
    #   self.run = self.myEcho()

    def run(self):
        self.myEcho()

    def myEcho(self):

        while True:
            with  open('/tmp/myEcho.log','a') as f:
                try:
                    f.write(asctime())
                    f.flush()
                except Exception:
                    pass
                finally:
                    f.close()
            sleep(5)

if __name__ == '__main__':
    mydaemon = myDaemon()
    myRunner = DaemonRunner(mydaemon)
    myRunner.do_action()
```

使用 python_daemon写 daemon 程序只需要简单的3步：
- 1, 引入daemon_runner
- 2, 完成daemon app的代码, 需要注意的是daemon app中需要设置参数:
```
class myDaemon:
    def __init__(self):

        self.name = 'myDaemon'
        self.working_directory = '/home/chunsheng/workspace/py_daemon_test/src/py_daemon/'
        self.stdin_path = os.devnull
        self.stdout_path = os.path.join('daemon.log')
        self.stderr_path = os.path.join('daemon.log')
        self.pidfile_path = '/var/run/myDaemon.pid'
        self.pidfile_timeout = 120
```
- 3, 用DaemonRunner将daemon app实例化:
```


if __name__ == '__main__':
    mydaemon = myDaemon()
    myRunner = DaemonRunner(mydaemon)
    myRunner.do_action()

```

```
# python py_daemon.py
usage: py_daemon.py start|stop|restart
# python py_daemon.py start
# ps aux | grep python
root      8026  0.0  0.0  12952  3792 ?        S    14:50   0:00 python py_daemon.py start

# python py_daemon.py stop
```

##　参考

[参考](http://blog.chunshengster.me/2012/02/yong_python_daemon_lai_kuai_su_wan_cheng_unix_daemon.html)
[pep-3143](https://www.python.org/dev/peps/pep-3143/)
[how-do-you-create-a-daemon-in-python](http://stackoverflow.com/questions/473620/how-do-you-create-a-daemon-in-python)
[http://code.activestate.com/recipes/278731/](http://code.activestate.com/recipes/278731/)
