# Python的调试方法
---

## pdb
pdb模块
### 使用方式
####  使用方式 一
```
>>> import pdb
>>> import mymodule
>>> pdb.run('mymodule.test()')
> <string>(0)?()
(Pdb) continue
> <string>(1)?()
(Pdb) continue
NameError: 'spam'
> <string>(1)?()
(Pdb)
```

#### 使用方式二
```
python -m pdb myscript.py
```
当作为脚本调用时，如果正在调试的程序异常退出，pdb将自动进入事后调试。经post-mortem debugging（或正常退出程序后），pdb将重新启动程序。自动重新启动保留pdb的状态（例如断点），并且在大多数情况下比程序退出时退出调试器更有用。

#### 使用方式三
从正在运行的程序中断入调试器的典型用法是插入
```
import pdb; pdb.set_trace()

```


### pdb模块的相关函数
`pdb.run(statement[,globals[, locals]])`
debugger执行statement(字符串形式)语句.他在任何代码执行之前出现调试器提示; 您可以设置断点并键入continue，也可以使用step或next（所有这些命令在下面解释）逐步执行语句。
statement: 要调试的语句块，以字符串的形式表示
globals: 可选参数，设置statement运行的全局环境变量
locals: 可选参数，设置statement运行的局部环境变量


`pdb.runeval(expression[,globals[,locals]])`: 在调试器控制下评估表达式（以字符串形式给出）。当runeval()返回时，它返回表达式的值。否则这个函数类似于run()


`pdb.runcall(function[,argument,...])`: 调用传入的函数(或者对象的方法, 不是string类型)以及相关的参数. 当runcall()返回时，它返回所返回的任何函数调用。一旦输入该函数，就会显示调试器提示。

`pdb.set_trace()`: 在调用堆栈框架处输入调试器. 这对于在程序中的给定点硬编码断点是有用的，即使代码没有被调试（例如当断言失败时）。

`pdb.post_mortem([traceback])`:  输入给定traceback 对象的事后调试。如果没有给予traceback, 它使用当前正在处理的异常（如果使用缺省值，则必须处理异常）.

`pdb.pm()`: 输入`sys.last_traceback`中发现的traceback的事后调试。

run* 函数和set_trace()是用于实例化Pdb类和调用同名方法的别名。

`class pdb.Pdb(completekey='tab', stdin=None, stdout=None, skip=None)`

### pdb命令
调试器能够识别以下命令。大多数命令可以简化为一个或两个字母 ；例如h(elp)意味着可以用h或help，来输入帮助命令 （但不是he或hel，也不是H或HELP ）。命令的参数必须用空白 （空格或制表符） 隔开。可选参数括在方括号 ([]) 中的命令的语法 ；不，必须键入方括号。在该命令的语法的替代品被隔开的垂直栏 (|)。

输入一个空行重复输入的最后一个命令。例外： 如果上次执行的命令是列表命令，列出下一步 11 行。

调试器不能识别的命令被假定为 Python 语句和正在调试的程序的上下文中执行。Python 语句也可以有一个带惊叹号 (!) 作为前缀。这是强大的方式来检查程序正在调试 ；它是甚至可以改变一个变量或调用一个函数。当在此类声明中出现异常时，异常名称打印，但调试器的状态不会更改。

可能在单个行上，以分隔输入多个命令`;;`。（单个;不是使用原样传递到 Python 语法分析器的行中的多个命令分隔符。没有智能应用于分离命令 ；输入拆分第一； ；配对，即使它是在带引号的字符串。

调试器支持别名。别名可以有参数，它允许一个一定水平的背景下考试的适应性。

如果.pdbrc文件存在于用户的主目录或当前目录中，它是在读，因为如果它已被类型在调试器提示符下执行。这是特别有用的别名。如果这两个文件存在，主目录中的一个先读，那里定义别名可以通过本地文件重写。

`h(elp) [command]`: 无参数时，打印可用命令的列表。 使用command作为参数，打印有关该命令的帮助. help pdb显示完整的文档文件.如果定义了环境变量PAGER，则通过该命令管道化文件.由于command参数必须是标识符，因此必须输入help exec以获取帮助！命令。

`w(here)`: 打印堆栈跟踪，最新的帧在底部。箭头表示当前帧，它确定大多数命令的上下文。

`d(own)`: 将当前帧在堆栈跟踪中向下移动一级（到较新的帧）。

`u(p)`: 将当前帧在堆栈跟踪中向上移动一级（到较旧的帧）。

`b(reak) [[filename:]lineno | function[, condition]]`: 使用lineno参数，在当前文件中设置断点。使用function参数，在该函数中的第一个可执行语句中设置断点。行号可以用文件名和冒号作为前缀，以在另一个文件（可能是尚未加载的文件）中指定断点。 在sys.path上搜索文件.  请注意，每个断点都分配有一个数字，所有其他断点命令都引用该数字。
如果存在第二个参数，它是一个表达式，在断点被执行之前必须求值为true。
无参数，列出所有中断，包括每个断点，断点被命中的次数，当前忽略计数和相关条件（如果有）。

`tbreak [[filename:]lineno | function[, condition]]`:临时断点，当它第一次被击中时被自动删除。参数与break相同。

`cl(ear) [filename:lineno | bpnumber ...]]`:使用文件名：lineno参数，清除此行的所有断点。用断点号的空格分隔列表，清除那些断点。没有参数时，清除所有断点（但首先要求确认）。

`disable [bpnumber [bpnumber ... ]]`:禁用以空格分隔的断点号列表形式给出的断点。禁用断点意​​味着它不能导致程序停止执行，但是与清除断点不同，它保留在断点列表中，并且可以（重新）启用。

`enable [bpnumber [bpnumber ... ]]`: 启用指定的断点。

`ignore bpnumber [count]`: 设置给定断点号的忽略计数。如果省略count，则忽略计数设置为0。当忽略计数为零时，断点变为活动状态。当非零时，每次达到断点时计数递减，并且不禁用断点，并且任何关联条件的计算结果为true。

`condition bpnumber [condition]`: 条件是在断点被执行之前必须求值为true的表达式。如果条件不存在，则删除任何现有条件;即断点是无条件的。
> 当满足什么条件时, 执行断点


`commands [bpnumber]`: 指定断点编号bpnumber的命令列表。命令本身显示在以下行。键入包含“end”的行以终止命令。一个例子：
```
(Pdb) commands 1
(com) print some_variable
(com) end
(Pdb)
```
设置断点号处执行指定命令.使用该命令后进入cmd模式,然后可以输入相关要执行的命令, 输入end结束. 直接输入end会取消相应号的命令. 2.5版新加
> 在断点处触发的动作


`s(tep)`: 执行当前行，在第一个可能的时间停止(要么在被调用的函数中，要么在当前函数中的下一行) 单步运行, 但会进入到调用函数的内部.

`n(ext)`: 继续执行直到到达当前函数中的下一行或返回。next和step之间的区别是，step被调用的函数内的步进停止，而next以（几乎）全速运行被调用的函数，只在当前函数中的下一行停止。

`unt(il)`: 继续执行，直到行号大于当前行的行到达或从当前帧返回。

`r(eturn)`: 继续执行直到当前函数返回。

`c(ontinue)`: 继续执行，只有在遇到断点时停止。

`j(ump) lineno`: 设置将要执行的下一行。 仅在最下面的框架中可用。这允许您跳回并再次执行代码, 或跳转跳过您不想运行的代码。
应当注意，不是所有的跳转都是允许的 ---例如，不可能跳到for循环的中间或者跳出finally子句。

`l(ist) [first[, last]]`: 列出当前文件的源代码.如果没有参数，请列出当前行周围的11行或继续上一个列表. 使用一个参数，在该行列出11行。 有两个参数，列出给定的范围;如果第二个参数小于第一个，它将被解释为计数。

`a(rgs)`: 打印当前函数的参数列表。

`p expression`: 评估当前上下文中的表达式并打印其值。

`pp expression`: 像p命令一样，除了表达式的值是使用pprint模块打印的。

`alias [name [command]]`: 创建一个名为name的执行command的别名。

`unalias name`: 删除指定的别名。

`[!] statement`: 在当前堆栈帧的上下文中执行（一行）语句。可以省略感叹号，除非语句的第一个单词类似于调试器命令。设置全局变量,您可以在同一行上使用global命令为指定的命令添加前缀，例如：
```
(pdb) global list_options; list_options = ['-l']
```

运行时, 动态的改变值
```
[root@rcc-pok-idg-2255 ~]# python epdb2.py 
 > /root/epdb2.py(10)?() 
 -> b = "bbb"
 (Pdb) var = "1234"
 (Pdb) b = "avfe"
 *** The specified object '= "avfe"' is not a function 
 or was not found along sys.path. 
 (Pdb) !b="afdfd"
```

`run [args ...]`:重新启动debug 这个程序. 如果提供了一个参数，它将用“shlex”拆分，并将结果用作新的`sys.argv`。历史，断点，动作和调试器选项被保留。 “restart”是“run”的别名。

`q(uit)`: 退出调试,  执行中断
[http://gohom.win/2015/11/04/pyDebug/](http://gohom.win/2015/11/04/pyDebug/)
## ipdb
`pip install ipdb`
`set_trace()`

## pycharm



http://monklof.com/post/20/
https://www.ibm.com/developerworks/cn/linux/l-cn-pythondebugger/
