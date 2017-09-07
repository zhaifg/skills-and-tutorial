# errno
---
在日常开发中经常需要捕获各种异常, 做特殊处理.
```
import errono

def listdir(dirname):
    try:
        os.listdir(dirname)
    except OSError as e:
        error = e.errno
        if error == errno.ENOENT:
            print "No Such file or directory"
        elif error == errno.EACCESS:
            print 'Prmission denied'
        elif error == errno.ENOSPC:
            print "No space left on device"
        else:
            print e.strerror
```
