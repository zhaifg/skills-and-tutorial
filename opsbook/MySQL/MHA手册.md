# MHA的管理应用手册
---

## 1. MHA的介绍
MHA（Master High Availability）目前在MySQL高可用方面是一个相对成熟的解决方案，它由日本DeNA公司youshimaton（现就职于Facebook公司）开发，是一套优秀的作为MySQL高可用性环境下故障切换和主从提升的高可用软件。在MySQL故障切换过程中，MHA能做到在0~30秒之内自动完成数据库的故障切换操作，并且在进行故障切换的过程中，MHA能在最大程度上保证数据的一致性，以达到真正意义上的高可用。

该软件由两部分组成：`MHA Manager`（管理节点）和`MHA Node`（数据节点）。MHA Manager可以单独部署在一台独立的机器上管理多个master-slave集群，也可以部署在一台slave节点上。MHA Node运行在每台MySQL服务器上，MHA Manager会定时探测集群中的master节点，当master出现故障时，它可以自动将最新数据的slave提升为新的master，然后将所有其他的slave重新指向新的master。整个故障转移过程对应用程序完全透明。

在MHA自动故障切换过程中，MHA试图从宕机的主服务器上保存二进制日志，最大程度的保证数据的不丢失，但这并不总是可行的。例如，如果主服务器硬件故障或无法通过ssh访问，MHA没法保存二进制日志，只进行故障转移而丢失了最新的数据。使用MySQL 5.5的半同步复制，可以大大降低数据丢失的风险。MHA可以与半同步复制结合起来。如果只有一个slave已经收到了最新的二进制日志，MHA可以将最新的二进制日志应用于其他所有的slave服务器上，因此可以保证所有节点的数据一致性。

目前MHA主要支持一主多从的架构，要搭建MHA,要求一个复制集群中必须最少有三台数据库服务器，一主二从，即一台充当master，一台充当备用master，另外一台充当从库，因为至少需要三台服务器，出于机器成本的考虑，淘宝也在该基础上进行了改造，目前淘宝TMHA已经支持一主一从。

我们自己使用其实也可以使用1主1从，但是master主机宕机后无法切换，以及无法补全binlog。master的mysqld进程crash后，还是可以切换成功，以及补全binlog的。

[官方介绍](https://code.google.com/p/mysql-master-ha/)：

图01展示了如何通过MHA Manager管理多组主从复制。可以将MHA工作原理总结为如下：
![mha](D:/gitbook/opsbook/images/mha1.png)

1. 从宕机崩溃的master保存二进制日志事件（binlog events）;
2. 识别含有最新更新的slave；
3. 应用差异的中继日志（relay log）到其他的slave；
4. 应用从master保存的二进制日志事件（binlog events）；
5. 提升一个slave为新的master；
6. 使其他的slave连接新的master进行复制；

### MHA的功能
* 1.__自动的监控和故障切换切换master__
  MHA可以监控MySQL的复制环境的中主库, 提供自动故障切换. MHA通过验证所有slave的relay log事件的差异, 来确定复制的一致性,包括没有完整复制到slave, 并补偿没有完成复制的relay log 的slave. MHA通产可以在9-12秒的来完成故障转移,并在7-10秒钟内补偿各个slave 的binlog 的差异,选中一个新的master, 并关机避免脑裂的产生. 这一故障发生到处理完成,在10-30秒内完成. 通过配置文件来确定新的master的. 原来的主库突然停止时, 可能会造成从的relay log的缺失, 这一问题可以通过MHA来解决, 但是如果突然关机了, 会丢失数据.

* 2.__交互式(手动)进行故障转移__:
  MHA可以不使用MHA的监控MySQL的复制环境, 使用手工进行故障转移.

* 3.__非交互式的故障的转移__:
  在没有MHA的监控下的非交互式下,也可以进行MySQL的复制环境的Master的切换, 前提是我们使用其他的软件对Master的运行的进行监控,比如使用heartbeat(Pacemaker)来进行Master的MySQL运行监测,并完成VIP的切换,使用MHA来完成切换Master和binlog的 差异补偿.

* 4.__在线的切换master__:
  通常我们在有些时候,需要把现在Master切换到其他的机器上, 比如当前的Master的硬件的RAID或者内存有问题, 或者要使用其他更快搞好的机器来代替这台机器. 这是不是因为Master的宕机, 而是因为需要维护它, 想要尽快完成切换, 尽可能的减少宕机时间,
  当我们需要对现在的Master系统或者硬件进行维护时, 需要切换Master.
  MHA可以提供在0.5-2秒内阻塞Master的写入,并完美的完成Master的切换.

### 切换主库的困难
Master的故障迁移不是看起来那么简单的. 大多数MySQL的复制环境中, 是只有单台的写入的主库,和有多台slave的从库. 如果master crash掉, 需要从几台slave中挑选一台最接近Master的从库来充当新的主库. 挑选新的master的不是那么容易实现的. 即使当前最接近主库的slave可以使用,但可能像去其他的slave一样,可能会丢失一些bin log. 当连接到新的master时, 这么slave会丢失一些数据, 这回造成的数据的不一致. 为了避免数据的不一致, 需要在切换新的master之前, 把那些(没有收到)丢失的binlog补齐给slave, 然后再进行切换. 如果手动执行的,这是一个非常苦难和复杂的过程. 

__演示一下切换的过程__:

![mha-problem](D:/gitbook/opsbook/images/mha-problem.png)

图上所示, 当Master发生故障时, 什么让他困难?

目前大多数的MySQL的复制的故障时, 不得不手动进行故障转移. 通常一个小时或者几个小时来处理这个问题. 可能不是所有的slave都会收到相同的binlog, 从而导致了数据不一致, 而我们不得不修正数据.

MHA是一个全自动的master的尽可能快的故障转移和数据一致性性修复,没有任何备用机.

MHA提供自动和手动的方式来故障转移. 自动转移通过`master_manager`来完成,并且还会监控主从的可用性, 如果MHA的Manager不能访问到Maseter Server,  会自动启动非交互式的切换.

手动切换的命令是`masterha_master_switch`.

## 2. MHA的入门

```
yum install perl-DBD-MySQL
yum install perl-Config-Tiny
yum install perl-Log-Dispatch
yum install perl-Parallel-ForkManager
```

## 3. 相关命令
### 3.1 Manager 端
`masterha_check_ssh`              检查MHA的SSH配置状况
`masterha_check_repl`             检查MySQL复制状况
`masterha_manger`                 启动MHA
`masterha_check_status `          检测当前MHA运行状态
`masterha_master_monitor`         检测master是否宕机
`masterha_master_switch`          控制故障转移（自动或者手动）
`masterha_conf_host`              添加或删除配置的server信息

### 3.2 Node端
这些工具通常由MHA Manager的脚本触发，无需人为操作）主要包括以下几个工具

`save_binary_logs`                保存和复制master的二进制日志
`apply_diff_relay_logs`           识别差异的中继日志事件并将其差异的事件应用于其他的slave
`filter_mysqlbinlog`              去除不必要的ROLLBACK事件（MHA已不再使用这个工具）
`purge_relay_logs`                清除中继日志（不会阻塞SQL线程)



## 4. MHA的进阶

## 5. FAQ

## 6. 附加信息

## 7. 实例
### 7.1 试验环境架构

|角色|ip地址|主机名|server_id| 类型|
|---|----|----|----|----|
|Monitor host|192.168.0.20|server01|-|监控复制组|
|Master|192.168.0.50|server02|1|写入|
|Candicate master|192.168.0.60|server03|2|读|
|Slave|192.168.0.70|server04|3|读|

其中master对外提供写服务，备选master（实际的slave，主机名server03）提供读服务，slave也提供相关的读服务，一旦master宕机，将会把备选master提升为新的master，slave指向新的master

### 7.2 配置Host的相关IP,hostname,epel,
略

### 7.3 配置ssh的免密码登录
几台机器之间的相互免密码登录(略)

### 7.4 配置MySQL的主从同步(MySQL默认已安装)
设置主从时需要需要设置
```
log-bin = /mydata/data/logs/binlog/mysql-bin
log-bin-index = /mydata/data/logs/binlog/mysql-bin.index
relay_log = /mydata/data/logs/mysql-relay-bin
relay_log_index = /mydata/data/logs/mysql-relay-bin.index
```

1.master上:
`mysqldump --master-data=2 --single-transaction -R --triggers -A > all.sql`

2.创建复制用户
```sql
mysql> grant replication slave on *.* to 'repl'@'192.168.0.%' identified by '123456';
Query OK, 0 rows affected (0.00 sec)

mysql> flush privileges;
Query OK, 0 rows affected (0.00 sec)

mysql> 
```

3.查看 master信息
```
head -n 30 all.sql | grep 'CHANGE MASTER TO'
-- CHANGE MASTER TO MASTER_LOG_FILE='mysql-bin.000010', MASTER_LOG_POS=112;
```

4.把备份复制到server03和server04，也就是192.168.0.60和192.168.0.70
```
scp all.sql server03:/data/
scp all.sql server04:/data/
```

5.导入备份到server03,server04，执行复制相关命令
`mysql < /data/all.sql`

```
mysql> CHANGE MASTER TO MASTER_HOST='192.168.0.50',MASTER_USER='repl', MASTER_PASSWORD='123456',MASTER_LOG_FILE='mysql-bin.000010',MASTER_LOG_POS=112;
Query OK, 0 rows affected (0.02 sec)

mysql> start slave;
Query OK, 0 rows affected (0.01 sec)

mysql> 

[root@192.168.0.60 ~]# mysql -e 'show slave status\G' | egrep 'Slave_IO|Slave_SQL'
               Slave_IO_State: Waiting for master to send event
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
[root@192.168.0.60 ~]# 
```


6.两台slave服务器设置read_only（从库对外提供读服务，只所以没有写进配置文件，是因为随时slave会提升为master）
`mysql -e 'set global read_only=1'`


7.创建监控用户（在master上执行，也就是192.168.0.50）：
```
mysql> grant all privileges on *.* to 'root'@'192.168.0.%' identified  by '123456';
Query OK, 0 rows affected (0.00 sec)

mysql> flush  privileges;
Query OK, 0 rows affected (0.01 sec)
```

__注意__:
> binlog-do-db 和 replicate-ignore-db 设置必须相同。 MHA 在启动时候会检测过滤规则，如果过滤规则不同，MHA 不启动监控和故障转移。

### 7.5 安装MHA的node
1.yum安装(所有节点)
```
yum install perl-DBD-MySQL -y
yum install mha4mysql-node-X.Y-0.noarch.rpm

```

2.源码安装

```

at > /root/list << EOF
install DBD::mysql
EOF
for package in `cat /root/list`
do
    cpanm $package
done


 Install DBD::mysql if not installed
  $ tar -zxf mha4mysql-node-X.Y.tar.gz
  $ perl Makefile.PL
  $ make
  $ sudo make install
```

安装完成后会在/usr/local/bin目录下生成以下脚本文件：
```
[root@192.168.0.50 bin]# pwd
/usr/local/bin
[root@192.168.0.50 bin]# ll
total 40
-r-xr-xr-x 1 root root 15498 Apr 20 10:05 apply_diff_relay_logs
-r-xr-xr-x 1 root root  4807 Apr 20 10:05 filter_mysqlbinlog
-r-xr-xr-x 1 root root  7401 Apr 20 10:05 purge_relay_logs
-r-xr-xr-x 1 root root  7263 Apr 20 10:05 save_binary_logs
[root@192.168.0.50 bin]# 
```

### 7.6 安装MHA的Manager
1.yum安装
```
yum install perl-DBD-MySQL perl-Config-Tiny perl-Log-Dispatch perl-Parallel-ForkManager perl-Time-HiRes -y
yum install mha4mysql-manager-X.Y-0.noarch.rpm

```
2.源码安装
```
yum install perl-DBD-MySQL perl-Config-Tiny perl-Log-Dispatch perl-Parallel-ForkManager perl-Time-HiRes -y

$ tar -zxf mha4mysql-manager-X.Y.tar.gz
$ perl Makefile.PL
$ make
$ sudo make install

[root@192.168.0.20 bin]# ll
total 76
-r-xr-xr-x 1 root root 15498 Apr 20 10:58 apply_diff_relay_logs
-r-xr-xr-x 1 root root  4807 Apr 20 10:58 filter_mysqlbinlog
-r-xr-xr-x 1 root root  1995 Apr 20 11:33 masterha_check_repl
-r-xr-xr-x 1 root root  1779 Apr 20 11:33 masterha_check_ssh
-r-xr-xr-x 1 root root  1865 Apr 20 11:33 masterha_check_status
-r-xr-xr-x 1 root root  3201 Apr 20 11:33 masterha_conf_host
-r-xr-xr-x 1 root root  2517 Apr 20 11:33 masterha_manager
-r-xr-xr-x 1 root root  2165 Apr 20 11:33 masterha_master_monitor
-r-xr-xr-x 1 root root  2373 Apr 20 11:33 masterha_master_switch
-r-xr-xr-x 1 root root  3749 Apr 20 11:33 masterha_secondary_check
-r-xr-xr-x 1 root root  1739 Apr 20 11:33 masterha_stop
-r-xr-xr-x 1 root root  7401 Apr 20 10:58 purge_relay_logs
-r-xr-xr-x 1 root root  7263 Apr 20 10:58 save_binary_logs

```

复制相关脚本到/usr/local/bin目录(软件包解压缩后就有了，不是必须，因为这些脚本不完整，需要自己修改，这是软件开发着留给我们自己发挥的,如果开启下面的任何一个脚本对应的参数，而对应这里的脚本又没有修改，则会抛错，yum安装不会包括这些脚本)
```
[root@192.168.0.20 scripts]# pwd
/root/mha4mysql-manager-0.53/samples/scripts
[root@192.168.0.20 scripts]# ll
total 32
-rwxr-xr-x 1 root root  3443 Jan  8  2012 master_ip_failover                #自动切换时vip管理的脚本，不是必须，如果我们使用keepalived的，我们可以自己编写脚本完成对vip的管理，比如监控mysql，如果mysql异常，我们停止keepalived就行，这样vip就会自动漂移
-rwxr-xr-x 1 root root  9186 Jan  8  2012 master_ip_online_change           #在线切换时vip的管理，不是必须，同样可以可以自行编写简单的shell完成
-rwxr-xr-x 1 root root 11867 Jan  8  2012 power_manager                     #故障发生后关闭主机的脚本，不是必须
-rwxr-xr-x 1 root root  1360 Jan  8  2012 send_report                       #因故障切换后发送报警的脚本，不是必须，可自行编写简单的shell完成。
[root@192.168.0.20 scripts]# cp * /usr/local/bin/
[root@192.168.0.20 scripts]# 
```

### 7.7 配置MHA的Manager的配置文件
1.）创建MHA的工作目录，并且创建相关配置文件（在软件包解压后的目录里面有样例配置文件）
`mkdir -p /etc/masterha`

```
[root@192.168.0.20 ~]# cat /etc/masterha/app1.cnf 
[server default]
manager_workdir=/var/log/masterha/app1.log              //设置manager的工作目录
manager_log=/var/log/masterha/app1/manager.log          //设置manager的日志
master_binlog_dir=/data/mysql                         //设置master 保存binlog的位置，以便MHA可以找到master的日志，我这里的也就是mysql的数据目录
master_ip_failover_script= /usr/local/bin/master_ip_failover    //设置自动failover时候的切换脚本
master_ip_online_change_script= /usr/local/bin/master_ip_online_change  //设置手动切换时候的切换脚本
password=123456         //设置mysql中root用户的密码，这个密码是前文中创建监控用户的那个密码
user=root               设置监控用户root
ping_interval=1         //设置监控主库，发送ping包的时间间隔，默认是3秒，尝试三次没有回应的时候自动进行railover
remote_workdir=/tmp     //设置远端mysql在发生切换时binlog的保存位置
repl_password=123456    //设置复制用户的密码
repl_user=repl          //设置复制环境中的复制用户名
report_script=/usr/local/send_report    //设置发生切换后发送的报警的脚本
secondary_check_script= /usr/local/bin/masterha_secondary_check -s server03 -s server02 --user=root --master_host=server02 --master_ip=192.168.0.50 --master_port=3306               //一旦MHA到server02的监控之间出现问题，MHA Manager将会尝试从server03登录到server02
shutdown_script=""      //设置故障发生后关闭故障主机脚本（该脚本的主要作用是关闭主机放在发生脑裂,这里没有使用）
ssh_user=root           //设置ssh的登录用户名

[server1]
hostname=192.168.0.50
port=3306

[server2]
hostname=192.168.0.60
port=3306
candidate_master=1   //设置为候选master，如果设置该参数以后，发生主从切换以后将会将此从库提升为主库，即使这个主库不是集群中事件最新的slave
check_repl_delay=0   //默认情况下如果一个slave落后master 100M的relay logs的话，MHA将不会选择该slave作为一个新的master，因为对于这个slave的恢复需要花费很长时间，通过设置check_repl_delay=0,MHA触发切换在选择一个新的master的时候将会忽略复制延时，这个参数对于设置了candidate_master=1的主机非常有用，因为这个候选主在切换的过程中一定是新的master

[server3]
hostname=192.168.0.70
port=3306
[root@192.168.0.20 ~]# 
```

2.设置relay log的清除方式（在每个slave节点上）
```
[root@192.168.0.60 ~]# mysql -e 'set global relay_log_purge=0'
[root@192.168.0.70 ~]# mysql -e 'set global relay_log_purge=0'
```

__注意__:
>MHA在发生切换的过程中，从库的恢复过程中依赖于relay log的相关信息，所以这里要将relay log的自动清除设置为OFF，采用手动清除relay log的方式。在默认情况下，从服务器上的中继日志会在SQL线程执行完毕后被自动删除。但是在MHA环境中，这些中继日志在恢复其他从服务器时可能会被用到，因此需要禁用中继日志的自动删除功能。定期清除中继日志需要考虑到复制延时的问题。在ext3的文件系统下，删除大的文件需要一定的时间，会导致严重的复制延时。为了避免复制延时，需要暂时为中继日志创建硬链接，因为在linux系统中通过硬链接删除大文件速度会很快。（在mysql数据库中，删除大表时，通常也采用建立硬链接的方式）

MHA节点中包含了pure_relay_logs命令工具，它可以为中继日志创建硬链接，执行`SET GLOBAL relay_log_purge=1`,等待几秒钟以便SQL线程切换到新的中继日志，再执行`SET GLOBAL relay_log_purge=0`。
```
--user mysql                      用户名
--password mysql                  密码
--port                            端口号
--workdir                         指定创建relay log的硬链接的位置，默认是/var/tmp，由于系统不同分区创建硬链接文件会失败，故需要执行硬链接具体位置，成功执行脚本后，硬链接的中继日志文件被删除
--disable_relay_log_purge         默认情况下，如果relay_log_purge=1，脚本会什么都不清理，自动退出，通过设定这个参数，当relay_log_purge=1的情况下会将relay_log_purge设置为0。清理relay log之后，最后将参数设置为OFF。
```

3.设置定期清理relay脚本（两台slave服务器）
```
[root@192.168.0.60 ~]# cat purge_relay_log.sh 
#!/bin/bash
user=root
passwd=123456
port=3306
log_dir='/data/masterha/log'
work_dir='/data'
purge='/usr/local/bin/purge_relay_logs'

if [ ! -d $log_dir ]
then
   mkdir $log_dir -p
fi

$purge --user=$user --password=$passwd --disable_relay_log_purge --port=$port --workdir=$work_dir >> $log_dir/purge_relay_logs.log 2>&1
[root@192.168.0.60 ~]# 
```

4.添加到crontab
`0 4 * * * /bin/bash /root/purge_relay_log.sh`
purge_relay_logs脚本删除中继日志不会阻塞SQL线程。下面我们手动执行看看什么情况。
```
[root@192.168.0.60 ~]# purge_relay_logs --user=root --password=123456 --port=3306 -disable_relay_log_purge --workdir=/data/
2014-04-20 15:47:24: purge_relay_logs script started.
 Found relay_log.info: /data/mysql/relay-log.info
 Removing hard linked relay log files server03-relay-bin* under /data/.. done.
 Current relay log file: /data/mysql/server03-relay-bin.000002
 Archiving unused relay log files (up to /data/mysql/server03-relay-bin.000001) ...
 Creating hard link for /data/mysql/server03-relay-bin.000001 under /data//server03-relay-bin.000001 .. ok.
 Creating hard links for unused relay log files completed.
 Executing SET GLOBAL relay_log_purge=1; FLUSH LOGS; sleeping a few seconds so that SQL thread can delete older relay log files (if it keeps up); SET GLOBAL relay_log_purge=0; .. ok.
 Removing hard linked relay log files server03-relay-bin* under /data/.. done.
2014-04-20 15:47:27: All relay log purging operations succeeded.
[root@192.168.0.60 ~]# 
```

pure_relay_logs脚本参数如下所示：

### 7.8 测试ssh与主从同步的测试  
1.测试各个节点的ssh登录
```
 masterha_check_ssh --conf=/etc/masterha/app1.cnf

```
2.测试各个节点的主从设置
```
[root@192.168.0.20 ~]# masterha_check_repl --conf=/etc/masterha/app1.cnf
```

发现最后的结论说我的复制不是ok的。但是上面的信息明明说是正常的，自己也进数据库查看了。这里一直踩坑。一直纠结，后来无意中发现火丁笔记的博客，这才知道了原因，原来Failover两种方式：一种是虚拟IP地址，一种是全局配置文件。MHA并没有限定使用哪一种方式，而是让用户自己选择，虚拟IP地址的方式会牵扯到其它的软件,比如keepalive软件，而且还要修改脚本master_ip_failover。(最后修改脚本后才没有这个报.)

如果发现如下错误：
```
Can't exec "mysqlbinlog": No such file or directory at /usr/local/share/perl5/MHA/BinlogManager.pm line 99.
mysqlbinlog version not found!
Testing mysql connection and privileges..sh: mysql: command not found
```
解决方法如下，添加软连接（所有节点）
```
ln -s /usr/local/mysql/bin/mysqlbinlog /usr/local/bin/mysqlbinlog
ln -s /usr/local/mysql/bin/mysql /usr/local/bin/mysql
```
所以先暂时注释`master_ip_failover_script= /usr/local/bin/master_ip_failover`这个选项。后面引入keepalived后和修改该脚本以后再开启该选项。
```
[root@192.168.0.20 ~]# grep master_ip_failover /etc/masterha/app1.cnf
#master_ip_failover_script= /usr/local/bin/master_ip_failover
[root@192.168.0.20 ~]# 
```

8.检查MHA Manager的状态
```
[root@192.168.0.20 ~]# masterha_check_status --conf=/etc/masterha/app1.cnf
app1 is stopped(2:NOT_RUNNING).
```
注意：如果正常，会显示"PING_OK"，否则会显示"NOT_RUNNING"，这代表MHA监控没有开启。
### 7.9 测试启动MHA Manager
1.启动
```
[root@192.168.0.20 ~]# nohup masterha_manager --conf=/etc/masterha/app1.cnf --remove_dead_master_conf --ignore_last_failover < /dev/null > /var/log/masterha/app1/manager.log 2>&1 &  
[1] 30867
[root@192.168.0.20 ~]# 
```
__启动参数介绍：__
`--remove_dead_master_conf`      该参数代表当发生主从切换后，老的主库的ip将会从配置文件中移除。

`--manger_log`                            日志存放位置

`--ignore_last_failover`                 在缺省情况下，如果MHA检测到连续发生宕机，且两次宕机间隔不足8小时的话，则不会进行Failover，之所以这样限制是为了避免ping-pong效应。该参数代表忽略上次MHA触发切换产生的文件，默认情况下，MHA发生切换后会在日志目录，也就是上面我设置的/data产生app1.failover.complete文件，下次再次切换的时候如果发现该目录下存在该文件将不允许触发切换，除非在第一次切换后收到删除该文件，为了方便，这里设置为--ignore_last_failover。

2.查看MHA Manager监控是否正常：
```
[root@192.168.0.20 ~]# masterha_check_status --conf=/etc/masterha/app1.cnf
app1 (pid:20386) is running(0:PING_OK), master:192.168.0.50
[root@192.168.0.20 ~]# 
```

3.查看启动日志
```
[root@192.168.0.20 ~]# tail -n20 /var/log/masterha/app1/manager.log
Sun Apr 20 19:12:01 2014 - [info]   Connecting to root@192.168.0.70(192.168.0.70:22).. 
  Checking slave recovery environment settings..
    Opening /data/mysql/relay-log.info ... ok.
    Relay log found at /data/mysql, up to server04-relay-bin.000002
    Temporary relay log file is /data/mysql/server04-relay-bin.000002
    Testing mysql connection and privileges.. done.
    Testing mysqlbinlog output.. done.
    Cleaning up test file(s).. done.
Sun Apr 20 19:12:01 2014 - [info] Slaves settings check done.
Sun Apr 20 19:12:01 2014 - [info] 
192.168.0.50 (current master)
 +--192.168.0.60
 +--192.168.0.70

Sun Apr 20 19:12:01 2014 - [warning] master_ip_failover_script is not defined.
Sun Apr 20 19:12:01 2014 - [warning] shutdown_script is not defined.
Sun Apr 20 19:12:01 2014 - [info] Set master ping interval 1 seconds.
Sun Apr 20 19:12:01 2014 - [info] Set secondary check script: /usr/local/bin/masterha_secondary_check -s server03 -s server02 --user=root --master_host=server02 --master_ip=192.168.0.50 --master_port=3306
Sun Apr 20 19:12:01 2014 - [info] Starting ping health check on 192.168.0.50(192.168.0.50:3306)..
Sun Apr 20 19:12:01 2014 - [info] Ping(SELECT) succeeded, waiting until MySQL doesn't respond..
[root@192.168.0.20 ~]# 
```
其中"Ping(SELECT) succeeded, waiting until MySQL doesn't respond.."说明整个系统已经开始监控了。

4..关闭MHA Manage监控

关闭很简单，使用masterha_stop命令完成。
```
[root@192.168.0.20 ~]# masterha_stop --conf=/etc/masterha/app1.cnf
Stopped app1 successfully.
[1]+  Exit 1                  nohup masterha_manager --conf=/etc/masterha/app1.cnf --remove_dead_master_conf --ignore_last_failover --manager_log=/data/mamanager.log
[root@192.168.0.20 ~]# 
```
### 7.10 在线切换主库
手动failover，这种场景意味着在业务上没有启用MHA自动切换功能，当主服务器故障时，人工手动调用MHA来进行故障切换操作，具体命令如下：

注意：如果，MHA manager检测到没有dead的server，将报错，并结束failover： 
```
Mon Apr 21 21:23:33 2014 - [info] Dead Servers:
Mon Apr 21 21:23:33 2014 - [error][/usr/local/share/perl5/MHA/MasterFailover.pm, ln181] None of server is dead. Stop failover.
Mon Apr 21 21:23:33 2014 - [error][/usr/local/share/perl5/MHA/ManagerUtil.pm, ln178] Got ERROR:  at /usr/local/bin/masterha_master_switch line 53
```
进行手动切换命令如下：
```
[root@192.168.0.20 ~]# masterha_master_switch --master_state=dead --conf=/etc/masterha/app1.cnf --dead_master_host=192.168.0.50 --dead_master_port=3306 --new_master_host=192.168.0.60 --new_master_port=3306 --ignore_last_failover
```
输出的信息会询问你是否进行切换


#### 在线进行切换

在许多情况下， 需要将现有的主服务器迁移到另外一台服务器上。 比如主服务器硬件故障，RAID 控制卡需要重建，将主服务器移到性能更好的服务器上等等。维护主服务器引起性能下降， 导致停机时间至少无法写入数据。 另外， 阻塞或杀掉当前运行的会话会导致主主之间数据不一致的问题发生。 MHA 提供快速切换和优雅的阻塞写入，这个切换过程只需要 0.5-2s 的时间，这段时间内数据是无法写入的。在很多情况下，0.5-2s 的阻塞写入是可以接受的。因此切换主服务器不需要计划分配维护时间窗口。

MHA在线切换的大概过程：
1.检测复制设置和确定当前主服务器
2.确定新的主服务器
3.阻塞写入到当前主服务器
4.等待所有从服务器赶上复制
5.授予写入到新的主服务器
6.重新设置从服务器 

注意，在线切换的时候应用架构需要考虑以下两个问题：
> 
1.自动识别master和slave的问题（master的机器可能会切换），如果采用了vip的方式，基本可以解决这个问题。
2.负载均衡的问题（可以定义大概的读写比例，每台机器可承担的负载比例，当有机器离开集群时，需要考虑这个问题）

为了保证数据完全一致性，在最快的时间内完成切换，MHA的在线切换必须满足以下条件才会切换成功，否则会切换失败。
>
1.所有slave的IO线程都在运行
2.所有slave的SQL线程都在运行
3.所有的show slave status的输出中Seconds_Behind_Master参数小于或者等于running_updates_limit秒，如果在切换过程中不指定running_updates_limit,那么默认情况下running_updates_limit为1秒。
4.在master端，通过show processlist输出，没有一个更新花费的时间大于running_updates_limit秒。

__在线切换步骤如下：__

__首先，停掉MHA监控__：

    [root@192.168.0.20 ~]# masterha_stop --conf=/etc/masterha/app1.cnf

__其次，进行在线切换操作__（模拟在线切换主库操作，原主库192.168.0.50变为slave，192.168.0.60提升为新的主库）
```
[root@192.168.0.20 ~]# masterha_master_switch --conf=/etc/masterha/app1.cnf --master_state=alive --new_master_host=192.168.0.60 --new_master_port=3306 --orig_master_is_new_slave --running_updates_limit=10000
```
最后查看日志，了解切换过程，输出信息如下：
略

__其中参数的意思__：

`--orig_master_is_new_slave` 切换时加上此参数是将原 master 变为 slave 节点，如果不加此参数，原来的 master 将不启动

`--running_updates_limit=10000`,故障切换时,候选master 如果有延迟的话， mha 切换不能成功，加上此参数表示延迟在此时间范围内都可切换（单位为s），但是切换的时间长短是由recover 时relay 日志的大小决定 

__注意__：
>由于在线进行切换需要调用到master_ip_online_change这个脚本，但是由于该脚本不完整，需要自己进行相应的修改，我google到后发现还是有问题，脚本中new_master_password这个变量获取不到，导致在线切换失败，所以进行了相关的硬编码，直接把mysql的root用户密码赋值给变量new_master_password，如果有哪位大牛知道原因，请指点指点。这个脚本还可以管理vip。下面贴出脚本：

```perl
#!/usr/bin/env perl

#  Copyright (C) 2011 DeNA Co.,Ltd.
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#  Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

## Note: This is a sample script and is not complete. Modify the script based on your environment.

use strict;
use warnings FATAL => 'all';

use Getopt::Long;
use MHA::DBHelper;
use MHA::NodeUtil;
use Time::HiRes qw( sleep gettimeofday tv_interval );
use Data::Dumper;

my $_tstart;
my $_running_interval = 0.1;
my (
  $command,          $orig_master_host, $orig_master_ip,
  $orig_master_port, $orig_master_user, 
  $new_master_host,  $new_master_ip,    $new_master_port,
  $new_master_user,  
);


my $vip = '192.168.0.88/24';  # Virtual IP 
my $key = "1"; 
my $ssh_start_vip = "/sbin/ifconfig eth1:$key $vip";
my $ssh_stop_vip = "/sbin/ifconfig eth1:$key down";
my $ssh_user = "root";
my $new_master_password='123456';
my $orig_master_password='123456';
GetOptions(
  'command=s'              => \$command,
  #'ssh_user=s'             => \$ssh_user,  
  'orig_master_host=s'     => \$orig_master_host,
  'orig_master_ip=s'       => \$orig_master_ip,
  'orig_master_port=i'     => \$orig_master_port,
  'orig_master_user=s'     => \$orig_master_user,
  #'orig_master_password=s' => \$orig_master_password,
  'new_master_host=s'      => \$new_master_host,
  'new_master_ip=s'        => \$new_master_ip,
  'new_master_port=i'      => \$new_master_port,
  'new_master_user=s'      => \$new_master_user,
  #'new_master_password=s'  => \$new_master_password,
);

exit &main();

sub current_time_us {
  my ( $sec, $microsec ) = gettimeofday();
  my $curdate = localtime($sec);
  return $curdate . " " . sprintf( "%06d", $microsec );
}

sub sleep_until {
  my $elapsed = tv_interval($_tstart);
  if ( $_running_interval > $elapsed ) {
    sleep( $_running_interval - $elapsed );
  }
}

sub get_threads_util {
  my $dbh                    = shift;
  my $my_connection_id       = shift;
  my $running_time_threshold = shift;
  my $type                   = shift;
  $running_time_threshold = 0 unless ($running_time_threshold);
  $type                   = 0 unless ($type);
  my @threads;

  my $sth = $dbh->prepare("SHOW PROCESSLIST");
  $sth->execute();

  while ( my $ref = $sth->fetchrow_hashref() ) {
    my $id         = $ref->{Id};
    my $user       = $ref->{User};
    my $host       = $ref->{Host};
    my $command    = $ref->{Command};
    my $state      = $ref->{State};
    my $query_time = $ref->{Time};
    my $info       = $ref->{Info};
    $info =~ s/^\s*(.*?)\s*$/$1/ if defined($info);
    next if ( $my_connection_id == $id );
    next if ( defined($query_time) && $query_time < $running_time_threshold );
    next if ( defined($command)    && $command eq "Binlog Dump" );
    next if ( defined($user)       && $user eq "system user" );
    next
      if ( defined($command)
      && $command eq "Sleep"
      && defined($query_time)
      && $query_time >= 1 );

    if ( $type >= 1 ) {
      next if ( defined($command) && $command eq "Sleep" );
      next if ( defined($command) && $command eq "Connect" );
    }

    if ( $type >= 2 ) {
      next if ( defined($info) && $info =~ m/^select/i );
      next if ( defined($info) && $info =~ m/^show/i );
    }

    push @threads, $ref;
  }
  return @threads;
}

sub main {
  if ( $command eq "stop" ) {
    ## Gracefully killing connections on the current master
    # 1. Set read_only= 1 on the new master
    # 2. DROP USER so that no app user can establish new connections
    # 3. Set read_only= 1 on the current master
    # 4. Kill current queries
    # * Any database access failure will result in script die.
    my $exit_code = 1;
    eval {
      ## Setting read_only=1 on the new master (to avoid accident)
      my $new_master_handler = new MHA::DBHelper();

      # args: hostname, port, user, password, raise_error(die_on_error)_or_not
      $new_master_handler->connect( $new_master_ip, $new_master_port,
        $new_master_user, $new_master_password, 1 );
      print current_time_us() . " Set read_only on the new master.. ";
      $new_master_handler->enable_read_only();
      if ( $new_master_handler->is_read_only() ) {
        print "ok.\n";
      }
      else {
        die "Failed!\n";
      }
      $new_master_handler->disconnect();

      # Connecting to the orig master, die if any database error happens
      my $orig_master_handler = new MHA::DBHelper();
      $orig_master_handler->connect( $orig_master_ip, $orig_master_port,
        $orig_master_user, $orig_master_password, 1 );

      ## Drop application user so that nobody can connect. Disabling per-session binlog beforehand
      #$orig_master_handler->disable_log_bin_local();
      #print current_time_us() . " Drpping app user on the orig master..\n";
      #FIXME_xxx_drop_app_user($orig_master_handler);

      ## Waiting for N * 100 milliseconds so that current connections can exit
      my $time_until_read_only = 15;
      $_tstart = [gettimeofday];
      my @threads = get_threads_util( $orig_master_handler->{dbh},
        $orig_master_handler->{connection_id} );
      while ( $time_until_read_only > 0 && $#threads >= 0 ) {
        if ( $time_until_read_only % 5 == 0 ) {
          printf
"%s Waiting all running %d threads are disconnected.. (max %d milliseconds)\n",
            current_time_us(), $#threads + 1, $time_until_read_only * 100;
          if ( $#threads < 5 ) {
            print Data::Dumper->new( [$_] )->Indent(0)->Terse(1)->Dump . "\n"
              foreach (@threads);
          }
        }
        sleep_until();
        $_tstart = [gettimeofday];
        $time_until_read_only--;
        @threads = get_threads_util( $orig_master_handler->{dbh},
          $orig_master_handler->{connection_id} );
      }

      ## Setting read_only=1 on the current master so that nobody(except SUPER) can write
      print current_time_us() . " Set read_only=1 on the orig master.. ";
      $orig_master_handler->enable_read_only();
      if ( $orig_master_handler->is_read_only() ) {
        print "ok.\n";
      }
      else {
        die "Failed!\n";
      }

      ## Waiting for M * 100 milliseconds so that current update queries can complete
      my $time_until_kill_threads = 5;
      @threads = get_threads_util( $orig_master_handler->{dbh},
        $orig_master_handler->{connection_id} );
      while ( $time_until_kill_threads > 0 && $#threads >= 0 ) {
        if ( $time_until_kill_threads % 5 == 0 ) {
          printf
"%s Waiting all running %d queries are disconnected.. (max %d milliseconds)\n",
            current_time_us(), $#threads + 1, $time_until_kill_threads * 100;
          if ( $#threads < 5 ) {
            print Data::Dumper->new( [$_] )->Indent(0)->Terse(1)->Dump . "\n"
              foreach (@threads);
          }
        }
        sleep_until();
        $_tstart = [gettimeofday];
        $time_until_kill_threads--;
        @threads = get_threads_util( $orig_master_handler->{dbh},
          $orig_master_handler->{connection_id} );
      }



                print "Disabling the VIP on old master: $orig_master_host \n";
                &stop_vip();     


      ## Terminating all threads
      print current_time_us() . " Killing all application threads..\n";
      $orig_master_handler->kill_threads(@threads) if ( $#threads >= 0 );
      print current_time_us() . " done.\n";
      #$orig_master_handler->enable_log_bin_local();
      $orig_master_handler->disconnect();

      ## After finishing the script, MHA executes FLUSH TABLES WITH READ LOCK
      $exit_code = 0;
    };
    if ($@) {
      warn "Got Error: $@\n";
      exit $exit_code;
    }
    exit $exit_code;
  }
  elsif ( $command eq "start" ) {
    ## Activating master ip on the new master
    # 1. Create app user with write privileges
    # 2. Moving backup script if needed
    # 3. Register new master's ip to the catalog database

# We don't return error even though activating updatable accounts/ip failed so that we don't interrupt slaves' recovery.
# If exit code is 0 or 10, MHA does not abort
    my $exit_code = 10;
    eval {
      my $new_master_handler = new MHA::DBHelper();

      # args: hostname, port, user, password, raise_error_or_not
      $new_master_handler->connect( $new_master_ip, $new_master_port,
        $new_master_user, $new_master_password, 1 );

      ## Set read_only=0 on the new master
      #$new_master_handler->disable_log_bin_local();
      print current_time_us() . " Set read_only=0 on the new master.\n";
      $new_master_handler->disable_read_only();

      ## Creating an app user on the new master
      #print current_time_us() . " Creating app user on the new master..\n";
      #FIXME_xxx_create_app_user($new_master_handler);
      #$new_master_handler->enable_log_bin_local();
      $new_master_handler->disconnect();

      ## Update master ip on the catalog database, etc
                print "Enabling the VIP - $vip on the new master - $new_master_host \n";
                &start_vip();
                $exit_code = 0;
    };
    if ($@) {
      warn "Got Error: $@\n";
      exit $exit_code;
    }
    exit $exit_code;
  }
  elsif ( $command eq "status" ) {

    # do nothing
    exit 0;
  }
  else {
    &usage();
    exit 1;
  }
}

# A simple system call that enable the VIP on the new master 
sub start_vip() {
    `ssh $ssh_user\@$new_master_host \" $ssh_start_vip \"`;
}
# A simple system call that disable the VIP on the old_master
sub stop_vip() {
    `ssh $ssh_user\@$orig_master_host \" $ssh_stop_vip \"`;
}

sub usage {
  print
"Usage: master_ip_online_change --command=start|stop|status --orig_master_host=host --orig_master_ip=ip --orig_master_port=port --new_master_host=host --new_master_ip=ip --new_master_port=port\n";
  die;
}
```


### 7.11 切换脚本

### 7.12 高可用实现

#### 7.12.1 使用高可用软件(keepalived, heartbeat, Pacemaker+corosync)
* 1.keepalived的安装(server02, server03)
```
yum install keepalived
```

* 2.配合keepalived(在master上)
```
! Configuration File for keepalived

global_defs {
     notification_email {
     zzzz@163.com
   }
   notification_email_from dba@dbserver.com
   smtp_server 127.0.0.1
   smtp_connect_timeout 30
   router_id MySQL-HA
}

vrrp_instance VI_1 {
    state BACKUP
    interface eth1
    virtual_router_id 51
    priority 150
    advert_int 1
    nopreempt

    authentication {
    auth_type PASS
    auth_pass 1111
    }

    virtual_ipaddress {
        192.168.0.88
    }
}

```

其中`router_id` MySQL HA表示设定keepalived组的名称，将192.168.0.88这个虚拟ip绑定到该主机的eth1网卡上，并且设置了状态为backup模式，将keepalived的模式设置为非抢占模式（nopreempt），priority 150表示设置的优先级为150。下面的配置略有不同，但是都是一个意思。
在候选master上配置（192.168.0.60）
```
! Configuration File for keepalived

global_defs {
     notification_email {
     saltstack@163.com
   }
   notification_email_from dba@dbserver.com
   smtp_server 127.0.0.1
   smtp_connect_timeout 30
   router_id MySQL-HA
}

vrrp_instance VI_1 {
    state BACKUP
    interface eth1
    virtual_router_id 51
    priority 120
    advert_int 1
    nopreempt

    authentication {
    auth_type PASS
    auth_pass 1111
    }

    virtual_ipaddress {
        192.168.0.88
    }
}
```

* 3.启动keepalived服务，在master上启动并查看日志
```
[root@192.168.0.50 ~]# /etc/init.d/keepalived start
Starting keepalived:                                       [  OK  ]
[root@192.168.0.50 ~]# tail -f /var/log/messages
Apr 20 20:22:16 192 Keepalived_healthcheckers[15334]: Opening file '/etc/keepalived/keepalived.conf'.
Apr 20 20:22:16 192 Keepalived_healthcheckers[15334]: Configuration is using : 7231 Bytes
Apr 20 20:22:16 192 kernel: IPVS: Connection hash table configured (size=4096, memory=64Kbytes)
Apr 20 20:22:16 192 kernel: IPVS: ipvs loaded.
Apr 20 20:22:16 192 Keepalived_healthcheckers[15334]: Using LinkWatch kernel netlink reflector...
Apr 20 20:22:19 192 Keepalived_vrrp[15335]: VRRP_Instance(VI_1) Transition to MASTER STATE
Apr 20 20:22:20 192 Keepalived_vrrp[15335]: VRRP_Instance(VI_1) Entering MASTER STATE
Apr 20 20:22:20 192 Keepalived_vrrp[15335]: VRRP_Instance(VI_1) setting protocol VIPs.
Apr 20 20:22:20 192 Keepalived_vrrp[15335]: VRRP_Instance(VI_1) Sending gratuitous ARPs on eth1 for 192.168.0.88
Apr 20 20:22:20 192 Keepalived_healthcheckers[15334]: Netlink reflector reports IP 192.168.0.88 added
Apr 20 20:22:25 192 Keepalived_vrrp[15335]: VRRP_Instance(VI_1) Sending gratuitous ARPs on eth1 for 192.168.0.88
```

发现已经将虚拟ip 192.168.0.88绑定了网卡eth1上。

* 4.查看vip的绑定
```
[root@192.168.0.50 ~]# ip addr | grep eth1
3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    inet 192.168.0.50/24 brd 192.168.0.255 scope global eth1
    inet 192.168.0.88/32 scope global eth1
[root@192.168.0.50 ~]# 
```
在另外一台服务器，候选master上启动keepalived服务，并观察
```
[root@192.168.0.60 ~]# /etc/init.d/keepalived start ; tail -f /var/log/messages
Starting keepalived:                                       [  OK  ]
Apr 20 20:26:18 192 Keepalived_vrrp[9472]: Registering gratuitous ARP shared channel
Apr 20 20:26:18 192 Keepalived_vrrp[9472]: Opening file '/etc/keepalived/keepalived.conf'.
Apr 20 20:26:18 192 Keepalived_vrrp[9472]: Configuration is using : 62976 Bytes
Apr 20 20:26:18 192 Keepalived_vrrp[9472]: Using LinkWatch kernel netlink reflector...
Apr 20 20:26:18 192 Keepalived_vrrp[9472]: VRRP_Instance(VI_1) Entering BACKUP STATE
Apr 20 20:26:18 192 Keepalived_vrrp[9472]: VRRP sockpool: [ifindex(3), proto(112), unicast(0), fd(10,11)]
Apr 20 20:26:18 192 Keepalived_healthcheckers[9471]: Netlink reflector reports IP 192.168.80.138 added
Apr 20 20:26:18 192 Keepalived_healthcheckers[9471]: Netlink reflector reports IP 192.168.0.60 added
Apr 20 20:26:18 192 Keepalived_healthcheckers[9471]: Netlink reflector reports IP fe80::20c:29ff:fe9d:6a9e added
Apr 20 20:26:18 192 Keepalived_healthcheckers[9471]: Netlink reflector reports IP fe80::20c:29ff:fe9d:6aa8 added
Apr 20 20:26:18 192 Keepalived_healthcheckers[9471]: Registering Kernel netlink reflector
Apr 20 20:26:18 192 Keepalived_healthcheckers[9471]: Registering Kernel netlink command channel
Apr 20 20:26:18 192 Keepalived_healthcheckers[9471]: Opening file '/etc/keepalived/keepalived.conf'.
Apr 20 20:26:18 192 Keepalived_healthcheckers[9471]: Configuration is using : 7231 Bytes
Apr 20 20:26:18 192 kernel: IPVS: Registered protocols (TCP, UDP, AH, ESP)
Apr 20 20:26:18 192 kernel: IPVS: Connection hash table configured (size=4096, memory=64Kbytes)
Apr 20 20:26:18 192 kernel: IPVS: ipvs loaded.
Apr 20 20:26:18 192 Keepalived_healthcheckers[9471]: Using LinkWatch kernel netlink reflector...
```
从上面的信息可以看到keepalived已经配置成功。
__注意:__

> 上面两台服务器的keepalived都设置为了BACKUP模式，在keepalived中2种模式，分别是master->backup模式和backup->backup模式。这两种模式有很大区别。在master->backup模式下，一旦主库宕机，虚拟ip会自动漂移到从库，当主库修复后，keepalived启动后，还会把虚拟ip抢占过来，即使设置了非抢占模式（nopreempt）抢占ip的动作也会发生。在backup->backup模式下，当主库宕机后虚拟ip会自动漂移到从库上，当原主库恢复和keepalived服务启动后，并不会抢占新主的虚拟ip，即使是优先级高于从库的优先级别，也不会发生抢占。为了减少ip漂移次数，通常是把修复好的主库当做新的备库。

* 5.MHA引入keepalived（MySQL服务进程挂掉时通过MHA 停止keepalived）:
要想把keepalived服务引入MHA，我们只需要修改切换是触发的脚本文件master_ip_failover即可，在该脚本中添加在master发生宕机时对keepalived的处理。

编辑脚本`/usr/local/bin/master_ip_failover`，修改后如下，我对perl不熟悉，所以我这里完整贴出该脚本（主库上操作，192.168.0.50）。

```perl
#!/usr/bin/env perl

use strict;
use warnings FATAL => 'all';

use Getopt::Long;

my (
    $command,          $ssh_user,        $orig_master_host, $orig_master_ip,
    $orig_master_port, $new_master_host, $new_master_ip,    $new_master_port
);

my $vip = '192.168.0.88';
my $ssh_start_vip = "/etc/init.d/keepalived start";
my $ssh_stop_vip = "/etc/init.d/keepalived stop";

GetOptions(
    'command=s'          => \$command,
    'ssh_user=s'         => \$ssh_user,
    'orig_master_host=s' => \$orig_master_host,
    'orig_master_ip=s'   => \$orig_master_ip,
    'orig_master_port=i' => \$orig_master_port,
    'new_master_host=s'  => \$new_master_host,
    'new_master_ip=s'    => \$new_master_ip,
    'new_master_port=i'  => \$new_master_port,
);

exit &main();

sub main {

    print "\n\nIN SCRIPT TEST====$ssh_stop_vip==$ssh_start_vip===\n\n";

    if ( $command eq "stop" || $command eq "stopssh" ) {

        my $exit_code = 1;
        eval {
            print "Disabling the VIP on old master: $orig_master_host \n";
            &stop_vip();
            $exit_code = 0;
        };
        if ($@) {
            warn "Got Error: $@\n";
            exit $exit_code;
        }
        exit $exit_code;
    }
    elsif ( $command eq "start" ) {

        my $exit_code = 10;
        eval {
            print "Enabling the VIP - $vip on the new master - $new_master_host \n";
            &start_vip();
            $exit_code = 0;
        };
        if ($@) {
            warn $@;
            exit $exit_code;
        }
        exit $exit_code;
    }
    elsif ( $command eq "status" ) {
        print "Checking the Status of the script.. OK \n";
        #`ssh $ssh_user\@cluster1 \" $ssh_start_vip \"`;
        exit 0;
    }
    else {
        &usage();
        exit 1;
    }
}

# A simple system call that enable the VIP on the new master
sub start_vip() {
    `ssh $ssh_user\@$new_master_host \" $ssh_start_vip \"`;
}
# A simple system call that disable the VIP on the old_master
sub stop_vip() {
     return 0  unless  ($ssh_user);
    `ssh $ssh_user\@$orig_master_host \" $ssh_stop_vip \"`;
}

sub usage {
    print
    "Usage: master_ip_failover --command=start|stop|stopssh|status --orig_master_host=host --orig_master_ip=ip --orig_master_port=port --new_master_host=host --new_master_ip=ip --new_master_port=port\n";
}
```

现在已经修改这个脚本了，我们现在打开在上面提到过的参数，再检查集群状态，看是否会报错。
```
[root@192.168.0.20 ~]# grep 'master_ip_failover_script' /etc/masterha/app1.cnf
master_ip_failover_script= /usr/local/bin/master_ip_failover
[root@192.168.0.20 ~]# 
```

```
[root@192.168.0.20 ~]# masterha_check_repl --conf=/etc/masterha/app1.cnf  
Sun Apr 20 23:10:01 2014 - [info] Slaves settings check done.
Sun Apr 20 23:10:01 2014 - [info] 
192.168.0.50 (current master)
 +--192.168.0.60
 +--192.168.0.70

Sun Apr 20 23:10:01 2014 - [info] Checking replication health on 192.168.0.60..
Sun Apr 20 23:10:01 2014 - [info]  ok.
Sun Apr 20 23:10:01 2014 - [info] Checking replication health on 192.168.0.70..
Sun Apr 20 23:10:01 2014 - [info]  ok.
Sun Apr 20 23:10:01 2014 - [info] Checking master_ip_failover_script status:
Sun Apr 20 23:10:01 2014 - [info]   /usr/local/bin/master_ip_failover --command=status --ssh_user=root --orig_master_host=192.168.0.50 --orig_master_ip=192.168.0.50 --orig_master_port=3306 
Sun Apr 20 23:10:01 2014 - [info]  OK.
Sun Apr 20 23:10:01 2014 - [warning] shutdown_script is not defined.
Sun Apr 20 23:10:01 2014 - [info] Got exit code 0 (Not master dead).

MySQL Replication Health is OK.
```

`/usr/local/bin/master_ip_failover`添加或者修改的内容意思是当主库数据库发生故障时，会触发MHA切换，MHA Manager会停掉主库上的keepalived服务，触发虚拟ip漂移到备选从库，从而完成切换。当然可以在keepalived里面引入脚本，这个脚本监控mysql是否正常运行，如果不正常，则调用该脚本杀掉keepalived进程。



#### 7.12.4 通过脚本实现
通过脚本的方式管理VIP。这里是修改`/usr/local/bin/master_ip_failover`，也可以使用其他的语言完成，比如php语言。使用php脚本编写的failover这里就不介绍了。修改完成后内容如下，而且如果使用脚本管理vip的话，需要手动在master服务器上绑定一个vip.

` /sbin/ifconfig eth1:1 192.168.0.88/24` 
最好使用做一下arp广播
```perl
#!/usr/bin/env perl

use strict;
use warnings FATAL => 'all';

use Getopt::Long;

my (
    $command,          $ssh_user,        $orig_master_host, $orig_master_ip,
    $orig_master_port, $new_master_host, $new_master_ip,    $new_master_port
);

my $vip = '192.168.0.88/24';
my $key = '1';
my $ssh_start_vip = "/sbin/ifconfig eth1:$key $vip";
my $ssh_stop_vip = "/sbin/ifconfig eth1:$key down";

GetOptions(
    'command=s'          => \$command,
    'ssh_user=s'         => \$ssh_user,
    'orig_master_host=s' => \$orig_master_host,
    'orig_master_ip=s'   => \$orig_master_ip,
    'orig_master_port=i' => \$orig_master_port,
    'new_master_host=s'  => \$new_master_host,
    'new_master_ip=s'    => \$new_master_ip,
    'new_master_port=i'  => \$new_master_port,
);

exit &main();

sub main {

    print "\n\nIN SCRIPT TEST====$ssh_stop_vip==$ssh_start_vip===\n\n";

    if ( $command eq "stop" || $command eq "stopssh" ) {

        my $exit_code = 1;
        eval {
            print "Disabling the VIP on old master: $orig_master_host \n";
            &stop_vip();
            $exit_code = 0;
        };
        if ($@) {
            warn "Got Error: $@\n";
            exit $exit_code;
        }
        exit $exit_code;
    }
    elsif ( $command eq "start" ) {

        my $exit_code = 10;
        eval {
            print "Enabling the VIP - $vip on the new master - $new_master_host \n";
            &start_vip();
            $exit_code = 0;
        };
        if ($@) {
            warn $@;
            exit $exit_code;
        }
        exit $exit_code;
    }
    elsif ( $command eq "status" ) {
        print "Checking the Status of the script.. OK \n";
        exit 0;
    }
    else {
        &usage();
        exit 1;
    }
}

sub start_vip() {
    `ssh $ssh_user\@$new_master_host \" $ssh_start_vip \"`;
}
sub stop_vip() {
     return 0  unless  ($ssh_user);
    `ssh $ssh_user\@$orig_master_host \" $ssh_stop_vip \"`;
}

sub usage {
    print
    "Usage: master_ip_failover --command=start|stop|stopssh|status --orig_master_host=host --orig_master_ip=ip --orig_master_port=port --new_master_host=host --new_master_ip=ip --new_master_port=port\n";
}
```


为了防止脑裂发生，推荐生产环境采用脚本的方式来管理虚拟ip，而不是使用keepalived来完成。到此为止，基本MHA集群已经配置完毕。接下来就是实际的测试环节了。通过一些测试来看一下MHA到底是如何进行工作的。下面将从MHA自动failover，我们手动failover，在线切换三种方式来介绍MHA的工作情况。

### 7.13 在线自动切换测试
* 1.自动Failover（必须先启动MHA Manager，否则无法自动切换，当然手动切换不需要开启MHA Manager监控。各位童鞋请参考前面启动MHA Manager）

__自动failover模拟测试的操作步骤如下。__
- 1）使用sysbench生成测试数据（使用yum快速安装）
` yum install sysbench -y`
在主库（192.168.0.50）上进行sysbench数据生成，在sbtest库下生成sbtest表，共100W记录。
```
[root@192.168.0.50 ~]# sysbench --test=oltp --oltp-table-size=1000000 --oltp-read-only=off --init-rng=on --num-threads=16 --max-requests=0 --oltp-dist-type=uniform --max-time=1800 --mysql-user=root --mysql-socket=/tmp/mysql.sock --mysql-password=123456 --db-driver=mysql --mysql-table-engine=innodb --oltp-test-mode=complex prepare
```
- 2）停掉slave sql线程，模拟主从延时。（192.168.0.60）
```
mysql> stop slave io_thread;
Query OK, 0 rows affected (0.08 sec)

mysql> 
```
另外一台slave我们没有停止io线程，所以还在继续接收日志。

- 3）模拟sysbench压力测试。

在主库上（192.168.0.50）进行压力测试，持续时间为3分钟，产生大量的binlog。

```
[root@192.168.0.50 ~]# sysbench --test=oltp --oltp-table-size=1000000 --oltp-read-only=off --init-rng=on --num-threads=16 --max-requests=0 --oltp-dist-type=uniform --max-time=180 --mysql-user=root --mysql-socket=/tmp/mysql.sock --mysql-password=123456 --db-driver=mysql --mysql-table-engine=innodb --oltp-test-mode=complex run 
sysbench 0.4.12:  multi-threaded system evaluation benchmark

Running the test with following options:
Number of threads: 16
Initializing random number generator from timer.


Doing OLTP test.
Running mixed OLTP test
Using Uniform distribution
Using "BEGIN" for starting transactions
Using auto_inc on the id column
Threads started!
Time limit exceeded, exiting...
(last message repeated 15 times)
Done.

OLTP test statistics:
    queries performed:
        read:                            15092
        write:                           5390
        other:                           2156
        total:                           22638
    transactions:                        1078   (5.92 per sec.)
    deadlocks:                           0      (0.00 per sec.)
    read/write requests:                 20482  (112.56 per sec.)
    other operations:                    2156   (11.85 per sec.)

Test execution summary:
    total time:                          181.9728s
    total number of events:              1078
    total time taken by event execution: 2910.4518
    per-request statistics:
         min:                                934.29ms
         avg:                               2699.86ms
         max:                               7679.95ms
         approx.  95 percentile:            4441.47ms

Threads fairness:
    events (avg/stddev):           67.3750/1.49
    execution time (avg/stddev):   181.9032/0.11
```

- 4）开启slave（192.168.0.60）上的IO线程，追赶落后于master的binlog。
```
mysql> start slave io_thread;     
Query OK, 0 rows affected (0.00 sec)

mysql> 
```
- 5）杀掉主库mysql进程，模拟主库发生故障，进行自动failover操作。

`[root@192.168.0.50 ~]# pkill -9 mysqld`
- 6）查看MHA切换日志，了解整个切换过程，在192.168.0.20上查看日志：

```
[root@192.168.0.20 ~]# cat /var/log/masterha/app1/manager.log 
Mon Apr 21 20:15:45 2014 - [warning] Got error on MySQL select ping: 2006 (MySQL server has gone away)
Mon Apr 21 20:15:45 2014 - [info] Executing seconary network check script: /usr/local/bin/masterha_secondary_check -s server03 -s server02 --user=root --master_host=server02 --master_ip=192.168.0.50 --master_  Creating /tmp if not exists..    ok.
  Checking output directory is accessible or not..
   ok.
  Binlog found at /data/mysql, up to mysql-bin.000018
Mon Apr 21 20:15:48 2014 - [warning] Global configuration file /etc/masterha_default.cnf not found. Skipping.
Mon Apr 21 20:15:48 2014 - [info] Reading application default configurations from /etc/masterha/app1.cnf..
Mon Apr 21 20:15:48 2014 - [info] Reading server configurations from /etc/masterha/app1.cnf..
ble from server03. OK.
Monitoring server server02 is reachable, Master is not reachable from server02. OK.
Mon Apr 21 20:15:46 2014 - [info] Master is not reachable from all other monitoring servers. Failover should start.
Mon Apr 21 20:15:46 2014 - [warning] Got error on MySQL connect: 2013 (Lost connection to MySQL server at 'reading initial communication packet', system error: 111)
Mon Apr 21 20:15:46 2014 - [warning] Connection failed 1 time(s)..
Mon Apr 21 20:15:47 2014 - [warning] Got error on MySQL connect: 2013 (Lost connection to MySQL server at 'reading initial communication packet', system error: 111)
Mon Apr 21 20:15:47 2014 - [warning] Connection failed 2 time(s)..
Mon Apr 21 20:15:48 2014 - [warning] Got error on MySQL connect: 2013 (Lost connection to MySQL server at 'reading initial communication packet', system error: 111)
Mon Apr 21 20:15:48 2014 - [warning] Connection failed 3 time(s)..
Mon Apr 21 20:15:48 2014 - [warning] Master is not reachable from health checker!
Mon Apr 21 20:15:48 2014 - [warning] Master 192.168.0.50(192.168.0.50:3306) is not reachable!
Mon Apr 21 20:15:48 2014 - [warning] SSH is reachable.
Mon Apr 21 20:15:48 2014 - [info] Connecting to a master server failed. Reading configuration file /etc/masterha_default.cnf and /etc/masterha/app1.cnf again, and trying to connect to all servers to check server status..
Mon Apr 21 20:15:48 2014 - [warning] Global configuration file /etc/masterha_default.cnf not found. Skipping.
Mon Apr 21 20:15:48 2014 - [info] Reading application default configurations from /etc/masterha/app1.cnf..
Mon Apr 21 20:15:48 2014 - [info] Reading server configurations from /etc/masterha/app1.cnf..
Mon Apr 21 20:15:48 2014 - [info] Dead Servers:
Mon Apr 21 20:15:48 2014 - [info]   192.168.0.50(192.168.0.50:3306)
Mon Apr 21 20:15:48 2014 - [info] Alive Servers:
Mon Apr 21 20:15:48 2014 - [info]   192.168.0.60(192.168.0.60:3306)
Mon Apr 21 20:15:48 2014 - [info]   192.168.0.70(192.168.0.70:3306)
Mon Apr 21 20:15:48 2014 - [info] Alive Slaves:
Mon Apr 21 20:15:48 2014 - [info]   192.168.0.60(192.168.0.60:3306)  Version=5.5.19-ndb-7.2.4-gpl-log (oldest major version between slaves) log-bin:enabled
Mon Apr 21 20:15:48 2014 - [info]     Replicating from 192.168.0.50(192.168.0.50:3306)
Mon Apr 21 20:15:48 2014 - [info]     Primary candidate for the new Master (candidate_master is set)
Mon Apr 21 20:15:48 2014 - [info]   192.168.0.70(192.168.0.70:3306)  Version=5.5.19-ndb-7.2.4-gpl-log (oldest major version between slaves) log-bin:enabled
Mon Apr 21 20:15:48 2014 - [info]     Replicating from 192.168.0.50(192.168.0.50:3306)
Mon Apr 21 20:15:48 2014 - [info] Checking slave configurations..
Mon Apr 21 20:15:48 2014 - [info] Checking replication filtering settings..
Mon Apr 21 20:15:48 2014 - [info]  Replication filtering check ok.
Mon Apr 21 20:15:48 2014 - [info] Master is down!
Mon Apr 21 20:15:48 2014 - [info] Terminating monitoring script.
Mon Apr 21 20:15:48 2014 - [info] Got exit code 20 (Master dead).
Mon Apr 21 20:15:48 2014 - [info] MHA::MasterFailover version 0.53.
Mon Apr 21 20:15:48 2014 - [info] Starting master failover.
Mon Apr 21 20:15:48 2014 - [info] 
Mon Apr 21 20:15:48 2014 - [info] * Phase 1: Configuration Check Phase..
Mon Apr 21 20:15:48 2014 - [info] 
Mon Apr 21 20:15:48 2014 - [info] Dead Servers:
Mon Apr 21 20:15:48 2014 - [info]   192.168.0.50(192.168.0.50:3306)
Mon Apr 21 20:15:48 2014 - [info] Checking master reachability via mysql(double check)..
Mon Apr 21 20:15:48 2014 - [info]  ok.
Mon Apr 21 20:15:48 2014 - [info] Alive Servers:
Mon Apr 21 20:15:48 2014 - [info]   192.168.0.60(192.168.0.60:3306)
Mon Apr 21 20:15:48 2014 - [info]   192.168.0.70(192.168.0.70:3306)
Mon Apr 21 20:15:48 2014 - [info] Alive Slaves:
Mon Apr 21 20:15:48 2014 - [info]   192.168.0.60(192.168.0.60:3306)  Version=5.5.19-ndb-7.2.4-gpl-log (oldest major version between slaves) log-bin:enabled
Mon Apr 21 20:15:48 2014 - [info]     Replicating from 192.168.0.50(192.168.0.50:3306)
Mon Apr 21 20:15:48 2014 - [info]     Primary candidate for the new Master (candidate_master is set)
Mon Apr 21 20:15:48 2014 - [info]   192.168.0.70(192.168.0.70:3306)  Version=5.5.19-ndb-7.2.4-gpl-log (oldest major version between slaves) log-bin:enabled
Mon Apr 21 20:15:48 2014 - [info]     Replicating from 192.168.0.50(192.168.0.50:3306)
Mon Apr 21 20:15:49 2014 - [info] ** Phase 1: Configuration Check Phase completed.
Mon Apr 21 20:15:49 2014 - [info] 
Mon Apr 21 20:15:49 2014 - [info] * Phase 2: Dead Master Shutdown Phase..
Mon Apr 21 20:15:49 2014 - [info] 
Mon Apr 21 20:15:49 2014 - [info] Forcing shutdown so that applications never connect to the current master..
Mon Apr 21 20:15:49 2014 - [info] Executing master IP deactivatation script:
Mon Apr 21 20:15:49 2014 - [info]   /usr/local/bin/master_ip_failover --orig_master_host=192.168.0.50 --orig_master_ip=192.168.0.50 --orig_master_port=3306 --command=stopssh --ssh_user=root  


IN SCRIPT TEST====/etc/init.d/keepalived stop==/etc/init.d/keepalived start===

Disabling the VIP on old master: 192.168.0.50 
Mon Apr 21 20:15:49 2014 - [info]  done.
Mon Apr 21 20:15:49 2014 - [warning] shutdown_script is not set. Skipping explicit shutting down of the dead master.
Mon Apr 21 20:15:49 2014 - [info] * Phase 2: Dead Master Shutdown Phase completed.
Mon Apr 21 20:15:49 2014 - [info] 
Mon Apr 21 20:15:49 2014 - [info] * Phase 3: Master Recovery Phase..
Mon Apr 21 20:15:49 2014 - [info] 
Mon Apr 21 20:15:49 2014 - [info] * Phase 3.1: Getting Latest Slaves Phase..
Mon Apr 21 20:15:49 2014 - [info] 
Mon Apr 21 20:15:49 2014 - [info] The latest binary log file/position on all slaves is mysql-bin.000018:112
Mon Apr 21 20:15:49 2014 - [info] Latest slaves (Slaves that received relay log files to the latest):
Mon Apr 21 20:15:49 2014 - [info]   192.168.0.60(192.168.0.60:3306)  Version=5.5.19-ndb-7.2.4-gpl-log (oldest major version between slaves) log-bin:enabled
Mon Apr 21 20:15:49 2014 - [info]     Replicating from 192.168.0.50(192.168.0.50:3306)
Mon Apr 21 20:15:49 2014 - [info]     Primary candidate for the new Master (candidate_master is set)
Mon Apr 21 20:15:49 2014 - [info]   192.168.0.70(192.168.0.70:3306)  Version=5.5.19-ndb-7.2.4-gpl-log (oldest major version between slaves) log-bin:enabled
Mon Apr 21 20:15:49 2014 - [info]     Replicating from 192.168.0.50(192.168.0.50:3306)
Mon Apr 21 20:15:49 2014 - [info] The oldest binary log file/position on all slaves is mysql-bin.000018:112
Mon Apr 21 20:15:49 2014 - [info] Oldest slaves:
Mon Apr 21 20:15:49 2014 - [info]   192.168.0.60(192.168.0.60:3306)  Version=5.5.19-ndb-7.2.4-gpl-log (oldest major version between slaves) log-bin:enabled
Mon Apr 21 20:15:49 2014 - [info]     Replicating from 192.168.0.50(192.168.0.50:3306)
Mon Apr 21 20:15:49 2014 - [info]     Primary candidate for the new Master (candidate_master is set)
Mon Apr 21 20:15:49 2014 - [info]   192.168.0.70(192.168.0.70:3306)  Version=5.5.19-ndb-7.2.4-gpl-log (oldest major version between slaves) log-bin:enabled
Mon Apr 21 20:15:49 2014 - [info]     Replicating from 192.168.0.50(192.168.0.50:3306)
Mon Apr 21 20:15:49 2014 - [info] 
Mon Apr 21 20:15:49 2014 - [info] * Phase 3.2: Saving Dead Master's Binlog Phase..
Mon Apr 21 20:15:49 2014 - [info] 
Mon Apr 21 20:15:49 2014 - [info] Fetching dead master's binary logs..
Mon Apr 21 20:15:49 2014 - [info] Executing command on the dead master 192.168.0.50(192.168.0.50:3306): save_binary_logs --command=save --start_file=mysql-bin.000018  --start_pos=112 --binlog_dir=/data/mysql --output_file=/tmp/saved_master_binlog_from_192.168.0.50_3306_20140421201548.binlog --handle_raw_binlog=1 --disable_log_bin=0 --manager_version=0.53
  Creating /tmp if not exists..    ok.
 Concat binary/relay logs from mysql-bin.000018 pos 112 to mysql-bin.000018 EOF into /tmp/saved_master_binlog_from_192.168.0.50_3306_20140421201548.binlog ..
  Dumping binlog format description event, from position 0 to 112.. ok.
  Dumping effective binlog data from /data/mysql/mysql-bin.000018 position 112 to tail(131).. ok.
 Concat succeeded.
Mon Apr 21 20:15:50 2014 - [info] scp from root@192.168.0.50:/tmp/saved_master_binlog_from_192.168.0.50_3306_20140421201548.binlog to local:/var/log/masterha/app1.log/saved_master_binlog_from_192.168.0.50_3306_20140421201548.binlog succeeded.
Mon Apr 21 20:15:50 2014 - [info] HealthCheck: SSH to 192.168.0.60 is reachable.
Mon Apr 21 20:15:50 2014 - [info] HealthCheck: SSH to 192.168.0.70 is reachable.
Mon Apr 21 20:15:50 2014 - [info] 
Mon Apr 21 20:15:50 2014 - [info] * Phase 3.3: Determining New Master Phase..
Mon Apr 21 20:15:50 2014 - [info] 
Mon Apr 21 20:15:50 2014 - [info] Finding the latest slave that has all relay logs for recovering other slaves..
Mon Apr 21 20:15:50 2014 - [info] All slaves received relay logs to the same position. No need to resync each other.
Mon Apr 21 20:15:50 2014 - [info] Searching new master from slaves..
Mon Apr 21 20:15:50 2014 - [info]  Candidate masters from the configuration file:
Mon Apr 21 20:15:50 2014 - [info]   192.168.0.60(192.168.0.60:3306)  Version=5.5.19-ndb-7.2.4-gpl-log (oldest major version between slaves) log-bin:enabled
Mon Apr 21 20:15:50 2014 - [info]     Replicating from 192.168.0.50(192.168.0.50:3306)
Mon Apr 21 20:15:50 2014 - [info]     Primary candidate for the new Master (candidate_master is set)
Mon Apr 21 20:15:50 2014 - [info]  Non-candidate masters:
Mon Apr 21 20:15:50 2014 - [info]  Searching from candidate_master slaves which have received the latest relay log events..
Mon Apr 21 20:15:50 2014 - [info] New master is 192.168.0.60(192.168.0.60:3306)
Mon Apr 21 20:15:50 2014 - [info] Starting master failover..
Mon Apr 21 20:15:50 2014 - [info] 
From:
192.168.0.50 (current master)
 +--192.168.0.60
 +--192.168.0.70

To:
192.168.0.60 (new master)
 +--192.168.0.70
Mon Apr 21 20:15:50 2014 - [info] 
Mon Apr 21 20:15:50 2014 - [info] * Phase 3.3: New Master Diff Log Generation Phase..
Mon Apr 21 20:15:50 2014 - [info] 
Mon Apr 21 20:15:50 2014 - [info]  This server has all relay logs. No need to generate diff files from the latest slave.
Mon Apr 21 20:15:50 2014 - [info] Sending binlog..
Mon Apr 21 20:15:51 2014 - [info] scp from local:/var/log/masterha/app1.log/saved_master_binlog_from_192.168.0.50_3306_20140421201548.binlog to root@192.168.0.60:/tmp/saved_master_binlog_from_192.168.0.50_3306_20140421201548.binlog succeeded.
Mon Apr 21 20:15:51 2014 - [info] 
Mon Apr 21 20:15:51 2014 - [info] * Phase 3.4: Master Log Apply Phase..
Mon Apr 21 20:15:51 2014 - [info] 
Mon Apr 21 20:15:51 2014 - [info] *NOTICE: If any error happens from this phase, manual recovery is needed.
Mon Apr 21 20:15:51 2014 - [info] Starting recovery on 192.168.0.60(192.168.0.60:3306)..
Mon Apr 21 20:15:51 2014 - [info]  Generating diffs succeeded.
Mon Apr 21 20:15:51 2014 - [info] Waiting until all relay logs are applied.
Mon Apr 21 20:15:51 2014 - [info]  done.
Mon Apr 21 20:15:51 2014 - [info] Getting slave status..
Mon Apr 21 20:15:51 2014 - [info] This slave(192.168.0.60)'s Exec_Master_Log_Pos equals to Read_Master_Log_Pos(mysql-bin.000018:112). No need to recover from Exec_Master_Log_Pos.
Mon Apr 21 20:15:51 2014 - [info] Connecting to the target slave host 192.168.0.60, running recover script..
Mon Apr 21 20:15:51 2014 - [info] Executing command: apply_diff_relay_logs --command=apply --slave_user=root --slave_host=192.168.0.60 --slave_ip=192.168.0.60  --slave_port=3306 --apply_files=/tmp/saved_master_binlog_from_192.168.0.50_3306_20140421201548.binlog --workdir=/tmp --target_version=5.5.19-ndb-7.2.4-gpl-log --timestamp=20140421201548 --handle_raw_binlog=1 --disable_log_bin=0 --manager_version=0.53 --slave_pass=xxx
Mon Apr 21 20:15:51 2014 - [info] 
Applying differential binary/relay log files /tmp/saved_master_binlog_from_192.168.0.50_3306_20140421201548.binlog on 192.168.0.60:3306. This may take long time...
Applying log files succeeded.
Mon Apr 21 20:15:51 2014 - [info]  All relay logs were successfully applied.
Mon Apr 21 20:15:51 2014 - [info] Getting new master's binlog name and position..
Mon Apr 21 20:15:51 2014 - [info]  mysql-bin.000022:506716
Mon Apr 21 20:15:51 2014 - [info]  All other slaves should start replication from here. Statement should be: CHANGE MASTER TO MASTER_HOST='192.168.0.60', MASTER_PORT=3306, MASTER_LOG_FILE='mysql-bin.000022', MASTER_LOG_POS=506716, MASTER_USER='repl', MASTER_PASSWORD='xxx';
Mon Apr 21 20:15:51 2014 - [info] Executing master IP activate script:
Mon Apr 21 20:15:51 2014 - [info]   /usr/local/bin/master_ip_failover --command=start --ssh_user=root --orig_master_host=192.168.0.50 --orig_master_ip=192.168.0.50 --orig_master_port=3306 --new_master_host=192.168.0.60 --new_master_ip=192.168.0.60 --new_master_port=3306  


IN SCRIPT TEST====/etc/init.d/keepalived stop==/etc/init.d/keepalived start===

Enabling the VIP - 192.168.0.88 on the new master - 192.168.0.60 
Mon Apr 21 20:15:52 2014 - [info]  OK.
Mon Apr 21 20:15:52 2014 - [info] Setting read_only=0 on 192.168.0.60(192.168.0.60:3306)..
Mon Apr 21 20:15:52 2014 - [info]  ok.
Mon Apr 21 20:15:52 2014 - [info] ** Finished master recovery successfully.
Mon Apr 21 20:15:52 2014 - [info] * Phase 3: Master Recovery Phase completed.
Mon Apr 21 20:15:52 2014 - [info] 
Mon Apr 21 20:15:52 2014 - [info] * Phase 4: Slaves Recovery Phase..
Mon Apr 21 20:15:52 2014 - [info] 
Mon Apr 21 20:15:52 2014 - [info] * Phase 4.1: Starting Parallel Slave Diff Log Generation Phase..
Mon Apr 21 20:15:52 2014 - [info] 
Mon Apr 21 20:15:52 2014 - [info] -- Slave diff file generation on host 192.168.0.70(192.168.0.70:3306) started, pid: 31321. Check tmp log /var/log/masterha/app1.log/192.168.0.70_3306_20140421201548.log if it takes time..
Mon Apr 21 20:15:52 2014 - [info] 
Mon Apr 21 20:15:52 2014 - [info] Log messages from 192.168.0.70 ...
Mon Apr 21 20:15:52 2014 - [info] 
Mon Apr 21 20:15:52 2014 - [info]  This server has all relay logs. No need to generate diff files from the latest slave.
Mon Apr 21 20:15:52 2014 - [info] End of log messages from 192.168.0.70.
Mon Apr 21 20:15:52 2014 - [info] -- 192.168.0.70(192.168.0.70:3306) has the latest relay log events.
Mon Apr 21 20:15:52 2014 - [info] Generating relay diff files from the latest slave succeeded.
Mon Apr 21 20:15:52 2014 - [info] 
Mon Apr 21 20:15:52 2014 - [info] * Phase 4.2: Starting Parallel Slave Log Apply Phase..
Mon Apr 21 20:15:52 2014 - [info] 
Mon Apr 21 20:15:52 2014 - [info] -- Slave recovery on host 192.168.0.70(192.168.0.70:3306) started, pid: 31323. Check tmp log /var/log/masterha/app1.log/192.168.0.70_3306_20140421201548.log if it takes time..
Mon Apr 21 20:15:52 2014 - [info] 
Mon Apr 21 20:15:52 2014 - [info] Log messages from 192.168.0.70 ...
Mon Apr 21 20:15:52 2014 - [info] 
Mon Apr 21 20:15:52 2014 - [info] Sending binlog..
Mon Apr 21 20:15:52 2014 - [info] scp from local:/var/log/masterha/app1.log/saved_master_binlog_from_192.168.0.50_3306_20140421201548.binlog to root@192.168.0.70:/tmp/saved_master_binlog_from_192.168.0.50_3306_20140421201548.binlog succeeded.
Mon Apr 21 20:15:52 2014 - [info] Starting recovery on 192.168.0.70(192.168.0.70:3306)..
Mon Apr 21 20:15:52 2014 - [info]  Generating diffs succeeded.
Mon Apr 21 20:15:52 2014 - [info] Waiting until all relay logs are applied.
Mon Apr 21 20:15:52 2014 - [info]  done.
Mon Apr 21 20:15:52 2014 - [info] Getting slave status..
Mon Apr 21 20:15:52 2014 - [info] This slave(192.168.0.70)'s Exec_Master_Log_Pos equals to Read_Master_Log_Pos(mysql-bin.000018:112). No need to recover from Exec_Master_Log_Pos.
Mon Apr 21 20:15:52 2014 - [info] Connecting to the target slave host 192.168.0.70, running recover script..
Mon Apr 21 20:15:52 2014 - [info] Executing command: apply_diff_relay_logs --command=apply --slave_user=root --slave_host=192.168.0.70 --slave_ip=192.168.0.70  --slave_port=3306 --apply_files=/tmp/saved_master_binlog_from_192.168.0.50_3306_20140421201548.binlog --workdir=/tmp --target_version=5.5.19-ndb-7.2.4-gpl-log --timestamp=20140421201548 --handle_raw_binlog=1 --disable_log_bin=0 --manager_version=0.53 --slave_pass=xxx
Mon Apr 21 20:15:52 2014 - [info] 
Applying differential binary/relay log files /tmp/saved_master_binlog_from_192.168.0.50_3306_20140421201548.binlog on 192.168.0.70:3306. This may take long time...
Applying log files succeeded.
Mon Apr 21 20:15:52 2014 - [info]  All relay logs were successfully applied.
Mon Apr 21 20:15:52 2014 - [info]  Resetting slave 192.168.0.70(192.168.0.70:3306) and starting replication from the new master 192.168.0.60(192.168.0.60:3306)..
Mon Apr 21 20:15:52 2014 - [info]  Executed CHANGE MASTER.
Mon Apr 21 20:15:52 2014 - [info]  Slave started.
Mon Apr 21 20:15:52 2014 - [info] End of log messages from 192.168.0.70.
Mon Apr 21 20:15:52 2014 - [info] -- Slave recovery on host 192.168.0.70(192.168.0.70:3306) succeeded.
Mon Apr 21 20:15:52 2014 - [info] All new slave servers recovered successfully.
Mon Apr 21 20:15:52 2014 - [info] 
Mon Apr 21 20:15:52 2014 - [info] * Phase 5: New master cleanup phease..
Mon Apr 21 20:15:52 2014 - [info] 
Mon Apr 21 20:15:52 2014 - [info] Resetting slave info on the new master..
Mon Apr 21 20:15:53 2014 - [info]  192.168.0.60: Resetting slave info succeeded.
Mon Apr 21 20:15:53 2014 - [info] Master failover to 192.168.0.60(192.168.0.60:3306) completed successfully.
Mon Apr 21 20:15:53 2014 - [info] Deleted server1 entry from /etc/masterha/app1.cnf .
Mon Apr 21 20:15:53 2014 - [info] 

----- Failover Report -----

app1: MySQL Master failover 192.168.0.50 to 192.168.0.60 succeeded

Master 192.168.0.50 is down!

Check MHA Manager logs at server01:/var/log/masterha/app1/manager.log for details.

Started automated(non-interactive) failover.
Invalidated master IP address on 192.168.0.50.
The latest slave 192.168.0.60(192.168.0.60:3306) has all relay logs for recovery.
Selected 192.168.0.60 as a new master.
192.168.0.60: OK: Applying all logs succeeded.
192.168.0.60: OK: Activated master IP address.
192.168.0.70: This host has the latest relay log events.
Generating relay diff files from the latest slave succeeded.
192.168.0.70: OK: Applying all logs succeeded. Slave started, replicating from 192.168.0.60.
192.168.0.60: Resetting slave info succeeded.
Master failover to 192.168.0.60(192.168.0.60:3306) completed successfully.
[root@192.168.0.20 ~]#
```

看到最后的Master failover to 192.168.0.60(192.168.0.60:3306) completed successfully.说明备选master现在已经上位了。


从上面的输出可以看出整个MHA的切换过程，共包括以下的步骤：

1.配置文件检查阶段，这个阶段会检查整个集群配置文件配置
2.宕机的master处理，这个阶段包括虚拟ip摘除操作，主机关机操作（这个我这里还没有实现，需要研究）
3.复制dead maste和最新slave相差的relay log，并保存到MHA Manger具体的目录下
4.识别含有最新更新的slave
5.应用从master保存的二进制日志事件（binlog events）
6.提升一个slave为新的master进行复制
7.使其他的slave连接新的master进行复制

## 8.Running MHA Manager from daemontools

8.1 使用nohup方式的后台启动
```
manager_host$ nohup masterha_manager --conf=/etc/app1.cnf < /dev/null > /var/log/masterha/app1/app1.log 2>&1 &
```

8.2 使用daemontools方式
```shell
yum install daemontools
manager_host# mkdir /service/masterha_app1

manager_host# cat /service/masterha_app1/run
#!/bin/sh
exec masterha_manager --conf=/etc/app1.cnf --wait_on_monitor_error=60 --wait_on_failover_error=60 >> /var/log/masterha/app1/app1.log 2>&1

manager_host# chmod 755 /service/masterha_app1/run

## stopping monitoring
manager_host# svc -d /service/masterha_app1

## starting monitoring
manager_host# svc -u /service/masterha_app1

```

## 9.修复宕机的Master 
通常情况下自动切换以后，原master可能已经废弃掉，待原master主机修复后，如果数据完整的情况下，可能想把原来master重新作为新主库的slave，这时我们可以借助当时自动切换时刻的MHA日志来完成对原master的修复。下面是提取相关日志的命令：
```
[root@192.168.0.20 app1]# grep -i "All other slaves should start" manager.log 
Mon Apr 21 22:28:33 2014 - [info]  All other slaves should start replication from here. Statement should be: CHANGE MASTER TO MASTER_HOST='192.168.0.60', MASTER_PORT=3306, MASTER_LOG_FILE='mysql-bin.000022', MASTER_LOG_POS=506716, MASTER_USER='repl', MASTER_PASSWORD='xxx';
[root@192.168.0.20 app1]# 
```
获取上述信息以后，就可以直接在修复后的master上执行change master to相关操作，重新作为从库了。

最后补充一下邮件发送脚本send_report ，这个脚本在询问一位朋友后可以使用，如下：
```perl
#!/usr/bin/perl

#  Copyright (C) 2011 DeNA Co.,Ltd.
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#  Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

## Note: This is a sample script and is not complete. Modify the script based on your environment.

use strict;
use warnings FATAL => 'all';
use Mail::Sender;
use Getopt::Long;

#new_master_host and new_slave_hosts are set only when recovering master succeeded
my ( $dead_master_host, $new_master_host, $new_slave_hosts, $subject, $body );
my $smtp='smtp.163.com';
my $mail_from='xxxx';
my $mail_user='xxxxx';
my $mail_pass='xxxxx';
my $mail_to=['xxxx','xxxx'];
GetOptions(
  'orig_master_host=s' => \$dead_master_host,
  'new_master_host=s'  => \$new_master_host,
  'new_slave_hosts=s'  => \$new_slave_hosts,
  'subject=s'          => \$subject,
  'body=s'             => \$body,
);

mailToContacts($smtp,$mail_from,$mail_user,$mail_pass,$mail_to,$subject,$body);

sub mailToContacts {
    my ( $smtp, $mail_from, $user, $passwd, $mail_to, $subject, $msg ) = @_;
    open my $DEBUG, "> /tmp/monitormail.log"
        or die "Can't open the debug      file:$!\n";
    my $sender = new Mail::Sender {
        ctype       => 'text/plain; charset=utf-8',
        encoding    => 'utf-8',
        smtp        => $smtp,
        from        => $mail_from,
        auth        => 'LOGIN',
        TLS_allowed => '0',
        authid      => $user,
        authpwd     => $passwd,
        to          => $mail_to,
        subject     => $subject,
        debug       => $DEBUG
    };

    $sender->MailMsg(
        {   msg   => $msg,
            debug => $DEBUG
        }
    ) or print $Mail::Sender::Error;
    return 1;
}



# Do whatever you want here

exit 0;
```

