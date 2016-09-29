# MySQL GTID 与多线程复制
---
## 1. 什么是GTID?
GTID(Global Transaction ID)是对于一个已提交事务的编号，并且是一个全局唯一的编号。 GTID实际上是由UUID+TID组成的。其中UUID是一个MySQL实例的唯一标识。TID代表了该实例上已经提交的事务数量，并且随着事务提交单调递增。下面是一个GTID的具体形式.

`GTID = source_id:transaction_id`  --> `3E11FA47-71CA-11E1-9E33-C80AA9429562:23`

## 2. GTID的作用 多线程复制
1. 根据GTID可以知道事物最初是在哪个实例提交的.
2. GTID的存在方便了Replication的Failover.

MySQL5.6的GTID出现以前的replication failover的操作过程.
假设有一个如下图的环境![](images/failover.jpg), 此时, Server A 的服务器宕机,需要将业务切换到 Server B 上. 同事,我们又需要将 Server C 的复制源切换成 Server B. 复制源修改命令很简单`CHANGE MASTER TO MASTER_HOST='xxx', MASTER_LOG_FILE='xxx', MASTER_LOG_POS=nnnn`. 而难点在于,由于同一个事物在每台机器上的所在的binlog名字和位置都不一样, 那么怎么知道 Server C 当前的同步停止点对应到 Server B 的`Master_log_file` 和 `master_log_pos` 的位置. 这也就是`M-S`集群需要使用 `MMM`,  `MHA` 这样的额外管理工具的一个重要原因.  这个问题在GTID出现之后, 就显得非常简单. 由于同一个事务的GTID在所有的节点上的值是一致的, 那么根据 Server C 当前停止GTID就能唯一定位到 Server B 上的GTID. 甚至由于 `MASTER_AUTO_POSITION` 功能的出现, 我们都不需要知道GTID的具体位置了, 直接使用`CHANGE MASTER TO MASTER_HOST='xxx', MASTER_AUTO_POSITION`就可以直接完成 failover 的工作.

### 多线程复制
MySQL 5.6之前的版本，同步复制是单线程的，队列的，只能一个一个执行，在5.6里，可以做到多个库之间的多线程复制，例如数据库里，存放着用户表，商品表，价格表，订单表，那么将每个业务表单独放在一个库里，这时就可以做到多线程复制，但一个库里的表，多线程复制是无效的。
注，每个数据库仅能使用一个线程，复制涉及到多个数据库时多线程复制才有意义。

## 3. 开启GTID的复制(第一次开启主从复制时)
这是安装[官网文档](http://dev.mysql.com/doc/refman/5.6/en/replication-gtids-howto.html)进行的, 必须要停机. Percona, Facebook 等提供另一种方式,实现.


### 3.1 如果已经开启复制,  先设置所有为 readonly
```
mysql> SET @@global.read_only = ON;
```
### 3.2 停止所有相关的MySQL.

### 3.3 开启GTID, 所有机器
设置my.cnf, 所有的MySQL
```
binlog_format = row
gtid-mode = ON
enforce-gtid-consistency = ON  
log-bin=mysql-bin
log-slave-updates
```

`enforce-gtid-consistency` 设置这项时, 必须开启`gtid-mode=on`, 
开启gtid时, `log-bin=mysql-bin`, `log-slave-updates`, `gtid-mode = ON` 时必须的

通过命令参数启动gtid
`mysqld_safe --gtid_mode=ON --log-bin --log-slave-updates --enforce-gtid-consistency & `

### 3.4 设置主从连接
在slave上
```
mysql> CHANGE MASTER TO 
     >     MASTER_HOST = host,
     >     MASTER_PORT = port,
     >     MASTER_USER = user,
     >     MASTER_PASSWORD = password,
     >     MASTER_AUTO_POSITION = 1;
     >     
mysql>START SLAVE;
```


### 3.5 禁用只读

```
mysql> SET @@global.read_only = OFF;
```

### 3.6 可能出现的问题
__change master to 后的warnings__

在按照文档的操作change master to后，会发现有两个warnings。其实是两个安全性警告，不影响正常的同步（有兴趣的读者可以看下关于该warning的具体介绍。warning的具体内容如下：
```
slave1 [localhost] {msandbox} ((none)) > stop slave;
Query OK, 0 rows affected (0.03 sec)

slave1 [localhost] {msandbox} ((none)) > change master to master_host='127.0.0.1',master_port =21288,master_user='rsandbox',master_password='rsandbox',master_auto_position=1;
Query OK, 0 rows affected, 2 warnings (0.04 sec)

slave1 [localhost] {msandbox} ((none)) > show warnings;
+-------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                                                                                                                                                                                                              |
+-------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Note  | 1759 | Sending passwords in plain text without SSL/TLS is extremely insecure.                                                                                                                                                                                                               |
| Note  | 1760 | Storing MySQL user name or password information in the master info repository is not secure and is therefore not recommended. Please consider using the USER and PASSWORD connection options for START SLAVE; see the 'START SLAVE Syntax' in the MySQL Manual for more information. |
+-------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
2 rows in set (0.00 sec)
```


## GTID与多线程复制 相关参数
要在MySQL 5.6中使用复制功能，其服务配置段[mysqld]中于少应该定义如下选项，

`binlog-format`：二进制日志的格式，有row、statement和mixed几种类型；需要注意的是：`当设置隔离级别为READ-COMMITED必须设置二进制日志格式为ROW，现在MySQL官方认为STATEMENT这个已经不再适合继续使用`；`但mixed类型在默认的事务隔离级别下，可能会导致主从数据不一致`；

`log-slave-updates`、`gtid-mode`、`enforce-gtid-consistency`、`report-port`和`report-host`：用于启动GTID及满足附属的其它需求；

`master-info-repository`和`relay-log-info-repository`：启用此两项，可用于实现在崩溃时保证二进制及从服务器安全的功能；

`sync-master-info`：启用之可确保无信息丢失；
`slave-paralles-workers`：设定从服务器的SQL线程数；0表示关闭多线程复制功能；

`binlog-checksum`、`master-verify-checksum`和`slave-sql-verify-checksum`：启用复制有关的所有校验功能；

`binlog-rows-query-log-events`：启用之可用于在二进制日志记录事件相关的信息，可降低故障排除的复杂度；

`log-bin`：启用二进制日志，这是保证复制功能的基本前提；
`server-id`：同一个复制拓扑中的所有服务器的id号必须惟一。

## 5.GTID 运维
启用的GTID后,如果主从发生了错误后, 处理的方式, 跟传统方式是不同的.
[](http://www.oschina.net/translate/gtids-in-mysql-5-6-new-replication-protocol-new-ways-to-break-replication)

### 5.1 跳过事务

在不启用GTID时, 跳过某些事务,可以使用`SET GLOBAL sql_slave_counter = N` 来实现.
启动了GTID时,要使用`GTID XXX:N`注入空事务来跳过日志.

```
set  gtid_next = 'xxx:N'
BEGIN; commit;
set gtid_next = 'AUTOMATIC'
```

### 5.2 错误日志

如果你在一个slave上本地执行了一个事务 (在MySQL文档中被称为错误事务), 如果你被这个事务推送到新的master上时会发生什么呢?

1. 使用老协议，基本上没啥事（准确点说，新的master和其slave之间的数据将会出现不一致，但那在稍后就可能会被修复）.
2. 使用新协议，错误的事务将会被识别成为在每个地方都丢失了，并且将会自动在容错备份上被执行，这样就将会导致中断复制的隐患.

如果有一个master（M)和两个slave (S1 和 S2). 这里有两种将slave重连到新的master将会发生（带有不同复制错误的）失败的场景:

__场景一__:
```
# S1
mysql> CREATE DATABASE mydb;
# M
mysql> CREATE DATABASE IF NOT EXISTS mydb;
# Thanks to 'IF NOT EXITS', replication doesn't break on S1. Now move S2 to S1:
# S2
mysql> STOP SLAVE; CHANGE MASTER TO MASTER_HOST='S1'; START SLAVE;
# This creates a conflict with existing data!
mysql> SHOW SLAVE STATUS\G
[...]
Last_SQL_Errno: 1007
               Last_SQL_Error: Error 'Can't create database 'mydb'; database exists' on query. Default database: 'mydb'. Query: 'CREATE DATABASE mydb'
[...]
```

__场景二__:
```
# S1
mysql> CREATE DATABASE mydb;
# Now, we'll remove this transaction from the binary logs
# S1
mysql> FLUSH LOGS;
mysql> PURGE BINARY LOGS TO 'mysql-bin.000008';
# M
mysql> CREATE DATABASE IF NOT EXISTS mydb;
# S2
mysql> STOP SLAVE; CHANGE MASTER TO MASTER_HOST='S1'; START SLAVE;
# The missing transaction is no longer available in the master's binary logs!
mysql> SHOW SLAVE STATUS\G
[...]
Last_IO_Errno: 1236
                Last_IO_Error: Got fatal error 1236 from master when reading data from binary log: 'The slave is connecting using CHANGE MASTER TO MASTER_AUTO_POSITION = 1, but the master has purged binary logs containing GTIDs that the slave requires.'
[...]
```

你可以这样理解，错误的事务应该借助基于GTID的服务得以避免. 如果你需要运行一个本地事务，最好的选择是针对那条特定的语句禁用二进制日志:
```
mysql> SET SQL_LOG_BIN = 0;
mysql> # Run local transaction
```

### 5.3 如果slave所需要事务对应的GTID在master上已经被purge了

根据`show global variables like '%gtid%'`的命令结果我们可以看到，和GTID相关的变量中有一个`gtid_purged`。从字面意思以及 官方文档可以知道该变量中记录的是本机上已经执行过，但是已经被`purge binary logs to`命令清理的`gtid_set`。 本节中我们就要试验下，如果master上把某些slave还没有fetch到的gtid event purge后会有什么样的结果。

#### 5.3.1 指令在master上执行:
```
master [localhost] {msandbox} (test) > show global variables like '%gtid%';
+---------------------------------+----------------------------------------+
| Variable_name                   | Value                                  |
+---------------------------------+----------------------------------------+
| binlog_gtid_simple_recovery     | OFF                                    |
| enforce_gtid_consistency        | ON                                     |
| gtid_executed                   | 24024e52-bd95-11e4-9c6d-926853670d0b:1 |
| gtid_mode                       | ON                                     |
| gtid_owned                      |                                        |
| gtid_purged                     |                                        |
| simplified_binlog_gtid_recovery | OFF                                    |
+---------------------------------+----------------------------------------+
7 rows in set (0.01 sec)

master [localhost] {msandbox} (test) > flush logs;create table gtid_test2 (ID int) engine=innodb;
Query OK, 0 rows affected (0.04 sec)

Query OK, 0 rows affected (0.02 sec)

master [localhost] {msandbox} (test) > flush logs;create table gtid_test3 (ID int) engine=innodb;
Query OK, 0 rows affected (0.04 sec)

Query OK, 0 rows affected (0.04 sec)

master [localhost] {msandbox} (test) > show master status;
+------------------+----------+--------------+------------------+------------------------------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set                        |
+------------------+----------+--------------+------------------+------------------------------------------+
| mysql-bin.000005 |      359 |              |                  | 24024e52-bd95-11e4-9c6d-926853670d0b:1-3 |
+------------------+----------+--------------+------------------+------------------------------------------+
1 row in set (0.00 sec)

master [localhost] {msandbox} (test) > purge binary logs to 'mysql-bin.000004';
Query OK, 0 rows affected (0.03 sec)

master [localhost] {msandbox} (test) > show global variables like '%gtid%';
+---------------------------------+------------------------------------------+
| Variable_name                   | Value                                    |
+---------------------------------+------------------------------------------+
| binlog_gtid_simple_recovery     | OFF                                      |
| enforce_gtid_consistency        | ON                                       |
| gtid_executed                   | 24024e52-bd95-11e4-9c6d-926853670d0b:1-3 |
| gtid_mode                       | ON                                       |
| gtid_owned                      |                                          |
| gtid_purged                     | 24024e52-bd95-11e4-9c6d-926853670d0b:1   |
| simplified_binlog_gtid_recovery | OFF                                      |
+---------------------------------+------------------------------------------+
7 rows in set (0.00 sec)
```

#### 5.3.2  在slave2上重新做一次主从，以下命令在slave2上执行
```
slave2 [localhost] {msandbox} ((none)) > change master to master_host='127.0.0.1',master_port =21288,master_user='rsandbox',master_password='rsandbox',master_auto_position=1;
Query OK, 0 rows affected, 2 warnings (0.04 sec)

slave2 [localhost] {msandbox} ((none)) > start slave;
Query OK, 0 rows affected (0.01 sec)

slave2 [localhost] {msandbox} ((none)) > show slave status\G
*************************** 1. row ***************************
                          ......
             Slave_IO_Running: No
            Slave_SQL_Running: Yes
                          ......
                   Last_Errno: 0
                   Last_Error:
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 0
              Relay_Log_Space: 151
                          ......
                Last_IO_Errno: 1236
                Last_IO_Error: Got fatal error 1236 from master when reading data from binary log: 'The slave is connecting using CHANGE MASTER TO MASTER_AUTO_POSITION = 1, but the master has purged binary logs containing GTIDs that the slave requires.'
               Last_SQL_Errno: 0
               Last_SQL_Error:
                          ......
                Auto_Position: 1
1 row in set (0.00 sec)

```

### 5.4 忽略purged的部分，强行同步

那么实际生产应用当中，偶尔会遇到这样的情况：某个slave从备份恢复后（或者load data infile）后，DBA可以人为保证该slave数据和master一致；或者即使不一致，这些差异也不会导致今后的主从异常（例如：所有master上只有insert没有update）。这样的前提下，我们又想使slave通过replication从master进行数据复制。此时我们就需要跳过master已经被purge的部分，那么实际该如何操作呢？ 我们还是以实验一的情况为例：

先确认master上已经purge的部分。从下面的命令结果可以知道master上已经缺失`24024e52-bd95-11e4-9c6d-926853670d0b:1`这一条事务的相关日志.

```
master [localhost] {msandbox} (test) > show global variables like '%gtid%';
+---------------------------------+------------------------------------------+
| Variable_name                   | Value                                    |
+---------------------------------+------------------------------------------+
| binlog_gtid_simple_recovery     | OFF                                      |
| enforce_gtid_consistency        | ON                                       |
| gtid_executed                   | 24024e52-bd95-11e4-9c6d-926853670d0b:1-3 |
| gtid_mode                       | ON                                       |
| gtid_owned                      |                                          |
| gtid_purged                     | 24024e52-bd95-11e4-9c6d-926853670d0b:1   |
| simplified_binlog_gtid_recovery | OFF                                      |
+---------------------------------+------------------------------------------+
7 rows in set (0.00 sec)

```

在slave上通过`set global gtid_purged='xxxx'`的方式，跳过已经purge的部分.

```
slave2 [localhost] {msandbox} ((none)) > stop slave;
Query OK, 0 rows affected (0.04 sec)

slave2 [localhost] {msandbox} ((none)) > set global gtid_purged = '24024e52-bd95-11e4-9c6d-926853670d0b:1';
Query OK, 0 rows affected (0.05 sec)

slave2 [localhost] {msandbox} ((none)) > start slave;
Query OK, 0 rows affected (0.01 sec)

slave2 [localhost] {msandbox} ((none)) > show slave status\G                
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                          ......
              Master_Log_File: mysql-bin.000005
          Read_Master_Log_Pos: 359
               Relay_Log_File: mysql_sandbox21290-relay-bin.000004
                Relay_Log_Pos: 569
        Relay_Master_Log_File: mysql-bin.000005
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
                          ......
          Exec_Master_Log_Pos: 359
              Relay_Log_Space: 873
                          ......
             Master_Server_Id: 1
                  Master_UUID: 24024e52-bd95-11e4-9c6d-926853670d0b
             Master_Info_File: /data/mysql/rsandbox_mysql-5_6_23/node2/data/master.info
                    SQL_Delay: 0
          SQL_Remaining_Delay: NULL
      Slave_SQL_Running_State: Slave has read all relay log; waiting for the slave I/O thread to update it
                          ......
           Retrieved_Gtid_Set: 24024e52-bd95-11e4-9c6d-926853670d0b:2-3
            Executed_Gtid_Set: 24024e52-bd95-11e4-9c6d-926853670d0b:1-3
                Auto_Position: 1
1 row in set (0.00 sec)
```

可以看到此时slave已经可以正常同步，并补齐了 `24024e52-bd95-11e4-9c6d-926853670d0b:2-3` 范围的binlog日志.


## 参考:
[卢钧轶](http://cenalulu.github.io/mysql/mysql-5-6-gtid-basic/)
[官网建议](http://dev.mysql.com/doc/refman/5.6/en/replication-gtids-howto.html)
[MySQL 复制：GTIDS实现自动故障恢复](http://www.oschina.net/translate/mysql_replication_self_healing_recovery)
