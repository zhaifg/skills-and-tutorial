# 读awk 手册
----


```
pattern {action}
pattern {action}
```

怎么执行awk
awk 'program' input-file1 input-file2
awk -f program-file input-file1 input-file2

## awk 命令行模式

-F fs
-f source-file
--file source-file

-v var=val
--assign var=val

...

## awk的环境变量
GAWK_MSEC_SLEEP
GAWK_READ_TIMEOUT

```
#!/bin/awk -f
BEGIN {print "Don't Panic"}
```

awk程序中用注释##
```
## awk 'BEGIN { print "Here is a single quote <'"'"'>" }'

[root@yimiwork_211 awk]# awk 'BEGIN { print "Here is a single quote <'"'"'>" }'
Here is a single quote <'>
# OR
awk 'BEGIN { print "Here is a single quote <'\''>" }'

```

## if分支
```
awk ' $1> 1100 { print $1} $1 < 1100 {print $2 } ' arr.dat 
7:26
7:27
1101
7:45
7:46
7:49
7:51
7:57
7:59
8:01
8:05
8:12
[root@yimiwork_211 awk]# awk '{ if  ($1> 1100) { print $1} else {print $2 }} ' arr.dat 
7:26
7:27
1101
7:45
7:46
7:49
7:51
7:57
7:59
8:01
8:05
8:12
[root@yimiwork_211 awk]# awk '{ if  ($1> 1100) {print $1} else {print $2 }} ' arr.dat 
7:26
7:27
1101
7:45
7:46
7:49
7:51
7:57
7:59
8:01
8:05
8:12
[root@yimiwork_211 awk]# awk '{ if  ($1> 1100) {print "-->", $1} else {print $2 }} ' arr.dat 
7:26
7:27
--> 1101
7:45
7:46
7:49
7:51
7:57
7:59
8:01
8:05
```

## 转义符 \


## 模式

- 1. BEGIN { 语句 }
在读取任何输入前执行一次 语句

- 2. END { 语句 }
读取所有输入之后执行一次 语句

- 3. 表达式 { 语句 }
对于 表达式 为真（即，非零或非空）的行，执行 语句

- 4. /正则表达式/ { 语句 }
如果输入行包含字符串与 正则表达式 相匹配，则执行 语句

- 5. 组合模式 { 语句 }
一个 组合模式 通过与（&&），或（||），非（|），以及括弧来组合多个表达式；对于组合模式为真的每个输入行，执行 语句

- 6. 模式1，模式2 { 语句 }
范围模式(range pattern)匹配从与 模式1 相匹配的行到与 模式2 相匹配的行（包含该行）之间的所有行，对于这些输入行，执行 语句 。
BEGIN和END不与其他模式组合。范围模式不可以是任何其他模式的一部分。BEGIN和END是仅有的必须搭配动作的模式。

## 定义多个分隔符
awk -F'[-:]'  -或:

1.外部传入参数
比如从外面传入超时的阀值，注意threshold在命令行中的位置。

awk '{if($(NF)*1>threshold) print}' threshold=20 access.log
2.常用函数
最有用是gsub和sub，match，index等。其中gsub将一个字符串替换为目标字符串，可选定整行替换或只替换某一列。

awk '{gsub("ms]","",$NF); if( $NF>100 ) print}' access.log

3. 正则表达式分隔符
```
$ echo ' a  b  c  d ' | awk 'BEGIN { FS = "[ \t\n]+" }
>                                  { print $2 }'
```

4. getline



## 内置变量
BINMODE #
CONVFMT
FIELDWIDTHS #
FPAT #
FS
IGNORECASE #
LINT #
OFMT
OFS
PREC #
ROUNDMODE 
RS
SUBSEP
TEXTDOMAIN

## 内置函数

## 数组
定义形式
a[0]=1
a[2]=2
a['如家']='ddd'
a['dog']
## 字符串处理

## 运算符


