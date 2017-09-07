# Linux系统的故障排查
---

##　硬件设备的故障

网卡故障
=====
- 1 诊断网卡故障
```shell
[root@localhost ~]#dmesg | grep eth
eth0:registered as PCnet/PCI II 79C970A
eth0:link up
eth0:no IPv6 routers present
[root@localhost ~]#
```
以上命令列出了引导信息中包含eth字符串的行，如果出现类似与“eth0:link up”的提示，表示Linux已经检测到了网卡，并处于正常工作状态。还有一条lspci命令可以列出系统检测到所有PCI设备，如果使用的网卡是PCI总线的，应该能看到这块网卡的信息。最后可以用ethtool查看以太网的链路连接是否正常。

```
[root@localhost ~]#ethtool eth0
Settings for eth0:
       Current message level: 0x00000007 (7)
       Link detected:yes
[root@localhost ~]#
```

如果看到“Link detected:yes”一行，表明网卡也对方的网络线路连接是正常的。

- 2 网卡驱动程序
在RHEL 6中，需要先查看或者设置/etc/modeprobe.cong文件，它包含了有关模块的安装和别名信息。
```
[root@localhost ~]#more /etc/modeprobe.cong 
alias scsi_hostadapter mptbase 
... 
alias eth0 pcnet32 
[root@localhost ~]#
```
以上显示中，最后一行“alias eth0 pcnet32”表示为pcnet32定义了一个别名eth0,也就是说，目前使用的以太网卡接口eth0对应的模块是pcnet32,可以使用一下命令当前系统装载的模块中是否有pcnet32模块。
```
[root@localhost 2.6.18-8.e15]#lsmod | grep pcnet32
pcnet32       35269      0
mii            9409      1   pcnet32 
[root@localhost 2.6.18-8.e15]#
```
可以发现，pcnet32已经安装。因此，如果网卡已经被Linux检测到，但执行“ipconfig -a”命令时却看不到eth0接口，可以按照以上方法把网卡的驱动程序模块找到，再看看这个模块是否已经安装。

