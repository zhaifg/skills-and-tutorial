# heartbeat 3.x（No CRM）

标签（空格分隔）： HA

---

## heartbeat介绍
Heartbeat 项目是 Linux-HA 工程的一个组成部分，Linux-HA的全称是High-Availability Linux，心跳服务和集群通信是高可用集群的两个关键组件，在 Heartbeat 项目里，由 heartbeat 模块实现了这两个功能。
Linux-HA的官方网站：
[HA01][1]
[HA02][2]


## HA集群相关术语 
- 1.节点（node） 
运行heartbeat进程的一个独立主机，称为节点，节点是HA的核心组成部分，每个节点上运行着操作系统和heartbeat软件服务，在heartbeat集群中，节点有主次之分，分别称为主节点和备用/备份节点，每个节点拥有唯一的主机名，并且拥有属于自己的一组资源，主节点上一般运行着一个或多个应用服务。而备用节点一般处于监控状态。

- 2.资源（resource） 
资源是一个节点可以控制的实体，并且当节点发生故障时，这些资源能够被其它节点接管，heartbeat中，可以当做资源的实体有：
  磁盘分区、文件系统、IP地址、应用程序服务、NFS文件系统

- 3.事件（event） 
也就是集群中可能发生的事情，例如节点系统故障、网络连通故障、网卡故障、应用程序故障等。这些事件都会导致节点的资源发生转移，HA的测试也是基于这些事件来进行的。 

- 4.动作（action） 
事件发生时HA的响应方式，动作是由shell脚步控制的，例如，当某个节点发生故障后，备份节点将通过事先设定好的执行脚本进行服务的关闭或启动。进而接管故障节点的资源。

**Heartbeat的版本与组件**
说明：Heartbeat有三个版本分别为`Heartbeat v1.x`，`Heartbeat v2.x`，`Heartbeat v3.x`。`Heartbeat v1.x`和`Heartbeat v2.x`版本的组成结构十分简单，所有模块都集中在heartbeat中，到了v3版本后，整个heartbeat项目进行了拆分，分为不同的项目来分别进行开发。

- . **Heartbeat v1.x与v2.x的组件**
`heartbeat`：节点间通信检测模块
`ha-logd`：集群事件日志服务
`CCM（Consensus Cluster Membership）`：集群成员一致性管理模块
`LRM （Local Resource Manager）`：本地资源管理模块
`Stonith Daemon`： 使出现问题的节点从集群环境中脱离或重启
`CRM（Cluster resource management）`：集群资源管理模块
`Cluster policy engine`： 集群策略引擎
`Cluster transition engine`：集群转移引擎（也叫策略执行引擎）

`Heartbeat v1.x`与`Heartbeat v2.x`**区别**：
在Heartbeat v2.x中增加了一个新的集群资源管理器`crm`，在Heartbeat v1.x中的集群资源管理器是`haresource`，Heartbeat v2.x中为了兼容v1.x保留了`haresource`，但同时又新增了一个功能更强大的`crm资源管理器`。crm管理方式有，一种是`基于命令行crmsh`，一种是基于`图形界面的hb_gui`。

- . **Heartbeat v3.x的组件**
`Heartbeat`：将原来的消息通信层独立为heartbeat项目，新的heartbeat只负责维护集群各节点的信息以及它们之前通信。
`Cluster Glue`：相当于一个中间层，它用来将`heartbeat`和`pacemaker`关联起来，主要包含2个部分，即为`LRM`和`STONITH`。
`Resource Agent`：用来控制服务启停，监控服务状态的脚本集合，这些脚本将被LRM调用从而实现各种资源启动、停止、监控等等。
`Pacemaker`：也就是`Cluster Resource Manager`（集群资源管理器，简称CRM），用来管理整个HA的控制中心，客户端通过pacemaker来配置管理监控整个集群。

- Heartbeat各个版本之间的异同
与1.x风格相比，Heartbeat2.1.x版本之后功能变化如下：
1. 保留原有所有功能
  如，网络,heartbeat ,机器down时均可切换资源.
2. 自动监控资源
  默认情况下每2分钟检测资源运行情况，如果发现资源不在，则尝试启动资源， 如果60s后还未启动成功，则资源切换向另节点。时间可以修改。
3. 可以对各资源组实现独立监控.
  比如apache运行在node1上,tomcat运行在node2上,Heartbeat可同时实现两台主机的服务监控。
4. 同时监控系统负载
可以自动将资源切换到负载低的node上。Heartbeat官方最后一个STABLE release 2.x 版本是2.1.4，Heartbeat 3官方正式发布的首个版本是3.0.2，Heartbeat 3与Heartbeat2.x的最大差别在于，Heartbeat3.x按模块把的原来Heartbeat2.x拆分为多个子项目，但是HA实现原理与Heartbeat2.x基本相同。配置也基本一致。

>  本人的系统环境为CentOS 6.5,epel源里默认的是heartbeat 3.x，此环境中的用heartbeat 3.x，但是不用CRM模块。

##　测试环境规划

|主机名|外网IP|心跳IP|
|-----|-----|------|
|node01（主）|172.16.0.208|172.16.20.208|
|node02|172.16.0.209|172.16.20.209|

VIP（172.16.0.210）

##　安装前配置
1. 时间要同步，selinux，iptables
2. hostname，/etc/hosts与IP要一致
3. 心跳线，网关，路由设定等
4. epel源添加

##　heartbeat 安装
```
yum install heartbeat-devel heartbeat-libs heartbeat cluster-glue
```

## heartbeat目录以及重要文件介绍
heartbeat 默认的配置文件路径在`/etc/ha.d`目录下，默认没有配置文件，需要从`/usr/share/doc/heartbeat-3.0.4`复制。主要配置文件`authkeys`,`ha.cf` ,`haresources`

1. `authkeys` #是节点之间的认证key文件，我们不能让什么服务器都加入集群中来，加入集群中的节点都是需要认证的
2. `ha.cf`  #heartbeat的主配置文件
3. `haresources` #集群资源管理配置文件（在heartbeat所有版本中都是支持haresources来配置集群中的资源的）

### authkeys

文件格式：
```
auth <num>  #用下面定义的哪种算法做认证
<num> <algorithm> <secret>  # num定义的算法ID，algorithm算法：sha，md5等；secret：密钥
```
 authkeys文件用于设定heartbeat的认证方式，共有三种可用的认证方式：crc、md5和sha1，三种认证方式的安全性依次提高，但是占用的系统资源也依次增加。如果heartbeat集群运行在安全的网络上，可以使用crc方式，如果HA每个节点的硬件配置很高，建议使用sha1，这种认证方式安全级别最高，如果是处于网络安全和系统资源之间，可以使用md5认证方式。这里我们使用crc认证方式，设置如下：
auth 1  
1 crc  
#2 sha1 sha1_any_password  
#3 md5 md5_any_password 

需要说明的一点是：无论auth后面指定的是什么数字，在下一行必须作为关键字再次出现，例如指定了“auth 6”，下面一定要有一行“6 认证类型”。
最后确保这个文件的权限是600（即-rw-------）。


```
dd if=/dev/random bs=512 count=1 | openssl md5 #生成密钥随机数
0+1 records in 
0+1 records out 
128 bytes (128 B) copied, 0.000214 seconds, 598 kB/s 
a4d20b0dd3d5e35e0f87ce4266d1dd64


[root@node1 ha.d]# vim authkeys
#auth 1
#1 crc 
#2 sha1 HI! 
#3 md5 Hello!
auth 1
1 md5 a4d20b0dd3d5e35e0f87ce4266d1dd64

[root@node1 ha.d]# chmod 600 authkeys  #修改密钥文件的权限为600
[root@node1 ha.d]# ll 
总计 56 
-rw------- 1 root root   691 08-07 16:45 authkeys 

```

或者通过这个脚本方式：
```
( echo -ne "auth 1\n1 sha1 "; \
  dd if=/dev/urandom bs=512 count=1 | openssl md5 ) \
  > /etc/ha.d/authkeys
chmod 0600 /etc/ha.d/authkeys
```
### ha.cf
```
#debugfile /var/log/ha-debug  
logfile /var/log/ha-log     #指名heartbeat的日志存放位置。  
crm |no    #是否开启Cluster Resource Manager（集群资源管理）功能。  
#bcast eth1   #指明心跳使用以太网广播方式，并且是在eth1接口上进行广播。  
keepalive 2    #指定心跳间隔时间为2秒（即每两秒钟在eth1上发送一次广播）。  
deadtime 30    #指定备用节点在30秒内没有收到主节点的心跳信号后，则立即接管主节点的服务资源。  
warntime 10    #指定心跳延迟的时间为十秒。当10秒钟内备份节点不能接收到主节点的心跳信号时，就会往日志中写入一个警告日志，但此时不会切换服务。  
initdead 120   #在某些系统上，系统启动或重启之后需要经过一段时间网络才能正常工作，该选项用于解决这种情况产生的时间间隔。取值至少为deadtime的两倍。   
udpport 694   #设置广播通信使用的端口，694为默认使用的端口号。  
#baud 19200    #设置串行通信的波特率。  
#serial /dev/ttyS0   #选择串行通信设备，用于双机使用串口线连接的情况。如果双机使用以太网。  
#ucast eth0 192.168.1.2 #采用网卡eth0的udp单播来组织心跳，后面跟的IP地址应为双机对方的IP地址。  
mcast eth1 225.0.0.75 694 1 0 #采用网卡eth1的Udp多播来组织心跳，一般在备用节点不止一台时使用。Bcast、ucast和mcast分别代表广播、单播和多播，是组织心跳的三种方式，任选其一即可。 

auto_failback on #用来定义当主节点恢复后，是否将服务自动切回，heartbeat的两台主机分别为主节点和备份节点。主节点在正常情况下占用资源并运行所有的服务，遇到故障时把资源交给备份节点并由备份节点运行服务。在该选项设为on的情况下，一旦主节点恢复运行，则自动获取资源并取代备份节点，如果该选项设置为off，那么当主节点恢复后，将变为备份节点，而原来的备份节点成为主节点。  
#stonith baytech /etc/ha.d/conf/stonith.baytech   # stonith的主要作用是使出现问题的节点从集群环境中脱离，进而释放集群资源，避免两个节点争用一个资源的情形发生。保证共享数据的安全性和完整性。  
#watchdog /dev/watchdog #该选项是可选配置，是通过Heartbeat来监控系统的运行状态。使用该特性，需要在内核中载入"softdog"内核模块，用来生成实际的设备文件，如果系统中没有这个内核模块，就需要指定此模块，重新编译内核。编译完成输入"insmod softdog"加载该模块。然后输入"grep misc /proc/devices"(应为10)，输入"cat /proc/misc |grep watchdog"(应为130)。最后，生成设备文件："mknod /dev/watchdog c 10 130" 。即可使用此功能。  
node node1  #主节点主机名，可以通过命令“uanme –n”查看。  
node node2  #备用节点主机名。  
ping 172.16.0.1 #选择ping的节点，ping 节点选择的越好，HA集群就越强壮，可以选择固定的路由器作为ping节点，但是最好不要选择集群中的成员作为ping节点，ping节点仅仅用来测试网络连接。  

ping_group group1 192.168.12.251 192.168.12.239  #类似于ping。  
#respawn hacluster /usr/local/ha/lib/heartbeat/ipfail  
#apiauth pingd gid=haclient uid=hacluster 
#respawn hacluster /usr/local/ha/lib/heartbeat/pingd -m 100 -d 5s #该选项是可选配置，列出与heartbeat一起启动和关闭的进程，该进程一般是和heartbeat集成的插件，这些进程遇到故障可以自动重新启动。最常用的进程是pingd，此进程用于检测和监控网卡状态，需要配合ping语句指定的ping node来检测网络的连通性。其中hacluster表示启动pingd进程的身份。  
#下面的配置是关键，也就是激活crm管理，开始使用v2 style格式  
#crm respawn   
#注意，还可以使用crm yes的写法，但这样写的话，如果后面的cib.xml配置有问题  
#会导致heartbeat直接重启该服务器，所以，测试时建议使用respawn的写法  
#下面是对传输的数据进行压缩，是可选项  
compression     bz2  
compression_threshold 2  
注意，v2 style不支持ipfail功能，须使用pingd代替  
```

### 资源文件(/etc/ha.d/haresources)
Haresources文件用于指定双机系统的`主节点`、`集群IP`、`子网掩码`、`广播地址`以及`启动的服务`等集群资源，文件每一行可以包含一个或多个资源脚本名，资源之间使用空格隔开，参数之间使用两个冒号隔开，在两个HA节点上该文件必须完全一致，此文件的一般格式为：
`node-name network  <resource-group> `

`node-name`表示主节点的主机名，必须和`ha.cf`文件中指定的节点名一致，`network`用于设定集群的IP地址、子网掩码、网络设备标识等，需要注意的是，这里指定的IP地址就是`集群对外服务的IP地址`，`resource-group`用来指定需要heartbeat托管的服务，也就是这些服务可以由heartbeat来启动和关闭，如果要托管这些服务，必须将服务写成可以通过`start/stop`来启动和关闭的脚步，然后放到`/etc/init.d/`或者`/etc/ha.d/resource.d/`目录下，heartbeat会根据脚本的名称自动去`/etc/init.d`或者`/etc/ha.d/resource.d/`目录下找到相应脚步进行启动或关闭操作。
`LSB`： Linux标准脚本文件（init script），通常放在/etc/init.d/目录下，heartbeat1.x版本之前的管理脚本一半放在/etc/ha.d/resource.d，在这里是/usr/local/ha/etc/ha.d/resource.d 

`OCF`：Open Cluster Framework，默认放在/usr/lib/resource.d/heartbeat/目录下；在这里是/usr/local/ha/etc/ha.d/resource.d

**下面介绍一下ocf和lsb格式的区别**： 
`LSB格式的脚本必须支持status功能，必须能接收start,stop,status,三个参数`；
而如果是`OCF格式`,则必须支持`start,stop,monitor`三个参数.其中status和monitor参数是用来监控资源的,非常重要. 
例如LSB风格的脚本,运行./Mysql status时候， 返回值包含OK或则running则表示资源正常，返回值包含stopped或者No则表示资源不正常。 假如是OCF风格的脚本,运行./Mysql monitor时候, 返回0表示资源是正常的, 返回7表示资源出现问题. 
 
下面对配置方法进行具体说明：
`node1 IPaddr::192.168.60.200/24/eth0/  Filesystem::/dev/sdb5::/webdata::ext3  httpd tomcat`

其中，`node1`是HA集群的主节点，`IPaddr`为heartbeat自带的一个执行脚步，heartbeat首先将执行
`/etc/ha.d/resource.d/IPaddr 192.168.60.200/24 start`
的操作，也就是虚拟出一个子网掩码为`255.255.255.0`，IP为`192.168.60.200`的地址，此IP为heartbeat对外提供服务的网络地址，同时指定此IP使用的网络接口为eth0，接着，heartbeat将执行共享磁盘分区的挂载操作，
`“Filesystem::/dev/sdf1::/data1::ext3”`相当于在命令行下执行mount操作，
即`“mount –t ext3 /dev/sdf1 /data1”`，最后依次启动httpd和tomcat服务。

```
node1.test.com IPaddr::192.168.18.200/24/eth0 httpd
node1.test.com IPaddr::192.168.18.200/24/eth0 Filesystem::192.168.18.95:/web::/var/www/html::nfs  httpd
node1 IPaddr::192.168.79.135/24/eth0 drbddisk::r0 Filesystem::/dev/drbd1::/data::ext3

```

### 配置备份节点的heartbeat
备节点安装方式同主，配置文件要相同，拷贝主的配置文件到备。 
```    
    [root@node2 ~]#scp –r node1:/etc/ha.d/*  /etc/ha.d/
```

### 配置httpd并进行切换
node1 和 node2上都执行。
```
yum install httpd httpd-devel httpd-tools

#node1
echo "<h1>This is node1</h1> " > /var/www/html/index.html

#node1
echo "<h1>This is node1</h1> " > /var/www/html/index.html
```

>  安装的httpd服务不要设置自动启动，要用heartbeat来启动 ？    

### 启动heartbeat

首先启动主
`/etc/init.d/heartbeat start`

然后启动备
node1 Log：
```
Jul 21 18:09:22 node01 heartbeat: [5554]: info: Pacemaker support: false
Jul 21 18:09:22 node01 heartbeat: [5554]: WARN: Logging daemon is disabled --enabling logging daemon is recommended
Jul 21 18:09:22 node01 heartbeat: [5554]: info: **************************
Jul 21 18:09:22 node01 heartbeat: [5554]: info: Configuration validated. Starting heartbeat 3.0.4
Jul 21 18:09:22 node01 heartbeat: [5555]: info: heartbeat: version 3.0.4
Jul 21 18:09:22 node01 heartbeat: [5555]: WARN: No Previous generation - starting at 1437473363
Jul 21 18:09:22 node01 heartbeat: [5555]: info: Heartbeat generation: 1437473363
Jul 21 18:09:22 node01 heartbeat: [5555]: info: No uuid found for current node - generating a new uuid.
Jul 21 18:09:22 node01 heartbeat: [5555]: info: Creating FIFO /var/lib/heartbeat/fifo.
Jul 21 18:09:22 node01 heartbeat: [5555]: info: glib: UDP multicast heartbeat started for group 225.0.0.178 port 694 interface eth1 (ttl=1 loop=0)
Jul 21 18:09:22 node01 heartbeat: [5555]: info: glib: ping heartbeat started.
Jul 21 18:09:22 node01 heartbeat: [5555]: info: G_main_add_TriggerHandler: Added signal manual handler
Jul 21 18:09:22 node01 heartbeat: [5555]: info: G_main_add_TriggerHandler: Added signal manual handler
Jul 21 18:09:22 node01 heartbeat: [5555]: info: G_main_add_SignalHandler: Added signal handler for signal 17

## 这时备还没有启动-

Jul 21 18:09:22 node01 heartbeat: [5555]: info: Local status now set to: 'up'
Jul 21 18:09:22 node01 heartbeat: [5555]: info: Link 172.16.0.1:172.16.0.1 up.
Jul 21 18:09:22 node01 heartbeat: [5555]: info: Status update for node 172.16.0.1: status ping
Jul 21 18:09:49 node01 heartbeat: [5555]: info: Link node2:eth1 up.
Jul 21 18:09:49 node01 heartbeat: [5555]: info: Status update for node node2: status up
harc(default)[5565]:    2015/07/21_18:09:49 info: Running /etc/ha.d//rc.d/status status
Jul 21 18:09:50 node01 heartbeat: [5555]: info: Comm_now_up(): updating status to active
Jul 21 18:09:50 node01 heartbeat: [5555]: info: Local status now set to: 'active'
Jul 21 18:09:51 node01 heartbeat: [5555]: info: Status update for node node2: status active
harc(default)[5585]:    2015/07/21_18:09:51 info: Running /etc/ha.d//rc.d/status status
Jul 21 18:10:02 node01 heartbeat: [5555]: info: remote resource transition completed.
Jul 21 18:10:02 node01 heartbeat: [5555]: info: remote resource transition completed.
Jul 21 18:10:02 node01 heartbeat: [5555]: info: Initial resource acquisition complete (T_RESOURCES(us))



/usr/lib/ocf/resource.d//heartbeat/IPaddr(IPaddr_172.16.0.210)[5645]:   2015/07/21_18:10:02 INFO:  Resource is stopped
Jul 21 18:10:03 node01 heartbeat: [5609]: info: Local Resource acquisition completed.
harc(default)[5728]:    2015/07/21_18:10:03 info: Running /etc/ha.d//rc.d/ip-request-resp ip-request-resp
ip-request-resp(default)[5728]: 2015/07/21_18:10:03 received ip-request-resp IPaddr::172.16.0.210/24/eth0 OK yes
ResourceManager(default)[5751]: 2015/07/21_18:10:03 info: Acquiring resource group: node01
IPaddr::172.16.0.210/24/eth0 httpd
/usr/lib/ocf/resource.d//heartbeat/IPaddr(IPaddr_172.16.0.210)[5779]:   2015/07/21_18:10:03 INFO:  Resource is stopped

ResourceManager(default)[5751]: 2015/07/21_18:10:03 info: Running /etc/ha.d/resource.d/IPaddr 172.16.0.210/24/eth0 start
IPaddr(IPaddr_172.16.0.210)[5904]:      2015/07/21_18:10:04 INFO: Adding inet address 172.16.0.210/24 with broadcast address 172.16.0.255 to device eth0
IPaddr(IPaddr_172.16.0.210)[5904]:      2015/07/21_18:10:04 INFO: Bringing device eth0 up
IPaddr(IPaddr_172.16.0.210)[5904]:      2015/07/21_18:10:04 INFO: /usr/libexec/heartbeat/send_arp -i 200 -r 5 -p /var/run/resource-agents/send_arp-172.16.0.210 eth0 172.16.0.210 auto not_used not_used
/usr/lib/ocf/resource.d//heartbeat/IPaddr(IPaddr_172.16.0.210)[5878]:   2015/07/21_18:10:04 INFO:  Success
Jul 21 18:12:42 node01 heartbeat: [5555]: info: Heartbeat shutdown in progress. (5555)
Jul 21 18:12:42 node01 heartbeat: [6003]: info: Giving up all HA resources.
ResourceManager(default)[6016]: 2015/07/21_18:12:43 info: Releasing resource group: node01 IPaddr::172.16.0.210/24/eth0 httpd
```

## 故障模拟

- 停止主heartbeat
备机可以接管

- 开启主heartbeat
如果`auto_failback`为on 主的重新启动会抢占回来资源

- down掉主心跳线模拟脑裂
 裂脑了
- down httpd
down 掉httpd时, 不会切换, heartbeat不能检测到httpd的状态, 需要手动写脚本

- 让主节点系统内核崩溃
    当主节点系统崩溃后，网络也就失去了响应，那么备用节点的heartbeat进程就会立刻检测到主节点网络故障，然后进行资源切换，但是由于主节点系统内核崩溃，导致自身不能卸载所占有的资源，例如共享磁盘分区、集群服务IP等，那么此时如果没有类似Stonith设备的话，就会出现资源争用的情况，但是如果有Stonith设备，Stonith设备会首先将故障的主节点电源关闭或者重启此节点等操作，这样就让主节点释放了集群资源，当Stonith设备完成所有操作时，备份节点才拿到接管主节点资源的所有权，从而接管主节点的资源。 

## heartbeat与keepalived的区别


## heartbeat的注意事项
1. heartbeat 可以有多台组成,
2. heartbeat 版本选择
3. heartbeat的对于应用的监控问题


## 脑裂原因：
- 高可用服务器对之间的心跳线链路故障，导致无法正常通信
1. 心跳线问题(断了，松动，老化)
2. 网卡问题（相关驱动），IP配置以及冲突。
3. 心跳线间连接设备故障(网卡以及交换机)
4. 仲裁的机器出问题。

- 高可用服务器对上开启了防火墙阻挡了心跳信息。
- 其他服务配置不当等原因。如心跳方式不同，心跳广播方式不同，软件bug等


  [1]: http://www.linux-ha.org
  [2]: http://linux-ha.org
