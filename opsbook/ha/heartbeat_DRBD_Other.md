# heartbeat DRBD与其他的软件的高可用
---
## heartbeat_DRBD_NFS

### 1.系统规划

### 2.安装前配置
1. 时间同步
2. iptables与selinux

### 3.安装heartbeat

### 4.安装DRBD与配置硬盘的同步

### 5.安装NFS与配置NFS
```
yum install nfs-utils rpcbind
vim /etc/exports

```

### 6.整合三个软件
设置heartbeat的/etc/ha.d/haresource文件
```
yimiwork_215 IPaddr::192.168.8.220/24/eth0 drbddisk::drbd Filesystem::/dev/drbd1::/data::ext4 killnfsd
```

### 7.killnfsd脚本以及增加应用监控脚本

__killnfsd脚本文件的作用：__
1. drbd主备切换时，若nfs没有启动，则此脚本会把nfs启动
2. drbd主备切换时，若nfs已启动，则此脚本会重启nfs服务，因为NFS服务切换后，必须重新mount一下nfs共享出来的目录，否则会出现stale NFS file handle的错误


`vim /etc/ha.d/resource.d/killnfsd`
```bash
#!/bin/bash
killall -9 nfsd; /etc/init.d/nfs restart; exit 0
```
`chmod 755 /etc/ha.d/resource.d/killnfsd`

### 8.注意事项
1. nfs,heartbeat,drbd建议不要设置成开启自动启动;需要手工启动,避免数据不一致
2. 启动时, 需要先启动drbd,再启动heartbeat. 不然,heartbeat配置会有错误
3. 当故障时,修复时heartbeat不要重新抢夺资源.
4. heartbeat仅仅是一个心跳转换软件,不能对应用软件进行监控, 需要手动检测应用状态
5. drbd-8.4新版本中,启动drbd并加载到内核使用`/etc/init.d/drbd`, 直接modprobe drbd时,drbd启动时会失败.

### 9.测试
#### 9.1 启动drbd

#### 9.2 启动heartbeat

#### 9.3 客户端挂载nfs

#### 9.4 关掉主的电源
nfs的成功切换
#### 9.5 停掉drbd
1. heartbeat不能切换, 因为hearteat没有监控功能
2. 配置drbd的handler处理, 失去连接等处理
3. 自己写脚本处理,重启
```
#vi /opt/monitor/nfs/monitornfs.sh
#!/bin/bash
#监控nfs服务的运行情况
 
while true
do
    drbdstatus=`cat /proc/drbd 2> /dev/null  | grep ro | tail -n1 | awk -F':' '{print $4}' | awk -F'/' '{print $1}'`   #判断drbd的状态
    nfsstatus=`/etc/init.d/nfs status | grep -c running`    #判断nfs是否运行
 
    if [ -z  $drbdstatus ];then
        sleep 10
        continue
    elif [ $drbdstatus == 'Primary' ];then     #若drbd是Primary状态
        if [ $nfsstatus -eq 0 ];then           #若nfs未运行
            /etc/init.d/nfs start &> /dev/null   #启动nfs服务
            /etc/init.d/nfs start &> /dev/null
            newnfsstatus=`/etc/init.d/nfs status | grep -c running`     #再次判断nfs是否成功启动
            if [ $newnfsstatus -eq 0 ];then         #若nfs未运行,也就是无法启动
                /etc/init.d/heartbeat  stop &> /dev/null        #将heartbeat服务stop掉，目的是自动切换到另一台备用机
                /etc/init.d/heartbeat  stop &> /dev/null
            fi
        fi
    fi
    sleep 5
done
 
 
##注意：不要将此监控脚本放到/data/目录下，挂载drbd设备时，会把此脚本覆盖掉
 
chmod  u+x /opt/monitor/nfs/monitornfs.sh
nohup bash /opt/monitor/nfs/monitornfs.sh &     #放在后台运行
##别忘了设置开机自动启动
```

### 9.6 模拟脑裂

把主节点的eth1关掉（ifdown eth1），再把eth1启动（ifup eth1）,此时两个节点都变成了StandAlone状态
```
##解决脑裂的方法
##备用节点：
[root@dbm134 ~]# drbdadm secondary r0
[root@dbm134 ~]# drbdadm disconnect all
[root@dbm134 ~]# drbdadm -- --discard-my-data connect r0 
 
##主节点：
[root@dbm135 ~]# drbdadm disconnect all
[root@dbm135 ~]# drbdadm connect r0
[root@dbm135 ~]# drbdsetup /dev/drbd0 primary
[root@dbm135 ~]# mount /dev/drbd0 /data/
```
__注意__：
>在解决脑裂时，把上面所有步骤都操作完后，有时候客户端会挂载正常，有时候则挂载不正常；若不正常，可以尝试把主节点的heartbeat服务重启一下

## heartbeat_DRBD_MySQL

### 1. 时间同步
### 2. iptables与selinux

### 3.安装heartbeat

### 4.安装DRBD与配置硬盘的同步

### 5.安装MySQL,配置MySQL
1. 安装MySQL
2. 设置MySQL的data和binlog目录等到drbd所指定的路径
3. 初始化,若已初始化, rsync目录到drbd资源目录
4. 整合配置
```
yimiwork_215 IPaddr::192.168.8.220/24/eth0 drbddisk::drbd:: Filesystem::/dev/drbd1::/data::ext4 mysqld
```
