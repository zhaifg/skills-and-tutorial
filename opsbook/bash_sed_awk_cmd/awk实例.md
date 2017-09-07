# awk练习实例

awk测试数据文件data1.dat
```
A125 Jenny 100 210
A341 Dan 110 215
P158 Max 130 209
P148 John 125 220
A123 Linda 95 210
```

## 测试案例

- 1. 组装部门员工调薪5%,(组装部门员工之ID以"A"开头)
所有员工最后之薪资率若仍低于100, 则以100计.
编写awk程序打印新的员工薪资率报表.

[分析 ] : 这个程序须先判断所读入的数据行是否合于指定条件, 再进行某些动作.awk中 Pattern { Actions } 的语法已涵盖这种 " if ( 条件) { 动作} "的架构. 编写如下之程序, 并取名 `adjust1.awk`
```
$1 ~ /^A.*/ { $3 *= 1.05 } $3<100 { $3 = 100 }
{ printf("%s %8s %d\n", $1, $2, $3)}
```

```
 awk '($1 ~ /A.*/) {$3= $3 * 1.05} ($3<100){$3=100}{ print $1,$2,$3}' data.dat
```


## awk 数组

**awk中数组的特性**
> 
- 使用字符串当数组的下标(index).
- 使用数组前不须宣告数组名及其大小.

**例如**: 希望用数组来记录 reg.dat 中各门课程的修课人数.
这情况,有二项信息必须储存:

- (a) 课程名称, 如: "O.S.","Arch.".. ,共有哪些课程事先并不明确.
- (b)各课程的修课人数. 如: 有几个人修"O.S."
- 
在awk中只要用一个数组就可同时记录上列信息. 其方法如下:
使用一个数组 Number[ ] :
以课程名称当 Number[ ] 的下标.
以 Number[ ] 中不同下标所对映的元素代表修课人数.

**例如**:
有2个学生修 "O.S.", 则以 `Number["O.S."] = 2` 表之.
若修"O.S."的人数增加一人,则 `Number["O.S."] = Number["O.S."] + 1` 或 `Number["O.S."]++ `.
如何取出数组中储存的信息

awk 提供了一个指令, 藉由该指令awk会自动找寻数组中使用过的所有下标. 以 Number[ ] 为例, awk将会找到 "O.S.", "Arch.",...
使用该指令时, 须指定所要找寻的数组, 及一个变量. awk会使用该的变量来记录从数组中找到的每一个下标. 例如
`for(course in Number){....}`
指定用 `course` 来记录 awk 从`Number[ ] `中所找到的下标. awk每找到一个下标时, 就用course记录该下标之值且执行{....}中之指令. 藉由这个方式便可取出数组中储存的信息.
(详见下例)

**[ 范例 : ] 统计各科修课人数,并印出结果**.
建立如下程序,并取名为 `course.awk`:
```
{ for( i=2; i <= NF; i++) Number[$i]++ }
END{for(course in Number) printf("%10s %d\n", course, Number[course] )}
执行下列命令 :
$awk -f course.awk reg.dat
执行结果如下 :
  Graphics 2
      O.S. 2
  Discrete 3
      A.I. 1
      D.S. 1
     Arch. 2
 Algorithm 2
```
[ 说 明 : ]
 
这程序包含二个Pattern { Actions }指令.
{ for( i=2; i <= NF; i++) Number[$i]++ }
END{for(course in Number) printf("%10s %d\n", course, Number[course] )}
第一个Pattern { Actions }指令中省略了Pattern 部分. 故随着
每笔数据行的读入其Actions部分将逐次无条件被执行.
以awk读入第一笔资料 " Mary O.S. Arch. Discrete" 为例, 因为该笔数据 NF = 4(有4个字段), 故该 Action 的for Loop中i = 2,3,4.
i $i 最初 Number[$i] Number[$i]++ 之后
i=2时 $i="O.S." Number["O.S."]的值从默认的0,变成了1 ;
i=3时 $i="Arch." Number["Arch."]的值从默认的0,变成了1 ;
同理,i=4时 $i="Discrete" Number["Discrete"]的值从默认的0,变成了1 ;
 
第二个 Pattern { Actions }指令中END 为awk之保留字, 为 Pattern 的一种.
END 成立(其值为true)的条件是: "awk处理完所有数据, 即将离开程序时. "
平常读入数据行时, END并不成立, 故其后的Actions 并不被执行;
唯有当awk读完所有数据时, 该Actions才会被执行 ( 注意, 不管数据行有多少笔, END仅在最后才成立, 故该Actions仅被执行一次.)
BEGIN 与 END 有点类似, 是awk中另一个保留的Pattern.
唯一不同的是: "以 BEGIN 为 Pattern 的 Actions 于程序一开始执行时, 被执行一次."
NF 为awk的内建变量, 用以表示awk正处理的数据行中, 所包含的字段个数.
 
awk程序中若含有以 $ 开头的自定变量, 都将以如下方式解释 :
以 i= 2 为例, $i = $2 表第二个字段数据. ( 实际上, $ 在 awk 中为一运算符(Operator), 用以取得字段数据.)


`姓名,学科1,学科2,学科3`
```
Mary O.S. Arch. Discrete
Steve D.S. Algorithm Arch.
Wang Discrete Graphics O.S.
Lisa Graphics A.I.
Lily Discrete Algorithm
```

## my
```
awk '{for(i=2;i<=NF;i++) num[$NF]++ } END {for (n in num) print n, num[n]}' edu.dat

```

## awk 中使用shell命令读取信息
awk 'BEGIN {print `who`}'


## 统计输入最多一行
```
awk '{if(length($0) > max) max=length($0)}' data.txt 

```
