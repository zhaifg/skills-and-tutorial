# Python3 学习手册
---

## 多个变量赋值
```python
# p = (4, 5)
x, y =p
print(y)
print(x)
5
4


data = ['ACME', 50, 91.1, (2012,12,21)]
name, shares, price, date = data
print(name)
print(shares)
print(price)
print(date)


# 过滤掉一些
_, shares_1, price_1, _ = data
print(shares_1)
print(price_1)

# 使用*列表过滤掉中间的数据
grades = [1,2,3,4,5]
first, *middle, last = grades

1
[2, 3, 4]
5
```

通过某个字段分组
from itertools import groupby

ChainMap

yield from
print('hello world', file=f)

## 内置函数
abs()
all(iterable): iterable 所有元素返回true
any(iterable): iterable 有元素返回true
ascii(object)
bin()
bool()
bytearray() Return a new array of bytes
bytes()
callable()
chr()
classmethod()
compile()
complex()
delattr()
dict()
dir()
divmod()
enumerate()
eval()
exec()
filter()
format()
frozenset()
getattr()
globals()
hasattr()
hash()
help()
hex()
id()
input()
int()
isinstance()
issubclass()
iter()
len()
list()
locals()
map()
max()
memoryview()
min()
next()
object()
oct()
open()
ord()
pow()
print()
property()
range()
repr()
reversed()
round()
set()
settattr()
slice()
sorted()
staticmethod()
str()
sum()
super()
tuple()
tyoe()
vars()
zip()
__import__()
