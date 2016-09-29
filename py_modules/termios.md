#termios
---


```python

def getpass(prompt="Password: "):
    import termios, sys
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~termios.ECHO          # lflags
    try:
        termios.tcsetattr(fd, termios.TCSADRAIN, new)
        passwd = raw_input(prompt)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return passwd

```

```python

import termois, TERMIOS
import sys

fileno = sys.stdin.fileno()

attr = termios.tcgetattr(fileno)
orig = attr[:]
print "attr=>", attr[:4] # flags

# disable echo flag
attr[3] = attr[3] & ~termios.ECHO

try:
        termios.tcsetattr(fileno, termios.TCSADRAIN, attr)
        passwd = raw_input(prompt)
    finally:
        termios.tcsetattr(fileno, termios.TCSADRAIN, orig)
```
