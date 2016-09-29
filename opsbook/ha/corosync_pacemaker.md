# corosync与PaceMaker基于nginx的web高可用的实例学习

(2).软件环境
corosync-1.4
pacemaker-1.x

## 1. 架构环境
|主机名| 应用IP|数据IP|功能|VIP|
|---|---|---|---|---|
|yimiwork_215|192.168.8.215|192.168.80.215|primary|192.168.8.220|
|yimiwork_216|192.168.8.216|192.168.80.216|standby|192.168.8.220|
|yimiwork_nfs|192.168.8.200||nfs /data||

## 2. 主机名配置及解析
## 3. ssh互信
## 4. iptables,selinux
## 5. 安装
### 5.1 设置crmsh的源
```
[haclustering]
name=HA Clustering
baseurl=http://download.opensuse.org/repositories/network:/ha-clustering:/Stable/CentOS_CentOS-6/
enabled=1
gpgcheck=0
```
### 5.2 安装
```
yum install pacemaker corosync crmsh
```

## 6. 配置corosync
### 6.1 编辑corosync.conf
```
cd  /etc/corosync
mv corosync.conf.example corosync.conf

```
`vim corosync.conf`
```
# Please read the corosync.conf.5 manual page
compatibility: whitetank

totem {
        version: 2
        secauth: on  #启用验证
        threads: 2  # 线程的个数

        interface {
                ringnumber: 0
#                member {
#                    memberaddr: 192.168.80.215
#                }
#                member {
#                    memberaddr: 192.168.80.216
#                }

    
                bindnetaddr: 192.168.80.0 # 绑定的网段
                mcastaddr: 239.255.10.1 # 组播地址
                mcastport: 5405
                ttl: 1
        }
}

logging {
        fileline: off
        to_stderr: no
        to_logfile: yes
        logfile: /var/log/cluster/corosync.log
        to_syslog: yes
        debug: off
        timestamp: on
        logger_subsys {
                subsys: AMF
                debug: off
        }
}

amf {
    mode: disabled
}

aisexec {
    user: root
    group: root
}

```
### 6.2 启用Pacemaker
`vim service.d/pcmk`
```
service {
   name: pacemaker
   ver: 0
}

```

### 6.3 生成密钥文件
注：corosync生成key文件会默认调用/dev/random随机数设备，一旦系统中断的IRQS的随机数不够用，将会产生大量的等待时间，因此，为了节约时间，我们在生成key之前讲random替换成urandom，以便节约时间。
```
[root@yimiwork_215 corosync]# mv /dev/{random,random.bak}  
[root@yimiwork_215 corosync]# ln -s /dev/urandom /dev/random
[root@yimiwork_215 corosync]# corosync-keygen  
Corosync Cluster Engine Authentication key generator.  
Gathering 1024 bits for key from /dev/random.  
Press keys on your keyboard to generate entropy.  
Writing corosync key to /etc/corosync/authkey.
```
###  6.4 查看生成的key文件
```
[root@yimiwork_215 corosync]# ll 
总用量 24  
-r-------- 1 root root  128 8月  13 14:16 authkey  
-rw-r--r-- 1 root root  521 8月  13 11:11 corosync.conf  
-rw-r--r-- 1 root root  445 5月  15 05:09 corosync.conf.example  
-rw-r--r-- 1 root root 1084 5月  15 05:09 corosync.conf.example.udpu  
drwxr-xr-x 2 root root 4096 5月  15 05:09 service.d  
drwxr-xr-x 2 root root 4096 5月  15 05:09 uidgid.d
```
### 6.5 将key文件authkey与配置文件corosync.conf复制到yimiwork_216上

## 7. 启动corosync
```
/etc/init.d/corosync start
```
### 7.1 查看启动日志
```
less /var/log/cluster/corosync.log
```
### 7.2 查看心跳状态
```

```

### 7.3 查看状态
```
[root@yimiwork_215 ~]# crm_mon
Last updated: Tue Aug 13 17:41:31 2013 
Last change: Tue Aug 13 14:20:40 2013 via crmd on yimiwork_215  
Stack: classic openais (with plugin)  
Current DC: yimiwork_216 - partition with quorum  
Version: 1.1.8-7.el6-394e906  
2 Nodes configured, 2 expected votes  
0 Resources configured.
Online: [ yimiwork_215 yimiwork_216 ]
```
注：大家可以看到，集群运行正常，yimiwork_215与yimiwork_216都在线，DC是yimiwork_216节点。但是还没有配置资源，配置资源就要用到pacemaker.



## 8. 利用crmsh对pacemaker与corosync进行配置

### 8.1 Pacemaker 配置资源方法
* (1).命令配置方式
  - crmsh
  - pcs
* (2).图形配置方式
  - pygui
  - hawk
  - LCMC
  - pcs

注：
> 本文主要的讲解的是crmsh


##  9.crmsh 简单说明
注：以下上pacemaker 1.1.8的更新说明，最重要的我用红色标记出来，从pacemaker 1.1.8开始，crm sh 发展成一个独立项目，pacemaker中不再提供，说明我们安装好pacemaker后，是不会有crm这个命令行模式的资源管理器的。

### 9.1 crmsh的基本使用
crmsh的配置方式类似于路由器交换机的配置方式.crm命令进入crmsh的配置界面
```
[root@yimiwork_215 ~]# crm 
crm(live)# help # 使用help或者?进行查询命令

crm(live)#configure    #输入configure就会进入，configure模式下， 
crm(live)configure#    #敲两下tab键就会显示configure下全部命令  
```

###(0) 查询命令的使用方式
```
crm(live)configure# help node
Define a cluster node

The node command describes a cluster node. Nodes in the CIB are
commonly created automatically by the CRM. Hence, you should not
need to deal with nodes unless you also want to define node
attributes. Note that it is also possible to manage node
attributes at the node level.

Usage:

node [$id=<id>] <uname>[:<type>]
  [description=<description>]
  [attributes [$id=<id>] [<score>:] [rule...]
    <param>=<value> [<param>=<value>...]] | $id-ref=<ref>
  [utilization [$id=<id>] [<score>:] [rule...]
    <param>=<value> [<param>=<value>...]] | $id-ref=<ref>

type :: normal | member | ping | remote

Example:

node node1
node big_node attributes memory=64


crm(live)configure# 

```

### (1)使用在show命令查看配置详情:
```
rm(live)configure# show
node yimiwork_215
node yimiwork_216 \
    attributes standby=off
property cib-bootstrap-options: \
    dc-version=1.1.14-8.el6-70404b0 \
    cluster-infrastructure="classic openais (with plugin)" \
    expected-quorum-votes=2 \
    last-lrm-refresh=1465912707

```

###  (2). 使用`verify`验证配置,使用commit提交配置_
```
crm(live)configure# verify
crm(live)configure# commit
```



###  (3).查看当前集群系统所支持的类型
```
crm(live)# ra
crm(live)ra# classes  
lsb 
ocf / heartbeat pacemaker redhat 
service 
stonith
```

###   (4).查看某种类别下的所用资源代理的列表
```shell
crm(live)ra# list lsb
auditd              blk-availability    corosync            corosync-notifyd    crond               halt 
htcacheclean        httpd               ip6tables           iptables            killall             lvm2-lvmetad 
lvm2-monitor        messagebus          netconsole          netfs               network             nfs 
nfslock             ntpd                ntpdate             pacemaker           postfix             quota_nld 
rdisc               restorecond         rpcbind             rpcgssd             rpcidmapd           rpcsvcgssd 
rsyslog             sandbox             saslauthd           single              sshd                svnserve 
udev-post           winbind          
crm(live)ra# list ocf heartbeat
AoEtarget           AudibleAlarm        CTDB                ClusterMon          Delay               Dummy 
EvmsSCC             Evmsd               Filesystem          ICP                 IPaddr              IPaddr2 
IPsrcaddr           IPv6addr            LVM                 LinuxSCSI           MailTo              ManageRAID 
ManageVE            Pure-FTPd           Raid1               Route               SAPDatabase         SAPInstance 
SendArp             ServeRAID           SphinxSearchDaemon  Squid               Stateful            SysInfo 
VIPArip             VirtualDomain       WAS                 WAS6                WinPopup            Xen 
Xinetd              anything            apache              conntrackd          db2                 drbd 
eDir88              ethmonitor          exportfs            fio                 iSCSILogicalUnit    iSCSITarget 
ids                 iscsi               jboss               lxc                 mysql               mysql-proxy 
nfsserver           nginx               oracle              oralsnr             pgsql               pingd 
portblock           postfix             proftpd             rsyncd              scsi2reservation    sfex 
symlink             syslog-ng           tomcat              vmware           
crm(live)ra# list ocf pacemaker
ClusterMon     Dummy          HealthCPU      HealthSMART    Stateful       SysInfo        SystemHealth   controld 
o2cb           ping           pingd
```

###   (5).查看某个资源代理的配置方法
```
crm(live)ra# info ocf:heartbeat:IPaddr
Manages virtual IPv4 addresses (portable version) (ocf:heartbeat:IPaddr)
This script manages IP alias IP addresses
It can add an IP alias, or remove one.
Parameters (* denotes required, [] the default):
ip* (string): IPv4 address
    The IPv4 address to be configured in dotted quad notation, for example 
    "192.168.1.1".
nic (string, [eth0]): Network interface
    The base network interface on which the IP address will be brought 
    online. 
    If left empty, the script will try and determine this from the 
    routing table. 
    Do NOT specify an alias interface in the form eth0:1 or anything here; 
    rather, specify the base interface only. 
    Prerequisite: 
    There must be at least one static IP address, which is not managed by 
    the cluster, assigned to the network interface. 
    If you can not assign any static IP address on the interface, 
```

在创建资源之前因为没有 stonith 设备,需要把pacemaker的stonith禁用

> crm configure property stonith-enabled=false 

## 10. 创建一个web集群的vip资源


```
# 使用primitive 增加一个资源
Usage:

primitive <rsc> {[<class>:[<provider>:]]<type>|@<template>}
  [description=<description>]
  [[params] attr_list]
  [meta attr_list]
  [utilization attr_list]
  [operations id_spec]
    [op op_type [<attribute>=<value>...] ...]

attr_list :: [$id=<id>] [<score>:] [rule...]
             <attr>=<val> [<attr>=<val>...]] | $id-ref=<id>
id_spec :: $id=<id> | $id-ref=<id>
op_type :: start | stop | monitor

Example:

primitive apcfence stonith:apcsmart \
  params ttydev=/dev/ttyS0 hostlist="node1 node2" \
  op start timeout=60s \
  op monitor interval=30m timeout=60s

primitive www8 apache \
  configfile=/etc/apache/www8.conf \
  operations $id-ref=apache_ops

primitive db0 mysql \
  params config=/etc/mysql/db0.conf \
  op monitor interval=60s \
  op monitor interval=300s OCF_CHECK_LEVEL=10

primitive r0 ocf:linbit:drbd \
  params drbd_resource=r0 \
  op monitor role=Master interval=60s \
  op monitor role=Slave interval=300s

primitive xen0 @vm_scheme1 xmfile=/etc/xen/vm/xen0

primitive mySpecialRsc Special \
  params 3: rule #uname eq node1 interface=eth1 \
  params 2: rule #uname eq node2 interface=eth2 port=8888 \
  params 1: interface=eth0 port=9999

```

### 10.1 创建VIP
```
crm(live)# configure 
crm(live)configure# primitive vip ocf:heartbeat:IPaddr params ip=192.168.8.220 nic=eth0 cidr_netmask=24
crm(live)configure# show
node yimiwork_215 
node yimiwork_216 
primitive vip ocf:heartbeat:IPaddr \  
    params ip="192.168.8.220" nic="eth0" cidr_netmask="24"
property $id="cib-bootstrap-options" \ 
    dc-version="1.1.8-7.el6-394e906" \ 
    cluster-infrastructure="classic openais (with plugin)" \ 
    expected-quorum-votes="2" \ 
    stonith-enabled="false" 
crm(live)configure# verify #检查一下配置文件有没有错误 
crm(live)configure# commit #提交配置的资源，在命令行配置资源时，只要不用commit提交配置好资源，就不会生效，一但用commit命令提交，就会写入到cib.xml的配置文件中
crm(live)# status #查看一下配置好的资源状态，有一个资源vip，运行在node1上
Last updated: Thu Aug 15 14:24:45 2013 
Last change: Thu Aug 15 14:21:21 2013 via cibadmin on yimiwork_215 
Stack: classic openais (with plugin) 
Current DC: yimiwork_215 - partition with quorum 
Version: 1.1.8-7.el6-394e906 
2 Nodes configured, 2 expected votes 
1 Resources configured.
Online: [ yimiwork_215 yimiwork_216 ]
 vip    (ocf::heartbeat:IPaddr):    Started yimiwork_215
```

###10.2 测试vip的漂移
查看一下yimiwork_215节点上的ip，大家可以看到vip已经生效，而后我们到yimiwork_216上通过如下命令停止yimiwork_215上的corosync服务，再查看状态  
```shell
[root@yimiwork_215 ~]# ifconfig
eth0      Link encap:Ethernet  HWaddr 00:0C:29:91:45:90
          inet addr:192.168.8.215  Bcast:192.168.8.255  Mask:255.255.255.0 
          inet6 addr: fe80::20c:29ff:fe91:4590/64 Scope:Link 
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1 
          RX packets:375197 errors:0 dropped:0 overruns:0 frame:0 
          TX packets:291575 errors:0 dropped:0 overruns:0 carrier:0 
          collisions:0 txqueuelen:1000  
          RX bytes:55551264 (52.9 MiB)  TX bytes:52697225 (50.2 MiB)
eth0:0    Link encap:Ethernet  HWaddr 00:0C:29:91:45:90
          inet addr:192.168.8.220  Bcast:192.168.8.255  Mask:255.255.255.0 
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0 
          inet6 addr: ::1/128 Scope:Host 
          UP LOOPBACK RUNNING  MTU:16436  Metric:1 
          RX packets:6473 errors:0 dropped:0 overruns:0 frame:0 
          TX packets:6473 errors:0 dropped:0 overruns:0 carrier:0 
          collisions:0 txqueuelen:0  
          RX bytes:875395 (854.8 KiB)  TX bytes:875395 (854.8 KiB)
```

测试，停止yimiwork_215节点上的corosync，可以看到yimiwork_215已经离线
```
[root@yimiwork_216 ~]# ssh yimiwork_215 "service corosync stop" 
Signaling Corosync Cluster Engine (corosync) to terminate: [确定] 
Waiting for corosync services to unload:..[确定] 
[root@yimiwork_216 ~]# crm status 
Cannot change active directory to /var/lib/pacemaker/cores/root: No such file or directory (2) 
Last updated: Thu Aug 15 14:29:04 2013 
Last change: Thu Aug 15 14:21:21 2013 via cibadmin on yimiwork_215 
Stack: classic openais (with plugin) 
Current DC: yimiwork_216 - partition WITHOUT quorum  
Version: 1.1.8-7.el6-394e906 
2 Nodes configured, 2 expected votes 
1 Resources configured.
Online: [ yimiwork_216 ] 
OFFLINE: [ yimiwork_215 ]
```

__重点说明__：
> 上面的信息显示yimiwork_215已经离线，但资源vip却没能在yimiwork_216上启动。这是因为此时的集群状态为"WITHOUT quorum"，即已经失去了quorum，此时集群服务本身已经不满足正常运行的条件，这对于只有两节点的集群来讲是不合理的。因此，我们可以通过如下的命令来修改忽略quorum不能满足的集群状态检查：`property no-quorum-policy=ignore`

```
crm(live)# configure 
crm(live)configure# property no-quorum-policy=ignore 
crm(live)configure# show 
node yimiwork_215 
node yimiwork_216 
primitive vip ocf:heartbeat:IPaddr \ 
    params ip="192.168.18.200" nic="eth0" cidr_netmask="24" 
property $id="cib-bootstrap-options" \ 
    dc-version="1.1.8-7.el6-394e906" \ 
    cluster-infrastructure="classic openais (with plugin)" \ 
    expected-quorum-votes="2" \ 
    stonith-enabled="false" \ 
    no-quorum-policy="ignore" 
crm(live)configure# verify
crm(live)configure# commit
```

片刻之后，集群就会在目前仍在运行中的节点yimiwork_216上启动此资源了，如下所示：
```
[root@yimiwork_216 ~]# crm status
Last updated: Thu Aug 15 14:38:23 2013 
Last change: Thu Aug 15 14:37:08 2013 via cibadmin on yimiwork_216 
Stack: classic openais (with plugin) 
Current DC: yimiwork_216 - partition WITHOUT quorum 
Version: 1.1.8-7.el6-394e906 
2 Nodes configured, 2 expected votes 
1 Resources configured.
Online: [ yimiwork_216 ] 
OFFLINE: [ yimiwork_215 ]
 vip    (ocf::heartbeat:IPaddr):    Started yimiwork_216
```
好了，验正完成后，我们正常启动yimiwork_215

```
[root@yimiwork_216 ~]# ssh yimiwork_215 "service corosync start"
Starting Corosync Cluster Engine (corosync): [确定] 
[root@yimiwork_216 ~]# crm status 
Last updated: Thu Aug 15 14:39:45 2013 
Last change: Thu Aug 15 14:37:08 2013 via cibadmin on yimiwork_216 
Stack: classic openais (with plugin) 
Current DC: yimiwork_216 - partition with quorum 
Version: 1.1.8-7.el6-394e906 
2 Nodes configured, 2 expected votes 
1 Resources configured.
Online: [ yimiwork_215 yimiwork_216 ]
 vip    (ocf::heartbeat:IPaddr):    Started yimiwork_216
[root@yimiwork_216 ~]#
```

正常启动yimiwork_215后，集群资源vip很可能会重新从yimiwork_216转移回yimiwork_215，但也可能不回去。资源的这种在节点间每一次的来回流动都会造成那段时间内其无法正常被访问，所以，我们有时候需要在资源因为节点故障转移到其它节点后，即便原来的节点恢复正常也禁止资源再次流转回来。这可以通过定义资源的黏性(stickiness)来实现。在创建资源时或在创建资源后，都可以指定指定资源黏性。好了，下面我们来简单回忆一下，资源黏性。

### 10.3 资源黏性

资源黏性是指：`资源更倾向于运行在哪个节点`。

__资源黏性值范围及其作用__：

`0`：这是默认选项。资源放置在系统中的最适合位置。这意味着当负载能力“较好”或较差的节点变得可用时才转移资源。此选项的作用基本等同于自动故障回复，只是资源可能会转移到非之前活动的节点上；

`大于0`：资源更愿意留在当前位置，但是如果有更合适的节点可用时会移动。值越高表示资源越愿意留在当前位置；

`小于0`：资源更愿意移离当前位置。绝对值越高表示资源越愿意离开当前位置；

`INFINITY`：如果不是因节点不适合运行资源（节点关机、节点待机、达到migration-threshold 或配置更改）而强制资源转移，资源总是留在当前位置。此选项的作用几乎等同于完全禁用自动故障回复；

`-INFINITY`：资源总是移离当前位置；

我们这里可以通过以下方式为资源指定默认黏性值： `rsc_defaults resource-stickiness=100`
```
crm(live)configure# rsc_defaults resource-stickiness=100
crm(live)configure# verify  
crm(live)configure# show  
node yimiwork_215 
node yimiwork_216 
primitive vip ocf:heartbeat:IPaddr \ 
    params ip="192.168.8.220" nic="eth0" cidr_netmask="24" 
property $id="cib-bootstrap-options" \ 
    dc-version="1.1.8-7.el6-394e906" \ 
    cluster-infrastructure="classic openais (with plugin)" \ 
    expected-quorum-votes="2" \ 
    stonith-enabled="false" \ 
    no-quorum-policy="ignore" 
rsc_defaults $id="rsc-options" \ 
    resource-stickiness="100" 
crm(live)configure# commit
```

### 10.4 添加web server的资源 nginx
接下来我们将此http服务添加为集群资源。将nginx添加为集群资源.

接下来新建资源 nginx ：   
```
crm(live)# configure  
crm(live)configure# primitive nginx lsb:nginx 
crm(live)configure# show 
node yimiwork_215
node yimiwork_216 \
    attributes standby=off
primitive nginx lsb:nginx
primitive vip IPaddr \
    params ip=192.168.8.220 nic=eth0 cidr_netmask=24
order nginx-after-vip Mandatory: vip nginx
colocation nginx-ip INFUNTY: nginx vip
property cib-bootstrap-options: \
    dc-version=1.1.14-8.el6-70404b0 \
    cluster-infrastructure="classic openais (with plugin)" \
    expected-quorum-votes=2 \
    stonith-enabled=false \
    no-quorum-policy=ignore \
    last-lrm-refresh=1465912707

crm(live)configure# verify  
crm(live)configure# commit
```
来查看一下资源状态
```
[root@yimiwork_215 ~]# crm status
Last updated: Tue Jun 14 23:26:19 2016      Last change: Tue Jun 14 21:59:00 2016 by root via crm_attribute on yimiwork_216
Stack: classic openais (with plugin)
Current DC: yimiwork_215 (version 1.1.14-8.el6-70404b0) - partition with quorum
2 nodes and 2 resources configured, 2 expected votes

Online: [ yimiwork_215 yimiwork_216 ]

Full list of resources:

 vip    (ocf::heartbeat:IPaddr):    Started yimiwork_215
 nginx  (lsb:nginx):    Started yimiwork_216
```

从上面的信息中可以看出vip和nginx有可能会分别运行于两个节点上，这对于通过此IP提供Web服务的应用来说是不成立的，即此两者资源必须同时运行在某节点上。有两种方法可以解决:
1. 一种是定义组资源，将vip与nginx同时加入一个组中，可以实现将资源运行在同节点.
2. 2.另一种是定义资源约束可实现将资源运行在同一节点上。

### 10.5 定义组资源
```
crm(live)# configure 
crm(live)configure# group nginxgroup vip nginx 
crm(live)configure# show 
node yimiwork_215 
node yimiwork_216 
primitive nginx lsb:nginx 
primitive vip ocf:heartbeat:IPaddr \ 
    params ip="192.168.18.200" nic="eth0" cidr_netmask="24" 
group webservice vip nginx 
property $id="cib-bootstrap-options" \ 
    dc-version="1.1.8-7.el6-394e906" \ 
    cluster-infrastructure="classic openais (with plugin)" \ 
    expected-quorum-votes="2" \ 
    stonith-enabled="false" \ 
    no-quorum-policy="ignore" 
rsc_defaults $id="rsc-options" \ 
    resource-stickiness="100" 
crm(live)configure# verify  
crm(live)configure# commit
```
再次查看一下资源状态
```
[root@node1 ~]# crm status
Last updated: Thu Aug 15 15:33:09 2013 
Last change: Thu Aug 15 15:32:28 2013 via cibadmin on yimiwork_215 
Stack: classic openais (with plugin) 
Current DC: yimiwork_216 - partition with quorum 
Version: 1.1.8-7.el6-394e906 
2 Nodes configured, 2 expected votes 
2 Resources configured.
Online: [ yimiwork_215 yimiwork_216 ]
 Resource Group: webservice
     vip    (ocf::heartbeat:IPaddr):    Started yimiwork_216 
     nginx    (lsb:nginx):    Started yimiwork_216
```

模拟故障:
1. 停止corosync: 成功
2. 停止nginx

### 10.6 定义资源约束
我们先让yimiwork_216上线，再删除组资源
```
crm(live)node# online
[root@node1 ~]# crm_mon
Last updated: Thu Aug 15 15:48:38 2013
Last change: Thu Aug 15 15:46:21 2013 via crm_attribute    on yimiowrk_216 
Stack: classic openais (with plugin) 
Current DC: yimiowrk_216 - partition with quorum 
Version: 1.1.8-7.el6-394e906 
2 Nodes configured, 2 expected votes 
2 Resources configured.
Online: [ yimiowrk_215 yimiowrk_216 ]
 Resource Group: nginxgroup
     vip        (ocf::heartbeat:IPaddr):        Started yimiowrk_215 
     nginx    (lsb:nginx):    Started yimiowrk_215
```
删除组资源操作
```
crm(live)# resource 
crm(live)resource# show  
 Resource Group: nginxgroup 
     vip    (ocf::heartbeat:IPaddr):    Started  
     nginx    (lsb:nginx):    Started  
crm(live)resource# stop nginxgroup  #停止资源 
crm(live)resource# show 
 Resource Group: nginxgroup 
     vip    (ocf::heartbeat:IPaddr):    Stopped  
     nginx    (lsb:nginx):    Stopped  
crm(live)resource# cleanup nginxgroup  #清理资源 
Cleaning up vip on yimiowrk_215 
Cleaning up vip on yimiowrk_216 
Cleaning up nginx on yimiowrk_215 
Cleaning up nginx on yimiowrk_216 
Waiting for 1 replies from the CRMd. OK
crm(live)# configure 
crm(live)configure# delete  
cib-bootstrap-options   yimiowrk_215          rsc-options             nginxgroup           
nginx                   yimiowrk_216          vip                  
crm(live)configure# delete nginxgroup #删除组资源 
crm(live)configure# show 
node yimiowrk_215 
node yimiowrk_216 \ 
    attributes standby="off" 
primitive nginx lsb:nginx 
primitive vip ocf:heartbeat:IPaddr \ 
    params ip="192.168.8.220" nic="eth0" cidr_netmask="24" 
property $id="cib-bootstrap-options" \ 
    dc-version="1.1.8-7.el6-394e906" \ 
    cluster-infrastructure="classic openais (with plugin)" \ 
    expected-quorum-votes="2" \ 
    stonith-enabled="false" \ 
    no-quorum-policy="ignore" \ 
    last-lrm-refresh="1376553277" 
rsc_defaults $id="rsc-options" \ 
    resource-stickiness="100" 
crm(live)configure# commit

[root@yimiwork_215 ~]# crm_mon
Last updated: Thu Aug 15 15:56:59 2013
Last change: Thu Aug 15 15:56:12 2013 via cibadmin on yimiowrk_215 
Stack: classic openais (with plugin) 
Current DC: yimiowrk_216 - partition with quorum 
Version: 1.1.8-7.el6-394e906 
2 Nodes configured, 2 expected votes 
2 Resources configured.
Online: [ yimiowrk_215 yimiowrk_216 ]
vip     (ocf::heartbeat:IPaddr):        Started yimiowrk_215
nginx   (lsb:nginx):    Started yimiowrk_216
```


大家可以看到资源又重新运行在两个节点上了，下面我们来定义约束！使资源运行在同一节点上。首先我们来回忆一下资源约束的相关知识，资源约束则用以指定在哪些群集节点上运行资源，以何种顺序装载资源，以及特定资源依赖于哪些其它资源。pacemaker共给我们提供了三种资源约束方法：

1. `Resource Location（资源位置）`：定义资源可以、不可以或尽可能在哪些节点上运行；
2. `Resource Collocation（资源排列）`：排列约束用以定义集群资源可以或不可以在某个节点上同时运行；
3. `Resource Order（资源顺序）`：顺序约束定义集群资源在节点上启动的顺序；

定义约束时，还需要指定分数。各种分数是集群工作方式的重要组成部分。其实，从迁移资源到决定在已降级集群中停止哪些资源的整个过程是通过以某种方式修改分数来实现的。分数按每个资源来计算，资源分数为负的任何节点都无法运行该资源。在计算出资源分数后，集群选择分数最高的节点。INFINITY（无穷大）目前定义为 1,000,000。加减无穷大遵循以下3个基本规则：

1. 任何值 + 无穷大 = 无穷大
2. 任何值 - 无穷大 = -无穷大
3. 无穷大 - 无穷大 = -无穷大

定义资源约束时，也可以指定每个约束的分数。分数表示指派给此资源约束的值。分数较高的约束先应用，分数较低的约束后应用。通过使用不同的分数为既定资源创建更多位置约束，可以指定资源要故障转移至的目标节点的顺序。因此，对于前述的vip和nginx可能会运行于不同节点的问题，可以通过以下命令来解决：

```
crm(live)configure# show 
node yimiowrk_215 
node yimiowrk_216 \ 
    attributes standby="off" 
primitive nginx lsb:nginx 
primitive vip ocf:heartbeat:IPaddr \ 
    params ip="192.168.8.220" nic="eth0" cidr_netmask="24" 
colocation nginx-with-ip INFUNTY: nginx vip 
property $id="cib-bootstrap-options" \ 
    dc-version="1.1.8-7.el6-394e906" \ 
    cluster-infrastructure="classic openais (with plugin)" \ 
    expected-quorum-votes="2" \ 
    stonith-enabled="false" \ 
    no-quorum-policy="ignore" \ 
    last-lrm-refresh="1376553277" 
rsc_defaults $id="rsc-options" \ 
    resource-stickiness="100" 
crm(live)configure# show xml
   <rsc_colocation id="nginx-with-ip" score-attribute="INFUNTY" rsc="nginx" with-rsc="vip"/>

[root@yimiwork_216 ~]# crm_mon
Last updated: Thu Aug 15 16:12:18 2013
Last change: Thu Aug 15 16:12:05 2013 via cibadmin on yimiowrk_215 
Stack: classic openais (with plugin) 
Current DC: yimiowrk_216 - partition with quorum 
Version: 1.1.8-7.el6-394e906 
2 Nodes configured, 2 expected votes 
2 Resources configured.
Online: [ yimiowrk_215 yimiowrk_216 ]
vip     (ocf::heartbeat:IPaddr):        Started yimiowrk_215
nginx   (lsb:nginx):    Started yimiowrk_215
```
所有资源全部运行在yimiwork_215上

### 10.7 定义启动顺序
我们还得确保nginx在某节点启动之前得先启动vip，这可以使用如下命令实现：
```
crm(live)# configure 
crm(live)configure# order nginx-after-vip mandatory: vip nginx 
crm(live)configure# verify  

crm(live)configure# show  
node yimiowrk_215 \ 
    attributes standby="on" 
node nyimiowrk_216 \ 
    attributes standby="off" 
primitive nginx lsb:nginx \ 
    meta target-role="Started" 
primitive vip ocf:heartbeat:IPaddr \ 
    params ip="192.168.8.220" nic="eth0" cidr_netmask="24" \ 
    meta target-role="Started" 
colocation nginx-with-ip INFUNTY: nginx vip 
order nginx-after-vip inf: vip nginx 
property $id="cib-bootstrap-options" \ 
    dc-version="1.1.8-7.el6-394e906" \ 
    cluster-infrastructure="classic openais (with plugin)" \ 
    expected-quorum-votes="2" \ 
    stonith-enabled="false" \ 
    no-quorum-policy="ignore" \ 
    last-lrm-refresh="1376554276" 
rsc_defaults $id="rsc-options" \ 
    resource-stickiness="100" 

crm(live)configure# show xml
 <rsc_order id="nginx-after-vip" score="INFINITY" first="vip" then="nginx"/>
crm(live)configure# commit
```
此外，由于HA集群本身并不强制每个节点的性能相同或相近。所以，某些时候我们可能希望在正常时服务总能在某个性能较强的节点上运行，这可以通过位置约束来实现：
`crm(live)configure# location prefer-node1 vip node_pref::200: yimiwork_215`

## 11. 配置nfs与nginx的高可用集群
### 11.1 添加nfs的资源
```
crm(live)configure# show
node yimiwork_215
node yimiwork_216 \
    attributes standby=off
primitive nginx lsb:nginx
primitive vip IPaddr \
    params ip=192.168.8.220 nic=eth0 cidr_netmask=24
property cib-bootstrap-options: \
    dc-version=1.1.14-8.el6-70404b0 \
    cluster-infrastructure="classic openais (with plugin)" \
    expected-quorum-votes=2 \
    stonith-enabled=false \
    no-quorum-policy=ignore \
    last-lrm-refresh=1465912707

crm(live)configure# primitive nfs ocf:heartbeat:Filesystem params device=192.168.8.212:/www directory=/www fstype=nfs

crm(live)configure# verify
WARNING: nfs: default timeout 20s for start is smaller than the advised 60
WARNING: nfs: default timeout 20s for stop is smaller than the advised 60
crm(live)configure# show
node yimiwork_215
node yimiwork_216 \
    attributes standby=off
primitive nfs Filesystem \
    params device="192.168.8.212:/www" directory="/www" fstype=nfs
primitive nginx lsb:nginx
primitive vip IPaddr \
    params ip=192.168.8.220 nic=eth0 cidr_netmask=24
property cib-bootstrap-options: \
    dc-version=1.1.14-8.el6-70404b0 \
    cluster-infrastructure="classic openais (with plugin)" \
    expected-quorum-votes=2 \
    stonith-enabled=false \
    no-quorum-policy=ignore \
    last-lrm-refresh=146591
```

### 11.2 查看的crm集群的状态
```
crm(live)# status
Last updated: Wed Jun 15 10:23:55 2016      Last change: Wed Jun 15 10:23:42 2016 by root via cibadmin on yimiwork_215
Stack: classic openais (with plugin)
Current DC: yimiwork_215 (version 1.1.14-8.el6-70404b0) - partition with quorum
2 nodes and 3 resources configured, 2 expected votes

Online: [ yimiwork_215 yimiwork_216 ]

Full list of resources:

 vip    (ocf::heartbeat:IPaddr):    Started yimiwork_215
 nginx  (lsb:nginx):    Started yimiwork_216
 nfs    (ocf::heartbeat:Filesystem):    Started yimiwork_215

```
三个资源,不在同一台主机上.

### 11.3 定义资源组
```
crm(live)configure# 
crm(live)configure# group webservice vip nfs nginx
crm(live)configure# verify
WARNING: nfs: default timeout 20s for start is smaller than the advised 60
WARNING: nfs: default timeout 20s for stop is smaller than the advised 60
crm(live)configure# show 
node yimiwork_215
node yimiwork_216 \
    attributes standby=off
primitive nfs Filesystem \
    params device="192.168.8.212:/www" directory="/www" fstype=nfs
primitive nginx lsb:nginx
primitive vip IPaddr \
    params ip=192.168.8.220 nic=eth0 cidr_netmask=24
group webservice vip nfs nginx
property cib-bootstrap-options: \
    dc-version=1.1.14-8.el6-70404b0 \
    cluster-infrastructure="classic openais (with plugin)" \
    expected-quorum-votes=2 \
    stonith-enabled=false \
    no-quorum-policy=ignore \
    last-lrm-refresh=1465912707
crm(live)configure# cd ..

There are changes pending. Do you want to commit them (y/n)? y
crm(live)# status
Last updated: Wed Jun 15 10:26:38 2016      Last change: Wed Jun 15 10:26:36 2016 by root via cibadmin on yimiwork_215
Stack: classic openais (with plugin)
Current DC: yimiwork_215 (version 1.1.14-8.el6-70404b0) - partition with quorum
2 nodes and 3 resources configured, 2 expected votes

Online: [ yimiwork_215 yimiwork_216 ]

Full list of resources:

 Resource Group: webservice
     vip    (ocf::heartbeat:IPaddr):    Started yimiwork_215
     nfs    (ocf::heartbeat:Filesystem):    Started yimiwork_215
     nginx  (lsb:nginx):    Started yimiwork_215

```

可以看到三个资源都在同一台机器上了.

__故障模拟__:
```
crm(live)# node
crm(live)node# standby
crm(live)node# show
yimiwork_215: normal
    standby=on
yimiwork_216: normal
    standby=off
crm(live)node# cd ..

crm(live)# status
Last updated: Wed Jun 15 10:28:45 2016      Last change: Wed Jun 15 10:28:32 2016 by root via crm_attribute on yimiwork_215
Stack: classic openais (with plugin)
Current DC: yimiwork_215 (version 1.1.14-8.el6-70404b0) - partition with quorum
2 nodes and 3 resources configured, 2 expected votes

Node yimiwork_215: standby
Online: [ yimiwork_216 ]

Full list of resources:

 Resource Group: webservice
     vip    (ocf::heartbeat:IPaddr):    Started yimiwork_216
     nfs    (ocf::heartbeat:Filesystem):    Started yimiwork_216
     nginx  (lsb:nginx):    Started yimiwork_216


```
可以看到资源转到了,另一台上去了.

## 12. 实例: corosync+Pacemaker+drbd+mysql
### 12.1、环境准备(同上)
### 12.2、Corosync 安装与配置(同上)
### 12.3、Pacemaker 安装与配置(同上)
### 12.4、DRBD 安装与配置(同DRBD的实例)
### 12.5、MySQL 安装与配置(略,data等目录选择drbd的)
### 12.6、crmsh 资源管理
#### 1. 增加drbd资源

```
crm(live)# configure
crm(live)configure#primitive mysqldrbd ocf:heartbeat:drbd params drbd_resource=web op start timeout=240 op  stop timeout=100 op monitor role=Master interval=20 timeout=30 op monitor role=Slave interval=30 timeout=30
crm(live)configure#ms ms_mysqlddrbd meta master-max=1 master-node-max=1 clone-max=2 clone-node-max=1 notify=true
crm(live)configure#
crm(live)configure#
crm(live)configure#
crm(live)configure#
crm(live)configure#
crm(live)configure#

crm(live)configure# show
node yimiowrk_215
node yimiowrk_216 
primitive mysqldrbd ocf:heartbeat:drbd \  
        params drbd_resource="web" \  
        op start timeout="240" interval="0" \  
        op stop timeout="100" interval="0" \  
        op monitor role="Master" interval="20" timeout="30" \  
        op monitor role="Slave" interval="30" timeout="30"  
ms ms_mysqldrbd mysqldrbd \  
        meta master-max="1" master-node-max="1" clone-max="2" clone-node-max="1" notify="true"  
property $id="cib-bootstrap-options" \  
        dc-version="1.1.8-7.el6-394e906" \  
        cluster-infrastructure="classic openais (with plugin)" \  
        expected-quorum-votes="2" \  
        stonith-enabled="false" \  
        no-quorum-policy="ignore"
[root@yimiwork_215 ~]# crm status 

Last updated: Sat Aug 17 20:14:16 2013  
Last change: Sat Aug 17 20:12:55 2013 via cibadmin on yimiowrk_215 
Stack: classic openais (with plugin)  
Current DC: yimiowrk_215- partition with quorum  
Version: 1.1.8-7.el6-394e906  
2 Nodes configured, 2 expected votes  
2 Resources configured.
Online: [ yimiowrk_215 yimiowrk_216]
 Master/Slave Set: ms_mysqldrbd [mysqldrbd] 
     Masters: [ yimiowrk_216]  
     Slaves: [ yimiwork_215 ]
```

#### 2. 增加文件系统资源
```
crm(live)# configure
crm(live)configure#primitive  mystore ocf:heartbeat:Filesystem params device=/dev/drbd0 driectory=/mydata fstype=ext4 op start timeout=60 op stop timeout=60
crm(live)configure#verify
crm(live)configure#colocation mystore_with_ms_mysqldrbd inf: ms_mysqldrbd:Master

crm(live)configure#order mystore_with_after_ms_mysqldrbd mandatory: ms_mysqlddrbd:promote mystore:start
crm(live)configure#verify
crm(live)configure#commit
crm(live)configure#show
node yimiowrk_215 
node yimiowrk_216  
primitive mysqldrbd ocf:heartbeat:drbd \  
        params drbd_resource="web" \  
        op start timeout="240" interval="0" \  
        op stop timeout="100" interval="0" \  
        op monitor role="Master" interval="20" timeout="30" \  
        op monitor role="Slave" interval="30" timeout="30"  
primitive mystore ocf:heartbeat:Filesystem \  
        params device="/dev/drbd0" directory="/mydata" fstype="ext3" \  
        op start timeout="60" interval="0" \  
        op stop timeout="60" interval="0"  
ms ms_mysqldrbd mysqldrbd \  
        meta master-max="1" master-node-max="1" clone-max="2" clone-node-max="1" notify="true"  
colocation mystore_with_ms_mysqldrbd inf: mystore ms_mysqldrbd:Master  
order mystore_after_ms_mysqldrbd inf: ms_mysqldrbd:promote mystore:start  
property $id="cib-bootstrap-options" \  
        dc-version="1.1.8-7.el6-394e906" \  
        cluster-infrastructure="classic openais (with plugin)" \  
        expected-quorum-votes="2" \  
        stonith-enabled="false" \  
        no-quorum-policy="ignore"
[root@yimiwork_215 ~]# crm status 
Cannot change active directory to /var/lib/pacemaker/cores/root: No such file or directory (2)  
Last updated: Sat Aug 17 20:37:26 2013  
Last change: Sat Aug 17 20:19:51 2013 via cibadmin on yimiowrk_215  
Stack: classic openais (with plugin)  
Current DC: yimiowrk_215 - partition with quorum  
Version: 1.1.8-7.el6-394e906  
2 Nodes configured, 2 expected votes  
3 Resources configured.
Online: [ yimiowrk_215 yimiowrk_216 ]
 Master/Slave Set: ms_mysqldrbd [mysqldrbd] 
     Masters: [ yimiowrk_216 ]  
     Slaves: [ yimiowrk_215 ]  
 mystore    (ocf::heartbeat:Filesystem):    Started yimiowrk_216
 
[root@yimiwork_216 ~]# mount 
/dev/sda2 on / type ext4 (rw)  
proc on /proc type proc (rw)  
sysfs on /sys type sysfs (rw)  
devpts on /dev/pts type devpts (rw,gid=5,mode=620)  
tmpfs on /dev/shm type tmpfs (rw)  
/dev/sda1 on /boot type ext4 (rw)  
/dev/sda3 on /data type ext4 (rw)  
none on /proc/sys/fs/binfmt_misc type binfmt_misc (rw)  
/dev/drbd0 on /mydata type ext3 (rw)
```


#### 4.增加mysql资源
```
crm(live)# configure
crm(live)configure#primitive mysqld lsb:mysqld
crm(live)configure#colocation mysqld_with_mysqtore inf: mysqld mystore
crm(live)configure#verify
crm(live)configure#show

crm(live)configure#order mysqld_after_mystore mandatory: mysotre mysqld
crm(live)configure#verify
crm(live)configure#show
node yimiowrk_215  
node yimiowrk_216  
primitive mysqld lsb:mysqld  
primitive mysqldrbd ocf:heartbeat:drbd \  
    params drbd_resource="web" \  
    op start timeout="240" interval="0" \  
    op stop timeout="100" interval="0" \  
    op monitor role="Master" interval="20" timeout="30" \  
    op monitor role="Slave" interval="30" timeout="30"  
primitive mystore ocf:heartbeat:Filesystem \  
    params device="/dev/drbd0" directory="/mydata" fstype="ext4" \  
    op start timeout="60" interval="0" \  
    op stop timeout="60" interval="0"  
ms ms_mysqldrbd mysqldrbd \  
    meta master-max="1" master-node-max="1" clone-max="2" clone-node-max="1" notify="true"  
colocation mysqld_with_mystore inf: mysqld mystore  
colocation mystore_with_ms_mysqldrbd inf: mystore ms_mysqldrbd:Master  
order mystore_after_ms_mysqldrbd inf: ms_mysqldrbd:promote mystore:start  
property $id="cib-bootstrap-options" \  
    dc-version="1.1.8-7.el6-394e906" \  
    cluster-infrastructure="classic openais (with plugin)" \  
    expected-quorum-votes="2" \  
    stonith-enabled="false" \  
    no-quorum-policy="ignore"


crm(live)configure#commit

crm status 
 
Last updated: Sat Aug 17 20:46:35 2013  
Last change: Sat Aug 17 20:46:07 2013 via cibadmin on yimiowrk_215  
Stack: classic openais (with plugin)  
Current DC: yimiowrk_215 - partition with quorum  
Version: 1.1.8-7.el6-394e906  
2 Nodes configured, 2 expected votes  
4 Resources configured.
Online: [ yimiowrk_215 yimiowrk_216 ]
 Master/Slave Set: ms_mysqldrbd [mysqldrbd] 
     Masters: [ yimiowrk_216 ]  
     Slaves: [ yimiowrk_215 ]  
 mystore    (ocf::heartbeat:Filesystem):    Started yimiowrk_216  
 mysqld    (lsb:mysqld):    Started yimiowrk_216

```

#### 5.增加vip资源
```
crm(live)# configure
crm(live)configure#primitive vip ocf:heartbeat:IPaddr params ip=192.16.8.220 nic=eth0 cidr_netmask=24
crm(live)configure#colocation vip_with_ms_mysqldrbd inf: ms_mysqldrbd:Master vip
crm(live)configure#verify
crm(live)configure#show
ode yimiowrk_215 
node yimiowrk_216  
primitive mysqld lsb:mysqld  
primitive mysqldrbd ocf:heartbeat:drbd \  
        params drbd_resource="web" \  
        op start timeout="240" interval="0" \  
        op stop timeout="100" interval="0" \  
        op monitor role="Master" interval="20" timeout="30" \  
        op monitor role="Slave" interval="30" timeout="30"  
primitive mystore ocf:heartbeat:Filesystem \  
        params device="/dev/drbd0" directory="/mydata" fstype="ext3" \  
        op start timeout="60" interval="0" \  
        op stop timeout="60" interval="0"  
primitive vip ocf:heartbeat:IPaddr \  
        params ip="192.168.8.220" nic="eth0" cidr_netmask="255.255.255.0"  
ms ms_mysqldrbd mysqldrbd \  
        meta master-max="1" master-node-max="1" clone-max="2" clone-node-max="1" notify="true"  
colocation mysqld_with_mystore inf: mysqld mystore  
colocation mystore_with_ms_mysqldrbd inf: mystore ms_mysqldrbd:Master  
colocation vip_with_ms_mysqldrbd inf: ms_mysqldrbd:Master vip  
order mysqld_after_mystore inf: mystore mysqld  
order mystore_after_ms_mysqldrbd inf: ms_mysqldrbd:promote mystore:start  
property $id="cib-bootstrap-options" \  
        dc-version="1.1.8-7.el6-394e906" \  
        cluster-infrastructure="classic openais (with plugin)" \  
        expected-quorum-votes="2" \  
        stonith-enabled="false" \

crm(live)# status
crm(live)# Last updated: Sat Aug 17 20:53:15 2013  
Last change: Sat Aug 17 20:52:11 2013 via cibadmin on yimiowrk_215  
Stack: classic openais (with plugin)  
Current DC: yimiowrk_215 - partition with quorum  
Version: 1.1.8-7.el6-394e906  
2 Nodes configured, 2 expected votes  
5 Resources configured.
Online: [ yimiowrk_215 yimiowrk_216 ]
 Master/Slave Set: ms_mysqldrbd [mysqldrbd] 
     Masters: [ yimiowrk_215 ]  
     Slaves: [ yimiowrk_216 ]  
 mystore    (ocf::heartbeat:Filesystem):    Started yimiowrk_215  
 mysqld    (lsb:mysqld):    Started yimiowrk_215  
 vip    (ocf::heartbeat:IPaddr):    Started yimiowrk_215
```


Error: Unable to communicate with yimiwork_215
