# tty   
---
需要`termios`模块

The tty module defines functions for putting the tty into cbreak and raw modes.

Because it requires the termios module, it will work only on Unix.

The tty module defines the following functions:

## tty.setraw(fd[, when])
Change the mode of the file descriptor fd to raw. If when is omitted, it defaults to termios.TCSAFLUSH, and is passed to termios.tcsetattr().

## tty.setcbreak(fd[, when])
Change the mode of file descriptor fd to cbreak. If when is omitted, it defaults to termios.TCSAFLUSH, and is passed to termios.tcsetattr().

```python

import os, sys
fileno = sys.stdin.fileno()

tty.setraw(fileno)
print raw_input("INPUT: ")

tty.setbreak(fileno)
print raw_input("break: ")

os.system("stty sane")


```

let g:ycm_server_keep_logfiles = 1
let g:ycm_server_log_level = 'debug'
