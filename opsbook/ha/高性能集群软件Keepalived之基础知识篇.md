# 高性能集群软件Keepalived之基础知识篇

标签（空格分隔）：HA Keepalived

---

## 一、Keepalived介绍
Keepalived是Linux下一个轻量级的高可用解决方案，它与HeartBeat、RoseHA实现的功能类似，都可以实现服务或者网络的高可用，但是又有差别：HeartBeat是一个专业的、功能完善的高可用软件，它提供了HA软件所需的基本功能，比如心跳检测和资源接管，监测集群中的系统服务，在群集节点间转移共享IP地址的所有者等，HeartBeat功能强大，但是部署和使用相对比较麻烦；与HeartBeat相比，Keepalived主要是通过虚拟路由冗余来实现高可用功能，虽然它没有HeartBeat功能强大，但Keepalived部署和使用非常简单，所有配置只需一个配置文件即可完成。这也是本章重点介绍Keepalived的原因。

## 二、Keepalived是什么
Keepalived起初是为LVS设计的，专门用来监控集群系统中各个服务节点的状态。它根据layer3, 4 & 5交换机制检测每个服务节点的状态，如果某个服务节点出现异常，或工作出现故障，Keepalived将检测到，并将出现故障的服务节点从集群系统中剔除，而在故障节点恢复正常后，Keepalived又可以自动将此服务节点重新加入到服务器集群中，这些工作全部自动完成，不需要人工干涉，需要人工完成的只是修复出现故障的服务节点。
Keepalived后来又加入了VRRP的功能，VRRP是Virtual Router Redundancy Protocol（虚拟路由器冗余协议）的缩写，它出现的目的是为了解决静态路由出现的单点故障问题，通过VRRP可以实现网络不间断地、稳定地运行。因此，Keepalived一方面具有服务器状态检测和故障隔离功能，另一方面也具有HA cluster功能.下面详细介绍下VRRP协议的实现过程。

##三、 VRRP协议与工作原理
在现实的网络环境中，主机之间的通信都是通过配置静态路由（默认网关）完成的，而主机之间的路由器一旦出现故障，通信就会失败，因此，在这种通信模式中，路由器就成了一个单点瓶颈，为了解决这个问题，就引入了VRRP协议。

熟悉网络的读者对VRRP协议应该并不陌生。它是一种主备模式的协议，通过VRRP可以在网络发生故障时透明地进行设备切换而不影响主机间的数据通信，这其中涉及两个概念：物理路由器和虚拟路由器。

VRRP可以将两台或多台物理路由器设备虚拟成一个虚拟路由器，这个虚拟路由器通过虚拟IP（一个或多个）对外提供服务，而在虚拟路由器内部，是多个物理路由器协同工作，同一时间只有一台物理路由器对外提供服务，这台物理路由器被称为主路由器（处于MASTER角色）。一般情况下MASTER由选举算法产生，它拥有对外服务的虚拟IP，提供各种网络功能，如ARP请求、ICMP、数据转发等。而其他物理路由器不拥有对外的虚拟IP，也不提供对外网络功能，仅仅接收MASTER的VRRP状态通告信息，这些路由器被统称为备份路由器（处于BACKUP角色）。当主路由器失效时，处于BACKUP角色的备份路由器将重新进行选举，产生一个新的主路由器进入MASTER角色继续提供对外服务，整个切换过程对用户来说完全透明。
    
每个虚拟路由器都有一个唯一标识，称为VRID，一个VRID与一组IP地址构成了一个虚拟路由器。在VRRP协议中，所有的报文都是通过IP多播形式发送的，而在一个虚拟路由器中，只有处于MASTER角色的路由器会一直发送VRRP数据包，处于BACKUP角色的路由器只接收MASTER发过来的报文信息，用来监控MASTER运行状态，因此，不会发生BACKUP抢占的现象，除非它的优先级更高。而当MASTER不可用时，BACKUP也就无法收到MASTER发过来的报文信息，于是就认定MASTER出现故障，接着多台BACKUP就会进行选举，优先级最高的BACKUP将成为新的MASTER，这种选举并进行角色切换的过程非常快，因而也就保证了服务的持续可用性。
    
## 四、Keepalived工作原理
上节简单介绍了Keepalived通过VRRP实现高可用功能的工作原理，而Keepalived作为一个高性能集群软件，它还能实现对集群中服务器运行状态的监控及故障隔离。下面继续介绍下Keepalived对服务器运行状态监控和检测的工作原理。

Keepalived工作在TCP/IP参考模型的第三、第四和第五层，也就是网络层、传输层和应用层。根据TCP/IP参考模型各层所能实现的功能，Keepalived运行机制如下
。
在网络层，运行着四个重要的协议：互连网协议IP、互连网控制报文协议ICMP、地址转换协议ARP以及反向地址转换协议RARP。Keepalived在网络层采用的最常见的工作方式是通过ICMP协议向服务器集群中的每个节点发送一个ICMP的数据包（类似于ping实现的功能），如果某个节点没有返回响应数据包，那么就认为此节点发生了故障，Keepalived将报告此节点失效，并从服务器集群中剔除故障节点。

在传输层，提供了两个主要的协议：传输控制协议TCP和用户数据协议UDP。传输控制协议TCP可以提供可靠的数据传输服务，IP地址和端口，代表一个TCP连接的一个连接端。要获得TCP服务,须在发送机的一个端口上和接收机的一个端口上建立连接，而Keepalived在传输层就是利用TCP协议的端口连接和扫描技术来判断集群节点是否正常的。比如，对于常见的Web服务默认的80端口、SSH服务默认的22端口等，Keepalived一旦在传输层探测到这些端口没有响应数据返回，就认为这些端口发生异常，然后强制将此端口对应的节点从服务器集群组中移除。

在应用层，可以运行FTP、TELNET、SMTP、DNS等各种不同类型的高层协议，Keepalived的运行方式也更加全面化和复杂化，用户可以通过自定义Keepalived的工作方式，例如用户可以通过编写程序来运行Keepalived，而Keepalived将根据用户的设定检测各种程序或服务是否允许正常，如果Keepalived的检测结果与用户设定不一致时，Keepalived将把对应的服务从服务器中移除。

## 五、Keepalived的体系结构
Keepalived是一个高度模块化的软件，结构简单，但扩展性很强，如有兴趣的读者，可以阅读下Keepalived的源码。下图是官方给出的Keepalived体系结构拓扑图。

![keepalived的架构图][1]

 从图中可以看出，Keepalived的体系结构从整体上分为两层，分别是用户空间层（User Space）和内核空间层（Kernel Space）.下面介绍Keepalived两层结构的详细组成及实现的功能。
   
内核空间层处于最底层，它包括IPVS和NETLINK两个模块。IPVS模块是Keepalived引入的一个第三方模块，通过IPVS可以实现基于IP的负载均衡集群。IPVS默认包含在LVS集群软件中。而对于LVS集群软件，相信做运维的朋友并不陌生：在LVS集群中，IPVS安装在一个叫做Director Server的服务器上，同时在Director Server上虚拟出一个IP地址来对外提供服务，而用户必须通过这个虚拟IP地址才能访问服务。这个虚拟IP一般称为LVS的VIP，即Virtual IP。访问的请求首先经过VIP到达Director Server，然后由Director Server从服务器集群节点中选取一个服务节点响应用户的请求。
    
Keepalived最初就是为LVS提供服务的，由于Keepalived可以实现对集群节点的状态检测，而IPVS可以实现负载均衡功能，因此，Keepalived借助于第三方模块IPVS就可以很方便地搭建一套负载均衡系统。在这里有个误区，由于Keepalived可以和IPVS一起很好地工作，因此很多初学者都以为Keepalived就是一个负载均衡软件，这种理解是错误的。
    
在Keepalived中，IPVS模块是可配置的，如果需要负载均衡功能，可以在编译Keepalived时打开负载均衡功能，反正，也可以通过配置编译参数关闭。
NETLINK模块主要用于实现一些高级路由框架和一些相关的网络功能，完成用户空间层Netlink Reflector模块发来的各种网络请求。
    
用户空间层位于内核空间层之上，Keepalived的所有具体功能都在这里实现，下面介绍、几个重要部分所实现的功能。

在用户空间层，Keepalived又分为四个部分，分别是Scheduler I/O Multiplexer、Memory Management、Control Plane和Core components。其中，Scheduler I/O Multiplexer是一个I/O复用分发调度器，它负责安排Keepalived所有内部的任务请求。Memory Management是一个内存管理机制，这个框架提供了访问内存的一些通用方法。Control Plane是Keepalived的控制面板，可以实现对配置文件进行编译和解析，Keepalived的配置文件解析比较特殊，它并不是一次解析所有模块的配置，而是只有在用到某模块时才解析相应的配置。最后详细说一下Core components，这个部分是Keepalived的核心组件，包含了一些列功能模块，主要有WatchDog、Checkers、VRRP Stack、IPVS wrapper和Netlink Reflector，下面介绍每个模块所实现的功能如下。

**（1）WatchDog**
WatchDog是计算机可靠性领域中一个极为简单又非常有效的检测工具，它的工作原理是针对被监视的目标设置一个计数器和一个阈值，WatchDog会自己增加此计数值，然后等待被监视的目标周期性地重置该计数值。一旦被监控目标发生错误，就无法重置此计数值，WatchDog就会检测到，于是就采取对应的恢复措施，例如重启或关闭。
在Linux中很早就引入了WatchDog功能，而Keepalived正是通过WatchDog的运行机制来监控Checkers和VRRP进程的。

**（2）Checkers**
这是Keepalived最基础的功能，也是最主要的功能，可实现对服务器运行状态检测和故障隔离。

**（3）VRRP Stack**
这是Keepalived后来引入的VRRP功能，可以实现HA集群中失败切换（Failover）功能。Keepalived通过VRRP功能再结合LVS负载均衡软件即可部署一套高性能的负载均衡集群系统。

**（4）IPVS wrapper**
这是IPVS功能的一个实现。IPVS wrapper模块可以将设置好的IPVS规则发送到内核空间并提交给IPVS模块，最终实现IPVS模块的负载均衡功能。

**（5）Netlink Reflector**
用来实现高可用集群中Failover时虚拟IP（VIP）的设置和切换。Netlink Reflector的所有请求最后都发送到内核空间的NETLINK模块来完成。




  [1]: http://7xkabv.com1.z0.glb.clouddn.com/la_keepalived.png