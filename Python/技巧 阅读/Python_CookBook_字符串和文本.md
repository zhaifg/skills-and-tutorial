# 字符串和文本
---

## 使用多个界定符分割你符串
1. 简单的分割:split()
2. 灵活的分割: re.split()

## 字符串匹配开头和结尾
1. startswith()/ endswith()

如果想检查多种匹配的可能, 只需要将所有的匹配项放入到一个元组中,然后传给startswith/endswith方法中
```
choices = ('http', 'https')
url = 'http://www.python.org'
print(url.startswith(choices))
>> True
```

2. 正则实现
3

## shell通配符
- fnmatch模块提供了两个函数: fnmatch和fnmatchcase()

## 字符串搜索和替换
str.find, startswith, endswith
正则匹配
match, findall()

### 替换
str.replace()
re.sub()

## 字符串忽略大小写的搜索和替换
re模块的re.IGNORECASE

## 最短匹配模式

r'(.*)': 贪婪模式
r('.*?'): 最短模式

## 多行匹配模式

`r'/\*(.*?)\*/'`  匹配C语言的注释
re.DOTALL: 可以让正则表达式中点(.)匹配包括换行符在内的任一字符.
`re.complie(r'/\*(.*?)\*/', re.DOTALL)`

## Unicode
在unicode中, 一个字符串可是使用多个合法的编码.
unicodedata模块使字符编码标准化
`unicodedata.normalize('NFD', s2)`
