# Java的应用的故障排查
---
## Java进程CPU使用率高排查
生产java应用，CPU使用率一直很高，经常达到100%，通过以下步骤完美解决，分享一下。

1. `jps` 获取Java进程的PID。
2. `jstack pid >> java.txt` 导出CPU占用高进程的线程栈。
3. `top -H -p PID` 查看对应进程的哪个线程占用CPU过高。
4. `echo “obase=16; PID” `| bc 将线程的PID转换为16进制。` ps -mp 2633 -o THREAD,tid,time | sort -rn` 或者使用printf, 使用python
5. 在第二步导出的`Java.txt`中查找转换成为`16进制的线程PID`。找到对应的线程栈。
6. 分析负载高的线程栈都是什么业务操作。优化程序并处理问题。
