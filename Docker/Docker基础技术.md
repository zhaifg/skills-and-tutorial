# Docker 基础技术
---
## AUFS
AUFS 是一种 Union File System, 所谓UnioinFS就是把不同物理位置的目录合并mount到同一个目录中. UnionFS等等主要一各应用是, 吧一张CD/DVD和一个硬盘目录联合mount 在一起, 然后, 你就可以对这个制度的CD/DVD上的文件进行修改了.

实例(ubuntu 14.04)

- 1, 我们肩上两个目录(水果和蔬菜), 并在这个两个目录中放上一些文件, 水果中有苹果和番茄, 蔬菜有胡萝卜和番茄
```
$ tree
.
├── fruits
│   ├── apple
│   └── tomato
└── vegetables
    ├── carrots
    └── tomato
```

- 2,我们输入一下命令
```
mkdir mnt

mount -t aufs -o dirs=./fruits:./vegetables none ./mnt
 tree ./mnt
./mnt
├── apple
├── carrots
└── tomato

```
我们可以看到在./mnt目录下有三个文件，苹果apple、胡萝卜carrots和蕃茄tomato。水果和蔬菜的目录被union到了./mnt目录下了。

- 3, 我们来修改下期中文件内容
```
echo mnt > ./mnt/apple
> cat ./mnt/apple
mnt

> cat ./friuts/apple
mnt

```

上面的示例，我们可以看到./mnt/apple的内容改了，./fruits/apple的内容也改了。

- 4, 
```
 echo mnt_carrots > ./mnt/carrots
$ cat ./vegetables/carrots
 
$ cat ./fruits/carrots
mnt_carrots
```
上面的示例，我们可以看到，我们修改了./mnt/carrots的文件内容，./vegetables/carrots并没有变化，反而是./fruits/carrots的目录中出现了carrots文件，其内容是我们在./mnt/carrots里的内容。

也就是说，我们在mount aufs命令中，我们没有指它vegetables和fruits的目录权限，默认上来说，命令行上第一个（最左边）的目录是可读可写的，后面的全都是只读的。（一般来说，最前面的目录应该是可写的，而后面的都应该是只读的）

所以，如果我们像下面这样指定权限来mount aufs，你就会发现有不一样的效果（记得先把上面./fruits/carrots的文件删除了）：

```
$ sudo mount -t aufs -o dirs=./fruits=rw:./vegetables=rw none ./mnt
 
$ echo "mnt_carrots" > ./mnt/carrots
 
$ cat ./vegetables/carrots
mnt_carrots
 
$ cat ./fruits/carrots
cat: ./fruits/carrots: No such file or directory
```


现在，在这情况下，如果我们要修改./mnt/tomato这个文件，那么究竟是哪个文件会被改写？

```
$ echo "mnt_tomato" > ./mnt/tomato
 
$ cat ./fruits/tomato
mnt_tomato
 
$ cat ./vegetables/tomato
I am a vegetable
```

> 可见，如果有重复的文件名，在mount命令行上，越往前的就优先级越高。


关于docker的分层镜像，除了aufs，docker还支持btrfs, devicemapper和vfs，你可以使用 -s 或 –storage-driver= 选项来指定相关的镜像存储。在Ubuntu 14.04下，docker默认Ubuntu的 aufs（在CentOS7下，用的是devicemapper，关于devicemapper，我会以以后的文章中讲解）你可以在下面的目录中查看相关的每个层的镜像：

`/var/lib/docker/aufs/diff/<id>`
在docker执行起来后（比如：docker run -it ubuntu /bin/bash ），你可以从/sys/fs/aufs/si_[id]目录下查看aufs的mount的情况，下面是个示例：

```
#ls /sys/fs/aufs/si_b71b209f85ff8e75/
br0      br2      br4      br6      brid1    brid3    brid5    xi_path
br1      br3      br5      brid0    brid2    brid4    brid6 
 
# cat /sys/fs/aufs/si_b71b209f85ff8e75/*
/var/lib/docker/aufs/diff/87315f1367e5703f599168d1e17528a0500bd2e2df7d2fe2aaf9595f3697dbd7=rw
/var/lib/docker/aufs/diff/87315f1367e5703f599168d1e17528a0500bd2e2df7d2fe2aaf9595f3697dbd7-init=ro+wh
/var/lib/docker/aufs/diff/d0955f21bf24f5bfffd32d2d0bb669d0564701c271bc3dfc64cfc5adfdec2d07=ro+wh
/var/lib/docker/aufs/diff/9fec74352904baf5ab5237caa39a84b0af5c593dc7cc08839e2ba65193024507=ro+wh
/var/lib/docker/aufs/diff/a1a958a248181c9aa6413848cd67646e5afb9797f1a3da5995c7a636f050f537=ro+wh
/var/lib/docker/aufs/diff/f3c84ac3a0533f691c9fea4cc2ceaaf43baec22bf8d6a479e069f6d814be9b86=ro+wh
/var/lib/docker/aufs/diff/511136ea3c5a64f264b78b5433614aec563103b4d4702f3ba7d4d2698e22c158=ro+wh
64
65
66
67
68
69
70
/run/shm/aufs.xino
```

你会看到只有最顶上的层（branch）是rw权限，其它的都是ro+wh权限只读的。

关于docker的aufs的配置，你可以在/var/lib/docker/repositories-aufs这个文件中看到。

### AUFS的一些特性
AUFS有所有Union FS的特性, 把多个目录, 合并成一个目录, 并可以为每个需要合并多目录指定相应的权限, 实时的添加, 删除, 修改已经被mount好目录. 而且还能在多个可携带branch/dir间进行负载均衡.

上面的例子, 我们已经看到AUFS的mount的实例了, 下面我们看看呗union目录的相关权限:

* rw 表示可以写可读  read-write
* ro 表示read-only, 如果你不指定权限, 那么除了第一个外ro是默认值, 对于ro分支, 器永远不会收到写的操作, 也不会收到查找whiteout 操作
* rr 表示real-read-only, 与 read-only 不同的是, rr标记的是天生就是只读分支, 这样, AUFS可以提高性能, 比如不在设置inotify 来检查文件变动通知
权限中, 我们看到了一个术语: whiteout, 下面解释下这个术语

### 相关术语
Branch 就是 各个要被 union 其阿里的目录(就是我在上面使用的dirs的命令行参数)

* Branch 根据 union 的顺序形成一个stack, 一般来说最上面的是可写的, 下面的都是只读的
* Branch的stack可以在mount后进行修改, 比如: 修改顺序, 加入新的branch, 或是删除其中的branch, 或是直接修改branch的权限

Whiteout 和 opaque
* 如果UnionFS 中的某个目录被删除了, 那么就应该不可见了, 就算在底层的branch中的还有这个目录, 那也应该不可见了
* Whiteout 就是某个上层目录覆盖了下层的相同名字的目录. 用于隐藏底层分支的文件, 也用于组织readdir进入底层分支
* Opaque的意思就是不允许任何的某个目录显示出来
* 在隐藏底层档的情况下, whiteout 的名字'.wh.<filename>'
* 在阻止readdir情况下, 名字'. whi..wh..opq' 货' .wh.__dir_opaque'
### 相关问题

其一, 你可能会问, 要文件在原来的地方被修改了会怎么样? mount的目录会一起改变吗?
答案是会的, 也是可以不会的. 因为你可以指定一个叫udba的参数(全称: User's Direct Branch Access), 这个参数有三个值:
* udba=none, 设置上这个参数后, AUFS会运转的更快, 因为那些不在mount目录里发生的修改, aufs不会同步过来, 所以会有数据出错的问题.
* udba=reval   设置上这个参数后, AUFS会查找文件有没有被更新, 如果有的话, 就会把修改拉到mount目录中
* udba=notify  这个参数会让AUFS 为所有的 branch注册notify, 这样可以让AUFS在更新文件修改的性能更高点.


`create=rr | round−robin `轮询。下面的示例可以看到，新创建的文件轮流写到三个目录中
```
hchen$ sudo mount -t aufs  -o dirs=./1=rw:./2=rw:./3=rw -o create=rr none ./mnt
hchen$ touch ./mnt/a ./mnt/b ./mnt/c
hchen$ tree
.
├── 1
│   └── a
├── 2
│   └── c
└── 3
    └── b
```


`create=mfs[:second] | most−free−space[:second] `选一个可用空间最好的分支。可以指定一个检查可用磁盘空间的时间。

`create=mfsrr:low[:second] `选一个空间大于low的branch，如果空间小于low了，那么aufs会使用 round-robin 方式。

更多的关于AUFS的细节使用参数，大家可以直接在Ubuntu 14.04下通过 man aufs 来看一下其中的各种参数和命令。
