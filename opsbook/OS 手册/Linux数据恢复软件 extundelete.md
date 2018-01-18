# 数据恢复软件 extndelete 介绍
---
利用 inode 进行恢复

## 安装 extundelete
官网 http://extundelete.sourceforge.net
```
tar -xf extundelete.tar.gz
cd 
./configure
make 
make install

```

## extundelete 用法详解

extundelete：
`--superblock`:  显示超级块信息
`--journal`: 显示日志信息
`--after dtime`: 时间参数， 表示再某个时间段之后被删除的文件或目录
动作：
`--inode ino`： 显示节点“ino”的信息
`--block blk`: 显示数据块 “blk” 的信息
`--restore-inode ino[, ino,...]`: 文件恢复命令参数， 表示恢复节点“ino”的文件， 恢复的文件会自动放在当前目录下的TRESTORED_FILES 目录忠，使用节点编号作为扩展名
`--restore-file path`: 恢复命令参数， 表示见恢复指定路径 的文件， 并把恢复的文件放在当前目录下的RECOVERED_FILES 目录中。
`--restore-files path`: 恢复命令参数， 表示将恢复再路径中已列出的所有文件。
`--restore-all`： 恢复命令参数， 表示将尝试恢复所有目录的文件
`-j journal`: 表示从已经命名的文件中读取扩展日志
`-b blocknumber`: 表示使用之前备份的超级块来打开文件系统， 一般用于查看现有超级块是不是单签所要的文件
`-B blocksize` 通过指定数据块大小来打开文件系统， 一般用于查看已经知道大小的文件
## 实战

* 误删后， 第一时间卸载磁盘或分区， 或者进入单用户模式， 标志为只读。

```
umount /data
extundelete /dev/sdc1 --inode 2

extundelete /dev/sdc1 --restore-file passwd # 恢复passwd 文件

# 恢复一个目录

extundelete /dev/sdc1 --restore-directory 、ganglia-3.4。0
# 恢复所有
extundelete /dev/sdc1 --restore-all


# 恢复某个时间段

extundelete --after 1379150740 --restore-all /dev/sdc1
```