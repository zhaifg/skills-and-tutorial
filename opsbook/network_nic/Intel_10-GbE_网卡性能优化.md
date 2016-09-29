#Intel 10-GbE 网卡性能优化
---

这是一篇翻译文档，原文请见：http://dak1n1.com/blog/7-performance-tuning-intel-10gbe

默认情况下，Linux网络被配置成最佳可用性状态，但不是最佳性能状态。对于一个10GbE的网卡来讲，这是尤其明显的。内核的 send/recv 缓冲区，tcp堆栈的内存分配策略和 数据包的队列都设置的太小，以至于它们不能工作在最佳的性能状态。下面所做的一些测试和优化，希望能够给你的网卡带来一定的性能提升。

在Intel ixgb的驱动文档中，描述了三个可以优化的策略。从性能优化的提升能力上进行排序如下：

1．在服务器和交换机之间允许大帧传输
2．用sysctl来优化内核配置
3．用setpci来优化网卡的PCI配置

需要明确的是，上述优化列表仅仅是一些建议。大多数优化工作是调整一些（个）配置，然后进行压力测试来检查优化是否生效。因此，大家得到的结果可能是多种多样的。

在开始任何压力测试前，我们往往需要禁止掉 irqbanlace 和 cpuspeed。这样做可以让我们获得最大的网络吞吐量以得到最好的压力测试结果。
```
service irqbalance stop
service cpuspeed stop
chkconfig irqbalance off
chkconfig cpuspeed off
```
## （一）允许大帧数据传输

在linux系统中，配置大帧数据传输仅仅需要一条命令，或是在网卡的配置文件增加一行。

ifconfig eth2 mtu 9000 txqueuelen 1000 up
如果要让这个配置持久化，可以在网卡的配置文件中增加MTU的新值，将“eth2”换成你自己的网卡名字：
```
vim /etc/sysconfig/network-scripts/ifcfg-eth2

MTU=”9000″
```
## （二）Linux内核 sysctl 配置

在linux系统中有很多重要的配置会影响网络的性能。下面的这些配置项来源于 2008 Red Hat峰会  Mark Wagner的精彩的演讲 (http://www.redhat.com/promo/summit/2008/downloads/pdf/Thursday/Mark_Wagner.pdf )

核心的内存配置：
```
net.core.rmem_max –  max size of rx socket buffer

net.core.wmem_max – max size of tx socket buffer

net.core.rmem_default – default rx size of socket buffer

net.core.wmem_default – default tx size of socket buffer

net.core.optmem_max – maximum amount of option memory

net.core.netdev_max_backlog – how many unprocessed rx packets before kernel starts to drop them
```
下面是我修改后的 /etc/sysctl.conf 文件，可以把它添加到默认的配置后面：
```
 # — tuning — #

# Increase system file descriptor limit

fs.file-max = 65535

 

# Increase system IP port range to allow for more concurrent connections

net.ipv4.ip_local_port_range = 1024 65000

 

# — 10gbe tuning from Intel ixgb driver README — #

 

# turn off selective ACK and timestamps

net.ipv4.tcp_sack = 0

net.ipv4.tcp_timestamps = 0

 

# memory allocation min/pressure/max.

# read buffer, write buffer, and buffer space

net.ipv4.tcp_rmem = 10000000 10000000 10000000

net.ipv4.tcp_wmem = 10000000 10000000 10000000

net.ipv4.tcp_mem = 10000000 10000000 10000000

 

net.core.rmem_max = 524287

net.core.wmem_max = 524287

net.core.rmem_default = 524287

net.core.wmem_default = 524287

net.core.optmem_max = 524287

net.core.netdev_max_backlog = 300000
```
##（三）PCI 总线优化

如果你考虑让你的优化工作进一步深入，还可以针对该网卡插入的PCI总线进行调整。首先，需要找到要调整的PCI总线地址，通过lspci命令获取：
```
[chloe@biru ~]$ lspci

07:00.0 Ethernet controller: Intel Corporation 82599EB 10-Gigabit SFI/SFP+ Network Connection (rev 01)
```
这里的07:00.0 就是PCI总线的地址。现在我们可以在 /proc/bus/pci/devices里面找到更多的信息：
```
[chloe@biru ~]$ grep 0700 /proc/bus/pci/devices

0700    808610fb        28       d590000c       0        ecc1    0   d58f800c  0  0      80000    0    20  0   4000   0    0        ixgbehttp://dak1n1.com/blog/7-performance-tuning-intel-10gbe
```
正如我们看到的这样，各种PCI设备的信息就显示出来了。不过，我们最关注的数据在第二列，808610fb。这是设备的供应商ID和设备ID的组合。供应商ID：8086，设备ID：10fb。我们可以使用这些值来优化PCI总线的MMRBC（Maximum Memory Read Byte Count）。

下面的命令可以提升MMRBC到 4k 的读，提升总线上对爆发增长的处理能力。

`setpci -v -d 8086:10fb e6.b=2e`
关于这条命令：

-d 选项指明网卡在PCI-X总线结构上的位置

e6.b 是 PCI-X 命令的寄存器地址

2e是要配置值

下面是这个寄存器的其他可用值（尽管上面已经列出了一个，2e，是Intel ixgbe文档中推荐的配置值）
```
MM  value in bytes

22  512 (default)

26  1024

2a  2048

2e  4096
 
```
测试：

测试往往是在每一项配置调整的时候都要进行的，不过，我这里为了简洁仅仅展示一下优化前和优化后的结果对比。使用的压力测试工具是 “iperf”和 “netperf”

下面是 10GbE 网卡在优化前可能的性能状态：
```
 [  3]  0.0-100.0 sec   54.7 GBytes  4.70 Gbits/sec

 

bytes  bytes   bytes    secs.    10^6bits/sec

87380 16384 16384    60.00    5012.24
```
优化后：
```
 [  3]  0.0-100.0 sec   115 GBytes  9.90 Gbits/sec

 

bytes  bytes   bytes    secs.    10^6bits/sec

10000000 10000000 10000000    30.01    9908.08
```
哇！优化后带来非常巨大的变化。这是我花了几个小时候在我的HDFS集群中所看到的最好的结论。无论你的应用程序是怎样的，这些优化都应该很适合你。

## 参考
[香草的技术博客](http://blog.chunshengster.me/2013/11/intel_10_gbe_nic_performance_tunning.html)
