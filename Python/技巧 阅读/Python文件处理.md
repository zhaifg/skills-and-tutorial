# Python文件处理的技巧
---

## 计算文件行数
### 使用wc等d
### 小文件的处理
```
with open(f, 'r') as f:
    len(f.readlines())
```

### 大文件行数计算
- 1.普通的linux "\n"换行的
```
with open(f, 'r') as f:
    lines = 0
    for _, _ in enumerate(f):
        count += 1
```

- 2.windows文件"\r\n"
```python
with open('ss', 'r') as f:
    count = 0
    while True:
        buffer = f.read(1024 * 8092)
        count += buffer.count("\n")
        if not buffer:
            break
```



## 快速的到达文件尾部

```python
print "--1--"
currut_tell = 0
log = open(fs, 'r')
while True:
    fs = log.read(1024)
    if fs:
        pass
    else:
        currut_tell = log.tell()
        break
```