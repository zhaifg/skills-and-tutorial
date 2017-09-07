# struct--二进制数据结构
---
在字符串和二级制数据之间转换

struct 提供了一组处理结构值的模块级函数, 另外还有个Struct类. 格式指示符有字符串转换为一种编译表示, 这类似于正则表达式处理. 这个转换会耗费资源, 所以当创建一个Struct实例并在这个实力上调用方法时(而不是使用模块级别函数), 完成一次转换会更为高效.


### 打包和解包
Struct支持使用格式指示符将数据打包(packing)为字符串, 以及将字符串(unpacking)数据, 各式制服由数据类型的字符以及可选数量以及字节序指示符构成. 要全面了解目前的指示符要看标准文档.

下面的例子中, 指示符要求有一个整数或龙值, 一个包含两个字符的串, 以及一个浮点数. 格式指示符中包含的空格用来分割数据类型指示符, 在编译时会被忽略;
```python
In [19]: from struct import Struct

In [20]: values = (1, 'ab', 2.7)

In [21]: s = Struct('I 2s f')

In [22]: packed_data = s.pack(*values)

In [23]: values
Out[23]: (1, 'ab', 2.7)

In [24]: s.format
Out[24]: 'I 2s f'

In [25]: s.size
Out[25]: 12

In [26]: import binascii

In [27]: binascii.hexlify(packed_data)
Out[27]: '0100000061620000cdcc2c40'
```
解包

```
In [28]: unpacked_data = s.unpack(packed_data)

In [29]: unpacked_data
Out[29]: (1, 'ab', 2.700000047683716)
```



有的时候需要用python处理二进制数据，比如，存取文件，socket操作时.这时候，可以使用python的struct模块来完成.可以用 struct来处理c语言中的结构体.
 

struct模块中最重要的三个函数是pack(), unpack(), calcsize()

pack(fmt, v1, v2, ...)     按照给定的格式(fmt)，把数据封装成字符串(实际上是类似于c结构体的字节流)

unpack(fmt, string)       按照给定的格式(fmt)解析字节流string，返回解析出来的tuple

calcsize(fmt)                 计算给定的格式(fmt)占用多少字节的内存

Python中没有二进制类型，但是可以使用string字符串类型来存储二进制数据，然后使用struct模块来对二进制数据进行处理。下面将详细描述如何使用struct模块来处理二进制数据。

使用struct.pack把一个整数值打包成字符串，打开Python命令行，输入：

>>>import struct

>>> a =0x01020304

>>> str= struct.pack("I", a)

>>>repr(str)

"'\\x04\\x03\\x02\\x01'"

此时，str为一个字符串，字符串中的内容与整数a的二进制存储的内容相同。

 

使用struct.unpack把字符串解包成整数类型，如下：

>>> b =struct.unpack("I", str)

>>> b

(16909060,)

在解包之后，返回一个元组类型(tuple)的数据。

如果多个数据进行打包，可以在格式中指定打包的数据类型，然后数据通过参数传入：

>>> a ="hello"

>>> b ="world!"

>>> c =2

>>> d =45.123

>>> str= struct.pack("5s6sif", a, b, c, d)

等价于: struct.pack_into(“5s6sif”,str,  0, a, b, c, d)

>>> str

'helloworld!\x00\x02\x00\x00\x00\xf4}4B'

解包多个数据可以这样做：

>>>parts = struct.unpack("5s6sif", str)

等价于：  struct.unpack_from(“5s6sif”, str, 0)

>>>parts

('hello','world!', 2, 45.12300109863281)

从上可以看到浮点值在解包后与原来值不一样，这是因为浮点数的精度问题导致的。

struct模块中二进制格式化表示


计算格式字符串的大小函数：struct.calcsize(fmt)

>>>struct.calcsize("ihi")                       缺省为4字节对齐时，长度为12

12

>>>struct.calcsize("iih")                            当h在最后的时（此时不4字节对齐），长度为10

10

>>>struct.calcsize("@ihi")

12

>>>struct.calcsize("=ihi")

10

>>>struct.calcsize(">ihi")

10

>>>struct.calcsize("<ihi")

10

>>>struct.calcsize("!ihi")

10

注：二进制文件打开/读取的时候需要使用“rb”/“wb”模式以二进制方式打开/读取文件。

注：关于LE(little-endian)和BE（big-endian）区别：

LE—最符合人的思维的字节序，地址低位存储值的低位，地址高位存储值的高位。

BE—最直观的字节序，地址低位存储值的高位，地址高位存储值的低位。

例如：双字0X01020304在内存中存储方式，LE=0403 02 01，BE=01 02 03 04。

http://www.cnblogs.com/gala/archive/2011/09/22/2184801.html
http://blog.csdn.net/ithomer/article/details/5974029
https://docs.python.org/2/library/struct.html
