# getpass  curses
---

- getpass 提供两个函数

## getpass.getpass([prompt[,stream]])
提示用户输入密码,但是会输出,提示为内容是prompt内容.如果'Password:'.  `stream`在unix系统上,提示信息被写入类似 文件的stream中,默认是/dev/tty,如果不可用,则写入sys.err. 在windows `stream`参数不可用.
如果无回显输入不可用，getpass() 回退并向流 stream 中输出一个警告消息，从 sys.stdin 中读取并抛出异常 GetPassWarning

`exception getpass.GetPassWarning` 
Python内置异常 UserWarning 的子类，当密码输入可能被回显时抛出。


## getpass.getuser()
返回当前的'login name'. 这个函数检测环境变量`LOGNAME`,`USER`,`LNAME`and `USERNAME`
```
import getpass
import sys

if sys.stdin.isatty():
    p = getpass.getpass('Using getpass: ')
else:
    print 'Using readline'
    p = sys.stdin.readline().rstrip()

print 'Read: ', p
#With a tty:
```
```
$ python ./getpass_noterminal.py
Using getpass:
Read:  sekret
Without a tty:
```
```
$ echo "sekret" | python ./getpass_noterminal.py
Using readline
Read:  sekret
```

## curses 
ncurses（new curses）是一个程序库，它提供了API，可以允许程序员编写独立于终端的基于文本的用户界面。它是一个虚拟终端中的“类GUI”应用软件工具箱。它还优化了屏幕刷新方法，以减少使用远程shell时遇到的延迟。

curses是于ncurses系统的交互的接口. DOS, os/2.


https://docs.python.org/2.7/library/curses.html
