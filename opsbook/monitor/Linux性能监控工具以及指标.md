# Linux性能监控工具以及指标
---

## CPU
### 1.良好状态的指标
  * cpu利用率: User Time <= 70%, System Time <= 35%, User Time + System Time < = 70%
  * 上下文切换: 与cpu利用率有关, 如果cpu利用率良好, 大量的上下文切换也是可以接受的.
  * 可运行队列: 每个处理器的可运行队列<=3.

### 工具
#### top
```
top - 13:42:43 up 294 days, 13:23,  1 user,  load average: 1.46, 0.85, 0.49
Tasks: 364 total,   2 running, 362 sleeping,   0 stopped,   0 zombie
Cpu(s):  4.9%us,  0.2%sy,  0.0%ni, 94.6%id,  0.3%wa,  0.0%hi,  0.0%si,  0.0%st
Mem:  65973180k total, 65523672k used,   449508k free,    56300k buffers
Swap:        0k total,        0k used,        0k free, 12083084k cached

  PID USER      PR  NI  VIRT  RES  SHR S %CPU %MEM    TIME+  COMMAND
20829 mysql     20   0 56.9g  50g 7328 S 15.7 79.5   2020:57 mysqld     
  106 root      20   0     0    0    0 R  2.0  0.0 213:34.66 kblockd/0  
13459 root      20   0  309m 9456 2196 S  2.0  0.0 426:50.47 AliHids    
    1 root      20   0 19356 1176  876 S  0.0  0.0   0:00.89 init     
    2 root      20   0     0    0    0 S  0.0  0.0   0:00.01 kthreadd 
    3 root      RT   0     0    0    0 S  0.0  0.0   1:14.40 migration/0
    4 root      20   0     0    0    0 S  0.0  0.0   7:44.69 ksoftirqd/0
    5 root      RT   0     0    0    0 S  0.0  0.0   0:00.00 migration/0
    6 root      RT   0     0    0    0 S  0.0  0.0   0:32.10 watchdog/0
    7 root      RT   0     0    0    0 S  0.0  0.0   1:54.07 migration/1
    8 root      RT   0     0    0    0 S  0.0  0.0   0:00.00 migration/1
    9 root      20   0     0    0    0 S  0.0  0.0   5:27.35 ksoftirqd/1
   10 root      RT   0     0    0    0 S  0.0  0.0   0:22.91 watchdog/1
   11 root      RT   0     0    0    0 S  0.0  0.0   2:25.19 migration/2
   12 root      RT   0     0    0    0 S  0.0  0.0   0:00.00 migration/2
```
第一行后面的三个值是系统在之前1、5、15的平均负载，也可以看出系统负载是上升、平稳、下降的趋势，当这个值超过CPU可执行单元的数目，则表示CPU的性能已经饱和成为瓶颈了。

第二行统计了系统的任务状态信息。running很自然不必多说，包括正在CPU上运行的和将要被调度运行的；sleeping通常是等待事件(比如IO操作)完成的任务，细分可以包括interruptible和uninterruptible的类型；stopped是一些被暂停的任务，通常发送SIGSTOP或者对一个前台任务操作Ctrl-Z可以将其暂停；zombie僵尸任务，虽然进程终止资源会被自动回收，但是含有退出任务的task descriptor需要父进程访问后才能释放，这种进程显示为defunct状态，无论是因为父进程提前退出还是未wait调用，出现这种进程都应该格外注意程序是否设计有误。

第三行CPU占用率根据类型有以下几种情况：
- `(us) user`: CPU在低nice值(高优先级)用户态所占用的时间(nice<=0)。正常情况下只要服务器不是很闲，那么大部分的CPU时间应该都在此执行这类程序
- `(sy) system`: CPU处于内核态所占用的时间，操作系统通过系统调用(system call)从用户态陷入内核态，以执行特定的服务；通常情况下该值会比较小，但是当服务器执行的IO比较密集的时候，该值会比较大
- `(ni) nice`: CPU在高nice值(低优先级)用户态以低优先级运行占用的时间(nice>0)。默认新启动的进程nice=0，是不会计入这里的，除非手动通过renice或者setpriority()的方式修改程序的nice值
- `(id) idle`: CPU在空闲状态(执行kernel idle handler)所占用的时间
- `(wa) iowait`: 等待IO完成做占用的时间
- `(hi) irq`: 系统处理硬件中断所消耗的时间
- `(si) softirq`: 系统处理软中断所消耗的时间，记住软中断分为softirqs、tasklets(其实是前者的特例)、work queues，不知道这里是统计的是哪些的时间，毕竟work queues的执行已经不是中断上下文了
- `(st) steal`: 在虚拟机情况下才有意义，因为虚拟机下CPU也是共享物理CPU的，所以这段时间表明虚拟机等待hypervisor调度CPU的时间，也意味着这段时间hypervisor将CPU调度给别的CPU执行，这个时段的CPU资源被”stolen”了。这个值在我KVM的VPS机器上是不为0的，但也只有0.1这个数量级，是不是可以用来判断VPS超售的情况？

CPU占用率高很多情况下意味着一些东西，这也给服务器CPU使用率过高情况下指明了相应地排查思路：
　　(a) 当user占用率过高的时候，通常是某些个别的进程占用了大量的CPU，这时候很容易通过top找到该程序；此时如果怀疑程序异常，可以通过perf等思路找出热点调用函数来进一步排查；
　　(b) 当system占用率过高的时候，如果IO操作(包括终端IO)比较多，可能会造成这部分的CPU占用率高，比如在file server、database server等类型的服务器上，否则(比如>20%)很可能有些部分的内核、驱动模块有问题；
　　(c) 当nice占用率过高的时候，通常是有意行为，当进程的发起者知道某些进程占用较高的CPU，会设置其nice值确保不会淹没其他进程对CPU的使用请求；
　　(d) 当iowait占用率过高的时候，通常意味着某些程序的IO操作效率很低，或者IO对应设备的性能很低以至于读写操作需要很长的时间来完成；
　　(e) 当irq/softirq占用率过高的时候，很可能某些外设出现问题，导致产生大量的irq请求，这时候通过检查/proc/interrupts文件来深究问题所在；
　　(f) 当steal占用率过高的时候，黑心厂商虚拟机超售了吧！

　　第四行和第五行是物理内存和虚拟内存(交换分区)的信息:
　　total = free + used + buff/cache，现在buffers和cached Mem信息总和到一起了，但是buffers和cached
Mem的关系很多地方都没说清楚。其实通过对比数据，这两个值就是/proc/meminfo中的Buffers和Cached字段：Buffers是针对raw disk的块缓存，主要是以raw block的方式缓存文件系统的元数据(比如超级块信息等)，这个值一般比较小(20M左右)；而Cached是针对于某些具体的文件进行读缓存，以增加文件的访问效率而使用的，可以说是用于文件系统中文件缓存使用。
　　而avail Mem是一个新的参数值，用于指示在不进行交换的情况下，可以给新开启的程序多少内存空间，大致和free + buff/cached相当，而这也印证了上面的说法，free + buffers + cached Mem才是真正可用的物理内存。并且，使用交换分区不见得是坏事情，所以交换分区使用率不是什么严重的参数，但是频繁的swap in/out就不是好事情了，这种情况需要注意，通常表示物理内存紧缺的情况。

　　最后是每个程序的资源占用列表，其中CPU的使用率是所有CPU core占用率的总和。通常执行top的时候，本身该程序会大量的读取/proc操作，所以基本该top程序本身也会是名列前茅的。
　　top虽然非常强大，但是通常用于控制台实时监测系统信息，不适合长时间(几天、几个月)监测系统的负载信息，同时对于短命的进程也会遗漏无法给出统计信息。


#### htop

#### mpstat
* `mpstat -P ALL 1`
#### sar

#### vmstat




## 参考
http://techblog.netflix.com/2015/11/linux-performance-analysis-in-60s.html
http://man7.org/linux/man-pages/man5/proc.5.html
http://blog.scoutapp.com/articles/2015/02/24/understanding-linuxs-cpu-stats
https://yq.aliyun.com/articles/6047
https://wiki.mikejung.biz/Performance_Analysis
https://www.linux.com/learn/uncover-meaning-tops-statistics
https://taozj.org/201701/linux-performance-basic.html?hmsr=toutiao.io&utm_medium=toutiao.io&utm_source=toutiao.io
