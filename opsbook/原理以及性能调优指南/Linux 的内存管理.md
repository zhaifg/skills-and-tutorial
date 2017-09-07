# Linux 的内存管理
---

## 从free开始

在内存够用时，内核的思路是，如何尽量提高资源的利用效率，以加快系统整体响应速度和吞吐量？于是内存作为一个CPU和I／O之间的大buffer的功能就呼之欲出了。为此，内核设计了以下系统来做这个功能：
###Buffers／Cached
buffer和cache是两个在计算机技术中被用滥的名词，放在不通语境下会有不同的意义。在内存管理中，我们需要特别澄清一下，这里的buffer指Linux内存的：Buffer cache。这里的cache指Linux内存中的：Page cache。翻译成中文可以叫做缓冲区缓存和页面缓存。在历史上，它们一个（buffer）被用来当成对io设备写的缓存，而另一个（cache）被用来当作对io设备的读缓存，这里的io设备，主要指的是块设备文件和文件系统上的普通文件。但是现在，它们的意义已经不一样了。在当前的内核中，page cache顾名思义就是针对内存页的缓存，说白了就是，如果有内存是以page进行分配管理的，都可以使用page cache作为其缓存来使用。当然，不是所有的内存都是以页（page）进行管理的，也有很多是针对块（block）进行管理的，这部分内存使用如果要用到cache功能，则都集中到buffer cache中来使用。（从这个角度出发，是不是buffer cache改名叫做block cache更好？）然而，也不是所有块（block）都有固定长度，系统上块的长度主要是根据所使用的块设备决定的，而页长度在X86上无论是32位还是64位都是4k。

## free buffer/cached
Buffers are associated with a specific block device, and cover caching of filesystem metadata as well as tracking in-flight pages. The cache only contains parked file data. That is, the buffers remember what's in directories, what file permissions are, and keep track of what memory is being written from or read to for a particular block device. The cache only contains the contents of the files themselves.


Short answer: Cached is the size of the page cache. Buffers is the size of in-memory block I/O buffers. Cached matters; Buffers is largely irrelevant.

Long answer: Cached is the size of the Linux page cache, minus the memory in the swap cache, which is represented by SwapCached (thus the total page cache size is Cached + SwapCached). Linux performs all file I/O through the page cache. Writes are implemented as simply marking as dirty the corresponding pages in the page cache; the flusher threads then periodically write back to disk any dirty pages. Reads are implemented by returning the data from the page cache; if the data is not yet in the cache, it is first populated. On a modern Linux system, Cached can easily be several gigabytes. It will shrink only in response to memory pressure. The system will purge the page cache along with swapping data out to disk to make available more memory as needed.

Buffers are in-memory block I/O buffers. They are relatively short-lived. Prior to Linux kernel version 2.4, Linux had separate page and buffer caches. Since 2.4, the page and buffer cache are unified and Buffers is raw disk blocks not represented in the page cache—i.e., not file data. The Buffers metric is thus of minimal importance. On most systems, Buffers is often only tens of megabytes.


## buffer/cached 全都可以回收吗

## 其他的内存命令
vmstat
proc/meminfo

slab
共享内存 ipcs -m



[root@yimiwork_215 ~]# free -m
             total       used       free     shared    buffers     cached
Mem:          1869       1624        244          0        258        505
-/+ buffers/cache:        861       1008
Swap:         3999         43       3956


[root@yimiwork_215 ~]# free -m
             total       used       free     shared    buffers     cached
Mem:          1869       1625        244          0        258        505
-/+ buffers/cache:        861       1008
Swap:         3999         43       3956

[root@yimiwork_215 ~]# free -m
             total       used       free     shared    buffers     cached
Mem:          1869       1790         78          0        140        834
-/+ buffers/cache:        815       1053
Swap:         3999        100       3899
