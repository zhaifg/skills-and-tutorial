# CentOS 7 与CentOS 6的配置
---

1. 非root用户的默认的单个程序打开的进程最大值从1024升级为4096.
  配置`/etc/security/limits.d/*-nproc.conf` ( /etc/security/limits.d/20-nproc.conf)
  命令 ulimit -u
2. export command 
3. 新的日志框架:journald, `systemd.hournald`. 
  可以收集: syslog信息, kernel信息, 初始化ram,disk和刚启动的信息, 可以发送到标准输出和标准错误
  /run/log/journal.  与rsyslog 同时存在
4. /etc/sysconfig/i18n to /etc/locale.conf and /etc/vconsole.conf.
5. hostname variable is defined in /etc/hostname
6. 升级的yum
  yum group/yum groups

7. /etc/ifconfig --> ip  
8. CGroup的改变: Control groups are now mounted under /sys/fs/cgroup instead of /cgroup.
9. Changes to mount options
10.  nmcli con edit a
11.  Firewalld configuration details are not stored in /etc/sysconfig/iptables. Instead, configuration details are stored in various files in the /usr/lib/firewalld and /etc/firewalld directories
12. Chrony is a new NTP client provided in the chrony package


## 相关命令
### device相关的的
lsblk 查看device信息都
blkid 查看device id等, device 信息
```
blkid 

blkid
/dev/xvda1: UUID="2cf9a36f-eafe-4f5a-ada1-cf3994dcd11f" TYPE="ext4" 
/dev/xvdb1: UUID="9c270a2f-5463-4261-81d8-594652cbbe66" TYPE="ext4"


 sudo blkid /dev/sda2 
/dev/sda2: UUID="RWTWxx-96Sq-1yO5-nUCW-z7hb-ofWn-6nhdsh" TYPE="LVM2_member"

~]# blkid -po udev /dev/vda1
ID_FS_UUID=7fa9c421-0054-4555-b0ca-b470a97a3d84
ID_FS_UUID_ENC=7fa9c421-0054-4555-b0ca-b470a97a3d84
ID_FS_VERSION=1.0
ID_FS_TYPE=ext4
ID_FS_USAGE=filesystem
```

### findmnt

显示当前的挂载的文件系统信息
findmnt -l
-t 文件系统类型 findmnt -t xfs

```
findmnt
TARGET                           SOURCE                         FSTYPE     OPTIONS
/                                /dev/mapper/centos_devops-root xfs        rw,relatime,seclabel,attr2,inode64,noquota
├─/sys                           sysfs                          sysfs      rw,nosuid,nodev,noexec,relatime,seclabel
│ ├─/sys/kernel/security         securityfs                     securityfs rw,nosuid,nodev,noexec,relatime
│ ├─/sys/fs/cgroup               tmpfs                          tmpfs      ro,nosuid,nodev,noexec,seclabel,mode=755
│ │ ├─/sys/fs/cgroup/systemd     cgroup                         cgroup     rw,nosuid,nodev,noexec,relatime,xattr,release_agent=/usr/lib/systemd/systemd-cgroups-agent,name=systemd
│ │ ├─/sys/fs/cgroup/hugetlb     cgroup                         cgroup     rw,nosuid,nodev,noexec,relatime,hugetlb
│ │ ├─/sys/fs/cgroup/cpu,cpuacct cgroup                         cgroup     rw,nosuid,nodev,noexec,relatime,cpuacct,cpu
│ │ ├─/sys/fs/cgroup/cpuset      cgroup                         cgroup     rw,nosuid,nodev,noexec,relatime,cpuset
│ │ ├─/sys/fs/cgroup/perf_event  cgroup                         cgroup     rw,nosuid,nodev,noexec,relatime,perf_event
│ │ ├─/sys/fs/cgroup/freezer     cgroup                         cgroup     rw,nosuid,nodev,noexec,relatime,freezer
│ │ ├─/sys/fs/cgroup/devices     cgroup                         cgroup     rw,nosuid,nodev,noexec,relatime,devices
│ │ ├─/sys/fs/cgroup/memory      cgroup                         cgroup     rw,nosuid,nodev,noexec,relatime,memory
│ │ ├─/sys/fs/cgroup/net_cls     cgroup                         cgroup     rw,nosuid,nodev,noexec,relatime,net_cls
│ │ └─/sys/fs/cgroup/blkio       cgroup                         cgroup     rw,nosuid,nodev,noexec,relatime,blkio
│ ├─/sys/fs/pstore               pstore                         pstore     rw,nosuid,nodev,noexec,relatime
│ ├─/sys/fs/selinux              selinuxfs                      selinuxfs  rw,relatime
│ ├─/sys/kernel/debug            debugfs                        debugfs    rw,relatime
│ └─/sys/kernel/config           configfs                       configfs   rw,relatime
├─/proc                          proc                           proc       rw,nosuid,nodev,noexec,relatime
│ ├─/proc/sys/fs/binfmt_misc     systemd-1                      autofs     rw,relatime,fd=35,pgrp=1,timeout=300,minproto=5,maxproto=5,direct
│ └─/proc/fs/nfsd                nfsd                           nfsd       rw,relatime
├─/dev                           devtmpfs                       devtmpfs   rw,nosuid,seclabel,size=484800k,nr_inodes=121200,mode=755
│ ├─/dev/shm                     tmpfs                          tmpfs      rw,nosuid,nodev,seclabel
│ ├─/dev/pts                     devpts                         devpts     rw,nosuid,noexec,relatime,seclabel,gid=5,mode=620,ptmxmode=000
│ ├─/dev/mqueue                  mqueue                         mqueue     rw,relatime,seclabel
│ └─/dev/hugepages               hugetlbfs                      hugetlbfs  rw,relatime,seclabel
├─/run                           tmpfs                          tmpfs      rw,nosuid,nodev,seclabel,mode=755
│ └─/run/user/1000               tmpfs                          tmpfs      rw,nosuid,nodev,relatime,seclabel,size=100032k,mode=700,uid=1000,gid=1000
├─/var/lib/nfs/rpc_pipefs        sunrpc                         rpc_pipefs rw,relatime
└─/boot                          /dev/sda1                      xfs        rw,relatime,seclabel,attr2,inode64,noquota
```


### lspci
查看pci信息
lspci -v/ -vv

### lsusb

### lscpu

### rasdaemon
centos7 关于硬件错误的记录的程序
yum install rasdaemon


### net-snmp
```
yum install net-snmp net-snmp-libs net-snmp-utils
```

一些常见操作见文档
[snmp](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/System_Administrators_Guide/sect-System_Monitoring_Tools-Net-SNMP.html)


### openlmi
```
yum install tog-pegasus
yum install openlmi-{storage,networking,service,account,powermanagement}

# 配置用户访问
/etc/Pegasus/access.conf

passwd pegasus

systemctl start tog-pegasus.service

firewall-cmd --add-port 5989/tcp
firewall-cmd --permanent --add-port 5989/tcp

# client 端 
yum install openlmi-tools

```

配置ssl连接见文档


#### lmishell


### 文件系统

EXT4:
备份分区信息
dump

e2label /dev/sda1 /boot1
restore -rf /backup-files/sda1.dump
