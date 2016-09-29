# mysql_sandbox 工具
---
mysql_sandbox是一个MySQL多版本的生成的管理工具, 可以方便在建立MySQL 各个版本的数据库, 方便测试.

## 1. 安装

[官网](http://mysqlsandbox.net/)
```
# 下载 https://github.com/datacharmer/mysql-sandbox
git clone https://github.com/datacharmer/mysql-sandbox

export SANDBOX_BINARY=$HOME/opt/mysql

# root用户的安装
cd  mysql_sandbox
perl Makefile.PL 
make
make test
make install

# 普通用户
export PATH=$HOME/usr/local/bin:$PATH
export PERL5LIB=$HOME/usr/local/lib/perl5/site_perl/x.x.x
perl Makefile.PL PREFIX=$HOME/usr/local
make
make test
make install

```

## 2. 使用mysql_sandbox安装数据库环境

### 2.1 下载MySQL的二进制版本(Linux - Generic的tar.gz) 

```
wget   mysql-5.6.31-linux-glibc2.5-x86_64.tar.gz

```
### 2.2 建立单台数据库
```
# root 用户
export SANDBOX_AS_ROOT=1
export SANDBOX_BINARY=$HOME/opt/mysql
make_sandbox  --export_binaries --upper_directory=/opt/mysql
/path/to/mysql-5.6.31-linux-glibc2.5-x86_64.tar.gz
# 可以指定安装路径
```

### 2.3 建立一组主从的集群
```
[root@yimiwork_214 ~]# make_replication_sandbox --how_many_slaves=2 --sandbox_base_port=3306 --upper_directory=/data/mysql /root/mysql-5.6.31-linux-glibc2.5-x86_64.tar.gz 
installing and starting master
installing slave 1
installing slave 2
starting slave 1
........ sandbox server started
starting slave 2
............. sandbox server started
initializing slave 1
initializing slave 2
replication directory installed in /data/mysql/rsandbox_mysql-5_6_31

```

`how_many_slaves=2 ` : 是指有多少个slave
`sandbox_base_port`: master端口
`upper_directory`: 安装目录

### 循环复制

```
make_replication_sandbox  --circular=4  /root/mysql-5.6.31-linux-glibc2.5-x86_64.tar.gz 
```

### 2.5 配置文件的路径

`/data/mysql/rsandbox_mysql-5_6_31/master/my.sandbox.cnf` : master的配置文件
`/data/mysql/rsandbox_mysql-5_6_31/node{1,2,...}/my.sandbox.cnf`: slave的

### 2.6 相关命令
` /data/mysql/rsandbox_mysql-5_6_31/` 相关命令都在个目录里

## 3. sbtool 管理sandbox的命令

## 4. 详细见[文档](https://github.com/datacharmer/mysql-sandbox)
