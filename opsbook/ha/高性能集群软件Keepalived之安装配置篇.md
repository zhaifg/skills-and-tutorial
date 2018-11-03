# 高性能集群软件Keepalived之安装配置篇

---

## 一、Keepalived的安装过程
Keepalived的安装非常简单，下面通过源码编译的方式介绍下Keepalived的安装过程。首先打开Keepalived的官方网址http://www.keepalived.org，从中可以下载到各种版本的Keepalived，这里下载的是keepalived-1.2.12.tar.gz。以操作系统环境Centos6.3为例，Keepalived安装步骤如下：

```
[root@keepalived-master app]#tar zxvf keepalived-1.2.12.tar.gz
[root@keepalived-master app]#cd keepalived-1.2.12
[root@keepalived-master keepalived-1.2.12]#./configure   --sysconf=/etc \
> --with-kernel-dir=/usr/src/kernels/2.6.32-431.5.1.el6.x86_64
[root@keepalived-master keepalived-1.2.12]#make
[root@keepalived-master keepalived-1.2.12]#make install
[root@keepalived-master keepalived-1.2.12]#ln -s /usr/local/sbin/keepalived  /sbin/
[root@keepalived-master keepalived-1.2.12]# chkconfig  --add keepalived
[root@keepalived-master keepalived-1.2.12]# chkconfig  --level 35 keepalived on
```

在编译选项中，“`--sysconf`”指定了Keepalived配置文件的安装路径，
即路径为`/etc/Keepalived/Keepalived.conf`;“`--with-kernel-dir`”是个很重要的参数，但这个参数并不是要把Keepalived编译进内核，而是指定使用内核源码中的头文件，
即include目录。只有在使用LVS时，才需要用到“`--with-kernel-dir`”参数，其他时候
是不需要的。

在Keepalived输出的加载模块信息，其中：
`Use IPVS Framework`表示使用IPVS框架，也就是负载均衡模块，后面的“Yes”表示启用IPVS功能。一般在搭建高可用负载均衡集群时会启用IPVS功能，如果只是使用Keepalived的高可用功能，则不需要启用IPVS模块，可以在编译Keepalived时通过“`--disable-lvs`”关闭IPVS功能。

`IPVS sync daemon support`表示启用IPVS的同步功能，此模块一般和IPVS模块一起使用，如果需要关闭，可在编译Keepalived时通过“`--disable-lvs-syncd`”参数实现。

`IPVS use libnl`表示使用新版的libnl。libnl是NETLINK的一个实现，如果要使用新版的libnl，需要在系统中安装libnl和libnl-devel软件包。

`Use VRRP Framework`表示使用VRRP框架，这是实现Keepalived高可用功能必需的模块。

`Use VRRP VMAC`表示使用基础VMAC接口的xmit VRRP包，这是Keepalived在1.2.10版本及以后新增的一个功能。
至此，Keepalived的安装介绍完毕。下面开始进入Keepalived配置的讲解。


## 二、Keepalived的全局配置

在上节安装Keepalived的过程中，指定了Keepalived配置文件的路径为
`/etc/Keepalived/Keepalived.conf`,Keepalived的所有配置均在这个配置文件中完成。
由于Keepalived.conf文件中可配置的选项比较多，这里根据配置文件所实现的功能，将Keepalived配置分为三类，分别是：`全局配置(Global Configuration)`、`VRRPD配置`和`LVS配置`。下面将主要介绍下Keepalived配置文件中一些常用配置选项的含义和用法。

Keepalived的配置文件都是以块（block）的形式组织的，每个块的内容都包含在{}中，以“#”和“!”开头的行都是注释。全局配置就是对整个Keepalived都生效的配置，基本内容如下：

```
! Configuration File for keepalived
global_defs {
   notification_email {
     dba.gao@gmail.com
     zhaifengguo@163.com
   }
   notification_email_from Keepalived@localhost
   smtp_server 192.168.200.1
   smtp_connect_timeout 30
   router_id LVS_DEVEL 
}
```

全局配置以“`global_defs`”作为标识，在“global_defs”区域内的都是全局配置选项，
其中：

`notification_email` 用于设置报警邮件地址，可以设置多个，每行一个。注意，如果要开启邮件报警，需要开启本机的Sendmail服务。

`notification_email_from` 用于设置邮件的发送地址。
`smtp_server`用于设置邮件的smtp server地址。
`smtp_connect_timeout`用于设置连接smtp server的超时时间。

`router_id`表示运行Keepalived服务器的一个标识，是发邮件时显示在邮件主题中的信息。

## 三、Keepalived的VRRPD配置

VRRPD配置是Keepalived所有配置的核心，主要用来实现Keepalived的高可用功能。从结构上来看，VRRPD配置又可分为VRRP同步组配置和VRRP实例配置。

这里首先介绍`同步组`实现的主要功能。`同步组`是`相对于多个VRRP实例`而言的，`在多个VRRP实例`的环境中，每个VRRP实例所对应的网络环境会有所不同，假设一个实例处于网段A，另一个实例处于网段B，而如果VRRPD只配置了A网段的检测，那么当B网段主机出现故障时，VRRPD会认为自身仍处于正常状态，进而不会进行主备节点的切换，这样问题就出现了。同步组就是用来解决这个问题的，将所有VRRP实例都加入到同步组中，这样任何一个实例出现问题，都会导致Keepalived进行主备切换。

下面是两个同步组的配置样例：
```
vrrp_sync_group G1 {
  group {
    VI_1
    VI_2
    VI_5
  }
  notify_backup "/usr/local/bin/vrrp.back arg1 arg2"
  notify_master "/usr/local/bin/vrrp.mast arg1 arg2"
  notify_fault "/usr/local/bin/vrrp.fault arg1 arg2"
}

vrrp_sync_group G2 {
  group {
    VI_3
    VI_4
  }
}
```
其中，`G1同步组`包含`VI_1、VI_2、VI_5`三个VRRP实例，`G2同步组`包含`VI_3、VI_4`两个VRRP实例。这五个实例将在`vrrp_instance`段进行定义。另外，在`vrrp_sync_group`段中还出现了`notify_master`、`notify_backup`、`notify_fault`和`notify_stop`四个选项，这是Keepalived配置中的一个通知机制，也是Keepalived包含的四种状态。下面介绍每个选项的含义。

`notify_master`：指定当Keepalived进入Master状态时要执行的脚本，这个脚本可以是一个状态报警脚本，也可以是一个服务管理脚本。Keepalived允许脚本传入参数，因此灵活性很强。

`notify_backup`：指定当Keepalived进入Backup状态时要执行的脚本，同理，这个脚本可以是一个状态报警脚本，也可以是一个服务管理脚本。
notify_fault：指定当Keepalived进入Fault状态时要执行的脚本，脚本功能与前两个类似。

`notify_stop`：指定当Keepalived程序终止时需要执行的脚本。
下面正式进入VRRP实例的配置，也就是配置Keepalived的高可用功能。VRRP实例段主要用来配置节点角色（主或从）、实例绑定的网络接口、节点间验证机制、集群服务IP等。下面是实例VI_1的一个配置样例。
```
vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 51
    priority 100
    advert_int 1  
    mcast_src_ip <IPADDR>
    garp_master_delay  10 
  
 track_interface {
eth0 
eth1
}
    authentication {
        auth_type PASS
        auth_pass qwaszx
    }
    virtual_ipaddress {
     #<IPADDR>/<MASK>  brd  <IPADDR>  dev <STRING>  scope <SCOPT>  label <LABEL>
        192.168.200.16
        192.168.200.17 dev eth1
        192.168.200.18 dev eth2
    }
    virtual_routes {
#src  <IPADDR>  [to] <IPADDR>/<MASK>  via|gw  <IPADDR>  dev <STRING>  scope <SCOPE>
        src 192.168.100.1 to 192.168.109.0/24 via 192.168.200.254 dev eth1
        192.168.110.0/24 via 192.168.200.254 dev eth1
        192.168.111.0/24 dev eth2
        192.168.112.0/24 via 192.168.100.254
        192.168.113.0/24 via 192.168.100.252 or 192.168.100.253
}
nopreempt 
preemtp_delay  300
}
```

以上VRRP配置以`vrrp_instance`”作为标识，在这个实例中包含了若干配置选项，分别介绍如下：

`vrrp_instance`是VRRP实例开始的标识，后跟VRRP实例名称。

`state`用于指定Keepalived的角色，**MASTER**表示此主机是主服务器，BACKUP表示此主机是备用服务器。

`interface`  用于指定HA监测网络的接口。
`virtual_router_id` 是虚拟路由标识，这个标识是一个数字，同一个vrrp实例使用唯一的标识，即在同一个`vrrp_instance`下，`MASTER和BACKUP必须是一致的`。

`priority`用于定义节点优先级，数字越大表示节点的优先级就越高。在一个vrrp_instance下，MASTER的优先级必须大于BACKUP的优先级。

`advert_int` 用于设定MASTER与BACKUP主机之间同步检查的时间间隔，单位是秒。

`mcast_src_ip`用于设置发送多播包的地址，如果不设置，将使用绑定的网卡所对应的IP地址。

`garp_master_delay`用于设定在切换到Master状态后延时进行Gratuitous arp请求的时间。

`track_interface`用于设置一些额外的网络监控接口，其中任何一个网络接口出现故障，Keepalived都会进入FAULT状态。

`authentication`用于设定节点间通信验证类型和密码，验证类型主要有`PASS`和`AH`两种，在一个vrrp_instance下，MASTER与BACKUP必须使用相同的密码才能正常通信。

`virtual_ipaddress`用于设置虚拟IP地址（VIP），又叫做漂移IP地址。可以设置多个虚拟IP地址，每行一个。之所以称为漂移IP地址，是因为Keepalived切换到Master状态时，这IP地址会自动添加到系统中，而切换到BACKUP状态时，这些IP又会自动从系统中删除。
Keepalived通过“`ip address add`”命令的形式将VIP添加进系统中。要查看系统中添加
的VIP地址，可以通过“`ip add`”命令实现。“virtual_ipaddress”段中添加的IP形式可以
多种多样，例如可以写成 “`192.168.16.189/24 dev eth1`” 这样的形式，而Keepalived
会使用IP命令“`ip addr add 192.168.16.189/24 dev eth1`”将IP信息添加到系统中。
因此，这里的配置规则和IP命令的使用规则是一致的。

`virtual_routes`和`virtual_ipaddress`段一样，用来设置在切换时添加或删除相关路由信息。使用方法和例子可以参考上面的示例。通过`ip route`命令可以查看路由信息是否
添加成功，此外，也可以通过上面介绍的`notify_master`选项来代替`virtual_routes`实现相同的功能。

`nopreempt`设置的是高可用集群中的不抢占功能。在一个HA Cluster中，如果主节点死机了，备用节点会进行接管，主节点再次正常启动后一般会自动接管服务。这种来回切换的操作，对于实时性和稳定性要求不高的业务系统来说，还是可以接受的，而对于稳定性和实时性要求很高的业务系统来说，不建议来回切换，毕竟服务的切换存在一定的风险和不稳定性，在这种情况下，就需要设置nopreempt这个选项了。设置nopreempt可以实现主节点故障恢复后不再切回到主节点，让服务一直在备用节点工作，直到备用节点出现故障才会进行切换。在使用不抢占时，只能在`state`状态为`BACKUP`的节点上设置，而且这个节点的优先级必须高于其他节点。

`preemtp_delay`用于设置抢占的延时时间，单位是秒。有时候系统启动或重启之后网络需要经过一段时间才能正常工作，在这种情况下进行发生主备切换是没必要的，此选项就是用来设置这种情况发生的时间间隔。在此时间内发生的故障将不会进行切换，而如果超过`preemtp_delay`指定的时间，并且网络状态异常，那么才开始进行主备切换。

## 四、Keepalived的LVS配置
由于Keepalived属于LVS的扩展项目，因此， Keepalived可以与LVS无缝整合，轻松搭建一套高性能的负载均衡集群系统。下面介绍下Keepalived配置文件中关于LVS配置段的配置方法。
LVS段的配置以`virtual_server`作为开始标识，此段内容有两部分组成，分别是`real_server`段和`健康检测段`。下面是virtual_server段常用选项的一个配置示例：
```
virtual_server 192.168.12.200 80 {        
    delay_loop 6
lb_algo rr
lb_kind DR 
persistence_timeout 50
    persistence_granularity  <NETMASK>
protocol TCP
ha_suspend
virtualhost  <string>
sorry_server <IPADDR>  <PORT>
```

下面介绍每个选项的含义。
`virtual_server`：
设置虚拟服务器的开始，后面跟虚拟IP地址和服务端口，IP与端口之间用空格隔开。

`delay_loop`：设置健康检查的时间间隔，单位是秒。

`lb_algo`：设置负载调度算法，可用的调度算法有rr、wrr、lc、wlc、lblc、sh、dh等，常用的算法有rr和wlc。

`lb_kind`：设置LVS实现负载均衡的机制，有NAT、TUN和DR三个模式可选。

`persistence_timeout`：会话保持时间，单位是秒。这个选项对动态网页是非常有用的，为集群系统中的session共享提供了一个很好的解决方案。有了这个会话保持功能，用户的请求会一直分发到某个服务节点，直到超过这个会话的保持时间。需要注意的是，这个会话保持时间是最大无响应超时时间，也就是说，用户在操作动态页面时，如果在50秒内没有执行任何操作，那么接下来的操作会被分发到另外的节点，但是如果用户一直在操作动态页面，则不受50秒的时间限制。

`persistence_granularity`：此选项是配合persistence_timeout的，后面跟的值是子网掩码，表示持久连接的粒度。默认是255.255.255.255，也就是一个单独的客户端IP。如果将掩码修改为255.255.255.0，那么客户端IP所在的整个网段的请求都会分配到同一个real server上。

`protocol`：指定转发协议类型，有TCP和UDP两种可选。

`ha_suspend`：
节点状态从Master到Backup切换时，暂不启用real server节点的健康检查。

`virtualhost`：
在通过HTTP_GET/ SSL_GET做健康检测时，指定的Web服务器的虚拟主机地址。

`sorry_server`：相当于一个备用节点，在所有real server失效后，这个备用节点会启用。

下面是real_server段的一个配置示例：
```
real_server 192.168.12.132 80 {
weight 3
inhibit_on_failure
notify_up  <STRING> | <QUOTED-STRING>
notify_down <STRING> | <QUOTED-STRING>
}
```
下面介绍每个选项的含义。
`real_server`：是real_server段开始的标识，用来指定real server节点，后面跟的是real server的真实IP地址和端口，IP与端口之间用空格隔开。
`weight`：用来配置real server节点的权值。权值大小用数字表示，数字越大，权值越高。设置权值的大小可以为不同性能的服务器分配不同的负载，为性能高的服务器设置较高的权值，而为性能较低的服务器设置相对较低的权值，这样才能合理地利用和分配了系统资源。
`inhibit_on_failure`：
表示在检测到real server节点失效后，把它的“weight”值设为0，而不是从IPVS中删除。

`notify_up`：
此选项与上面介绍过的notify_maser有相同的功能，后跟一个脚本，表示在检测到real server节点服务处于UP状态后执行的脚本。

`notify_down`：表示在检测到real server节点服务处于DOWN状态后执行的脚本。
健康检测段允许多种检查方式，常见的有HTTP_GET、SSL_GET、TCP_CHECK、SMTP_CHECK、MISC_CHECK。首先看TCP_CHECK检测方式示例：
```
TCP_CHECK  {
connect_port 80
            connect_timeout  3 
            nb_get_retry  3 
            delay_before_retry  3 
        }
```
下面介绍每个选项的含义介。
`connect_port`：健康检查的端口，如果无指定，默认是real_server指定的端口。
`connect_timeout`：表示无响应超时时间，单位是秒，这里是3秒超时。
`nb_get_retry`：表示重试次数，这里是3次。
`delay_before_retry`：表示重试间隔，这里是间隔3秒。

### 下面是HTTP_GET和SSL_GET检测方式的示例：
```
HTTP_GET |SSL_GET
{
url  {         
path  /index.html
digest  e6c271eb5f017f280cf97ec2f51b02d3
status_code   200 
}
connect_port 80
bindto  192.168.12.80
connect_timeout  3
nb_get_retry  3 
delay_before_retry  2 
}
```
下面介绍每个选项的含义。
`url`：用来指定HTTP/SSL检查的URL信息，可以指定多个URL。
`path`：后跟详细的URL路径。
`digest`：
SSL检查后的摘要信息，这些摘要信息可以通过genhash命令工具获取。例如：genhash -s 192.168.12.80 -p 80 -u /index.html。

`status_code`：指定HTTP检查返回正常状态码的类型，一般是200。
`bindto`：表示通过此地址来发送请求对服务器进行健康检查。

###下面是MISC_CHECK检测方式的示例：
```
MISC_CHECK
{
  misc_path  /usr/local/bin/script.sh
  misc_timeout  5
  ! misc_dynamic
}
```
MISC健康检查方式可以通过执行一个外部程序来判断real server节点的服务状态，使用非常灵活。以下是常用的几个选项的含义。
`misc_path`：用来指定一个外部程序或者一个脚本路径。
`misc_timeout`：设定执行脚本的超时时间。
`misc_dynamic`：表示是否启用动态调整real server节点权重，“!misc_dynamic”表示不启用，相反则表示启用。在启用这功能后，Keepalived的healthchecker进程将通过退出状态码来动态调整real server节点的“weight”值，如果返回状态码为0，表示健康检查正常，real server节点权重保持不变；如果返回状态码为1，表示健康检查失败，那么就将real server节点权重设置为0；如果返回状态码为2~255之间任意数值，表示健康检查正常，但real server节点的权重将被设置为返回状态码减2，例如返回状态码为10，real server节点权重将被设置为8（10-2）。
到这里为止，Keepalived配置文件中常用的选项已经介绍完毕，在默认情况下，Keepalived在启动时会查找/etc/Keepalived/Keepalived.conf配置文件，如果配置文件放在其他路径下，通过“Keepalived  -f”参数指定配置文件的路径即可。
在配置Keepalived.conf时，需要特别注意配置文件的语法格式，因为Keepalived在启动时并不检测配置文件的正确性，即使没有配置文件，Keepalived也照样能够启动，所以一定要保证配置文件正确。


## 如何重定向Keepalived日志的输出路径


Keepalived默认所有的日志都是写入到`/var/log/message`下的，由于message的日志太多了，而Keepalived的日志又很难分离出来，所以本文提供了一个调整Keepalived日志输出路径的方法。
具体操作步骤如下：
## 一、修改 /etc/sysconfig/keepalived
把`KEEPALIVED_OPTIONS="-D"` 修改为`KEEPALIVED_OPTIONS="-D -d -S 0"`
> #其中-S指定syslog的facility

##二、重启服务
`service keepalived restart`

## 三、设置syslog，修改/etc/syslog.conf，添加内容如下
```
# keepalived -S 0 
local0.*                    /var/log/keepalived.log
```
注意：local0是l是字符L的小写


##四、Keepalived相关管理的知识拓展
```
/usr/local/keepalived/sbin/keepalived --vrrp                    -P    Only run with VRRP subsystem. 
/usr/local/keepalived/sbin/keepalived --check                  -C    Only run with Health-checker subsystem. 
/usr/local/keepalived/sbin/keepalived --dont-release-vrrp  -V    Dont remove VRRP VIPs & VROUTEs on daemon stop. 
/usr/local/keepalived/sbin/keepalived --dont-release-ipvs  -I    Dont remove IPVS topology on daemon stop. 
/usr/local/keepalived/sbin/keepalived --dont-fork        -n    Dont fork the daemon process. 
/usr/local/keepalived/sbin/keepalived --use-file           -f   Use the specified configuration file. Default is /etc/keepalived/keepalived.conf. 
/usr/local/keepalived/sbin/keepalived --dump-conf      -d    Dump the configuration data. 
/usr/local/keepalived/sbin/keepalived --log-console      -l    Log message to local console. 
/usr/local/keepalived/sbin/keepalived --log-detail         -D    Detailed log messages. 
/usr/local/keepalived/sbin/keepalived --log-facility        -S    0-7 Set syslog facility to LOG_LOCAL[0-7]. (default=LOG_DAEMON) 
/usr/local/keepalived/sbin/keepalived --help                 -h    Display this short inlined help screen. 
/usr/local/keepalived/sbin/keepalived --version             -v    Display the version number 
/usr/local/keepalived/sbin/keepalived --pid                   -p    pidfile 
/usr/local/keepalived/sbin/keepalived --checkers_pid     -c    checkers pidfile 
/usr/local/keepalived/sbin/keepalived --vrrp_pid            -r    vrrp pidfile
```

以上完，如有问题欢迎随时交流~~

http://blog.chinaunix.net/uid-25723371-id-4997741.html

