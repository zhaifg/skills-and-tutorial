# 数据结构结构和算法
---

## 通过某个字段将记录分组
`{'address': '1039 W GRANVILLE', 'date': '07/04/2012'}`
使用date分组后数据块进行迭代
```python
from operator import itemgetter
from itertools import groupby

rows.sort(key=itemgetter('date'))

for date, items in groupby(rows, key=itemgetter('date')):
    print(date)
    for i in items:
        print(' ', i)

```
groupby() 函数扫描整个序列并且查找连续相同值(或者根据指定key函数返回值相同)的元素序列. 在每次迭代的时候, 它会返回一个值和一个迭代器对象, 这个迭代对象可以生成元素值全部等于上面那个值的组中所有对象.

## 过滤
- 列表推到
  * 缺点: 数据量大时, 浪费内存
  * 迭代器: pos = (n for n in mylist if n > 0)--> for x in pos: print(x)
  * filter
  * itertools.compress(): 它以一个iterable对象和一个相应的Boolean选择器序列作为输入参数. 然后输出iterable对象中对应的选择器为True的元素. 当你需要用另外一个相关联的序列来过滤某个序列的时候, 这个函数非常有用.

## 从字典中提取子集

1. 推到公式: `dict((key, value) for key, value in prices.items() if value > 200 )`

## 命名元组
```
from collections import nametuple

User = nametuple("User", ["name", "age"])
user = User("zhaifg", "25")
# 元组默认不能修改, 需要修改时使用replace 方式
user._replace(age=34)
```

## 合并多个字典或 映射

假设你必须在两个字典中执行查找操作(比如先从a中找, 如果找不到再在b中找). 一个非常简单方案使用collections模块中的ChainMap类.
```
from collections import ChainMap
c = ChainMap(a, b)
print(c['x'])
print(c[]y'')
```
