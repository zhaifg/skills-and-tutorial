# bash shell 入门
---

## bash 介绍
bash，Unix shell的一种，在1987年由布莱恩·福克斯为了GNU计划而编写。1989年发布第一个正式版本，原先是计划用在GNU操作系统上，但能运行于大多数类Unix系统的操作系统之上，包括Linux与Mac OS X v10.4都将它作为默认shell。它也被移植到Microsoft Windows上的Cygwin与MinGW，或是可以在MS-DOS上使用的DJGPP项目。在Novell NetWare与Android在上也有移植。1990年后，Chet Ramey成为了主要的维护者。
为Bourne shell的后继兼容版本与开放源代码版本，它的名称来自Bourne shell（sh）的一个双关语（Bourne again / born again）：Bourne-Again SHell。
Bash是一个命令处理器，通常运行于文本窗口中，并能执行用户直接输入的命令。Bash还能从文件中读取命令，这样的文件称为脚本。和其他Unix shell 一样，它支持文件名替换（通配符匹配）、管道、here文档、命令替换、变量，以及条件判断和循环遍历的结构控制语句。包括关键字、语法在内的基本特性全部是从sh借鉴过来的。其他特性，例如历史命令，是从csh和ksh借鉴而来。总的来说，Bash虽然是一个满足POSIX规范的shell，但有很多扩展。
一个名为Shellshock的安全漏洞在2014年9月初被发现，并迅速导致互联网上的一系列攻击。这个漏洞可追溯到1989年发布的1.03版本。

bash的命令语法是Bourne shell命令语法的超集。数量庞大的Bourne shell脚本大多不经修改即可以在bash中执行，只有那些引用了Bourne特殊变量或使用了Bourne的内置命令的脚本才需要修改。bash的命令语法很多来自Korn shell（ksh）和C shell（csh），例如命令行编辑，命令历史，目录栈，$RANDOM和$PPID变量，以及POSIX的命令置换语法：$(...)。作为一个交互式的shell，按下TAB键即可自动补全已部分输入的程序名，文件名，变量名等等。
使用'function'关键字时，Bash的函数声明与Bourne/Korn/POSIX脚本不兼容（Korn shell 有同样的问题）。不过Bash也接受Bourne/Korn/POSIX的函数声明语法。因为许多不同，Bash脚本很少能在Bourne或Korn解释器中运行，除非编写脚本时刻意保持兼容性。然而，随着Linux的普及，这种方式正变得越来越少。不过在POSIX模式下，Bash更加匹配POSIX。
bash的语法针对Bourne shell的不足做了很多扩展。其中的一些列举在这里。


1. 输入判断
2. 目录判断
3. 结果判断
4. 日志输出
5. 错误输出
6. shell的单元测试
