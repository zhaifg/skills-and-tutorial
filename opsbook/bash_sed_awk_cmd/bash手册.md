# bash 手册
---

是以命令为基础, 加上控制语句, 循环语句组成.

## 名词定义
1. POSIX
2. blank: 空格或者tab
3. builtin: 一个由shell本身内部实现的命令，而不是文件系统中某处的可执行程序。
4. 控制操作(control operator): 如 `||`, `&&`,`&`,`:`,`;;`,';&’, ‘;;&’, ‘|’, ‘|&’, ‘(’, or ‘)’
5. 退出的状态(exit status): 命令执行完退出的状态0-255
6. 字段field: 一个文本单元，是一个shell扩展的结果。
7.  filename
8. job
9. job control
10. 元字符(metacharactor): 一个字符，当没有引号时，分隔单词。
元字符是一个空格，制表符，换行符或下列字符之一: |’, ‘&’, ‘;’, ‘(’, ‘)’, ‘<’, or ‘>’
11. name: 变量: 一个单词只由字母，数字和下划线组成，并以字母或下划线开头。
12. operator
13. process group
14. process group ID
15. 保留字符
16. 返回状态
17. 信号signal
18. 特殊内置
19. token
20. word:


## 基础语法
### 变量
用于一个固定名称,来指代某些内容, 可以是命令执行结果, 一个文件名称等.
格式: varname=value
> 变量名与值之间的等于号两侧不能有任何空格.
```
passwd_file=/etc/passwd
```

在定义变量时, 变量的值, 可以不使用引号来包裹, 但是在遇到value之间有空格或者tab时, 需要使用引号包裹, 不然定义的变量的值, 不是你想要的.

#### 引用变量
在定义变量后, 在其他地方引用时, 使用的是:以$符号开始的, 后面跟定义的变量名,例如引号前面定义的passwd_file变量.
`$pass_file`

定义的变量时特殊符号

1. 特殊符号
 - 反斜杠`\`: 使用特殊字符时使用,反斜杠.
 - 单引号: 单引号引用的东西,在输出时就是什么东西. 不会有转义变量替换等发生.
 - 双引号:  引号用的东西, 里面东西内容可以被其他的规则所代替, 比如里面`$`,`\`,`\``,`!`
```
passwd_file=/etc/passwd
echo "sss"
echo "!!"
echo '!!'
```
2. ANSI-C

### shell 命令

#### 简单命令

#### 管道(|,|&)
管道是由一个或者多个命令通过|或者|&进行分割的命令列表.
格式:
    `[time [-p]] [!] command1 [ | or |& command2 ] …`
每一个命令的输出通过管道输出,作为下一个命令的输入. 也就是每一个命令的读取前一个命令的输出. 在前面的任何命令都会全部执行完毕后才会输出给后面的命令.

如果`command1` 使用`|&`, 表示命令的标准错误输出也会重定向到标准输出中输出. 既是`2>&1 |` 的简写形式.

每一个命令都会在一个子shell环境中执行,管道的退出状态是管道中最后一个命令的退出状态，除非启用了pipefail选项。如果pipefail开启的话, 表示在管道连接的命令序列中，只要有任何一个命令返回非0值，则整个管道返回非0值，即使最后一个命令返回0.

POSIX MODE 时
#### 命令列表
是由一个或者多个管道命令, 以及使用`:`,`&`,`&&`或者`||`, 并且是以`;`,`&`,或者换行作为结束.
`&&`,`||`的优先级大于`;`,`&`.

如果一个命令是以`&`为结尾, 这个命令会异步在子shell中执行. 既是在后台执行. 这个shell不会等待任何shell完成才执行, 并且返回的状态是0; 当作业控制没有开启时, 异步执行的命令输入, 模式 是从/dev/null重定向输入的.

命令之间使用`;`分割时, 每一个命令都会等待前面的命令执行完成后, 才会执行下一个.


### 字符串处理

### 判断语句

### 算数表达式

### 条件语句

#### if
```
if test-commands; then
  consequent-commands;
[elif more-test-commands; then
  more-consequents;]
[else alternate-consequents;]
fi
```
if语句的判断条件test-commands, 可以是一组命令, 或者一个命令列表. 只要判断条件返回值是0, 则执行. 如果判断条件不是0, 那么依次执行elif语句, 当执行完成某个分支下的 more-consequents后,这个if会执行完毕.
#### case
```
case word in [ [(] pattern [| pattern]…) command-list ;;]… esac

echo -n "Enter the name of an animal: "
read ANIMAL
echo -n "The $ANIMAL has "
case $ANIMAL in
  horse | dog | cat) echo -n "four";;
  man | kangaroo ) echo -n "two";;
  *) echo -n "an unknown number of";;
esac
echo " legs."

```

#### select
`select name [in words …]; do commands; done`

```
select fname in *;
do
  echo you picked $fname \($REPLY\)
  break;
done
```


#### [[ ]]
[[ expression ]]
1. [[]] 表达式返回0或者1, 状态值取决于expression执行的结果. 
2. expression由bash条件表达式的描述语句组成. 在[[]]中被分割的文字和文件名表达式不被执行. `~`,参数, 变量, 算数表达式, 命令替换,过程处理是被执行的.
3. 在[[]]中使用'>','<'时, 比较是按照字典顺序的
4. 当使用`==`或者`!=`, 在操作符的右侧是字符串时, 使用,模式匹配进行比较, 并根据下面的规则进行匹配, 就好像启用了exglob shell 选项.
  * `=` 与 `==` 是相同的.
  * 如果启用了nocasematch, 不会忽略字符的大小写, 如果`==`匹配或者`!=`不匹配时, 返回0(True), 否则返回1.
5. `=~`的优先级与`==`相同.使用它时，运算符右侧的字符串被视为扩展正则表达式，并相应地匹配（如在regex3中).
  * 匹配返回0, 不匹配返回1, 正则表达式错误时, 返回2.
  * nocasematch启用, 忽略大小写匹配.
  * 处理括号时, 要小心.正常正常引号字符在括号之间失去其含义。引号字符在括号之间失去其含义。
  * 正则表达式中由括号子表达式匹配的子字符串保存在数组变量BASH_REMATCH中.具有索引0的BASH_REMATCH的元素是匹配整个正则表达式的字符串部分。具有索引n的BASH_REMATCH的元素是匹配第n个括号子表达式的字符串的部分。

`=~`的实例:
匹配一个line 变量里, 是否是由空格字符的任何数字（包括零），零个或一个“a”实例组成的值中的字符序列，然后是“b”:
```
[[ $line =~ [[:sapce:]]*(a)?b ]]
# aab, aaaab 匹配
```
将正则表达式存储在shell变量中通常是一种有用的方法，可以避免引用对shell特殊的字符时出现的问题。有时很难在不使用引号的情况下指定正则表达式，或者在注意shell的引用删除时跟踪正则表达式使用的引用。使用变量方式制定表达式, 比较合适. 如下
```
pattern='[[:space:]]*(a)?b'
[[ $line =~ $pattern ]]
```



### 循环
#### for
`for name [ [in [words …] ] ; ] do commands; done`

`for (( expr1 ; expr2 ; expr3 )) ; do commands ; done`
```
for (( i=0; i<=10; i++))
do
   echo $i
done

0
1
2
3
4
5
6
7
8
9
10

```
#### while
`while test-commands; do consequent-commands; done`

```
i=0;while [[ $i -le 10 ]]; do echo $i; let i++; done
0
1
2
3
4
5
6
7
8
9
10

i=0;
while : 
do 
  echo $i; 
  let i++;
 done
```


#### util
`until test-commands; do consequent-commands; done`
```
[root@yimi_test ~]# i=0
[root@yimi_test ~]# until [[ $i -ge  10 ]] ; do echo $i;let i++;done
0
1
2
3
4
5
6
7
8
9

```

### 脚本的变量传入和处理

## 并发

ls | parallel mv {} destdir
find . -type f -name '*.html' -print | parallel gzip


## 函数
```
name () compound-command [ redirections ]
function name [()] compound-command [ redirections ]
```
1. 如果使用function关键字, 则函数名后括号可以省略. 但后面的主体必须使用`{}`包裹
2. 使用unset -f name 删除函数定义
3. 除非发生语法错误或具有相同名称的只读函数已存在，否则函数定义的退出状态为零。当执行时，函数的退出状态是在主体中执行的最后一个命令的退出状态。
4. 由于历史的原因, 使用`{}`时,要使用分隔符或者新建一行进行分割, 因为`{`是保留关键字. 
5. 给函数传入参数时, 使用的是位置参数方式.`$#` 参数的个数. `$0` 是函数名
6. 函数的局部变量
7. 通过daclare -f 定义一个函数
8. FUNCNEST 设置FUNCNEST, 限制递归层数

## 参数和特殊的参数
### 位置参数

### 特殊的参数
1. `$*`: "$1 $2 …"
2. `$@`: $1 $2 ...
3. `$#`: 个数
4. `$?`: 上一个命令的返回值
5. `$-`: 列出当前bash的运行参数, 比如set -v或者-i这样的参数
6. `$$`: 当前shell的id
7. `$!`: 最近一个被放到后台任务管理的进程PID
8. `$0`
9. `$_`: 算是所有特殊变量中最诡异的一个了，在bash脚本刚开始的时候，它可以取到脚本的完整文件名。当执行完某个命令之后，它可以取到，这个命令的最后一个参数。当在检查邮件的时候，这个变量帮你保存当前正在查看的邮件名。



### shell的扩展
- 1.大括号扩展(brace expansion):
  * bash$ echo a{d,c,b}e --> ade ace abe
  * 使用`{x..y[..incr]}`生成队列
    - x,y 可以为数字时, 打印x,y之间与incr间隔相应的数, x = x + incr,`{1..17..2}`
    - 可以使用0, 作为输出的数字的宽度的填充
    - x,y可以是字母, 以字典顺序输出
  * mkdir /usr/local/src/bash/{old,new,dist,bugs}
  * chown root /usr/{ucb/{ex,edit},lib/{ex?.?*,how_ex}}
```bash
shell> echo {1..17}
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17
shell> echo {01..17}
01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17
shell> echo {01..17..2}
01 03 05 07 09 11 13 15 17
shell> echo {a..z..2}
a c e g i k m o q s u w y
shell> echo {a..m..2}
a c e g i k m
shell> echo {a..m}
a b c d e f g h i j k l m
```
- 2.波浪号扩展
  * ~ 代表用户的home目录,$HOME
  * ~/foo: $HOME/foo
  * ~+/foo: 相当于$PWD/foo
  * ~-/foo: ${OLDPWD-'~-'}/foo
  * ~N: N为数字, 提取目录栈的第N条目录, 相当于`dirs +N`
  * ~+N: `dirs +N`
  * ~-N: `dirs -N`
```
[root@iZ23f1y0tquZ log]# dir
dir        dircolors  dirname    dirs       
[root@iZ23f1y0tquZ log]# dirs
/var/log
[root@iZ23f1y0tquZ log]# dirs +2
-bash: dirs: directory stack empty
[root@iZ23f1y0tquZ log]# pushd . 
/var/log /var/log
[root@iZ23f1y0tquZ log]# pushd /var
/var /var/log /var/log
[root@iZ23f1y0tquZ var]# dirs +2
/var/log
[root@iZ23f1y0tquZ var]# dirs +1
/var/log
[root@iZ23f1y0tquZ var]# dirs +3
-bash: dirs: 3: directory stack index out of range
[root@iZ23f1y0tquZ var]# dirs 
/var /var/log /var/log
[root@iZ23f1y0tquZ var]# dirs +0
/var
[root@iZ23f1y0tquZ var]# popd 
/var/log /var/log
[root@iZ23f1y0tquZ log]# popd 
/var/log
[root@iZ23f1y0tquZ log]# popd 
-bash: popd: directory stack empty
[root@iZ23f1y0tquZ log]# 
[root@iZ23f1y0tquZ log]# pushd /var
/var /var/log
[root@iZ23f1y0tquZ var]# pushd /root
~ /var /var/log
[root@iZ23f1y0tquZ ~]# echo ~+2 
/var/log
[root@iZ23f1y0tquZ ~]# dirs
~ /var /var/log
[root@iZ23f1y0tquZ ~]# echo ~-2 
/root
[root@iZ23f1y0tquZ ~]# echo ~-2 
/root
[root@iZ23f1y0tquZ ~]# echo ~-2 

```
- 3.shell参数扩展
  * 使用$进行参数扩展:` ${parameter}`
  * 如果参数的第一个字符是感叹号(!),并且参数不是nameref，则它引入一个级别的可变间接。
  * `${paramter:-word}`: 如果paramter变量没有赋值,或者赋值为空或者没有定义. 则返回为word. parameter的原值不变,仅仅在此生效.
  * `${paramter:=word}`: 如果paramter为unset或null，则将word的扩展分配给参数。然后替换参数的值。不能以这种方式分配位置参数和特殊参数。
  * `${paramter:?word}`: 如果parameter没有定义或者没有赋值, 则word信息输入标准错误.
  * `${parameter:+word}`: 如果paramter没有定义和或者为空值,不进行替换. 其他的情况则替换.
  * `${parameter:offset}` or `${parameter:offset:length}`, 字符串截取, 类似于Python
    * 子串截取.  从指定offset开始, 截取指定length
    * 如果parameter是@, 由"@"货"*"线表的索引数组或者关联数组的名称, 规则如下:
      * 如果length不指定, 从offset开始到结尾;length和offset都是算术表达式
    * bash版本为4.1时, 不支持length和offset为负数.**冒号与负数之间有一个空格**
    * 如果parameter是@, 则length不能为负数.
    * 如果parameter是数组并下标是"@"或者"*"时, length为负数会出错. 其他的会且截取的是下标范围.
  * `${!prefix*}` `${!prefix@}`: 取出以prefix的开始的变量
  * `${!name[@]}` `${!name[*]}`: ?
  * `${#parameter}`: paramter的长度,如果parameter是@或者* 时, 返回位置参数的个数
  * `${parameter#word}` or `${parameter##word}`:  从最左边开始删除匹配word部分`#`最小匹配,`##`是贪婪匹配. word可以类似目录的匹配模式, 不是全部的正则. parameter是@,*时, 一次匹配处理每一个位置参数. 如果是数组时, 一次匹配每一个元素
  * `${parameter%word}  ${parameter%%word}`: 右匹配删除,类似`#`
  * `${parameter/pattern/string}`: 匹配与替换. pattern符合文件的扩展规则
  * `${parameter^pattern} ${parameter^^pattern} ${parameter,pattern} ${parameter,,pattern}`:  匹配的部分大小写转换, ^ 小-> 大
  * `${parameter@operator}`:
    * `Q`
    * `E`
    * `P`
    * `A`
    * `a`



```
$ string=01234567890abcdefgh
$ echo ${string:7}
7890abcdefgh
$ echo ${string:7:0}

$ echo ${string:7:2}
78
$ echo ${string:7:-2}
7890abcdef
$ echo ${string: -7}
bcdefgh
$ echo ${string: -7:0}

$ echo ${string: -7:2}
bc
$ echo ${string: -7:-2}
bcdef
$ set -- 01234567890abcdefgh
$ echo ${1:7}
7890abcdefgh
$ echo ${1:7:0}

$ echo ${1:7:2}
78
$ echo ${1:7:-2}
7890abcdef
$ echo ${1: -7}
bcdefgh
$ echo ${1: -7:0}

$ echo ${1: -7:2}
bc
$ echo ${1: -7:-2}
bcdef
$ array[0]=01234567890abcdefgh
$ echo ${array[0]:7}
7890abcdefgh
$ echo ${array[0]:7:0}

$ echo ${array[0]:7:2}
78
$ echo ${array[0]:7:-2}
7890abcdef
$ echo ${array[0]: -7}
bcdefgh
$ echo ${array[0]: -7:0}

$ echo ${array[0]: -7:2}
bc
$ echo ${array[0]: -7:-2}
bcdef

$ set -- 1 2 3 4 5 6 7 8 9 0 a b c d e f g h
$ echo ${@:7}
7 8 9 0 a b c d e f g h
$ echo ${@:7:0}

$ echo ${@:7:2}
7 8
$ echo ${@:7:-2}
bash: -2: substring expression < 0
$ echo ${@: -7:2}
b c
$ echo ${@:0}
./bash 1 2 3 4 5 6 7 8 9 0 a b c d e f g h
$ echo ${@:0:2}
./bash 1
$ echo ${@: -7:0}

$ array=(0 1 2 3 4 5 6 7 8 9 0 a b c d e f g h)
$ echo ${array[@]:7}
7 8 9 0 a b c d e f g h
$ echo ${array[@]:7:2}
7 8
$ echo ${array[@]: -7:2}
b c
$ echo ${array[@]: -7:-2}
bash: -2: substring expression < 0
$ echo ${array[@]:0}
0 1 2 3 4 5 6 7 8 9 0 a b c d e f g h
$ echo ${array[@]:0:2}
0 1
$ echo ${array[@]: -7:0}

vim a.sh
echo ${#@}
echo ${#*}
echo ${@#123}

bash a.sh 123233 123ddd 111 123

```
  
- 4.命令替换
`$(command)`
`\`command\``

- 5.算数扩展
`$((expression))`

- 6.过程替换
`<(list)` or `>(list)`
这两个符号可以将list的执行结果当成别的命令相应的输入和输出的文件操作, 比如我想比较两个命令执行结果的区别:
```
diff  <(df -h) <(df)
```

- 7.分词
是通过`$IFS`进行分词的, 空格, tab,新建一行

- 8.文件名扩展
使用`*`, `?`, `[`
了一些扩展功能的匹配，需要先使用内建命令shopt打开功能开关。支持的功能有

- 9.模式匹配
  * ` shopt -u extglob`
  * `*`
  * `?`
  * `[...]`
  * `?(pattern-list)`: 匹配所给的pattern的0次或者1次
  * `*(pattern-list)`: 匹配所给的pattern的0次以上包括0次
  * `+(pattern-list)`: 匹配所给的pattern的1次以上包括1次
  * `@(pattern-list)`: 匹配所给的pattern的1次
  * `!(pattern-list)`: 匹配非括号内所给pattern
  * 
- 10.quote removal
`\`, `,`, `"`

###　bash的执行的环境变量
1. 继承父shell的环境变量.
2. 在当前执行的目录里cd, pushd popd
3. 创建时的umask或者继承父shell的
The shell has an execution environment, which consists of the following:

- open files inherited by the shell at invocation, as modified by redirections supplied to the exec builtin

- the current working directory as set by cd, pushd, or popd, or inherited by the shell at invocation
- the file creation mode mask as set by umask or inherited from the shell’s parent
- current traps set by trap
- shell parameters that are set by variable assignment or with set or inherited from the shell’s parent in the environment
- shell functions defined during execution or inherited from the shell’s parent in the environment
- options enabled at invocation (either by default or with command-line arguments) or by set
options enabled by shopt (see The Shopt Builtin)
- shell aliases defined with alias (see Aliases)
- various process IDs, including those of background jobs (see Lists), the value of $$, and the value of $PPID

### 重定向
在执行命令之前, shell支持使用特殊符号进行输出输入重定向. 重定向允许命令的文件句柄被复制,打开, 关闭, 以及引用不同的文件, 且可以更改命令读取和写入的文件; 重定向可以在当前的shell环境中更新当前的文件句柄.重定向按照它们从左到右的顺序进行处理.

在文件描述符之前每一个重定向, 在它之前可以有一个行为{varname}的单词. 在这种情况下对于每一个重定向操作符,除了`>&-`和`<&-`, shell将会分配一个大于的10 的文件描述符, 并分配给{varname}. 如果{varname}前面是`>&-`和`<&-`, varname的值定义要关闭的文件描述符。

如果文件操作符的数字省略, 则是默认. `<  输入默认为 0`, `>  输出默认为 1`.

**重定向的顺序非常重要**:
`ls > dirlist 2>&1`: 当命令执行时, 标准输出和标准错误都会重定向输出到dirlist中.
`ls 2>&1 > dirlist`: 仅将标准输出定向到文件dirlist，因为标准错误是在标准输出重定向到dirlist之前的标准输出的副本。

**特殊的重定向符**
`/dev/fd/fd`: fd是有效数字时, 文件描述符会被复制
`/dev/stdin`:
`/dev/stdout`:
`/dev/stderr`:
`/dev/tcp/host/port` : 如果host是一个有效主机名,或互联网地址, port是有效端口或者服务名称,bash会尝试打开这个TCP socket
`/dev/udp/host/port`:

> 应该小心使用大于9的文件描述符重定向，因为它们可能与shell在内部使用的文件描述符冲突。

**输入重定向**:
`[n] < word` : 输入重定向会在n的文件描述上打开文件word的文件(可以是文件扩展)读取内容, 如果n省略时, n=0.


**输出重定向**:
输出重定可以从文件描述符为n上向名为word(可文件扩展)上输出内容, 如果n省略,n=1;
如果文件不存在则创建, 如果存在先清零,再输出.
`[n][|]>word`: 
如果重定向操作符是">",且`noclobber`被启用, 当word存在且word是一个正则形式时, 输出会失败. 如果操作符是`>|`,或者操作符是">"且noclobber是禁用的, 输出重定向会尝试输出到文件, 即使已经存在.

**追加输出**:
`[n]>>word`

**重定向标准输出和标准错误**:
`&>word`
`>&word`
以上两种形式首选第一个, 等用于`>word 2>&1`
使用第二个表单时，字词不能展开为数字或“ - ”。如果是，为了兼容性原因，其他重定向操作符适用。

```
&>>word
This is semantically equivalent to
>>word 2>&1
```


#### Here Document
这种类型重定向会从当前的源读取内容直到仅仅看到包含word的部分(尾部不能有空格)行结束.所有读到的行然后被用作命令的标准输入(或者如果指定了n，则为文件描述符n).

```
[n]<<[-]word
        here-document
delimiter
```
1. 在word不会执行参数,变量扩展,命令替换,算数运算,文件扩展.
2. 如果word是被引号引用, `delimiter`是word删除引号的部分, 这时here-document上所有扩展都会失效.
3. 如果没有
4. 如果操作符是`<<-`,所有的前面的`\t`包括word中,都会被删除
```
a="AGF"
cat<<"ww"pp
sdfsf
sdfsdf
${a}
'$'
sdfa
wwpp


# b.sh

a="AGF"
cat<<-  "ww"pp
sdfsf
        sdfsdf
${a}
'$
sdfsf'  dd
dd\tsss
\tsdfa
wwpp


nosomker@nosomker:~$ bash redirct.sh 
sdfsf
sdfsdf
${a}
'$
sdfsf'  dd
dd\tsss
\tsdfa


#---
[root@zorrozou-pc0 prime]# cat fdisk.sh 
#!/bin/bash

fdisk /dev/sdb << EOF
n
p


w
EOF
```

**Here Strings**
`[n]<<< word`

**复制文件描述符**
`[n]<&word`: 用于复制输入文件描述符. 如果字扩展到一个或多个数字，则用n表示的文件描述符是该文件描述符的副本. 如果word没有指定文件操作符的输入, 会报错. 如果word有`-`n则表示关闭这个文件操作符.

`[n]>&word`: 如果未指定n，则使用标准输出（文件描述符1）。如果word中的数字未指定打开的文件描述符输出，则会发生重定向错误。如果字评估为“ - ”，则文件描述符n被关闭。作为特殊情况，如果省略n，并且字未扩展为一个或多个数字或“ - ”，则标准输出和标准错误将如前所述重定向。
如果n没有指定数字，则默认复制0号文件描述符。word一般写一个已经打开的并且用来作为输入的描述符数字，表示将制订的n号描述符在制定的描述符上复制一个。如果word写的是“-”符号，则表示关闭这个文件描述符。如果word指定的不是一个用来输入的文件描述符，则会报错。

**移动文件描述符**:
`[n]<&digit-`: 移动文件描述符digit 到n, 或者到标准输入,n省略的话, digit在复制n后关闭.

`[n]>&digit-`:

这两个符号的意思都是将原来的描述符编号上打开,并且关闭原有描述符.

**打开读写文件描述符**
`[n]<>word`

```bash

# example 1
# 打开3号fd用来输入, 并关联文件/etc/passwd
exec 3 < /etc/passwd
# 让3号描述符成为标准输入
exec 0<&3
#此时cat的输入将是/etc/passwd, 会在屏幕上显示出/etc/passwd的内容
cat
#关闭3号描述符
exec 3>&-

# example 2
# 打开3号和4号描述符作为输出, 并且分别关联文件
exec 3 > /tmp/stdout
exec 4 > /tmp/stderr

# 将标准输入关联到3号描述符, 并关闭原来的1号的fd
exec 1>&3-
# 将标准错误关联到4号描述符, 并关闭原来的2号的fd
exec 2>&4-
# 这个find命令的所有正常输出都会写到/tmp/stdout文件中, 错误输出都会输出到/tmp/stderr文件中.
find /etc/ -name "passwd"

#关闭两个描述符.
exec 3>&-
exec 4>&-
```


### bash命令的搜索路径和执行
1. 如果命令里没有"/"搜索它, 当存在此名称的函数时,执行他.
2. 如果没有此名称的函数,则在内建命令里搜索,搜索到执行.
3. 如果既没有函数的定义,也不是内建名利, 则使用$PATH的路径搜索这个命令;(Bash有一个$PATH下所有可执行命令的 hash table.)

### 环境变量
当程序调用时, 会被给余一个string数组, 这个数组有name=value组成.

bash提供几种途径维护环境变量. 
在调用时，shell扫描其自己的环境并为找到的每个名称创建一个参数，自动将其标记以导出到子进程。已执行的命令继承环境。`export`和`declare -x`命令允许向环境中添加
和删除参数和函数。如果环境变量中参数中的一个值更新时, 新的值会替代原来的旧的值.


### 退出状态:
成功是为0.
0-255, shell一般使用>128的
If a command is not found, the child process created to execute it returns a status of 127. If a command is found but is not executable, the return status is 126.

### 信号

### shell 脚本
```
script_file.sh # subshell执行
bash  script_file.sh # 本shell 执行
```

## shell内建命令
1. `:` `: [arguments]` 除了扩展参数和执行重定向之外什么都不做. 返回状态为零.
2. `.`  `. filename [arguments]`, 读取并执行来自文件里的命令在当前的shell中. 如果filename不包含斜杠, 则从PATH的路径中搜索. 如果bash不是在POSIX模式,如果不在PATH里则搜索当前目录. 如果-T启用, 
3. `break`: 
4. `cd` `cd [-L|[-P [-e]] [-@]] [directory]`: `CDPATH`, 
  * `-P`: 如果进入的对象是一个软连接,那么指定-P时, 进入的实际的目录,而不是连接
5. `contiune`
6. `eval`: `eval [arguments]` 从参数中读取,并执行为单条命令, 返回的是执行的命令的返回值
7. `exec`: `ext [-cl] [-a name] [command [arguments]]`: 在comannd会代替当前的shell执行, 不会创建新的进程.
  * `-l` 在第0个参数上前边传上一个破折号. `login`就是这个执行的
  * `-c` 在空环境变量中执行.
  * `-a` 把name当做命令的第0个参数传入给command
  * 如果command不能执行, 在非交互模式下只有execfail开启, command不能执行才能退出, 返回失败状态.
  * 在交互模式下,如果文件不能执行则返回失败状态.
  * 不提供命令时, 可以使用重定向影响当前的shell环境.如果没有重定向错误, 则返回0
8. `exit`: `exit [n]` 
9. `export`: `export [-fn] [-p] [name[=value]`, 将每一个name=value定义到子进程的环境变量里
  * `-f` 定义的name是一个函数名称
  * `-n` 不再在环境变量中定义name
  * 如果names没有提供, 或者指定了-p, 会显示所有定义的变量
  * -p 显示定义的变量
10. `getopts`: `getopts optstring name [args]` , 类似python的包,通常是处理shell 脚本的位置参数.
  * optstring包含要选项字符, 用于被赋值的变量;
  * 如果字符后面有冒号, 该选项有一个参数. 字符参数与参数值应该用空格分开.
  * 冒号和问号不能用作可选字符.
  * 每次调用它时, getopts会将下一个选项放在变量名称中.如果变量值不存在,则初始化名称,并将要处理的下一个参数的索引放在变量`OPTIND`中.
  * 每次调用shell或shell脚本时，OPTIND都初始化为1。
  * 当选项需要参数时，getopts将该参数放入变量OPTARG.
  * getopts的错误显示有两种方式:
    * optstring的第一个字符是冒号时, 会不显示错误.
    * 正常情况下,当错误的参数或者漏掉操作参数时, 会打印诊断信息.
    * 如果OPTER 的值设置了为0, 不会有错误信息输出
11. `hash`, `hash [-r] [-p filename] [-dt] [name]`
12. `pwd`,`pwd [-LP]` 打印当前工作的绝对路径, `-P`打印实际路径, 如果是软连接的话
13. `readonly`: `readonly [-aAf] [-p] [name[=value]]` 设置为只读变量.
  * `-f`, 指定的是函数
  * `-a`, 指定是数组
  * `-A`, 联想数组
  * `-p`, 显示定义的只读变量
14. `return`, `return [n]`
15. `shift`, `shift [n]`
16. `test` or `[]` `test expr`, 评估条件表达式expr的值, 返回状态0或1, 每一个操作符和操作数都必须分割.
  * !expr
  * (expr)
  * expr1 -a expr2
  * expr1 -o expr2
17. times
18. `trap`, `trap [-lp] [arg] [sigspec ...]`,   当接收到`sigspec`信号后执行arg命令; 如果不指定arg, 只有sigspec时, 或者为`trap - sigspec` 时,会重置信号. 
  * arg等于空字符串, 忽略信号.
  * 如果arg不存在并且提供了-p，则shell将显示与每个sigspec相关联的trap命令。
  * 如果没有提供参数，或者仅给出-p，则trap将以可重复用作shell输入的形式打印与每个信号编号相关联的命令列表。
  * `-l`
  * 信号要么是名称,要么是数字, 前缀SIG可以省略
  * 当信号是0或者EXIT, arg在脚本退出时执行.
  * 当信号是`DEBUG`, 会在脚本第一个执行.
  * 如果sigspec是ERR，只要管道（可能由单个简单命令组成），列表或复合命令返回非零退出状态，命令arg就会满足以下条件, 不会执行.
    * 紧跟在util或者while之后的命令列表的一部分
    * 紧跟在if或者elif后面的
    * &&, || 的一部分的
    * 管道的最后一部分
19. `umask`, `umask [-p] [-S] [mode]`
20. `unset`, `unset [-fnv] [name]` 取消定义的变量,函数等
  * `-v` 取消变量
  * `-a` 取消函数
  * `-n` 取消变量, 以及变量所指向的变量
21. `alias`, `alias [-p] [name[=value] …]` `-p` 显示alias的定义的变量
22. `bind`,
  * 格式: 用来绑定键盘
    * `bind [-m keymap] [-lpsvPSVX]`
    * `bind [-m keymap] [-q function] [-u function] [-r keyseq]`
    * `bind [-m keymap] -f filename`
    * `bind [-m keymap] -x keyseq:shell-command`
    * `bind [-m keymap] keyseq:function-name`
    * `bind [-m keymap] keyseq:redline-command`
  * bind命令用于显示当前“readline”中键和function的绑定，绑定键序列与function或宏，设置“readline”变量。每个非选项参数都是一个命令，好像来自特殊文件“.inputrc”一样。所有的绑定和命令都必须作为一个单独的参数，例如’”\C-x\C-r”: re-read-init-file’
  * `-m keymap` 用参数keymap作为后续绑定的键映射, 参数可以设置`emacs`, `emacs-standard`, `emacs-meta`, `emacs-ctlx`、`vi`、`vi-move`、`vi-command`、`vi-insert`，其中`vi`和`vi-command`相同，emacs和emacs-standard相同。 
  * `-l` 列出所有的readline的function名称
  * `-p` 以可以作为重新输入的格式显示`readline`的function名称和绑定
  * `-P` 列出单签readline的function名称和绑定
  * `-s` 以作为重新输入的格式显示readliine绑定到宏的键序列和输出的字符串
  * `-S` 显示readline绑定到宏的键序列和输出的字符串
  * `-v` 亦可以作为重新输入的格式显示readline变量和值
  * `-V` 显示当前的readline变量名和值
  * `-f filename` 从文件filename中读取键绑定
  * `-q function` 查询与function绑定的键
  * `-u function` 解除所有与function绑定的键
  * `-r keyseq` 删除当前所有的与键序列keyseq的绑定
  * `-x keyseq:shell-command` 每次获取键keyseq都执行shell命令shell-command. 执行命令时, 变量READLINE_LINE保存readline缓冲的内容, 变量READLINE_POINT保存当前插入点的位置,如果这两个变量被修改, 新的变量值在编辑状态中出现.
  * `-X` 以作为重新输入的格式显示所有的绑定到shell命令的键序列
23. `builtin`: `builtin [shell-buitin [args]]` 运行一个shell builtin命令,并传递给他参数 args,builtin命令用以执行shell的内建命令，既然是内建命令，为什么还要以这种方式执行呢？因为shell命令执行时首先从函数开始，如果自定义了一个与内建命令同名的函数，那么就执行这个函数而非真正的内建命令。
24. `caller`, `caller [expr]`返回任何活动子例程调用（shell函数或使用。或source内置函数执行的脚本）的上下文。caller命令返回当前活动的子程序调用的上下文，即调用堆栈信息，包括shell函数和内建命令source执行的脚本。没有指定expr时，显示当前子程序调用的行号和源文件名。如果expr是一个非负整数，显示当前子程序调用的行号、子程序名和源文件名。caller命令打印出来的堆栈信息在调试程序时是很有帮助的，当前栈帧为0。如果shell没有子程序调用或者expr是一个无效的位置时，call命令返回false。
25. `command`command命令类似于builtin，也是为了避免调用同名的shell函数，命令包括shell内建命令和环境变量PATH中的命令。选项“-p”指定在默认的环境变量PATH中查找命令路径。选项“-v”和“-V”用于显示命令的描述，后者显示的信息更详细。
26. `declare`, `declare [-aAfFgilnrtux] [-p] [name[=value] …]`
  * 使用给定的属性定义变量, 如果没有names, 会显示values
  * `-p` 显示属性以及值,所有的.当-p与name参数一起使用时，将忽略除-f和-F之外的其他选项。
  * `-F` -F选项禁止显示函数定义;仅打印函数名称和属性。如果开启了extdebug,则显示源文件的内容
  * `-g`-g选项强制在全局作用域创建或修改变量，即使在shell函数中执行declare时也是如此。在所有其他情况下将被忽略。
  * `-a` 每一个name都是都是一个数组索引变量
  * `-A`, 每一个name都关联一个数组
  * `-f`, 定义一个函数
  * `-i`, 定义一个整数值
  * `-n`, 定义一个变量的引用.
  * `-r`, 只读变量
  * `-t`, 给每个name设置trace属性，对函数来说，可以继承调用shell的trap命令的DEBUG和RETURN属性，对变量则没什么意义。
  * `-u`, 变量值的所有小写转换成大写
  * `-x`, 将每一个name输出到环境变量
  * 对于上面的选项，可以使用加号“+”代替减号“-”，效果是关闭对应的属性，但是，“+a”和“+r”无效。
27. `echo`,`echo [-neE] [arg …]` 
  * 用于输出参数arg, 参数之间 用空格分隔, 即为是换行符. 
  * 选项`-n`,禁止输出结尾的换行符. 对于一些反斜杠"\"转移到特殊字符, echo默认不转义.
  * `-e`, 启用为可以转义的输出
  * `-E`, 禁止转义
  * 
28. `enable`, `enable [-a] [-dnps] [-f filename] [name ...]`enable命令用于启用或禁用shell内建命令
  * 在执行shell命令时，先查找是否属于内建命令，然后才在环境变量PATH中查找，如果使用enable禁用了这个命令，那么PATH中的同名命令就会执行。
  * `-n`, 用于禁用命令，不使用时则启用命令。
  * `-f`, 在支持动态加载的系统上，选项“-f”设置从动态库filename中加载新的内建命令
  * `-d`,则用来删除加载的这些命令
  * 如果不指定命令name或者只是使用了选项“-p”时，则输出当前启用的内建命令。
  * 选项`-a`显示所有的内建命令，包括启用的和禁止的命令。选项“-s”仅输出POSIX内建命令。
29. `help`,`help [-dms] [pattern]`显示builtin命令的帮助信息, 如果指定pattern,会显示匹配的部分.
  * `-d`, 显示简短的说明
  * `-m`, 显示每一部分, 类似于man page
  * `-s`, 简短显示匹配的`synopsis `不服
30. `let`, `let arg [arg ...]` `let expression [expression …]`用于数学表达式
31. `local`, `local [option] [name[=value] ...]`.local命令只能用于shell函数，声明变量name为局部变量，只对当前函数或其子进程有效，选项option可以是内建命令declare可以接受的选项。
32. `logout`,`logout [n]`在shell中，内建（builtin）命令logout用于退出登录shell。在Linux中，shell分为登录login和非登录nonlogin两种，登录shell如常用的”/bin/bash“，非登录shell如”/usr/sbin/nologin“，登录shell是用户可以登录使用的，登录以后可以与计算机交互，非登录shell则没有这个功能，但有其特殊用途，Linux上各用户的shell默认登录状态可查看文件”/etc/passwd“
33. `mapfile`, `mapfile [-n count] [-O origin] [-s count] [-t] [-u fd] [-C callback] [-c quantum] [array]` 类似于readarray
34. `printf`, `printf [-v var] format [arguments]`,  printf命令用于把格式化的参数arguments打印到标准输出, 格式由参数format控制. 如果指定了选项 `-v var`, 结果保存到变量var中, 而非打印到标准输出.
  * format 有三种格式, 1,原始字符串, 直接打印到标准输出.2, 转义字符序列, 先转义后打印到标准输出.3,控制字符串, 与后面的参数arguments对应.
  * `man 3 strftime`
35. `read`, `read [-ers] [-a aname] [-d delim] [-i text] [-n nchars] [-N nchars] [-p prompt] [-t timeout] [-u fd] [name ...]`
  * read用于从标注输入或者选项`-u`指定的文件描述符中读取一行文本, 把第一个单词复制给第一个名称.第二个单词复制给第二个名称name, 一次类推, 剩余的单词连同分隔符一起复制给最后一个名称aname, 则把结果复制给系统变量REPLAY
  * `-a aname`, 把各个单词一次赋值给数组name中从0开始的连续下标, 赋值之前name被unset, 使用了这个选项就会忽略其他的名称name
  * `-d delim`: 用分隔符delim的第一个字符来结束输入行, 而不是换行符.
  * `-e`, 如果标准输入赖在shell终端,使用`readline`来读取输入行
  * `-i text`, 如果使用`readline`来读取输入行,文本text在编辑前被放入到编辑缓冲中.
  * `-n nchars`, 最多赌球nchars字符
  * `-N nchars`, 最多读取nchars字符, 转义字符不进行转义
  * `-p prompt`, 如果在shell终端读取输入, 首先打印提示prompt, 提示不换行
  * `-r`, 反斜线这个转义字符不做特殊处理,当做普通字符
  * `-s`, 安静模式, 输入来自shell终端shi,不进行回显echo
  * `-t timeout`, 如果在超时时间timeout指定的秒数内, 还没有读入完整的一行,则读取超时并返回false. tineout可以是个带有小数的十进制数.这个选项只有在read命令从终端,管道,或者其他特殊文件读取输入时才有效, 从普通文件读取输入时,没有作用. 如果timeout为0, 则指定的文件描述符可用时返回true, 不可用时返回FALSE.  超时,返回状态大于128
  * `-u fd`, 从文件描述符fd读取输入
36. `readarray`, `readarray [-n count] [-O origin] [-s count] [-t] [-u fd] [-C callback] [-c quantum] [array]`
  * readyarray用于从标注输入或者-u指定的文件描述符fd中读取文本行, 然后赋值给索引数组array, 如果不指定数组array, 则使用默认的数组名MAPFILE
  * `-n count`, 复制最多count行, 如果count为0, 则复制所有的行
  * `-O, origin`, 从下表位置origin开始对数组赋值, 默认为0
  * `-s count`, 忽略开始读取的count行
  * `-t`, 删除文本航结尾的换行符
  * `-u fd`, 从文件描述符fd读取文本行
  * `-C callback`, 每当读取选项`-c`指定的quantum行时(默认为5000行), 就执行一次回调callback
37. `source`, `source filename`
38. `type`, `type [-aftpP] name [name ...]`, 用于查找shell命令name的类型.
  * `-t`, 用于显示name的类型,包括alias,shell保留字keyword, 函数function, 内建builtin和磁盘文件file.
  * 对于磁盘文件file来书, 选项`-p`可现实命令name指定的磁盘文件名.
  * `-P`强制在环境变量PATH中搜索命令name.
  * 如果多个地方都包括命令name, 使用选项`-a`可以把他们全部打印出来, 否则只显示第一个.
  * `-f`的作用是试图不在函数和内建命令查找name
39. `typeset`, `typeset [-afFgrxilnrtux] [-p] [name[=value] …]`,ksh中的, 类似于dalcare
40. `ulimit`, `ulimit [-HSTabcdefilmnpqrstuvx [limit]]`
  * 如果系统支持,ulimit命令能够控制shell中有效资源
  * `-H`, `-S`分别指硬限制,软限制, 硬限制设置后后不能由非root来增加值, 软限制则可能增加到硬限制的值, 这两个选项都不指定时会同时设置他们的值. limit可以是数字, 也可以是三个特殊的字符串,hard,soft,unlimilted, 不设置limit显示当前软限制的值, 此时除非设置了`-H`才显示硬限制
  * `-a` 显示当前所有的限制
  * `-b` 套接socket缓冲的最大长度
  * `-c` 科创家的core文件的最大数
  * `-d`, 一个进程的数据段的最大长度
  * `-e`, 调度优先级即nice的最大值
  * `-f`, shell以及子进程写文件时的最大长度
  * `-i`, 等待的信号的最大个数
  * `-l`, 所在内存中的最大长度
  * `-m`, 常住内存的最大值(许多系不支持这个值)
  * `-n`, 打开文件描述符的最大个数(许多系统机制设置这个值)
  * `-p`, block块 代销为512字节的管道长度
  * `-q`, POSIX消息队列的最大字节数
  * `-r`, 实时调度的最大优先级
  * `-s`, 堆栈stack的最大长度
  * `-t`, 累积CPU时间(秒)的最大值
  * `-u`, 单个用户可以拥有进程的最大数
  * `-v`, shell可用的虚拟内存的最大值
  * `-x`, 文件锁的最大个数
  * `-T`, 最大线程数
  - ulimit命令中, 如果设置了参数limit, 且没有使用选项`-a`, 指定的资源便会设置为这个新的limit值. 如果不使用任何选项的话, 默认使用`-f`.选项“-t”增值的单位为秒，“-p”增值的单位为块block即512字节，“-T”、“-b”、“-N”、“-u”则没有这种特殊的增长幅度，剩余其它选项的增值单位为1024各字节。
41. `unalias`, `unalias [-a] [name … ]`

#### 实例
getopts
```
#!/bin/bash

while  getopts "a:bc" arg
do
    case $arg in
       a)  
        echo "a's arg:OPTARG"
        ;;  
       b)  
        echo "b"
        ;;  
       ?)  
        echo "unknow argument"
        exit 1
        ;;  
     esac
done

[root@mail shell]# bash getopts_01.sh -a arg -b -c
a's arg:OPTARG
b
unknow argument


#--->

#!/bin/bash

usage() { echo "Usage: $0 [-s <45|90>] [-p <string>]" 1>&2; exit 1; }

while getopts ":s:p:" o; do
    case "${o}" in
        s)
            s=${OPTARG}
            ((s == 45 || s == 90)) || usage
            ;;
        p)
            p=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${s}" ] || [ -z "${p}" ]; then
    usage
fi

echo "s = ${s}"
echo "p = ${p}"

# Example runs:

$ ./myscript.sh
Usage: ./myscript.sh [-s <45|90>] [-p <string>]

$ ./myscript.sh -h
Usage: ./myscript.sh [-s <45|90>] [-p <string>]

$ ./myscript.sh -s "" -p ""
Usage: ./myscript.sh [-s <45|90>] [-p <string>]

$ ./myscript.sh -s 10 -p foo
Usage: ./myscript.sh [-s <45|90>] [-p <string>]

$ ./myscript.sh -s 45 -p foo
s = 45
p = foo

$ ./myscript.sh -s 90 -p bar
s = 90
p = bar
```

```shell
# getopts

# trap
# trap 'command_list'  signals
# 1.
#!/bin/bash
trap "echo 'Ctrl + C interrupt this scrpit now, exit';exit" SIGINT SIGQUIT
count=0
while :
do
   sleep 1
   let count++
   echo $count
done
#---
[root@mail ~]# bash trap_01.sh 
1
2
^CCtrl + C interrupt this scrpit now, exit

# 2
# trap1a
trap 'my_exit; exit' SIGINT SIGQUIT
count=0

my_exit()
{
echo "you hit Ctrl-C/Ctrl-\, now exiting.."
 # cleanp commands here if any
}

while :
 do
   sleep 1
   count=$(expr $count + 1)
   echo $count
 done
-->
[root@mail ~]# bash trap_02.sh  # 另一个终端kill -1 pid
1
2
3
4
^C5
^Cyou hit Ctrl-C/Ctrl-\, now exiting..
# 使用ERR在运行cmd错误时实现set -e的功能

# 向子进程发送信号
#!/bin/bash
# trapchild

sleep 120 &

pid="$!"

sleep 120 &
pid="$pid $!"

echo "my process pid is: $$"
echo "my child pid list is: $pid"

trap 'echo I am going down, so killing off my processes..; kill $pid; exit' SIGHUP SIGINT 
 SIGQUIT SIGTERM 

wait
-->
# 完成脚本执行后，将显示下面的内容：
my process pid is: 6553626
my child pid list is: 5767380 6488072
# 现在，向父进程发送一个 SIGTERM。脚本将终止，同时还将终止子进程。 
# kill -15 pid
I am going down, so killing off my processes..
```

**bind**

```
bind -x '"u": uname'
# 绑定 u执行uanme命令
```

```
$ umask
0002
$ umask() { echo "umask function"; }
$ umask
umask function
$ builtin umask
0002
$ unset -f umask
$ umask
0002
```

```
$ enable -s
enable .
enable :
enable break
enable continue
enable eval
enable exec
enable exit
enable export
enable readonly
enable return
enable set
enable shift
enable source
enable times
enable trap
enable unset
```

```
$ read foo
hello world
$ echo $foo
hello world
$ read foo bar
hello world
$ echo $foo
hello
$ echo $bar
world
$ read
hello world
$ echo $REPLY
hello world
$ read -a foo
hello a b c
$ echo ${foo[@]}
hello a b c
$ echo ${#foo[@]}
4
$ echo ${foo[0]}
hello
$ echo ${foo[3]}
c
$ read -p "Please input a string:" foo
Please input a string:hello
$ echo $foo
hello$ read foo
hello world
$ echo $foo
hello world
$ read foo bar
hello world
$ echo $foo
hello
$ echo $bar
world
$ read
hello world
$ echo $REPLY
hello world
$ read -a foo
hello a b c
$ echo ${foo[@]}
hello a b c
$ echo ${#foo[@]}
4
$ echo ${foo[0]}
hello
$ echo ${foo[3]}
c
$ read -p "Please input a string:" foo
Please input a string:hello
$ echo $foo
hello
```

```
$ readarray foo
hello world
hello bash
^C
$ echo ${foo[@]}
hello world hello bash
$ echo ${#foo[@]}
2
hanjunjie@hanjunjie-HP:~$ echo ${foo[0]}
hello world
hanjunjie@hanjunjie-HP:~$ echo ${foo[1]}
hello bash
```


```
$ type type
type is a shell builtin
$ type -t type
builtin
$ type pwd
pwd is a shell builtin
$ type -t pwd
builtin
$ type -a pwd
pwd is a shell builtin
pwd is /bin/pwd
$ type -t top
file
$ type top
top is /usr/bin/top
$ foo() { echo "function foo"; }
$ type foo
foo is a function
foo () 
{ 
    echo "function foo"
}
$ type -t foo
function
```


```shell
# 打印16进制
$ printf "%x\n" 17
11
$ printf "%X\n" 17
11
$ printf "%#x\n" 17
0x11
$ printf "%#X\n" 17
0X11

# 输出字符串宽度和对齐方式
$ printf "%d\n" 123
123
$ printf "%6d\n" 123
   123
$ printf "%-6d\n" 123
123 

# 设置输出字符串宽度和填充方式：
$ printf "%d\n" 123
123
$ printf "%6d\n" 123
   123
$ printf "%06d\n" 123
000123
# 正数前面添加空格：
$ printf "%d\n" 123
123
$ printf "% d\n" 123
 123
$ printf "%d\n" -123
-123
$ printf "% d\n" -123
-123
# 在正数前面添加加号
$ printf "%d\n" 123
123
$ printf "%+d\n" 123
+123
$ printf "%d\n" -123
-123
$ printf "%+d\n" -123
-123
# 设置数字输出格式为千分位
$ printf "%d\n" 123456789
123456789
$ printf "%'d\n" 123456789
123,456,789
# 设置浮点数精度：
$ printf "%f\n" 123
123.000000
$ printf "%.f\n" 123
123
$ printf "%.1f\n" 123
123.0
$ printf "%.3f\n" 123
123.000
```

## 变更shell的行为
### set
set允许您更改shell选项的值并设置位置参数，或显示shell变量的名称和值。
```
set [--abefhkmnptuvxBCEHPT] [-o option-name] [argument …]
set [+abefhkmnptuvxBCEHPT] [+o option-name] [argument …]
```

如果没有提供选项或者参数, 显示所有shell变量的名称及值，包括shell函数，但在posix模式下只显示shell变量。显示结果是根据当前语系进行排序的，输出形式是一种友好的可以直接用来设置变量的格式，只读变量不能进行重置。当指定了某些选项时，就可以设置shell属性了，选项后面的所有参数arg当作位置参数进行处理。


`-a`: 自动标记创建或修改的变量和函数, 他们可以导出到后续命令的环境中
`-b`: 启用了作业控制时这个命令才有效, 即时报告后台作业终止时的状态, 而不是等待下一个shell主提示符.
`-e`: 管道, 列表, 组合命令的退出状态非0立即退出, 但这些命令为while或者until后面的命令, if或者elif后面的测试命令, 最后一个&& 或||的前面的命令, 管道中不是最后一个命令或者使用"!"的命令时, 则不会立即退出. 忽略这个选项时, 组合命令而非子shell返回false不会退出shell. 如果通过内建命令trap设置了"ERR", 他们在shell退出前执行. 这个选项作用域当前shell, 那么, 子shell在执行完所有命令前就可能提前退出了. 需要注意的是, 如果当前环境忽略了这个选项, 即使设置了这个选项返回false, 组合命令或者shell函数执行时也不受这个选项影响.
`f`: 禁止路径名扩展
`-h`: 查找命令执行时记住命令位置, 默认状态是打开的.
`-k`: 把以赋值语句形式出现的所有参数都放置到命令环境中, 而不仅仅是命令前面的那部分
`-n`, 读取命令但不执行他们, 可用于shell脚本的语法检查, 在交互式shell中忽略.
`-o option-name`
  * `allexport` Same as -a.
  * `braceexpand` Same as -B.
  * `emacs` Use an emacs-style line editing interface (see Command Line Editing). This also affects the editing interface used for read -e.
  * `errexit` Same as -e.
  * `errtrace`Same as -E.
  * `functrace` Same as -T.
  * `hashall` Same as -h.
  * `histexpand` Same as -H.
  * `history` Enable command history, as described in Bash History Facilities. This option is on by default in interactive shells.
  * `ignoreeof` An interactive shell will not exit upon reading EOF.
  * `keyword` Same as -k.
  * `monitor` Same as -m.
  * `noclobber` Same as -C.
  * `noexec` Same as -n.
  * `noglob` Same as -f.
  * `nolog` Currently ignored.
  * `notify` Same as -b.
  * `nounset` Same as -u.
  * `onecmd` Same as -t.
  * `physical` Same as -P.
  * `pipefail`If set, the return value of a pipeline is the value of the last (rightmost) command to exit with a non-zero status, or zero if all commands in the pipeline exit successfully. This option is disabled by default.

  * `posix`Change the behavior of Bash where the default operation differs from the POSIX standard to match the standard (see Bash POSIX Mode). This is intended to make Bash behave as a strict superset of that standard.
  * `privileged` Same as -p.
  * `verbose` Same as -v.
  * `vi` Use a vi-style line editing interface. This also affects the editing interface used for read -e.
  * `xtrace` Same as -x.
`-p`: 打开特权模式。在此模式下，不会处理$BASH_ENV和$ENV文件. shell函数不会从环境变量中继承, 如果SHELLOPTS,BASHOPTS,CDPATH,GLOBIGNORE等变量在环境变量中, 会被忽略.
`-t`: 读取并执行一个命令后退出。
`-u`: 在执行参数扩展时，将特殊参数“@”或“*”以外的未设置变量和参数视为错误。错误消息将写入标准错误，非交互式shell将退出。如果shell以有效用户（组）id不等于真实用户（组）id启动，并且未提供-p选项，则将执行这些操作，并将有效用户标识设置为实际用户标识。如果在启动时提供了-p选项，则不会重置有效的用户标识。关闭此选项将使有效用户和组ID设置为实际用户和组标识。
`-v`: 打印读取的shell输入行。
`-x`: 在shell简单命令, for, case, select或者算术for命令扩展后, 显示`PS4`的扩展值, 随后是命令扩展后的参数.
`-B`, 默认打开, 扩展大括号
`-C`, 对于重定向运算符">", "&>" 和 "<>", 不覆盖已存在的文件, 使用">|"重定向时会覆盖.
`-E`: 对于内建命令"trap"的"ERR", 可以被shell函数, 命令替换和子shell中命令继承, 默认是不继承的.
`-H`, 打开历史命令"!", 在交互模式shell有效.
`-P`: 不跟踪符号链接, 使用实际的物理地址
`-T`: trap的"DEBUG"和"RETURN"可以被shell函数, 命令替换和子shell中的命令继承, 默认是不继承.
`--`: 如果这个选项后面没有其他参数, 位置参数, 位置参数将被重置, 否则, 即使有以"-"开头的参数, 位置参数也会被设置为参数arg
`-`：表示选项结束，让后续参数arg赋值给位置参数，“-x”和“-v”被关闭，如果没有其他的参数arg，位置参数保持不变。 

set命令的大部分选项默认是关闭的，减号“-”打开，加号“+”关闭，这些选项可以作为启动shell时的参数，启动参数保存在变量“$-”中。 

查看启动参数：
```
$ echo $-
himBH
1
2
1
2
```
未定义变量进行参数扩展时报错：
```
$ unset foo
$ echo $foo

$ set -u
$ echo $foo
bash: foo: unbound variable
$ set +u
$ echo $foo
```
打印读取的shell输入行：
```
$ uname
Linux
$ set -v
$ uname
uname
Linux
$ set +v
set +v
$ uname
Linux
```
打开与关闭历史命令：
```
$ set -H
$ uname
Linux
$ !!
uname
Linux
$ set +H
$ uname
Linux
$ !!
!!: command not found
```
重置位置参数：
```
$ foo() { echo "foo:" $1 $2; }
hanjunjie@hanjunjie-HP:~$ foo a b
foo: a b
$ foo() { set --; echo "foo:" $1 $2; }
$ foo a b
foo:
```
### Shopt

`shopt [-pqsu] [-o] [optname …]`
切换控制可选shell行为的设置值。这些设置可以是下面列出的设置，或者，如果使用-o选项，则可以使用set-in选项的-o选项设置这些设置(请参阅Set Builtin)。

`-s`: 启用每一个optname
`-u`: 禁用每一个optname
`-q`: quiet模式，不输出optname及其状态，只是可以通过shopt命令的退出状态来查看某个optname是否打开或关闭。 
`-p`: 以shopt命令的输入格式显示optname的状态。 
`-o`:  限制optname为内建命令set的选项"-o"支持的那些值.


## shell的变量
### bsh的变量
`CDPATH`: 冒号分割的目录列表, 用于内建命令的搜索
`HOME`: 当前用户的家目录
`IFS`: 字符域的分隔符, 用于当shell将单词作为扩展的一部分时。
`MAIL`:如果此参数设置为文件名或目录名，并且未设置MAILPATH变量，则Bash通知用户邮件到达指定的文件或Maildir格式目录
`MAILPATH`: 以冒号分隔的文件名列表，shell定期检查新邮件。每个列表条目可以指定当新邮件到达邮件文件时通过将文件名与具有'？'的邮件分开而打印的消息。在消息的文本中使用时，$ _扩展为当前邮件文件的名称。
`OPTARG`: 由getopts内置函数处理的最后一个选项参数的值。
`OPTIND`: 由getopts内置函数处理的最后一个选项参数的索引。
`PATH`: shell在其中查找命令的目录的冒号分隔列表。 PATH的值中的零长度（null）目录名表示当前目录。空目录名称可能显示为两个相邻的冒号，或作为初始或结尾冒号
`PS1`:主提示字符串. 默认为`\s-\v\$`,[Controlling the Prompt](https://www.gnu.org/software/bash/manual/bash.html#Controlling-the-Prompt)用于显示PS1之前展开的转义序列的完整列表。
`PS2`: 辅助提示字符串。默认值为'>'。

### Bash Variables
1. `BASH`
2. `BASHOPTS`
3. `BASHPID`
4. `BASH_ALIASES`
5. BASH_ARGC
6. BASH_ARGV
7. BASH_CMDS
8. BASH_COMMAND
9. BASH_COMPAT
10. BASH_ENV
11. BASH_EXECUTION_STRING
12. BASH_LINENO
13. BASH_LOADABLES_PATH
14. BASH_REMATCH
15. BASH_SOURCE
16. BASH_SUBSHELL
17. BASH_VERSINFO
18. BASH_VERSION
19. BASH_XTRACEFD
20. CHILD_MAX
21. COLUMNS
22. COMP_CWORD
23. COMP_LINE
24. COMP_POINT
25. COMP_TYPE
26. COMP_KEY
27. COMP_WORDBREAKS
28. COMP_WORDS
29. COMPREPLY
30. COPROC
31. DIRSTACK
32. EMACS
33. ENV
34. EUID
35. EXECIGNORE
36. FCEDIT
37. FIGNORE
38. FUNCNAME
39. FUNCNEST
40. GLOBIGNORE
41. GROUPS
42. histchars
43. `HISTCMD`: 命令历史的记录数
44. `HISTCONTROL`: 以冒号分隔的值列表，用于控制如何在历史列表中保存命令.如果值列表包含“ignorespace”，则以空格字符开头的行不会保存在历史记录列表中。值'ignoredups'导致与以前的历史记录条目匹配的行不被保存。值'ignoreboth'是'ignorespace'和'ignoredups'的缩写。
45. `HISTFILE`: 保存命令历史记录的文件的名称。默认值为~/.bash_history。
46. `HISTFILESIZE`: 历史记录文件中包含的最大行数。为此变量分配一个值时，如果需要，将截断历史记录文件，以便通过删除最早的条目来包含不超过该行数。当shell退出时，历史文件也被截断为这个大小。当shell退出时，历史文件也被截断为这个大小。
47. `HISTIGNORE`:以冒号分隔的模式列表，用于确定应在历史列表中保存哪些命令行。每个模式都锚定在行的开头，并且必须匹配整行（不附加隐式'*'）。在应用由HISTCONTROL指定的检查后，针对线测试每个图案。除了正常的shell模式匹配字符外，
48. `HISTSIZE`: 历史记录列表上要记住的最大命令数。如果值为0，则命令不保存在历史列表中。小于零的数值导致每个命令保存在历史列表中（没有限制）。在读取任何启动文件后，shell将默认值设置为500。
49. `HISTTIMEFORMAT`: 如果此变量设置为非空，则其值将用作strftime的格式字符串，以打印与历史记录内置程序显示的每个历史记录条目相关联的时间戳。如果设置了此变量，那么会将时间戳写入历史记录文件，以便可以跨shell会话保留时间戳。这使用历史注释字符来区分时间戳与其他历史记录行。
50. HOSTFILE
51. HOSTNAME
52. HOSTTYPE
53. IGNOREEOF
54. INPUTRC
55. `LANG`: 用于确定未使用以LC_开头的变量专门选择的任何类别的区域设置类别。
56. `LC_ALL`: 此变量覆盖LANG和指定语言环境类别的任何其他LC_变量的值。
57. LC_COLLATE
58. LC_CTYPE
59. LC_MESSAGES
60. LC_NUMERIC
61. LC_TIME
62. LINENO
63. LINES
64. MACHTYPE
65. MAILCHECK
66. MAPFILE
67. OLDPWD
68. OPTERR
69. OSTYPE
70. PIPESTATUS
71. POSIXLY_CORRECT
72. PPID
73. PROMPT_COMMAND
74. PROMPT_DIRTRIM
75. PS0
76. PS3
77. PS4
78. PWD
79. RANDOM
80. READLINE_LINE
81. READLINE_POINT
82. REPLY
83. SECONDS
84. SHELL
85. SHELLOPTS
86. SHLVL
87. TIMEFORMAT
88. `TMOUT`: 如果设置为大于零的值，TMOUT将被视为读取内置命令的默认超时（请参阅Bash Builtins）。如果在TMOUT秒后输入未从终端输入，则输入未到达，则select命令终止。 在交互式shell中，值被解释为在发出主提示后等待一行输入的秒数。如果一个完整的输入行没有到达，Bash等待这个秒数后终止。
89. TMPDIR
90. UID

## bash 特性
### 调用bash
```
bash [long-opt] [-ir] [-abefhkmnptuvxdBCDHP] [-o option] [-O shopt_option] [argument …]
bash [long-opt] [-abefhkmnptuvxdBCDHP] [-o option] [-O shopt_option] -c string [argument …]
bash [long-opt] -s [-abefhkmnptuvxdBCDHP] [-o option] [-O shopt_option] [argument …]
```

调用shell时，可以使用与set builtin一起使用的所有单字符选项（请参阅Set Builtin）作为选项。此外，还有几个可以使用的多字符选项。这些选项必须出现在命令行上，才能识别单字符选项。

`--debugger`: 安排在shell启动之前执行调试器配置文件。打开扩展调试模式（有关shopt内置函数的extdebug选项的描述，请参阅Shopt Builtin）。
`--dump-po-strings`: 在“$”之前的所有双引号字符串的列表打印在GNU gettext PO(portable object)文件格式的标准输出上. 与`-D`相同
`--help`: 显示帮助信息
`--init-file filename`, `--rcfile filename`: 在交互式shell中从文件名（而不是~/ .bashrc）执行命令。
`--noediting`: Do not use the GNU Readline library (see Command Line Editing) to read command lines when the shell is interactive.
`--noprofile`: Don’t load the system-wide startup file /etc/profile or any of the personal initialization files ~/.bash_profile, ~/.bash_login, or ~/.profile when Bash is invoked as a login shell.
`--norc`: Don’t read the ~/.bashrc initialization file in an interactive shell. This is on by default if the shell is invoked as sh.
`--posix`: 
`--restricted`: 使shell成为受限外壳
`--verbose`:
`--version`:
`-c`: 从第一个非选项参数command_string读取和执行命令，然后退出。如果在command_string之后有参数，则第一个参数赋值为$0，剩余的参数赋值给位置参数。$ 0的赋值设置了shell的名称，用于警告和错误消息。
`-i`: 强制shell以交互方式运行。交互式外壳在交互式外壳中描述。当shell是交互式的时，这相当于使用'exec -l bash'启动登录shell。
`-l`, `--login`: 使这个shell像登录一样直接调用。
`-s`: 如果此选项存在，或者在选项处理后没有参数保留，则从标准输入读取命令。此选项允许在调用交互式shell时设置位置参数。
`-D`: 在“$”之前的所有双引号字符串的列表将打印在标准输出上。。这些是当前语言环境不是C或POSIX时要进行语言翻译的字符串（请参阅语言环境转换）。这意味着-n选项;不会执行任何命令。
`[-+]O [shopt_option]`: shopt_option是shopt内置函数接受的shell选项之一（参见The Shopt Builtin）。如果存在shopt_option，-O设置该选项的值; O unsets它。如果未提供shopt_option，则shopt接受的shell选项的名称和值将打印在标准输出上。如果调用选项为O，则输出以可重复用作输入的格式显示。
`--` A  - 表示选项的结束，并禁用进一步的选项处理。 - 之后的任何参数被视为文件名和参数。

### bash 启动的文件

**调用作为交互式登录shell，或者使用--login**
当bash以交互方式或者非交互时指定`--login`方式被调用时, bash第一个调用的是/etc/profile文件,如果存在的话. 之后调用`~/.bash_profile`,`~/.profile`.当shell启动时可以使用--noprofile选项来禁止此行为。
当交互式登录shell退出时，或非交互式登录shell执行exit builtin命令时，Bash从文件〜/ .bash_logout（如果存在）读取并执行命令。

**作为交互式非登录shell调用**
当是非登录方式调用时, 会读取`~/.bashrc`, `--norc`禁用
**非交互式调用**

**调用名为sh**
如果使用名称sh调用Bash，它会尽可能地模仿sh的历史版本的启动行为，同时遵循POSIX标准。
当作为交互式登录shell或作为具有--login选项的非交互式shell调用时，它首先尝试按顺序从/ etc / profile和〜/ .profile读取和执行命令。 --noprofile选项可用于禁止此行为。当调用作为名为sh的交互式shell时，Bash查找变量ENV，如果定义它，则扩展其值，并使用扩展的值作为要读取和执行的文件的名称。由于以sh调用的shell不会尝试从任何其他启动文件读取和执行命令，因此--rcfile选项不起作用。使用名称sh调用的非交互式shell不会尝试读取任何其他启动文件。当作为sh调用时，Bash在启动文件被读取后进入POSIX模式。
**在POSIX模式下调用**
当Bash在POSIX模式下启动时，与--posix命令行选项一样，它遵循启动文件的POSIX标准。在此模式下，交互式shell扩展ENV变量，并从名为扩展值的文件读取和执行命令。不会读取其他启动文件。
**由远程shell守护程序调用**
Bash尝试确定它的标准输入连接到网络连接时运行的时间，由远程shell守护程序（通常为rshd或安全shell守护程序sshd）执行时。如果Bash确定它正以这种方式运行，它会从〜/ .bashrc读取并执行命令，如果该文件存在并且可读。如果调用sh，它不会这样做。 --norc选项可用于禁止此行为，并且--rcfile选项可用于强制读取另一个文件，但是rshd和sshd通常不调用具有这些选项的shell或允许指定它们。
**调用具有不相等的有效和真实UID / GID**
如果Bash以有效用户（组）id不等于真实用户（组）id并且未提供-p选项启动，则不会读取启动文件，shell函数不会从环境继承，SHELLOPTS， BASHOPTS，CDPATH和GLOBIGNORE变量（如果它们出现在环境中）被忽略，并且有效用户ID设置为实际用户ID。如果在调用时提供了-p选项，则启动行为相同，但不会重置有效的用户标识。

### 交互式shell

#### 交互式shell 的行为
当shell以交互方式运行时，它以几种方式改变其行为。
1. 按照Bash启动文件中所述读取和执行启动文件。
2. 默认情况下启用作业控制（请参阅作业控制）.当作业控制生效时，Bash忽略键盘生成的作业控制信号SIGTTIN，SIGTTOU和SIGTSTP。
3. Bash在读取命令的第一行之前展开并显示PS1，并在读取多行命令的第二行和后续行之前展开和显示PS2. Bash在读取命令之后但在执行之前显示PS0。
4. Bash在打印主提示$ PS1之前将PROMPT_COMMAND变量的值作为命令执行.
5. Readline（参见命令行编辑）用于从用户终端读取命令。
6. Bash检查ignoreeof选项的值以set -o，而不是在读取命令时在其标准输入上接收到EOF时立即退出（请参阅Set Builtin）。
7. 默认情况下启用命令历史记录（请参阅Bash历史记录设置）和历史记录扩展（请参阅历史记录交互）。当启用历史记录的shell退出时，Bash会将命令历史记录保存到$ HISTFILE命名的文件。
8. 默认情况下执行别名扩展（见别名）。
9. 在没有任何trap的情况下，Bash忽略SIGTERM（参见信号）。
10. 在没有任何trap的情况下，捕获并处理SIGINT（见信号）。SIGINT将中断一些shell内建。
11. 如果启用了huponexit shell选项（参见信号），交互式登录shell会在退出时向所有作业发送SIGHUP。
12. -n调用选项被忽略，“set -n”没有效果（请参阅Set Builtin）。
13. Bash会定期检查邮件，具体取决于MAIL，MAILPATH和MAILCHECK shell变量的值（请参见Bash变量）。
14. 在启用“set -u”之后引用未绑定的shell变量所导致的扩展错误不会导致shell退出（请参阅Set Builtin）。
15. 当${var:?word}扩展中的var未设置或为null时，shell将不会退出扩展错误（参见Shell参数扩展）。
16. shell内置命令遇到的重定向错误不会导致shell退出。
17. 当在POSIX模式下运行时，返回错误状态的特殊内置函数不会导致shell退出（参见Bash POSIX模式）。
18. 失败的exec不会导致shell退出（参见Bourne Shell Builtins）。
19. 解析器语法错误不会导致shell退出。
20. 默认情况下启用cd内置命令的目录参数的简单拼写校正（请参阅Shopt Builtin中内置的shopt的cdspell选项的描述）。
21. shell将检查TMOUT变量的值，如果在打印$ PS1后没有在指定的秒数内读取命令，则退出（参见Bash变量）。




### Bash条件表达式
条件表达式由`[[`复合命令和测试和`[`内置命令。

表达式可以是一元的或者二元的. 一元的往往是测试一个文件的状态.还有字符串运算符和数字比较运算符。Bash处理几个文件名，特别是当它们在表达式中使用。如果Bash运行的操作系统提供这些特殊文件，Bash将使用它们;否则它将在内部用这种行为来模拟它们：如果其中一个基本的文件参数是/dev/fd/ N形式，则检查文件描述符N.如果其中一个基本文件的文件参数是/dev/stdin，/dev/stdout或/dev/stderr中的一个，则分别检查文件描述符0,1或2。
当与[[，'<'和'>'操作符使用当前语言环境按字典顺序排序。测试命令使用ASCII排序。


`-a file`
True if file exists.

`-b file`
True if file exists and is a block special file.

`-c file`
True if file exists and is a character special file.

`-d file`
True if file exists and is a directory.

`-e file`
True if file exists.

`-f file`
True if file exists and is a regular file.

`-g file`
True if file exists and its set-group-id bit is set.

`-h file`
True if file exists and is a symbolic link.

`-k file`
True if file exists and its "sticky" bit is set.

`-p file`
True if file exists and is a named pipe (FIFO).

`-r file`
True if file exists and is readable.

`-s file`
True if file exists and has a size greater than zero.

`-t fd`
True if file descriptor fd is open and refers to a terminal.

`-u file`
True if file exists and its set-user-id bit is set.

`-w file`
True if file exists and is writable.

`-x file`
True if file exists and is executable.

`-G file`
True if file exists and is owned by the effective group id.

`-L file`
True if file exists and is a symbolic link.

`-N file`
True if file exists and has been modified since it was last read.

`-O file`
True if file exists and is owned by the effective user id.

`-S file`
True if file exists and is a socket.

`file1 -ef file2`
True if file1 and file2 refer to the same device and inode numbers.

`file1 -nt file2`
True if file1 is newer (according to modification date) than file2, or if file1 exists and file2 does not.

`file1 -ot file2`
True if file1 is older than file2, or if file2 exists and file1 does not.

`-o optname`
True if the shell option optname is enabled. The list of options appears in the description of the -o option to the set builtin (see The Set Builtin).

`-v varname`
True if the shell variable varname is set (has been assigned a value).

`-R varname`
True if the shell variable varname is set and is a name reference.

`-z string`
True if the length of string is zero.

`-n string`
string
True if the length of string is non-zero.

`string1 == string2`
`string1 = string2`
True if the strings are equal. When used with the [[ command, this performs pattern matching as described above (see Conditional Constructs).

‘=’ should be used with the test command for POSIX conformance.

`string1 != string2`
True if the strings are not equal.

`string1 < string2`
True if string1 sorts before string2 lexicographically.

`string1 > string2`
True if string1 sorts after string2 lexicographically.

`arg1 OP arg2`
`OP` is one of `‘-eq’`,` ‘-ne’`, `‘-lt’`, `‘-le’`, `‘-gt’`, or `‘-ge’`. These arithmetic binary operators return true if arg1 is equal to, not equal to, less than, less than or equal to, greater than, or greater than or equal to arg2, respectively. Arg1 and arg2 may be positive or negative integers.

### Shell Arithmetic


`id++ id--`
variable post-increment and post-decrement

`++id --id`
variable pre-increment and pre-decrement

`- +`
unary minus and plus

`! ~`
logical and bitwise negation

`**`
exponentiation

`* / %`
multiplication, division, remainder

`+ -`
addition, subtraction

`<< >>`
left and right bitwise shifts

`<= >= < >`
comparison

`== !=`
equality and inequality

`&`
bitwise AND

`^`
bitwise exclusive OR

`|`
bitwise OR

`&&`
logical AND

`||`
logical OR

`expr ? expr : expr`
conditional operator

`= *= /= %= += -= <<= >>= &= ^= |=`
assignment

`expr1 , expr2`
comma

### 别名
别名允许在字被用作简单命令的第一个字时替换字符串。 shell维护可以使用alias和unalias builtin命令设置和取消设置的别名列表。
每个简单命令的第一个单词（如果未引用）将被检查以查看其是否具有别名。如果是，那个单词被替换为别名的文本。字符'/'，'$'，'`'，'='和上面列出的任何shell元字符或引用字符可能不会出现在别名中。
替换文本的第一个单词将被测试别名，但是与展开的别名相同的单词不会再次展开。这意味着，例如，可以将ls别名为“ls -F”，并且Bash不尝试递归地扩展替换文本。如果别名值的最后一个字符为空，那么还会检查别名后面的下一个命令字以进行别名扩展。

关于别名的定义和使用的规则有点混乱。 Bash总是读取至少一个完整的输入行，然后在该行上执行任何命令。读取命令时，别名将扩展，而不是在执行命令时扩展。因此，出现在与另一个命令相同行上的别名定义在读取下一行输入之前不会生效。该行上别名定义之后的命令不受新别名的影响。当执行函数时，这种行为也是一个问题。在读取函数定义时扩展别名，而不是在函数执行时扩展别名，因为函数定义本身是一个命令。因此，在函数中定义的别名直到函数执行后才可用。为了安全起见，请始终将别名定义放在单独的行上，并且不要在复合命令中使用别名。
## 数组

### １．数组的定义
Bash提供一维索引和关联数组变量.任何变量可以用作索引数组; declare builtin将显式声明一个数组。对数组的大小没有最大限制，也没有任何要求成员被连续索引或分配的要求。索引数组使用整数（包括算术表达式（参见Shell算术））引用，并且是从零开始的;关联数组使用任意字符串。除非另有说明，索引数组索引必须是非负整数。

`name[subscript]=value`
`declare -a name`
`declare -a name[subscript]`
`declare -A name`
`name=(value1 value2 … )`

```bash
names = ("aa" "cc", "bbb")
names = ($(ls *))
names[11]=22
names[12]=23

```  
### ２．数组遍历
```bash
adobe=('flash' 'flex' 'photoshop')
echo ${adobe[0]}

for var in ${adobe[@]}
do
  echo $var
done

len=${#adobe[@]}

for((i=0; i<$len;i++))
do
  echo ${adobe[$i]}
done

```

### ３．数组元素增删改
```bash
adobe=('Flash' 'Flex' 'Photoshop' 'Dreamweaver' 'Premiere')

[root@woke001 /root]#echo ${adobe[@]/Flash/FlashCS5}
FlashCS5 Flex Photoshop Dreamweaver Premiere

# 将替换后的值重新保存成数组
adobe=(${adobe[@]/Flash/FlashCS5})

[root@woke001 /root]#adobe[2]="dfsfs"

[root@woke001 /root]#echo ${adobe[2]}
dfsfs


# 删除
adobe=(${adobe[@]:0:2} ${adobe[@]:3})

adobe=(${adobe[@]/Photoshop/})
echo ${adobe[@]}
# 打印
# Flash Flex Dreamweaver Premier

```

### ４．数组相关的函数
```bash
# 数组的长度
echo ${#adobe[@]}

# 获取数组中的一部分
[root@woke001 /root]#adobe=('Flash' 'Flex' 'Photoshop' 'Dreamweaver' 'Premiere')

[root@woke001 /root]#echo ${#adobe[@]}
5
[root@woke001 /root]#echo ${adobe[@]:1:3}
Flex Photoshop Dreamweaver

[root@woke001 /root]#echo ${adobe[@]:3}
Dreamweaver Premiere

# 数组连接
adobe2=('Fireworks' 'Illustrator')


[root@woke001 /root]#adobe3=(${adobe[@]} ${adobe2[@]})

[root@woke001 /root]#echo ${#adobe3[@]}
7
```

### 目录堆栈(Directory Stack Builtins)
`dirs [-clpv] [+N|-N]`
显示记住的当前的 目录列表. 目录列表的添加使用`pushed`命令.poped命令从list删除. 当前的目录总是在栈的第一个.

`-c`: 清空目录栈的所有
`-l`: 使用完整路径名生成列表;默认列表格式使用波浪号表示主目录。默认列表格式使用波浪号表示主目录。
`-p`: 使dirs打印目录堆栈，每行一个条目。
`-v`: 使dirs以每行一个条目打印目录堆栈，为每个条目在堆栈中添加其索引。
`+N`: 显示第N个目录（从没有选项的调用时由dirs打印的列表左侧开始计数),从零开始
`-N`: 显示第N个目录（从没有选项的调用时由dirs打印的列表右侧开始计数),从零开始

`pushed [-n] [+N | -N] dir`
将当前目录保存在目录堆栈的顶部，然后cd到dir。没有参数，pushd交换顶部的两个目录，并使新的顶部当前目录。
`-n`: 当旋转或将目录添加到堆栈时，抑制目录的正常更改，以便只处理堆栈。
`+N`: 通过旋转堆栈，将第N个目录（从由dirs打印的列表的左边开始，从零开始）到列表的顶部。
`-N`: 通过旋转堆栈，将第N个目录（从由dirs打印的列表的右侧计数，从零开始）到列表的顶部。
`dir`: 使dir成为堆栈的顶部，使其成为新的当前目录，就像它作为参数提供给cd内置函数一样。

`popd [-n] [+N | -N]`
当没有给出参数时，popd从栈中删除顶层目录并执行一个cd到新的顶层目录。元素从0开始编号，从列出的第一个目录开始;也就是说，popd等价于popd 0。
`-n`: 当没有给出参数时，popd从栈中删除顶层目录并执行一个cd到新的顶层目录。元素从0开始编号，从列出的第一个目录开始;也就是说，popd等价于popd 0。
`+N`: 删除从零开始的第N个目录（从dirs打印的列表左侧开始计数）。
`-N`: 从零开始删除第N个目录（从dirs打印的列表右侧开始计数）。

### bash的严格模式

### POSIX 模式

## 作业控制
### 作业控制基础

## 命令行编辑

## 使用历史记录
