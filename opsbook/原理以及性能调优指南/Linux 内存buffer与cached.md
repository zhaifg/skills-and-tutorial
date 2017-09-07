# Linux free命令的bufferd与cached
---
Short answer: **Cached** is the size of the page cache. **Buffers** is the size of in-memory block I/O buffers. **Cached** matters; **Buffers** is largely irrelevant.

Long answer: Cached is the size of the Linux page cache, minus the memory in the swap cache, which is represented by SwapCached (thus the total page cache size is Cached + SwapCached). Linux performs all file I/O through the page cache. Writes are implemented as simply marking as dirty the corresponding pages in the page cache; the flusher threads then periodically write back to disk any dirty pages. Reads are implemented by returning the data from the page cache; if the data is not yet in the cache, it is first populated. On a modern Linux system, Cached can easily be several gigabytes. It will shrink only in response to memory pressure. The system will purge the page cache along with swapping data out to disk to make available more memory as needed.

Buffers are in-memory block I/O buffers. They are relatively short-lived. Prior to Linux kernel version 2.4, Linux had separate page and buffer caches. Since 2.4, the page and buffer cache are unified and Buffers is raw disk blocks not represented in the page cache—i.e., not file data. The Buffers metric is thus of minimal importance. On most systems, Buffers is often only tens of megabytes.



The "cached" total will also include some other memory allocations, such as any tmpfs filesytems. To see this in effect try:
```
mkdir t
mount -t tmpfs none t
dd if=/dev/zero of=t/zero.file bs=10240 count=10240
sync; echo 3 > /proc/sys/vm/drop_caches; free -m
umount t
sync; echo 3 > /proc/sys/vm/drop_caches; free -m
```
and you will see the "cache" value drop by the 100Mb that you copied to the ram-based filesystem (assuming there was enough free RAM, you might find some of it ended up in swap if the machine is already over-committed in terms of memory use). The "sync; echo 3 > /proc/sys/vm/drop_caches" before each call to free should write anything pending in all write buffers (the sync) and clear all cached/buffered disk blocks from memory so free will only be reading other allocations in the "cached" value.

The RAM used by virtual machines (such as those running under VMWare) may also be counted in free's "cached" value, as will RAM used by currently open memory-mapped files (this will vary depending on the hypervisor/version you are using and possibly between kernel versions too).

So it isn't as simple as "buffers counts pending file/network writes and cached counts recently read/written blocks held in RAM to save future physical reads", though for most purposes this simpler description will do.
[Linux内存中的Cache真的能被回收么](http://liwei.life/2016/04/26/linux%E5%86%85%E5%AD%98%E4%B8%AD%E7%9A%84cache%E7%9C%9F%E7%9A%84%E8%83%BD%E8%A2%AB%E5%9B%9E%E6%94%B6%E4%B9%88%EF%BC%9F/)
[](https://www.quora.com/What-is-the-major-difference-between-the-buffer-cache-and-the-page-cache#)
[](https://www.quora.com/What-is-the-difference-between-Buffers-and-Cached-columns-in-proc-meminfo-output)
