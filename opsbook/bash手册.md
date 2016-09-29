# bash 手册
---

## 基础语法


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

### bash命令的搜索路径和执行
1. 如果命令里没有"/"搜索它, 当存在此名称的函数时,执行他.
2. 如果没有此名称的函数,则在内建命令里搜索,搜索到执行.
3. 如果既没有函数的定义,也不是内建名利, 则使用$PATH的路径搜索这个命令;(Bash有一个$PATH下所有可执行命令的 hash table.)
4. 如果

## 数组

### １．数组的定义
`name[subscript]=value`

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
