# DRBD

## DRBD是什么?
 Distributed Replicated Block Device, 是软件实现,没有共享存储的,在各台主机 通过复制镜像设备块(硬盘,分区, 逻辑分区等).

 **工作原理**:
 每个设备（drbd 提供了不止一个设备）都有一个状态，可能是‘主’状态或‘从’状态。在主节点上，应用程序应能运行和访问drbd设备（/dev/drbd*）。每次写入都会发往本地磁盘设备和从节点设备中。从节点只能简单地把数据写入它的磁盘设备上。 读取数据通常在本地进行。 如果主节点发生故障，心跳（heartbeat或corosync）将会把从节点转换到主状态，并启动其上的应用程序。（如果您将它和无日志FS 一起使用，则需要运行fsck）。如果发生故障的节点恢复工作，它就会成为新的从节点，而且必须使自己的内容与主节点的内容保持同步。当然，这些操作不会干扰到后台的服务。


__DRBD与HA集群__:
 大部分现行高可用性集群（如：惠普、IBM、Dell）使用的是共享存储器，因此存储器连接多个节点（用共享的SCSI 总线或光纤通道就可以做到）。DRBD 也可以作为一个共享的设备，但是它并不需要任何不常见的硬件。它在IP 网络中运行，而且在价格上IP 网络要比专用的存储网络经济的多。目前，DRBD 每次只允许对一个节点进行读写访问，这对于通常的故障切换高可用性集群来讲已经足够用了。现在的版本将支持两个节点同时进行读写存取。这很有用，比如对GFS 来讲就是如此。兼容性DRBD可以在IDE、SCSI 分区和整个驱动器之上运行，但不能在回路模块设备上运行。（如果您硬要这样做，它就会发生死锁）。DRBD 也不能在回送网络设备中运行。（因为它同样会发生死锁：所有请求都会被发送设备占用，发送流程也会阻塞在sock_sendmsg（）中。有时，接收线程正从网络中提取数据块，并试图把它放在高速缓存器中；但系统却要把一些数据块从高速缓存器中取到磁盘中。这种情况往往会在接收器的环境下发生，因为所有的请求都已经被接收器块占用了。

 drbd镜像数据的特点:
 1. 实时的
 2. 透明, 通过复制设备块, 对上层软件透明
 3. 同步或者异步的复制.

drbd的核心是通过Linux的内核是实现的. drbd构成虚拟设备块,所以它是位于系统的I/O协议栈.

**drbd功能**
1. 单主模式: 
2. 双主模式:  这种多终端写的模式,需要有文件锁的文件系统的使用, 如GFS,OCFS, 默认是关闭的, 需要在配置文件中开启

__drbd的数据校验__
drbd通过块级别的校验通过MD5,SHA-1, CRC-32C.

__脑裂的通知和自动恢复__


## DRBD的版本
1. drbd 8.0-8.3
2. drbd 8.4.x
3. drbd 9.x

### DRBD 复制模式
`协议A`：异步复制协议。本地写成功后立即返回，数据放在发送buffer中，可能丢失。

`协议B`：内存同步（半同步）复制协议。本地写成功并将数据发送到对方后立即返回，如果双机掉电，数据可能丢失。

`协议C`：同步复制协议。本地和对方写成功确认后返回。如果双机掉电或磁盘同时损坏，则数据可能丢失。

`一般用协议C`，但选择C协议将影响流量，从而影响网络时延。为了数据可靠性，我们在生产环境中还是用C协议。

### 角色
在drbd构造的集群中，资源具有角色的概念，分别为`primary`和`secondary`。
所有设为primary的资源将不受限制进行读写操作。可以创建文件系统，可以使用裸设备,甚至直接io。所有设为secondary的设备中不能挂载，不能读写

### 传输协议
1. TCP over IPv4
2. TCP over IPv6
3. SDP: BSD风格的
4. SuperSockets:


### 高效的同步:

## DRBD的管理工具
drbd通过`drdbadm`, `drbdsetup`, `drbdmeta`等命令管理.
主要配置文件为`/etc/drbd.conf`
`drbdadm`：高级管理工具，管理/etc/drbd.conf，向drbdsetup和drbdmeta发送指令。
`drbdsetup`：配置装载进kernel的DRBD模块，平时很少直接用。
`drbdmeta`：管理META数据结构，平时很少直接用。

### drbd配置文件

DRBD的主配置文件为`/etc/drbd.conf`；为了管理的便捷性，目前通常会将些配置文件分成多个部分，且都保存至`/etc/drbd.d`目录中，主配置文件中仅使用`include`指令将这些配置文件片断整合起来。通常，`/etc/drbd.d`目录中的配置文件为`global_common.conf`和所有以`.res`结尾的文件。其中`global_common.conf`中主要定义`global`段和`common`段，而每一个`.res`的文件用于定义一个资源。
在配置文件中，`global段仅能出现一次`，且如果所有的配置信息都保存至同一个配置文件中而不分开为多个文件的话`，global段必须位于配置文件的最开始处`。目前global段中可以定义的参数仅有`minor-count`, `dialog-refresh`, `disable-ip-verification`和`usage-count`。

`common段`则用于定义被每一个资源默认继承的参数，可以在资源定义中使用的参数都可以在common段中定义。实际应用中，common段并非必须，但建议将多个资源共享的参数定义为common段中的参数以降低配置文件的复杂度。

`net`：网络配置相关的内容，可以设置是否允许双主节点（allow-two-primaries）等。

`startup`：启动时候的相关设置，比如设置启动后谁作为primary（或者两者都是primary：become-primary-on both）

`syncer`： 同步相关的设置。可以设置“重新”同步（re-synchronization）速度（rate）设置，也可以设置是否在线校验节点之间的数据一致性 （verify-alg 检测算法有md5，sha1以及crc32等）。数据校验可能是一个比较重要的事情，在打开在线校验功能后，我们可以通过相关命令（`drbdadm verify resource_name`）来启动在线校验。在校验过程中，drbd会记录下节点之间不一致的block，但是不会阻塞任何行为，即使是在该不一致的 block上面的io请求。当不一致的block发生后，drbd就需要有re-synchronization动作，而syncer里面设置的rate 项，主要就是用于re-synchronization的时候，因为如果有大量不一致的数据的时候，我们不可能将所有带宽都分配给drbd做re- synchronization，这样会影响对外提提供服务。rate的设置和还需要考虑IO能力的影响。如果我们会有一个千兆网络出口，但是我们的磁盘 IO能力每秒只有50M，那么实际的处理能力就只有50M，一般来说，设置网络IO能力和磁盘IO能力中最小者的30%的带宽给re- synchronization是比较合适的（官方说明）。另外，drbd还提供了一个临时的rate更改命令，可以临时性的更改syncer的rate 值：
`drbdsetup /dev/drbd0 syncer -r 100M`
这样就临时的设置了re-synchronization的速度为`100M`。不过在re-synchronization结束之后，你需要通过
`drbdadm adjust resource_name`
来让drbd按照配置中的rate来工作



`resource段`则用于定义drbd资源，每个资源通常定义在一个单独的位于`/etc/drbd.d`目录中的以`.res`结尾的文件中。资源在定义时必须为其命名，名字可以由非空白的ASCII字符组成。每一个资源段的定义中至少要包含两个host子段，以定义此资源关联至的节点，其它参数均可以从common段或drbd的默认中进行继承而无须定义。

__资源节点的配置__
`Resource name`：可以是除了空白字符的任意的ACSII码字符
`DRBD device`：在双方节点上，此DRBD设备的设备文件；一般为/dev/drbdN，其主设备号147
`Disk configuration`：在双方节点上，各自提供的存储设备
`Nerwork configuration`：双方数据同步时所使用的网络属性

### metadata
DRBD将数据的各种信息块保存在一个专用的区域里，这些metadata包括了
1. DRBD设备的大小
2. 产生的标识
3. 活动日志
4. 快速同步的位图
5. 
metadata的存储方式有`内部`和`外部`两种方式，使用哪种配置都是在资源配置中定义的

#### 内部meta data
内部metadata存放在同一块硬盘或分区的最后的位置上
__优点__：metadata和数据是紧密联系在一起的，如果硬盘损坏，metadata同样就没有了，同样在恢复的时候，metadata也会一起被恢复回来
__缺点__：metadata和数据在同一块硬盘上，对于写操作的吞吐量会带来负面的影响，因为应用程序的写请求会触发metadata的更新，这样写操作就会造成两次额外的磁头读写移动。
#### 外部meta data
外部的metadata存放在和数据磁盘分开的独立的块设备上
__优点__：对于一些写操作可以对一些潜在的行为提供一些改进
__缺点__：metadata和数据不是联系在一起的，所以如果数据盘出现故障，在更换新盘的时候就需要认为的干预操作来进行现有node对心硬盘的同步了
如果硬盘上有数据，并且硬盘或者分区不支持扩展，或者现有的文件系统不支持shrinking，那就必须使用外部metadata这种方式了。
可以通过下面的命令来计算metadata需要占用的扇区数


```
resource web { #资源名为“web”
  on yimiwork_215 { #设置节点cluster1 
    device    /dev/drbd0; #指出drbd的标示名   
    disk      /dev/sda5; #指出作为drbd的设备 
    address   172.16.100.11:7789; #指定ip和端口号 
    meta-disk internal; #网络通信属性，指定drbd的元数据在本机   
  }   
  on yimiwork_216 {   
    device    /dev/drbd0;   
    disk      /dev/sda5;   
    address   172.16.100.12:7789;   
    meta-disk internal;   
  }   
}
```

### 配置文件解析
- 1.drbd.conf
```
include "drbd.d/global_common.conf";
include "drbd.d/*.res";
```

- 2.drbd.d/global_common.conf
```
# DRBD is the result of over a decade of development by LINBIT.
# In case you need professional services for DRBD or have
# feature requests visit http://www.linbit.com

global {
        usage-count yes; # 是否被linbit公司统计数量
        # minor-count dialog-refresh disable-ip-verification
        # cmd-timeout-short 5; cmd-timeout-medium 121; cmd-timeout-long 600;
}

common {
        handlers {
                # These are EXAMPLE handlers only.
                # They may have severe implications,
                # like hard resetting the node under certain circumstances.
                # Be careful when chosing your poison.
                # 在一些时间发生时,一些处理操作
                # pri-on-incon-degr "/usr/lib/drbd/notify-pri-on-incon-degr.sh; /usr/lib/drbd/notify-emergency-reboot.sh; echo b > /proc/sysrq-trigger ; reboot -f";
                # pri-lost-after-sb "/usr/lib/drbd/notify-pri-lost-after-sb.sh; /usr/lib/drbd/notify-emergency-reboot.sh; echo b > /proc/sysrq-trigger ; reboot -f";
                # local-io-error "/usr/lib/drbd/notify-io-error.sh; /usr/lib/drbd/notify-emergency-shutdown.sh; echo o > /proc/sysrq-trigger ; halt -f";
                # fence-peer "/usr/lib/drbd/crm-fence-peer.sh";
                # split-brain "/usr/lib/drbd/notify-split-brain.sh root";
                # out-of-sync "/usr/lib/drbd/notify-out-of-sync.sh root";
                # before-resync-target "/usr/lib/drbd/snapshot-resync-target-lvm.sh -p 15 -- -c 16k";
                # after-resync-target /usr/lib/drbd/unsnapshot-resync-target-lvm.sh;
        }

        startup {
                # wfc-timeout degr-wfc-timeout outdated-wfc-timeout wait-after-sb
        }

        options {
                # cpu-mask on-no-data-accessible
        }
        disk {
                # on-io-error <strategy>;配置I/O错误处理策略为 detach pass_on 这是默认和推荐的选项，如果在节点上发生底层的硬盘I/O错误，它会将设备运行在Diskless无盘模式下
                pass_on：DRBD会将I/O错误报告到上层，在主节点上，它会将其报告给挂载的文件系统，但是在此节点上就往往忽略（因此此节点上没有可以报告的上层）
-local-in-error：调用本地磁盘I/O处理程序定义的命令；这需要有相应的local-io-error调用的资源处理程序处理错误的命令；这就给管理员有足够自由的权力命令命令或是脚本调用local-io-error处理I/O错误

                # size on-io-error fencing disk-barrier disk-flushes 
                # disk-drain md-flushes resync-rate resync-after al-extents
                # c-plan-ahead c-delay-target c-fill-target c-max-rate
                # c-min-rate disk-timeout
        }

        net {
                # protocol timeout max-epoch-size max-buffers unplug-watermark
                # connect-int ping-int sndbuf-size rcvbuf-size ko-count
                # allow-two-primaries cram-hmac-alg shared-secret after-sb-0pri
                # after-sb-1pri after-sb-2pri always-asbp rr-conflict
                # ping-timeout data-integrity-alg tcp-cork on-congestion
                # congestion-fill congestion-extents csums-alg verify-alg
                # use-rle
                # verify-alg <algorithm>; 校验方式sha1, md5, and crc32c
               # protocol C; # 同步方式为C
               #  data-integrity-alg <algorithm>; 复制刘璐完整性验证
               #cram-hmac-alg "sha1"; #设置加密算法sha1  
               # shared-secret "mydrbdlab"; #设置加密key  
        }
        syncer { 
            rate 200M;  # 时的网络速率最大值，单位是字节 200M * 0.3 mb/s
        }
}
            
```

- 3.drbd.d/.res
```
resource web {
    device    /dev/drbd0;#DRBD设备名称
    disk      /dev/sdb1; #drbd0使用的磁盘分区为"sdb1"
    meta-disk internal;
    
    on yimiwork_215 { #第个主机说明以on开头，后面是主机名称
        address   192.168.1.201:7789; #设置DRBD监听地址与端口
    }
    on yimiwork_216 {
        address   192.168.1.202:7789;
   }
}
```
### 二进制安装 8.4

CentOS:
```
yum install -y gcc gcc-c++ make perl kernel-devel kernel-headers flex
wget http://mirror.symnds.com/distributions/elrepo/elrepo/el6/x86_64/RPMS/elrepo-release-6-6.el6.elrepo.noarch.rpm

yum localinstall elrepo-release-6-6.el6.elrepo.noarch.rpm 
yum install drbd84-utils
yum install drbd84 kmod-drbd84

```

Debian:
```
apt-get install drbd8-utils
# or
apt-get install drbd8-utils drbd8-module

```
### 源码安装
```
# http://mirror.symnds.com/distributions/elrepo/elrepo/el6/x86_64/RPMS/
# wget http://mirror.symnds.com/distributions/elrepo/elrepo/el6/x86_64/RPMS/drbd84-utils-8.9.5-1.el6.elrepo.x86_64.rpm
#安装依赖包
yum install -y gcc gcc-c++ make perl kernel-devel kernel-headers flex 

rpm -vih drbd84-utils-8.4.4-2.el6.elrepo.x86_64.rpm kmod-drbd84-8.4.4-1.el6.elrepo.x86_64.rpm

tar zxvf drbd-8.4.4.tar.gz
cd drbd-8.4.4
./configure --prefix=/usr/local/drbd --with-km #--with-km，启用内核模块
make KDIR=/usr/src/kernels/2.6.32-358.23.2.el6.x86_64/ #指定内核源码路径，根据自己系统来
make install

chkconfig --add drbd
chkconfig drbd on

cp drbd/drbd.ko /lib/modules/`uname -r`/kernel/lib/   #加载DRBD模块到内核中
modprobe drbd
lsmod | grep drbd  #由此查看drbd模块已经加载
drbd                  333755  0
libcrc32c 

```

### 配置drbd的步骤
1. 准备一个磁盘或者一个分区
  磁盘可以是分区,软raid分区,LVM分区,或者其他的块设备
  比如/dev/sda7
2. 配置网络,
  - 确保网络质量,建议进行bonding,active-backup
  - 机器之间的防火墙设置,drbd通过两个端口进行监听和复制,7788,7789
  - selinux的设置
3. 配置drbd的资源, 修改配置文件
4. 在主的server上初始化drbd的资源
5. 启动服务
6. 做主从的同步的初始化.


## drbd运行维护
`drbd-overview`, `cat /proc/drbd`
```
cat /proc/drbd #查看drbd状态，显示两个节点默认都处于Secondary状态
version: 8.4.4 (api:1/proto:86-101)
GIT-hash: 599f286440bd633d15d5ff985204aff4bccffadd build by phil@Build64R6, 2013-10-14 15:33:06
 0: cs:Connected ro:Secondary/Secondary ds:Inconsistent/Inconsistent C

```
cs：两台数据连接状态
ro：两台主机的状态
ds：磁盘状态是“UpToDate/UpToDate”，同步状态。
dw: 表示磁盘写信息
dr: 表示磁盘读信息

### drbd的drbd-overview的值
```
[root@yimiwork_216 data]# drbd-overview 
 1:drbd/0  WFConnection Primary/Unknown UpToDate/DUnknown /data ext4 2.0G 56M 1.8G 3% 
```
本地和对等节点的硬盘有可能为下列状态之一：
`Diskless 无盘`：本地没有块设备分配给DRBD使用，这表示没有可用的设备，或者使用drbdadm命令手工分离或是底层的I/O错误导致自动分离
`Attaching`：读取无数据时候的瞬间状态
`Failed 失败`：本地块设备报告I/O错误的下一个状态，其下一个状态为Diskless无盘
`Negotiating`：在已经连接的DRBD设置进行Attach读取无数据前的瞬间状态
`Inconsistent`：数据是不一致的，在两个节点上（初始的完全同步前）这种状态出现后立即创建一个新的资源。此外，在同步期间（同步目标）在一个节点上出现这种状态
`Outdated`：数据资源是一致的，但是已经过时
`DUnknown`：当对等节点网络连接不可用时出现这种状态
`Consistent`：一个没有连接的节点数据一致，当建立连接时，它决定数据是UpToDate或是Outdated
`UpToDate`：一致的最新的数据状态，这个状态为正常状态

`ds:UpToDate/Inconsistent`表示两节点正在同步数据

### 连接状态
资源的连接状态；一个资源可能有以下连接状态中的一种
`StandAlone 独立的`：网络配置不可用；资源还没有被连接或是被管理断开（使用 drbdadm disconnect 命令），或是由于出现认证失败或是脑裂的情况

`Disconnecting 断开`：断开只是临时状态，下一个状态是StandAlone独立的
Unconnected 

悬空：是尝试连接前的临时状态，可能下一个状态为`WFconnection`和`WFReportParams`

`Timeout 超时`：与对等节点连接超时，也是临时状态，下一个状态为Unconected悬空
`BrokerPipe`：与对等节点连接丢失，也是临时状态，下一个状态为Unconected悬空
`NetworkFailure`：与对等节点推动连接后的临时状态，下一个状态为Unconected悬空
`ProtocolError`：与对等节点推动连接后的临时状态，下一个状态为Unconected悬空
`TearDown 拆解`：临时状态，对等节点关闭，下一个状态为Unconected悬空
`WFConnection`：等待和对等节点建立网络连接
`WFReportParams`：已经建立TCP连接，本节点等待从对等节点传来的第一个网络包
`Connected 连接`：DRBD已经建立连接，数据镜像现在可用，节点处于正常状态
`StartingSyncS`：完全同步，有管理员发起的刚刚开始同步，未来可能的状态为SyncSource或PausedSyncS
`StartingSyncT`：完全同步，有管理员发起的刚刚开始同步，下一状态为WFSyncUUID
`WFBitMapS`：部分同步刚刚开始，下一步可能的状态为SyncSource或PausedSyncS
`WFBitMapT`：部分同步刚刚开始，下一步可能的状态为WFSyncUUID
`WFSyncUUID`：同步即将开始，下一步可能的状态为SyncTarget或PausedSyncT
`SyncSource`：以本节点为同步源的同步正在进行
`SyncTarget`：以本节点为同步目标的同步正在进行
`PausedSyncS`：以本地节点是一个持续同步的源，但是目前同步已经暂停，可能是因为另外一个同步正在进行或是使用命令(drbdadm pause-sync)暂停了同步
`PausedSyncT`：以本地节点为持续同步的目标，但是目前同步已经暂停，这可以是因为另外一个同步正在进行或是使用命令(drbdadm pause-sync)暂停了同步
`VerifyS`：以本地节点为验证源的线上设备验证正在执行
`VerifyT`：以本地节点为验证目标的线上设备验证正在执行

### 启用和禁用资源
```
######手动启用资源
drbdadm up <resource>
######手动禁用资源
drbdadm down <resource>
注释：
resource：为资源名称；当然也可以使用all表示[停用|启用]所有资源
```
### 升级和降级资源
```
######升级资源
drbdadm primary <resource>
######降级资源
drbdadm secondary <resource>
注释：在单主模式下的DRBD，两个节点同时处于连接状态，任何一个节点都可以在特定的时间内变成主；但两个节点中只能一为
```

### 重新配置资源
`drbdadm adjust <resource>/all`

### 在线验证
验证算法的配置
```
resource <resource>
  net {
    verify-alg <algorithm>;
  }
  ...
}
or在common配置
```
```
 drbdadm verify <resource>
```

### 临时的设置同步的速率
```
drbdadm disk-options --c-plan-ahead=0 --resync-rate=110M <resource>
# 恢复或者重启
 drbdadm adjust <resource>
```

### 拥塞策略和暂停复制的配置
```
resource <resource> {
  net {
    on-congestion pull-ahead;
    congestion-fill 2G;
    congestion-extents 2000;
    ...
  }
  ...
}
```

### 禁用缓存
```
resource <resource>
  disk {
    disk-flushes no;
    ...
  }
  ...
}
```

### 脑裂时处理(建议手动修复)
```
resource <resource>
  handlers {
    split-brain <handler>;
    split-brain "/usr/lib/drbd/notify-split-brain.sh root";
    ...
  }
  ...
}
```

### 调整文件系统的大小
[官网](https://www.drbd.org/en/doc/users-guide-84/s-resizing)


## 实例(单主)
|主机名| 应用IP|数据IP|功能|磁盘|
|---|---|---|---|---|
|yimiwork_215|192.168.8.215|192.168.80.215|primary|/dev/sdb|
|yimiwork_216|192.168.8.216|192.168.80.216|standby|/dev/sdb|

### 1.安装epel源
### 2.安装drbd
```bash
yum install -y gcc gcc-c++ make perl kernel-devel kernel-headers flex
wget http://mirror.symnds.com/distributions/elrepo/elrepo/el6/x86_64/RPMS/elrepo-release-6-6.el6.elrepo.noarch.rpm

yum localinstall elrepo-release-6-6.el6.elrepo.noarch.rpm 
yum install drbd84-utils
yum install drbd84 kmod-drbd84
modprobe drbd
# 如果升级了 kernel 重启
reboot
```
### 3.在主上配置drbd
```
#global_common.conf

global {
        usage-count no;
        # minor-count dialog-refresh disable-ip-verification
        # cmd-timeout-short 5; cmd-timeout-medium 121; cmd-timeout-long 600;
}

common {
       protocol C;      #使用DRBD的同步协议

        disk {
            on-io-error detach;
        }
        handler {
             pri-on-incon-degr "echo o > /proc/sysrq-trigger ; halt -f";
                pri-lost-after-sb "echo o > /proc/sysrq-trigger ; halt -f";
                local-io-error "echo o > /proc/sysrq-trigger ; halt -f";
                fence-peer "/usr/lib64/heartbeat/drbd-peer-outdater -t 5";
                pri-lost "echo pri-lost. Have a look at the log files. | mail -s 'DRBD Alert' reboot";
                split-brain "/usr/lib/drbd/notify-split-brain.sh root";
                out-of-sync "/usr/lib/drbd/notify-out-of-sync.sh root";
                before-resync-target "/usr/lib/drbd/snapshot-resync-target-lvm.sh -p 15 -- -c 16k";
                after-resync-target /usr/lib/drbd/unsnapshot-resync-target-lvm.sh;
        }
        net {
            cram-hmac-alg "sha1"; #设置加密算法
            shared-secret "safasdfsaf";
        }

       syncer {
           rate 900M; # 设置主备节点同步时的网络速率
       }
}

# drbd.res drbd.res 与资源的名字要一致
resource drbd{

    device    /dev/drbd0;
    disk      /dev/sdb1;
    meta-disk internal;

    on yimiwork_215 {
        address   192.168.80.215:7789;
    }
    on  yimiwork_216 {
        address   192.168.80.216:7789;
   }

}

```

### 4.复制配置文件到从机.使其两端的配置一样
### 5.初始化资源并在启动服务
```
# yimiwork_215
[root@yimiwork_215 ~]# drbdadm create-md drbd
initializing activity log
NOT initializing bitmap
Writing meta data...
New drbd meta data block successfully created.

# yimiwork_216
[root@yimwork_216 ~]# drbdadm create-md drbd
initializing activity log
NOT initializing bitmap
Writing meta data...
New drbd meta data block successfully created.

# yimiwork_215
/etc/init.d/drbd start 
Starting DRBD resources: [
     create res: drbd
   prepare disk: drbd
    adjust disk: drbd
     adjust net: drbd
]
.

# yimiwork_216
/etc/init.d/drbd start
Starting DRBD resources: [
     create res: drbd
   prepare disk: drbd
    adjust disk: drbd
     adjust net: drbd
]
.


```

### 6.查看启动状态
```
# yimiwork_215
[root@yimiwork_215 ~]# cat /proc/drbd
version: 8.4.7-1 (api:1/proto:86-101)
GIT-hash: 3a6a769340ef93b1ba2792c6461250790795db49 build by mockbuild@Build64R6, 2016-01-12 13:27:11

 1: cs:Connected ro:Secondary/Secondary ds:Inconsistent/Inconsistent C r-----
    ns:0 nr:0 dw:0 dr:0 al:0 bm:0 lo:0 pe:0 ua:0 ap:0 ep:1 wo:f oos:2096348

# yimiwork_216
[root@yimiwork_216 ~]# cat /proc/drbd
version: 8.4.7-1 (api:1/proto:86-101)
GIT-hash: 3a6a769340ef93b1ba2792c6461250790795db49 build by mockbuild@Build64R6, 2016-01-12 13:27:11

 1: cs:Connected ro:Secondary/Secondary ds:Inconsistent/Inconsistent C r-----
    ns:0 nr:0 dw:0 dr:0 al:0 bm:0 lo:0 pe:0 ua:0 ap:0 ep:1 wo:f oos:2096348

```
__命令查看一下__
yimiwork_215
```
drbd-overview  
1:drbd/0  Connected Secondary/Secondary Inconsistent/Inconsistent 
```
yimiwork_216
```
drbd-overview  
1:drbd/0  Connected Secondary/Secondary Inconsistent/Inconsistent 
```

从上面的信息中可以看出此时两个节点均处于Secondary状态。于是，我们接下来需要将其中一个节点设置为Primary。在要设置为Primary的节点上执行如下命令：`drbdsetup /dev/drbd0 primary –o` ,也可以在要设置为Primary的节点上使用如下命令来设置主节点：


`drbdadm -- --overwrite-data-of-peer primary drbd`

### 7.将yimiwork_215设置为主节点
```bash
#yimiwork_215为主节点 
[root@yimiwork_215 ~]# drbdadm -- --overwrite-data-of-peer primary drbd
[root@yimiwork_215 ~]# drbd-overview 
 1:drbd/0  SyncSource Primary/Secondary UpToDate/Inconsistent 
    [=>..................] sync'ed: 14.9% (1786076/2096348)K          
[root@yimiwork_215 ~]# drbd-overview 
 1:drbd/0  SyncSource Primary/Secondary UpToDate/Inconsistent 
    [===>................] sync'ed: 24.1% (1596636/2096348)K          
[root@yimiwork_215 ~]# drbd-overview 
 1:drbd/0  SyncSource Primary/Secondary UpToDate/Inconsistent 
    [====>...............] sync'ed: 25.8% (1559772/2096348)K          
[root@yimiwork_215 ~]# drbd-overview 
 1:drbd/0  SyncSource Primary/Secondary UpToDate/Inconsistent 
    [====>...............] sync'ed: 27.6% (1519836/2096348)K
#注：大家可以看到正在同步数据，得要一段时间

 drbd-overview #yimiwork_216为从节点 
 [root@yimiwork_216 ~]# drbd-overview 
 1:drbd/0  Connected Secondary/Primary UpToDate/UpToDate 
```

同步完成后，查看一下
```bash
[root@yimiwork_215 ~]# drbd-overview 
   1:drbd/0  Connected Primary/Secondary UpToDate/UpToDate 
[root@yimiwork_216 ~]# drbd-overview 
  1:drbd/0  Connected Primary/Secondary UpToDate/UpToDate 
```

### 8.格式化并挂载 (只格式化主的, 从会同步过去)
```bash 
[root@yimiwork_215 ~]# mkfs.ext4 /dev/drbd1
mke2fs 1.41.12 (17-May-2010)
Filesystem label=
OS type: Linux
Block size=4096 (log=2)
Fragment size=4096 (log=2)
Stride=0 blocks, Stripe width=0 blocks
131072 inodes, 524087 blocks
26204 blocks (5.00%) reserved for the super user
First data block=0
Maximum filesystem blocks=536870912
16 block groups
32768 blocks per group, 32768 fragments per group
8192 inodes per group
Superblock backups stored on blocks: 
    32768, 98304, 163840, 229376, 294912

Writing inode tables: done                            
Creating journal (8192 blocks): done
Writing superblocks and filesystem accounting information: done

This filesystem will be automatically checked every 35 mounts or
180 days, whichever comes first.  Use tune2fs -c or -i to override.


[root@yimiwork_215 ~]# mkdir /data
[root@yimiwork_215 ~]# mount /dev/drbd1 /data
[root@yimiwork_215 ~]# mount
/dev/mapper/VolGroup-lv_root on / type ext4 (rw)
proc on /proc type proc (rw)
sysfs on /sys type sysfs (rw)
devpts on /dev/pts type devpts (rw,gid=5,mode=620)
tmpfs on /dev/shm type tmpfs (rw)
/dev/mapper/VolGroup-mydata on /mnt/xvdb1/mysqldata type xfs (rw)
/dev/sda1 on /boot type ext4 (rw)
/dev/mapper/VolGroup-LogVol02 on /home type ext4 (rw)
none on /proc/sys/fs/binfmt_misc type binfmt_misc (rw)
vmware-vmblock on /var/run/vmblock-fuse type fuse.vmware-vmblock (rw,nosuid,nodev,default_permissions,allow_other)
sunrpc on /var/lib/nfs/rpc_pipefs type rpc_pipefs (rw)
gvfs-fuse-daemon on /root/.gvfs type fuse.gvfs-fuse-daemon (rw,nosuid,nodev)
/dev/drbd1 on /data type ext4 (rw)

cd /data

[root@yimiwork_215 data]# cp /root/percona-server-5.6.26-74.0.tar.gz .
[root@yimiwork_215 data]# ls
lost+found  percona-server-5.6.26-74.0.tar.gz
[root@yimiwork_215 data]# 
[root@yimiwork_215 data]# 
[root@yimiwork_215 data]# touch {a,b,c}.txt
[root@yimiwork_215 data]# ls
a.txt  b.txt  c.txt  lost+found  percona-server-5.6.26-74.0.tar.gz
[root@yimiwork_215 data]# ls
a.txt  b.txt  c.txt  lost+found  percona-server-5.6.26-74.0.tar.gz
[root@yimiwork_215 data]# 


```

### 9.切换Primary和Secondary节点
说明：对主Primary/Secondary模型的drbd服务来讲，在某个时刻只能有一个节点为Primary，因此，要切换两个节点的角色，只能在先将原有的Primary节点设置为Secondary后，才能原来的Secondary节点设置为Primary。

* 9.1yimiwork_215:
```
[root@yimiwork_215 ~]# umount /data/ 
[root@yimiwork_215 ~]# drbdadm secondary drbd
```
* 9.2查看状态yimiwork_215
```
[root@yimiwork_216 ~]# drbd-overview 
 1:drbd/0  Connected Secondary/Secondary Inconsistent/Inconsistent 
[root@yimiwork_216 ~]# drbd-overview 
 1:drbd/0  Connected Secondary/Primary UpToDate/UpToDate
```
* 9.3 设置yimiwork_216为主
```
# yimiwork_216:
[root@yimiwork_216 ~]# drbdadm primary drbd
```
* 9.4 查看状态yimiwork_216
```
[root@yimiwork_216 ~]# drbd-overview 
 1:drbd/0  Connected Primary/Secondary UpToDate/UpToDate 
[root@yimiwork_216 ~]# mkdir /data  
[root@yimiwork_216 ~]# mount /dev/drbd1 /data/
```
* 9.5 使用下面的命令查看在此前在主节点上复制至此设备的文件是否存在   
```
[root@yimiwork_216 ~]# cd /data/
[root@yimiwork_216 data]# ls
a.txt  b.txt  c.txt  lost+found  percona-server-5.6.26-74.0.tar.gz

```

### 10.强制同步数据

## 三个节点的配置
```
resource r0 {
  net {
    protocol C;
  }

  on alice {
    device     /dev/drbd0;
    disk       /dev/sda6;
    address    10.0.0.1:7788;
    meta-disk internal;
  }

  on bob {
    device    /dev/drbd0;
    disk      /dev/sda6;
    address   10.0.0.2:7788;
    meta-disk internal;
  }
}

resource r0-U {
  net {
    protocol A;
  }

  stacked-on-top-of r0 {
    device     /dev/drbd10;
    address    192.168.42.1:7788;
  }

  on charlie {
    device     /dev/drbd10;
    disk       /dev/hda6;
    address    192.168.42.2:7788; # Public IP of the backup node
    meta-disk  internal;
  }
}
```

[官网三个节点](https://www.drbd.org/en/doc/users-guide-84/s-three-nodes)

## 脑裂以及修复

split brain实际上是指在某种情况下，造成drbd的两个节点断开连接，都以primary的身份来运行。当drbd某primary节点连接对方节点准备 发送信息的时候如果发现对方也是primary状态，那么会立刻自行断开连接，并认定当前已经发生split brain了，这时候他会在系统日志中记录以下信息：`“Split-Brain detected,dropping connection!”`当发生split brain之后，如果查看连接状态，其中至少会有一个是`StandAlone状态`，另外一个可能也是`StandAlone`（如果是同时发现split brain状态），也有可能是`WFConnection`的状态。

如果我们在配置文件中配置了自动解决`split brain`（好像linbit不推荐这样做），drbd会自行解决`split brain`问题，可通过如下策略进行配置:

1. Discarding modifications made on the “younger” primary。在这种模式下，当网络重新建立连接并且发现了裂脑，DRBD会丢弃最后切换到主节点上的主机所修改的数据。

2. Discarding modifications made on the “older” primary. 在这种模式下，当网络重新建立连接并且发现了裂脑，DRBD丢弃首先切换到主节点上的主机后所修改的数据。

3. Discarding modifications on the primary with fewer changes.在这种模式下，当网络重新建立连接并且发现了裂脑，DRBD会比较两台主机之间修改的数据量，并丢弃修改数据量较少的主机上的所有数据。

4. Graceful recovery from split brain if one host has had no intermediate changes.在这种模式下，如果其中一个主机在脑裂期间并没有数据修改，DRBD会自动重新进行数据同步，并宣布脑裂问题已解决。(这种情况几乎不可 能存在)

注意：
> 自动裂脑自动修复能不能被接受取决于个人应用。考虑 建立一个DRBD的例子库。在“丢弃修改比较少的主节点的修改”兴许对web应用好过数据库应用。与此相反，财务的数据库则是对于任何修改的丢失都是不能 容忍的，这就需要不管在什么情况下都需要手工修复裂脑问题。因此需要在启用裂脑自动修复前考虑你的应用情况。


如果没有配置 split brain自动解决方案，我们可以手动解决。首先我们必须要确定哪一边应该作为解决问题后的primary，一旦确定好这一点，那么我们同时也就确定接受 丢失在split brain之后另外一个节点上面所做的所有数据变更了。当这些确定下来后，我们就可以通过以下操作来恢复了：

1.首先在确定要作为secondary的节点上面切换成secondary并放弃该资源的数据：
```
    drbdadm secondary resource_name
    drbdadm — –discard-my-data connect resource_name
```
2.在要作为primary的节点重新连接secondary（如果这个节点当前的连接状态为WFConnection的话，可以省略）
```
    drbdadm connect resource_name
```
当作完这些动作之后，从新的primary到secondary的re-synchnorisation会自动开始。


脑裂发生时,节点变成了StandAlone, 选择一个节点,运行
```
drbdadm secondary <resource>
drbdadm connect --discard-my-data <resource>
```
如果另一个节点也是`StandALone`,然后在其上运行
```
drbdadm connect <resource>
```

### 实例

注释：我们还接着上面的实验继续进行，现在NOD2为主节点而NOD1为备节点
#### 1、断开主(parmary)节点；关机、断开网络或重新配置其他的IP都可以；这里选择的是断开网络
#### 2、查看两节点状态
```
[root@nod2 ~]# drbd-overview
0:drbd/0WFConnection Primary/UnknownUpToDate/DUnknownC r----- /mntext4 2.0G 68M 1.9G 4%
[root@nod1 ~]# drbd-overview
0:drbd/0StandAlone Secondary/UnknownUpToDate/DUnknownr-----

######由上可以看到两个节点已经无法通信；NOD2为主节点，NOD1为备节点
```


#### 3、将NOD1节点升级为主(primary)节点并挂载资源
```
[root@nod1 ~]# drbdadm primary drbd
[root@nod1 ~]# drbd-overview
0:drbd/0StandAlone Primary/UnknownUpToDate/DUnknownr-----
[root@nod1 ~]# mount /dev/drbd0 /mnt/
[root@nod1 ~]# mount | grep drbd0
/dev/drbd0on /mnttypeext4 (rw)
```

#### 4、假如原来的主(primary)节点修复好重新上线了，这时出现了脑裂情况
```
[root@nod2 ~]# tail -f /var/log/messages
Sep 19 01:56:06 nod2 kernel: d-con drbd: Terminating drbd_a_drbd
Sep 19 01:56:06 nod2 kernel: block drbd0: helper command: /sbin/drbdadminitial-split-brain minor-0 exitcode 0 (0x0)
Sep 19 01:56:06 nod2 kernel: block drbd0: Split-Brain detected but unresolved, dropping connection!
Sep 19 01:56:06 nod2 kernel: block drbd0: helper command: /sbin/drbdadmsplit-brain minor-0
Sep 19 01:56:06 nod2 kernel: block drbd0: helper command: /sbin/drbdadmsplit-brain minor-0exitcode 0 (0x0)
Sep 19 01:56:06 nod2 kernel: d-con drbd: conn( NetworkFailure -> Disconnecting )
Sep 19 01:56:06 nod2 kernel: d-con drbd: error receiving ReportState, e: -5 l: 0!
Sep 19 01:56:06 nod2 kernel: d-con drbd: Connection closed
Sep 19 01:56:06 nod2 kernel: d-con drbd: conn( Disconnecting -> StandAlone )
Sep 19 01:56:06 nod2 kernel: d-con drbd: receiver terminated
Sep 19 01:56:06 nod2 kernel: d-con drbd: Terminating drbd_r_drbd
Sep 19 01:56:18 nod2 kernel: block drbd0: role( Primary -> Secondary )
```
#### 5、再次查看两节点的状态
```
[root@nod1 ~]# drbdadm role drbd
Primary/Unknown
[root@nod2 ~]# drbdadm role drbd
Primary/Unknown
```

#### 6、查看NOD1与NOD2连接状态
```
[root@nod1 ~]# drbd-overview
0:drbd/0StandAlone Primary/UnknownUpToDate/DUnknownr----- /mntext4 2.0G 68M 1.9G 4%
[root@nod2 ~]# drbd-overview
0:drbd/0WFConnection Primary/UnknownUpToDate/DUnknownC r----- /mntext4 2.0G 68M 1.9G 4%
######由上可见，状态为StandAlone时，主备节点是不会通信的
```
#### 7、查看DRBD的服务状态
```
[root@nod1 ~]# service drbd status
drbd driver loaded OK; device status:
version: 8.4.3 (api:1/proto:86-101)
GIT-hash: 89a294209144b68adb3ee85a73221f964d3ee515 build by gardner@, 2013-05-27 04:30:21
m:res   cs          ro               ds                 p       mounted  fstype
0:drbd  StandAlone  Primary/UnknownUpToDate/DUnknownr-----  ext4
[root@nod2 ~]# service drbd status
drbd driver loaded OK; device status:
version: 8.4.3 (api:1/proto:86-101)
GIT-hash: 89a294209144b68adb3ee85a73221f964d3ee515 build by gardner@, 2013-05-27 04:30:21
m:res   cs            ro               ds                 p  mounted  fstype
0:drbd  WFConnection  Primary/UnknownUpToDate/DUnknownC  /mntext4
```
####  8、在NOD1备用节点处理办法

```
[root@nod1 ~]# umount /mnt/
[root@nod1 ~]# drbdadm disconnect drbd
drbd: Failure: (162) Invalid configuration request
additional info from kernel:
unknown connection
Command 'drbdsetup disconnect ipv4:192.168.137.225:7789 ipv4:192.168.137.222:7789'terminated with exitcode 10
[root@nod1 ~]# drbdadm secondary drbd
[root@nod1 ~]# drbd-overview
0:drbd/0StandAlone Secondary/UnknownUpToDate/DUnknownr-----
[root@nod1 ~]# drbdadm connect --discard-my-data drbd
######执行完以上三步后，你查看会发现还是不可用
[root@nod1 ~]# drbd-overview
0:drbd/0WFConnection Secondary/UnknownUpToDate/DUnknownC r-----
```
#### 9、需要在NOD2节点上重新建立连接资源

```
[root@nod2 ~]# drbdadm connect drbd
######查看节点连接状态
[root@nod2 ~]# drbd-overview
0:drbd/0Connected Primary/SecondaryUpToDate/UpToDateC r----- /mntext4 2.0G 68M 1.9G 4%
[root@nod1 ~]# drbd-overview
0:drbd/0Connected Secondary/PrimaryUpToDate/UpToDateC r-----
######由上可见已经恢复到正常运行状态
```

## 脑裂的自动处理

## drbd优化
1. 网络环境很重要，能使用千兆网卡的就不要使用百兆网卡，当前主流机器都是千兆网卡，交换机也考虑在里面，同时DRBD的数据同步使用的网络和提供服务的网络分开，尽量独立出来，例如：在两块网卡上直接连接一个网线，用过DRBD的数据同步。
 
2. 用作DRBD的分区的磁盘性能要尽量的好，例如可以考虑使用不少于6块15K的SAS盘做RAID10或RAID0（做好有BBU），来提供IO性能。在网络环境很好情况下DRBD分区可能会因为IO的写性能而成为瓶颈。
 
3. 尽量把系统更新成最新的kernel以及使用64bit的系统，同时使用最新版本的DRBD，之前在Florian's的blog上看到kernel2.6.13以及准备把DRBD作为linux kernel的主干分支。
 
4. 注意syncer rate参数设置。这个依赖网络速度和磁盘的写入速度。官方给一个值：
千兆网络同步速度大约在125MB/S， 百兆网络同步速度大约在11MB/S，但我测试同步速度最大能到218MB/S. 这个同步速度和磁盘写入速度（hdparm -Tt /dev/drbd0测试结果)中的最小值 * 30%后的值就是应该设置的值。例如：同步速度125MB/S，磁盘写入速度110MB/S，那么这个应该设置不能超过33MB/S
原因是，DRBD同步有个不同的进程用来做i数据的传输，一个replication进程用来同步一些block的修改，这个值不依赖这个值的设置，是在Synchronization进程使用的带宽之外的带宽来传输。一个Synchronization进程用来同步处理，受限于这个值的设置，所以这值应该多考虑好，如果把设置的太大，把所有的带宽占满了，会导致replication 进程没有可用带宽使用，导致IO停止出现同步不正常。
 
 5. 注意al-extents参数设置。al-extents控制着一次同时向磁盘写入多少个4M的block.
加大这个参数的值有几个好处：
（1）.可以减少更新元数据到drbd设备频率。
（2）. 降低同步数据时对IO流的中断数量。
（3）.提高修改DRBD 设备相应速度。
但存在一个风险，当primary node出现crash时，所有活动的数据（al-extends的值 x 4M block）需要在同步连接建立后重新同步。即存primary node出现crash时，secondary node 出现outdate的情况。我不建议在HA部署上调整这个参数，在某些CASE下可以用来提高性能。
 

## 参考
[DRBD使用gfs2,cman实现双主分布式文件存储方案](http://blog.sae.sina.com.cn/archives/3609)
[drbd优化](http://blog.sina.com.cn/s/blog_499740cb0100igsq.html)
