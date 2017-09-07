# 数据库的选型
---
1. 响应时间   查询和操作请求ms级别返回
2. 数据总量   1年内数据量大约为1TB
3. 每秒请求量   每秒有1w次请求
4. 读写比    读写比为4:1
5. 重要程度    核心系统, p1级别故障

              数据具有时效性,历史数据访问较少,一般会处理最近15天数据, 数据记录总体长度约为1kb


1. TPS
2. IOPS
3. CPU
4. Memory
5. IO



1. 响应时间   查询和操作请求ms级别返回


2. 数据总量   1年内数据量大约为1TB

3. 每秒请求量   每秒有1w次请求


4. 读写比    读写比为4:1


5. 重要程度    核心系统, p1级别故障

1TB数据量,每秒产生的数据大约:
- 1. 每秒产生的数据为1kb*1024*1024*1024/(365*24*60*60) = 34kb/s

每秒1w次请求,读写比为4:1
读/s: 10000/5 *4 =8000/s qps 写2000/s  tps

数据记录长度为1kb:
每秒有34条插入. 


## Step1：1年内数据量大约1T
结果：每秒产生的数据量为1*1024*1024*1024/(365*24*60*60) = 34KB/s

## Step2：每秒1w次请求；读写比是4:1
结果：每秒读请求10000/5*4 = 8000/s；每秒写请求数10000/5*1 = 2000/s

## Step3：记录长度大约为1KB
结果：根据Step1得出的结果，每秒insert的数据写入大约为34/s；根据Step2得到的每秒写2000/s，可知1966/s为update和delete操作。由于MySQL数据读写操作按照页来处理，页大小为16KB，假设每次操作的页都不相同。那么每秒写操作数据量为：16KB*2000/s = 32M/s，每秒读操作数据量为：16KB*8000/s = 128M/s。

## Step4：处理最近15天内的数据
结果：热数据量为：(1*1024/365)*15 = 42GB。

## Step5：操作ms级返回
结果：操作ms级别返回，并且读压力更大，那么需要尽可能的将热数据加载到内存。按照内存命中率接近100%计算的话，那么Innodb buffer大约为42GB，而其他内存需求大概为1~2GB，因此内存超配大约为45GB。按照超配原则，写带宽（wBPS）限制为50MB/s；读带宽（rBPS）限制为150MB/s。


 1*1024*1024*512/(365*24*60*60)=17kb/s
读写: 30000/2=15000
insert=17/s  14983/update  page 16kb 16kb*15000  读写235mb/s

1*1=14Gb  250mb/s



有多少数据加载的内存的,一般的业务15%-20%来规划热数据，比如：用户中心，订单之类的常见业务。另外一些特殊点的业务，具体情况具体分析。当用户有500G数据时, 需要500G*15%放入内存.


## 1、《Inexpensive SSDs for Database Workloads》
随着SSD的成本不断降低，数据库机型如何选择以及如何更好的利用SSD。文中指出
，对于之前担心SSD的写寿命问题，现在来看完全没有必要担心，在过保期内，完全不会成为问题。而在选择SSD的容量和选型时，需要根据业务的DB压力情况来选择，SSD最终会降低机器的IO压力，整体性能。
       
在使用SSD的使用方面，文中指出从应用和数据库层面来优化，减少对SSD的写入，更好的保护和延长SSD的寿命。值得注意是：
1）DoubleWrite数据单独存放，并放在HDD上。DoubleWrite单独存放在以下内容中介绍，存放在HDD上，是由于DoubleWrite是顺序读写。
2）事务日志存放在HDD上。原因也是顺序读写，使用HDD和Raid卡cache即可。
3）binlog日志存放在HDD上。binlog的读写也是顺序的，使用HDD即可。
4）临时空间建议使用tmpfs，即系统的/tmp目录。临时目录写入频繁，且顺序读写较多。
5）BufferPool增大。这样可以提高内存命中率，减少磁盘IO。
6）innodb事务日志增大。SSD的读写性能，可以减少恢复的时间。
7）innodb使用压缩。通过压缩，减少写入的数据量。
8）使用高压缩比的存储引擎。更高的压缩比，可以更大程度的减少写入的数据量。
从个人角度来看，SSD的成本会高一些，但是由于提高了单机的性能，会减少机器的数量和机柜成本投入、以及运维成本，对于规模化运维来说，的确是利大于弊。SSD的使用方面，大多数可以值得借鉴，但有些需要根据自己的需求进行选择。例如：在单机多实例的情况下，连续IO操作也变成随机IO，放在HDD对性能的影响较大，这些在统一化部署过程中，很多都尝试并付出了惨痛的教训。

2、《Configuration of the Doublewrite Buffer》
MySQL引入DoubleWrite主要是为了避免BufferPool中的数据部分写入到磁盘，而导致无法数据恢复的问题。正常情况下，DoubleWrite引入会影响5%~10%的性能损失。然而，在写入压力较大时，写入DoubleWrite就会与BufferPool的随机写入产生竞争，性能影响就会加剧。
Percona Server引入DoubleWrite独立文件（参数innodb_doublewrite_file），从共用表空间中分离出来。由于DoubleWrite写入是顺序的，官方建议使用HDD存放，并且最好存放在独立磁盘空间下，也可以与redo日志放在相同磁盘下。

个人认为，目前情况下，DoubleWrite不会造成很大的性能损失，并且如果系统文件层能够保证数据完整性的话，可以禁用DoubleWrite。此外，该参数的引入，还需要充分的性能测试和验证。

## 参考资料
1、[《Inexpensive SSDs for Database Workloads》](http://www.mysqlperformanceblog.com/2013/10/03/inexpensive-ssds-database-workloads/)
2、[《Configuration of the Doublewrite Buffer》](http://www.percona.com/doc/percona-server/5.5/performance/innodb_doublewrite_path.html?id=percona-server:features:percona_innodb_doublewrite_path)
 


数据库压测相关

http://mp.weixin.qq.com/s?__biz=MzI4NTA1MDEwNg==&mid=401415451&idx=1&sn=12ea92a1e3fdc9fe7c0e03d6bf3cb155&scene=21#wechat_redirect


## 安装部署

### 源码编译
1. 必要的包和工具
2. 功能需要的包

## 功能定制
1. MySQL限流
2. 并行复制
3. ThreadPool-2

### 资源池管理
1. 资源管理
2. 实例管理:
   cpu,内存,IO管控--->cgroup等


###　Thread Pool
在Oracle MySQL版本中的Thread pool是通过plugin的方式实现的.


传统的mysql server的连接模式是`one-to-one`的thread和连接的对应的.
连接断开后，这个线程进入thread_cache或者直接退出（取决于thread_cache设置及系统当前已经cache的线程数目），one-thread-per-connection调度的好处是实现简单，而且能够在系统没有遇到瓶颈之前保证较小的响应时间，比较适合活跃的长连接的应用场景.


传统方式存在的问题:
1. 当大量的连接并行执行时,意味着将会占用比较多的执行cpu时间,会减少cpu的cache的命中率会下降, 会影响server的性能; 大量的连接会占用大量的内存,可能会导致使用swap.并发较大时，会导致通过临界资源时，产生大量的锁竞争。这些问题在系统层都很难解决，只能通过应用层解决。
2. Innodb mutex锁
在并发较大时，会引起Innodb的mutex锁争用。当前解决方法是通过innodb_thread_concurrency参数，但是该参数自身也存在锁争用，同样影响了MySQL的性能。在我们的优化历程中，也尝试通过优化该参数，来解决并发情况下，性能降低的问题。但是测试过程中发现，会有大量的连接等待kernel mutex锁，但是持续的压力会导致MySQL的thread running，最终导致MySQL不可用。
Thread pool主要从四个方面考虑：减少SQL并发，使得有足够的资源；使用线程组，独立管理；使用优先级队列，限制并发执行的事务；避免死锁。
在以上阐述的内容中，几乎涵盖了我们遇到的所有现象和问题，而性能影响会如此严重，是我们始料未及的。


而在大量短连接或者高并发情况下，one-thread-per-connection需要创建/调度大量的线程，产生较高的的context-switch代价，从而使得系统性能下降




## MySQL的日志系统

Error log
--log-warning  记录交互错误, 连接中断
问题诊断

规模化运维如何解决
- 日志汇总
- 日志监控


Binlog
format
sync_binlog =1

--binlog-do-db, --binlog-ignore-db(Master端)

--replicate-do-db --replicate-ignore-db(Slave)

reset Master(除非放弃, 否则永远不要用)

purge binary logs xxxx (先备份,再purge)

mysqlbinlog:
  --database 数据库级别过滤
  --start...stop
  --文件正则: mysql-bin.00000[0-9]*
  --table: 表级别过滤(官方不支持)

binlog恢复数据库:
  - 部分恢复: mysqlbinlog 过滤解析, 应用sql
  - 全量恢复: apply binlog

flashback (row format)

data stream

slowlog
long_query_time:
   0  记录所有sql,流量回放, sql采集等
   #

log-slow-admin-statements:

general log: Global级别
sql_log_off:
数据审计
执行轨迹



redo log

undo log

## MySQL运维工具
vmstat

r, si,so , in, cs

iostat:io
- avgqu-sz await svctm

mpstat: CPU状况
  sys usr iowait

ifstat: 网络
- in out

dstat:


mysqladmin 
  status
  -i
  -r
  debug
  extended-status

tcprstat -l ip -p3306 -t 1 -n 0


tcpdump -s0 -l -w- dst ip and port 3306 | strings

perf list: 显示性能事件
perf top: 实时显示性能统计信息
perf stat: 分析整体性能
perf record: 分析一段时间内的性能
perf report: 根据record记录, 分析报告


pt-stalk 抓现场
pt-stalk 

orzdba:

### 复制相关
正确的判断主从同步方式:

- 通过MySQL的复制的binlog的日志情况进行验证
io_thread 执行的位置是`master_log_file`, `read_master_log_pos`
sql_thread 执行的位置是`relay_master_log_file`, `exec_master_log_pos`

```
if(Master_Log_File == Relay_Master_Log_File) and (Read_Master_Log_Pos == Exec_Master_Log_Pos)

```
通常下IO_Thread线程不会有延迟,如果也需要判断这个延迟时:
```
master.log_file = slave.master_log_file = slave.relay_master_log_file
master.log_pos = slave.read_master_pos = slave.exec_master_log_pos
```

- 通过维护监控表来判断复制延迟.
可以在MASTER上维护一个监控表，一般只有两个字段(id和time)，存储这最新最新时间戳（高版本MySQL可以采用event_scheduler来更新，低版本可以用Linux cron结合自动循环脚本来更新），然后在SLAVE上读取该字段的时间，只要MASTER和SLAVE的系统时间【NTP是必须的】一致，即可快速知道SLAVE和MASTER延迟差了多少
```
# 注意两边是的时间设设置要一致, ntp
create table heart_beat(id int not null, d1 timestamp, primary key(id));
insert into heart_beat(d1) values(now());

#在Master上不停的发起下面命令:
update heart_beat set d1=now() where id = 1;

# slave
select d1 from heart_beat where id = 1;
```

在高并发的系统下，这个时间戳需要细化到毫秒，否则哪怕时间一致，也是有可能会延迟数个binlog event的。


- 读多写少:
  Master(WR) + Slaves (跨机房)
     |
     |
Master(R) ---  Slaves 级联一部分()

读少写多

Master(WR) + M(s) 跨机房

读写平均

M(WR) | M(R)

读一致性权衡:


历史数据的迁移


Sharding:
