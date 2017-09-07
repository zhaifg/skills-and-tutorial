#读<<Shell脚本专家>>
----
## 调试
set -x
echo
debug: debug值

## 库函数
/etc/init.d/functions
. source NFS 集中存放--> git, ansible发放
## 日期和时间操作

从1970-1-1开始算
(year * 365) + (year/4)-(year/100)+(year/400)+(Month*306001/10000)+day 计算天数

以秒计算
date

## 比较测试
字符串比较时, 只有显示的字符串才需要引号, 字符串变量明泽不需要引导

getops

## 测试变量和设置默认值
-z var
${var:="some"}

## 非直接引用变量
## shell进程树

## shell中数学
expr
加减乘除
'expr $c + $d'
'expr $c - $d'
'expr $c \* $d'
'expr $c / $d'
'expr $c % $d'
$(())
let **
