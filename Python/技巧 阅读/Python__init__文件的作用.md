# Python __init__.py
---
每个Python模块下的都有一个这个文件, 当我们导入这个包的时候,__init__.py文件就会自动运行.

## __init__.py的作用有如下几点：

1. 相当于class中的def __init__(self):函数，用来初始化模块。

2. 把所在目录当作一个package处理

3. from-import 语句导入子包时需要用到它。 如果没有用到, 他们可以是空文件。

如引入package.module下的所有模块
`from package.module import * ``
这样的语句会导入哪些文件取决于操作系统的文件系统. 所以我们在__init__.py 中加入 __all__变量. 

该变量包含执行这样的语句时应该导入的模块的名字. 它由一个模块名字符串列表组成.


##　工厂函数

https://zh.wikipedia.org/wiki/%E5%B7%A5%E5%8E%82%E6%96%B9%E6%B3%95
https://young-py.gitbooks.io/mastering_object-oriented_python/content/1-1-5.html
