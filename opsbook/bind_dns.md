# dns
---
## DNS

###  客户端的设置
1.相关的配置文件

2. 查询命令
  host
  nslookup
  dig
  whois

## bind的安装
yum
```
yum install -y bind bind-utils  


 rpm -ql bind
/etc/NetworkManager/dispatcher.d/13-named
/etc/logrotate.d/named
/etc/named    
/etc/named.conf    #bind主配置文件
/etc/named.iscdlv.key
/etc/named.rfc1912.zones    #定义zone的文件
/etc/named.root.key
/etc/portreserve/named
/etc/rc.d/init.d/named    #bind脚本文件
/etc/rndc.conf    #rndc配置文件
/etc/rndc.key
/etc/sysconfig/named
/usr/lib64/bind
/usr/sbin/arpaname
/usr/sbin/ddns-confgen
/usr/sbin/dnssec-dsfromkey
/usr/sbin/dnssec-keyfromlabel
/usr/sbin/dnssec-keygen
/usr/sbin/dnssec-revoke
/usr/sbin/dnssec-settime
/usr/sbin/dnssec-signzone
/usr/sbin/genrandom
/usr/sbin/isc-hmac-fixup
/usr/sbin/lwresd
/usr/sbin/named
/usr/sbin/named-checkconf    #检测/etc/named.conf文件语法
/usr/sbin/named-checkzone    #检测zone和对应zone文件的语法
/usr/sbin/named-compilezone
/usr/sbin/named-journalprint
/usr/sbin/nsec3hash
/usr/sbin/rndc    #远程dns管理工具
/usr/sbin/rndc-confgen    #生成rndc密钥
 
#过长省略
 
/var/log/named.log
/var/named
/var/named/data
/var/named/dynamic
/var/named/named.ca    #根解析库
/var/named/named.empty
/var/named/named.localhost    #本地主机解析库
/var/named/named.loopback    
/var/named/slaves    #从文件夹
/var/run/named

[root@localhost ~]# rpm -ql bind-utils    #bind-utils包主要提供了一些检测工具
/usr/bin/dig    
/usr/bin/host    
/usr/bin/nslookup   
/usr/bin/nsupdate
/usr/share/man/man1/dig.1.gz
/usr/share/man/man1/host.1.gz
/usr/share/man/man1/nslookup.1.gz
/usr/share/man/man1/nsupdate.1.gz
```
源码
```
yum groupinstall "Development Tools" "Server Platform Development" --nogpgcheck

tar xf bind-9.9.5.tar.gz #解压源码包
 
cd bind-9.9.5
 
./configure --prefix=/usr/local/bind9 --sysconfdir=/etc/named/ --disable-ipv6 --disable-chroot --enable-threads    #配置config文件
 
useradd -u 53 named -r ; groupadd -g 53 named -r     #创建named用户和组
 
make && make install     #编译和配置
 
export PATH=/usr/local/bin9/bin:/usr/local/bin9/sbin:$PATH    #将bind的执行路径加入PATH中
source /etc/bashrc    #重读bash配置文件
 
echo "/usr/local/bind9/lib" > /etc/ld.so.conf.d/bind.conf    #导入库文件路径
 
echo "MANPATH /usr/local/bind9/share/man" >> /etc/man.config    #导入manual文件路径
 
 
新建主配置文件
 
vim /etc/named/named.conf
options {
  directory "/var/named";
   
  };    
zone "." IN {
  type hint;
  file "named.ca";
};
 
zone "localhost" IN {
    type master;
    file "localhost.zone";
    };
 
zone "0.0.127.in-addr.arpa {
    type master;
    file "name.local";
    };
 
 
[root@localhost bind9]# /usr/local/bind9/sbin/named-checkconf     #检查配置文件，提示没有文件夹
/etc/named/named.conf:2: change directory to '/var/named' failed: file not fou
nd
/etc/named/named.conf:2: parsing failed
[root@localhost bind9]# mkdir /var/named    #创建/var/named
[root@localhost bind9]# /usr/local/bind9/sbin/named-checkconf    #检测通过
 
 
手动创建zone文件
[root@localhost bind9]# cd /var/named/
 
[root@localhost named]# dig -t NS . @192.168.1.1    #通过dig命令获取根服务器地址
 
; <<>> DiG 9.8.2rc1-RedHat-9.8.2-0.37.rc1.el6 <<>> -t NS . @192.168.1.1
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 43106
;; flags: qr rd ra; QUERY: 1, ANSWER: 13, AUTHORITY: 0, ADDITIONAL: 0
 
;; QUESTION SECTION:
;.              IN  NS
 
;; ANSWER SECTION:
.           12787   IN  NS  m.root-servers.net.
.           12787   IN  NS  d.root-servers.net.
.           12787   IN  NS  i.root-servers.net.
.           12787   IN  NS  k.root-servers.net.
.           12787   IN  NS  a.root-servers.net.
.           12787   IN  NS  e.root-servers.net.
.           12787   IN  NS  c.root-servers.net.
.           12787   IN  NS  b.root-servers.net.
.           12787   IN  NS  h.root-servers.net.
.           12787   IN  NS  g.root-servers.net.
.           12787   IN  NS  f.root-servers.net.
.           12787   IN  NS  l.root-servers.net.
.           12787   IN  NS  j.root-servers.net.
 
;; Query time: 78 msec
;; SERVER: 192.168.1.1#53(192.168.1.1)
;; WHEN: Mon Mar 21 19:29:53 2016
;; MSG SIZE  rcvd: 228
 
[root@localhost named]# dig -t NS . @192.168.1.1 > named.ca    #将根服务器解析库重定向到named.ca文件中
 
 
创建localhost.zone文件
 
[root@localhost named]# vim localhost.zone
$TTL 600
@       IN      SOA     localhost. admin.localhost. (
        20160321
        1H
        5M
        7D
        1H
)
 
                IN      NS      localhost.
localhost.      IN      A       127.0.0.1
 
创建named.local文件
$TTL 600
@       IN      SOA     localhost. admin.localhost. (
        20160321
        1H
        5M
        7D
        1H
)
 
                IN      NS      localhost.
1               IN      PTR     localhost.
 
 
修改属主和权限
 
[root@localhost named]# chown root:named /var/named/ -R 
[root@localhost named]# chmod 770 /var/named/ -R
[root@localhost named]# chown root:named /etc/named/ -R
 
 
运行bind程序
[root@localhost bind9]# /usr/local/bind9/sbin/named -u named
 
查看监听端口
[root@localhost ~]# ss -unlp | grep 53
UNCONN     0      0           192.168.192.152:53                       *:*      users:(("named",
6949,513))UNCONN     0      0                 127.0.0.1:53                       *:*      users:(("named",
6949,512)

```

## 配置文件
named.conf
`acl`  定义访问控制列表
`controls`    定义rndc命令使用的控制通道，若省略，则只允许经过rndc.key认证的127.0.0.1的rndc控制
`include` 包含其他文件到配置文件
`key` 定义用于TSIG的授权密钥
`logging` 日志记录
`lwres`   将named同时配置成一个轻量级的解析器
`options` 定义全局选项
`trusted-keys`    为服务器定义 DNSSEC 加密密钥
`server`  设置每个服务器的特有选项
`view`    定义域名空间的一个视图
`zone`    定义一个区声明

可以使用三种注释风格：
```
/* C语言风格 */
// C++ 风格
# shell 风格
```

```
options {
        listen-on port 53 { 127.0.0.1; };
        listen-on-v6 port 53 { ::1; };
        directory       "/var/named";
        dump-file       "/var/named/data/cache_dump.db";
        statistics-file "/var/named/data/named_stats.txt";
        memstatistics-file "/var/named/data/named_mem_stats.txt";
        allow-query     { localhost; };
        recursion yes;
};

```

**options 中一般选项的含义**:
`directory` “路径”
定义服务器区数据库文件的工作目录，配置文件中使用的所有相对路径都是一个这个目录为基目录。
`notify` yes/no
如 named 是主服务器，当区数据库变化时将自动通知相应区的从服务器，默认为yes。
`recursion` yes/no
是否使用递归式 DNS 服务器，默认为yes。
`transfer-format one-answer/many-anser`
设置从主服务器向从服务器复制数据的方式，使用在主域名服务器上，是否允许在一条消息中放入多条应答信息，默认值为 many-answer
`forwarders {IPaddrs}`
设置全局转发器，列出要用作转发器的服务器 IP 地址
`forward only/first`
若值为 only，则服务器缓存数据并查询转发器，但从不查询其他的任何服务器，若转发器不能响应查询则查询失败；若值为 first，则在转发查询失败或没有查到结果时，会在本地发起正常查询。默认为 first
zone
root@jianlee:~/lab/koji/koji# sed -n -e '20,23p' /etc/bind/named.conf
zone "localhost" {
        type master;
        file "/etc/bind/db.local";
};
`type master/slave/hint/forward`
说明一个区的类型。master指示此区为主域名服务器;slave指示此区为辅助域名服务器;hint指示此区为根服务器的线索;forward指示此区为转发区。
`file “文件名”`
指出此区的域信息数据库文件名
`DNS 数据库`
一个域的 DNS 数据库是由这个域的主域名服务器的管理员所维护的文本文件的集合。这些文件经常被称为区文件，区文件定义了一个区的域名信息。每个区文件都是由若干个资源记录（RR，resource records）和分析器指令所组成。
资源记录
标志资源记录格式 ：
`[name]  [ttl]  [class]  type  data`
各个字段之间由空格或制表符分割，字段可以包含下面特殊字符：

```
;   注释
@   表示当前域
()  允许数据夸行，通常用于 SOA 记录
*   仅用于 name 字符的通配符
```

`name`
`name` 字段说明资源记录引用的对象名，可以是一台单独的主机也可以是个域名。
对象名可以是相对域名或全域名，全域名应该以“.”结束
若几条连续的 RR 记录涉及同一个对象名，则第一条 RR 记录后的 RR 记录可以省略对象名
若出现字段名字段，则必须出现在第一个字段
关于相对域名和全域名:
举例来说，在 ubuntu.org.cn 域中，相对域名 osmond 与全域名 osmond.ubuntu.org.cn. 等效；而 osmond.ubuntu.org.cn 由于没有以“.”结尾，被认为是一个相对域名，与其等效的全域名为 osmond.ubuntu.org.cn.ubuntu.org.cn.。因此在书写对象名时要特别小心。
ttl (time to live)
它以秒为单位定义该资源记录中的信息存放在高速缓存中的时间长度。通常省略该字段，而使用位于文件开始处的 $TTL 语句所指定值。

`class`
class 字段用于指定网络类型，可选的值有：IN、CH 和 HS，其中 IN （Internet）是广泛使用的一种。虽然 IN 是该字段的默认值，但通常我们会显示地指出。

`type`
type 字段用于说明 RR 的类型。常用的 RR 类型如下：
**区记录**
`SOA (Start Of Authority)`    SOA 记录标示一个授权区定义的开始。SOA 记录后的所有信息是控制这个区的
`NS (Name Server)`    标识区的域名服务器以及授权子域
2 基本记录
`A (Address)` 用于将主机名转换为 IP 地址，任何一个主机都只能有一个 A记录
`PTR (PoinTeR)`   将地址转换为主机名
`MX (Mail eXchanger)` 邮件交换记录。控制邮件的路由
3 安全记录
`KEY (Public Key)`    储存一个关于DNS 名称的公钥
`NXT (Next)`  与 DNSSEC 一起使用，用于指出一个特定名称不在域中
`SIG (Signatrue)` 指出带签名和身份认证的区信息，细节见 RFC 2535
4 可选记录
`CNAME (Canonical NAME)`  给定主机的别名，主机的规范名在A记录中给出
`SRV (Services)`  指出知名网络服务的信息
`TXT (Text)`  注释或非关键的信息

RR的顺序：
SOA RR 应该放在最前面
通常 NS RR 紧跟在 SOA RR 之后
其他记录的顺序无关紧要

`data`
取决于RR的类型


常用的资源记录
SOA 开始一个区
基本格式：
```
zone      IN      SOA   Hostname  Contact (
                        SerialNumber
                        Refresh
                        Retry
                        Expire
                        Minimum )
```
`Hostname`
存放本 Zone 的域名服务器的主机名

`Contact`
管理域的管理员的邮件地址

`SerialNumber`
本区配置数据的序列号，用于从服务器判断何时获取最新的区数据

`Refresh`
辅助域名服务器多长时间更新数据库

`Retry`
若辅助域名服务器更新数据失败，多长时间再试

`Expire`
若辅助域名服务器无法从主服务器上更新数据，原有的数据何时失效

`Minimum`
设置被缓存的否定回答的存活时间
```
jamond.net.   IN  SOA  ubuntu.jamond.net.  root.ubuntu.jamond.net. (
                        2006063000       ;序列号
                        3H               ;3小时后刷新
                        15M              ;15分钟后重试
                        1W               ;1星期后过期
                        1D )             ;否定缓存TTL为1天
```
对 Contact 来说，因为“@”在文件中有特殊含义，所以邮件地址 `root@ubuntu.jamond.net` 写为 root.ubuntu.jamond.net.
对 SerialNumber 来说，它可以是 32 位的任何整数，每当更新区文件时都应该增加此序列号的值，否则 named 将不会把区的更新数据传送到从服务器
缓存时间字段 Refresh、Retry、Expire、Minimum 可以使用时间单位字符 m、 h、d、w 分别表示分钟、小时、天、星期。
各个缓存时间字段的经验值为
Refresh — 1 到 6 小时
Retry — 20 到 60 分钟
Expire — 1 周 到 1 月
Minimum — 1 到 3 小时
Minimum 设置被缓存的否定回答的存活时间，而肯定回答（即真实记录）的默认值是在区文件开始处用 $TTL 语句设置的。

NS 标识一个区的权威服务器
包括主服务器和从服务器，并将子域授权赋予其他服务器，格式：
zone  [ttl]  IN  NS  hostname
**示例：**
```
jamond.net.  IN  NS  ubuntu.jamond.net.  ;指定 jamond.net. 的主服务器
jamond.net.  IN  NS  dapper.jamond.net.  ;指定 jamond.net. 的从服务器
osmond.jamond.net. IN  NS  ubuntu.osmond.jamond.net. ;指定委派域 osmond.jamond.net. 的主服务器
osmond.jamond.net. IN  NS  dapper.osmond.jamond.net. ;指定委派域 osmond.jamond.net. 的从服务器
```
若上面的记录紧跟在 SOA 记录后，也可以写成如下的形式：
```
IN  NS  ubuntu.jamond.net.  ;指定 jamond.net. 的主服务器
          IN  NS  dapper.jamond.net.  ;指定 jamond.net. 的从服务器
osmond    IN  NS  ubuntu.osmond.jamond.net. ;指定委派域 osmond.jamond.net. 的主服务器
osmond    IN  NS  dapper.osmond.jamond.net. ;指定委派域 osmond.jamond.net. 的从服务器
A — DNS数据库的核心
```
提供主机名到IP地址的映射，格式为：
hostname [ttl] IN A  IPAddress
举例：
ubuntu          IN    A      192.168.0.251
dapper          IN    A      192.168.0.252
ubuntu.osmond   IN    A      192.168.1.251
dapper.osmond   IN    A      192.168.1.252

PTR
PTR RR 提供了 IP 地址到主机名的映射。其格式为：
`IPAddress  [ttl]  IN  PTR  hostname`
例如： 在 168.192.in-addr.arpa 区中，前面的 ubuntu.jamond.net. 和 dapper.jamond.net. 所对应的 PTR 记录为
251.0          IN    PTR      ubuntu.jamond.net.
252.0          IN    PTR      dapper.jamond.net.

而在 0.168.192.in-addr.arpa 区中，前面的 ubuntu.jamond.net. 和 dapper.jamond.net. 所对应的 PTR 记录为
251          IN    PTR      ubuntu.jamond.net.
252          IN    PTR      dapper.jamond.net.

在 1.168.192.in-addr.arpa 区中，前面的 ubuntu.osmond.jamond.net. 和 dapper.osmond.jamond.net. 所对应的 PTR 记录为
251          IN    PTR      ubuntu.osmond.jamond.net.
252          IN    PTR      dapper.osmond.jamond.net.

在 PTR RR 中 hostname 应该使用全域名。例如 osmond.jamond.net 域的主机 ubuntu 应该写为 ubuntu.osmond.jamond.net. 。而 ubuntu.osmond.jamond.net 将被解析为 ubuntu.osmond.jamond.net.1.168.192.in-addr.arpa. 。
PTR RR 所提供的反向解析能够为任何对进入网络的请求进行认证的程序所使用，这些程序包括：sshd、tcpd、sendmail、syslogd 等。

`MX`
MX RR 用于邮件系统实现邮件路由。有关电子邮件的更多介绍请参见 FIXME 。 其格式为：
zone   [ttl]  IN   MX  preference   host
其中 preference 是优先级字段，数值越小优先级越高。
例如：
jamond.net.          IN    MX     5    ubuntu.jamond.net.
jamond.net.          IN    MX     10    ubuntu.jamond.net.

`CNAME`
CNAME RR 用于设置主机的别名。 其格式为：
nikename    [ttl]   IN  CNAME   hostname
例如：
ubuntu          IN    A      192.168.0.251
www             IN    CNAME  ubuntu
ftp             IN    CNAME  ubuntu
文件内必须有规范名字的 A RR。

分析器指令
在区文件中还可以使用分析器指令，分析器指令可以为 RR 的输入提供方便。
$ORIGIN — 设置默认域（或初始域）
$TTL — 为没有定义精确的生存期的 RR 定义缺省的 TTL 值


### rndc

`rndc（remote name daemon control）`：是一个系统管理员操作名称服务（DNS服务）的程序，使用rndc命令可以实现重新加载域名服务的配置文件或区文件，停止域名服务，显示域名服务状态等功能。
使用：
执行命令：
`#rndc-confgen`
该命令的输出结果中前半部分是配置文件/etc/rndc.conf的设置，后半部分给出了如何修改/etc/named.conf中key{…}、controls{…}的内容，这样做的目的是实现操作DNS服务时的数字认证。
或者像下面操作：
```
#rndc-confgen > /etc/rndc.conf
从rndc.conf文件中提取named.conf用的key
#cd /etc
#tail -10 rndc.conf | head -9 | sed s/#\ //g >> named.conf
rndc的常见用法:
#rndc status
#rndc start | stop | restart
#rndc reload ssti.net
```


手动创建bind主配置文件
```
[root@localhost etc]# vim named.conf    #不熟悉的可以直接通过修改原始的配置文件
options {
  directory "/var/named";
  
  };    
zone "." IN {
  type hint;
  file "named.ca";
};
include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";
```
定义一个zone
```
[root@localhost etc]# cat >> /etc/named.rfc1912.zones << EOF    #这里使用Here Document，不懂得可以搜素
> zone "anyisalin.com" IN {            #定义区域为anyisalin.com
>    type master;                    #设置类型为master
>    file "anyisalin.com.zone";        #解析库文件名称为anyisalin.com.zone
> };
> EOF
```

创建区域解析库文件
```
[root@localhost etc]# vim /var/named/anyisalin.com.zone 
$TTL 600    #定义全局默认超时时间
$ORIGIN anyisalin.com.    #定义后缀
@   IN  SOA    ns1.anyisalin.com.  admin.anyisalin.com. (
                20160321    #序列号
                1H    #刷新时间
                5M    #重试时间
                1W    #超时时间
                10M )    #否定答案缓存TTL值
        IN      NS      ns1
ns1     IN      A       192.168.192.150
        IN      MX 10   mail1
mail1   IN      A       192.168.192.1
www     IN      A       192.168.192.2
cname   IN      CNAME   www                #别名, 将cname.anyisalin.com. 解析到 www.anyisalin.com.的地址
*       IN      A       192.168.2.1    #泛域名解析，以上都不是的解析到192.168.2.1
```

检查、启动并测试

```
[root@localhost etc]# named-checkconf     #检查主配置文件语法
[root@localhost etc]# named-checkzone "anyisalin.com" /var/named/anyisalin.com.zone     #检查anyisalin.com zone所对应的解析库文件
zone anyisalin.com/IN: loaded serial 20160321
OK
[root@localhost etc]# service named start
Starting named:           
```


### 四、区域传送和子域授权
上面我们已经讲过，一个域内的DNS服务器一般都需要两个，我们这里就进行主从配置和区域传送

在从服务器安装bind并创建bind主配置文件
```
[root@localhost etc]# vim named.conf    #不熟悉的可以直接通过修改原始的配置文件
options {
  directory "/var/named";
  
  };    
zone "." IN {
  type hint;
  file "named.ca";
};
include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";
```
定义zone
```
[root@localhost named]# cat >> /etc/named.rfc1912.zones <<EOF        #这里定义方式和主服务器的配置略有不同
> zone "anyisalin.com" IN {
>   type slave;
>   masters { 192.168.192.150; };    #定义主服务器的IP地址
>   file "slaves/anyisalin.com.zone";    #定义传送文件的存放位置，必须要和源文件相同
>  };
> EOF
```

在主服务器的解析库中添加一条NS记录指向从服务器的地址
增量传送， #增量传送需要修改序列号！
```
[root@localhost etc]# vim /var/named/anyisalin.com.zone     #在主服务上执行！！！
$TTL 600
$ORIGIN anyisalin.com.
@   IN   SOA    ns1.anyisalin.com.  admin.anyisalin.com. (
        20160321
        1H
        5M
        1W
        10M )
 
       IN    NS      ns1
       IN    NS      ns2                #添加ns2记录
ns1    IN    A       192.168.192.150
ns2    IN    A       192.168.192.147        #添加ns2对应的A记录
       IN    MX  10  mail1
mail1  IN    A       192.168.192.1
www    IN    A       192.168.192.2
cname  IN    CNAME   www
*      IN    A       192.168.2.1
 
 
[root@localhost etc]# rndc reload    #重载配置文件
server reload successful
```

启动bind服务

子域授权---在主dns服务器添加两条记录

```
vim /var/named/anyisalin.com.zone
$TTL 600
$ORIGIN anyisalin.com.
@   IN  SOA    ns1.anyisalin.com.  admin.anyisalin.com. (
                20160324
                1H
                5M
                1W
                10M )
        IN      NS      ns1
        IN      NS      ns2
ns1     IN      A       192.168.192.150
ns2     IN     A   192.168.192.147
        IN      MX 10   mail1
mail1   IN      A       192.168.192.1
www     IN      A       192.168.192.2
cname   IN      CNAME   www
*       IN      A       192.168.2.1
new     IN      A       192.168.1.1
ops     IN      NS      ns1.ops        #添加一条NS记录将ops.anyisalin.com. 域授权给ns1.ops.anyisalin.com.进行管理
ns1.ops IN      NS      192.168.192.151    #对应上条的NS记录的A记录
```

在ns1.ops.anyisalin.com.主机上进行配置
```
vim /etc/named.conf        #配置bind主配置文件
options {
  directory "/var/named";
  };    
zone "." IN {
  type hint;
  file "named.ca";
};
include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";
```

```
[root@localhost ~]# cat >> /etc/named.rfc1912.zones <<EOF    #定义zone
> zone "ops.anyisalin.com" IN {
>    type master;
>    file "ops.anyisalin.com.zone";
> };
> EOF
```


```
[root@localhost named]# cat ops.anyisalin.com.zone     #定义解析库
$TTL 600
$ORIGIN ops.anyisalin.com.
@   IN  SOA ns1.ops.anyisalin.com.  admin.ops.anyisalin.com. (
        20160321
        1H
        5M
        7D
        1H
)
 
 
    IN  NS  ns1
ns1 IN  A   192.168.192.151
www IN  A   192.168.1.1
```


测试
```
[root@localhost named]# service named start
Starting named:                                            [  OK  ]
 
通过本机解析本域主机名
[root@localhost named]# host -t A www.ops.anyisalin.com 192.168.192.151
Using domain server:
Name: 192.168.192.151
Address: 192.168.192.151#53
Aliases: 
www.ops.anyisalin.com has address 192.168.1.1
 
通过父域DNS解析本域下的主机名
 
[root@localhost named]# host -t A www.ops.anyisalin.com 192.168.192.150
Using domain server:
Name: 192.168.192.150
Address: 192.168.192.150#53
Aliases: 
 
www.ops.anyisalin.com has address 192.168.2.1
 
通过本机DNS解析父域中的主机名
[root@localhost named]# host -t A www.anyisalin.com 192.168.192.151
;; connection timed out; trying next origin
Using domain server:
Name: 192.168.192.151
Address: 192.168.192.151#53
Aliases: 
 
Host www.anyisalin.com not found: 3(NXDOMAIN)
```


但是我们可能会发现一个问题，如果我需要解析父域中的主机名，只能通过递归到根域去解析，这是非常不便的，所以我们要设置转发器。

```
[root@localhost named]# cat >> /etc/named.rfc1912.zones <<EOF    #定义转发器
> zone "anyisalin.com" IN {
>     type forward;
>     forward  only ;
>     forwarders { 192.168.192.150; };
> };
> EOF
```


```
[root@localhost named]# rndc reload    #重载配置文件
server reload successful
[root@localhost named]# host -t A www.anyisalin.com 192.168.192.151    #使用本机进行解析
Using domain server:
Name: 192.168.192.151
Address: 192.168.192.151#53
Aliases: 
www.anyisalin.com has address 192.168.192.2    #现在能够得出结果
```

### 五、BIND视图实现智能DNS
大家都知道，中国的运营商之间的带宽是非常低，但是无论我们是哪个运营商的宽带，访问那些大型电商站点都是非常的快，那是因为在dns服务器中定义了来自哪些IP的请求解析成哪些地址，这就是视图的功能。

```
1、一旦启动了view, 所有的zone都只能在view中定义
2、仅有必要在匹配到允许递归请求的客户所在view定义根区域
3、客户端请求到达, 是自上而下检查每个view所服务器的客户端列表
 
[root@localhost etc]# vim /etc/named.conf    #修改主配置文件
acl mynet {
 
        192.168.192.150;
        127.0.0.0/8;
};
 
acl other {
        192.168.192.1;
};
 
 
 
 
options {
  directory "/var/named";
 
   dnssec-enable no;
   dnssec-validation no;
 
  };   
view "." {
match-clients { mynet; };
zone "." IN {
  type hint;
  file "named.ca";
};
};
include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";
 
vim /etc/named.rfc.1912.zones    #配置主配置文件
view mynet {    
 match-clients { mynet; };
 
zone "localhost.localdomain" IN {
    type master;
    file "named.localhost";
    allow-update { none; };
};
 
zone "localhost" IN {
    type master;
    file "named.localhost";
    allow-update { none; };
};
 
zone "1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa" IN {
    type master;
    file "named.loopback";
    allow-update { none; };
};
 
zone "1.0.0.127.in-addr.arpa" IN {
    type master;
    file "named.loopback";
    allow-update { none; };
};
 
zone "0.in-addr.arpa" IN {
    type master;
    file "named.empty";
    allow-update { none; };
};
 
zone "anyisalin.com" IN {
   type master;
   file "anyisalin.com.zone";
};
};
 
view other {
 match-clients { other; };
zone "anyisalin.com" IN {
  type master;
  file "anyisalin.com.other";
};
};


```

name.conf
rndc.conf

/usr/local/named/sbin/rndc-confgen  > /usr/local/named/etc/rndc.conf &

tail -10 rndc.conf | head - | sed s/#\ //g > named.conf

## 术语

### DNS资源记录类型
`SOA`：起始授权记录，一个区域的解析库中有且只能有一条SOA记录，必须为解析库中的第一条记录，定义主DNS服务器地址和相关事件时间定义。
`A`：实现FQDN ==> IP 
`MX`：标明提供邮件服务的主机
`NS`：标明当前域内的DNS服务器
`AAAA`：FQDN ==> IPv6
`CNAME`：Canonical Name，别名记录
`PTR`：IP ==> FQDN

`A记录`：IP IN  A Value ; 示例：192.168.1.1 IN A www.anyisalin.com.

`NS记录`：domain IN NS Value; 示例：anyisalin.com. IN  NS ns1.anyisalin.com. 一条NS记录必须要有一条与之对应的A记录

`MX记录`：domain IN NS priority Value; 示例：anyisalin.com. IN  MX 10 mail1.anyisalin.com. 一条MX记录必须要有与之对应的A记录, 优先级0-99，越低优先级越高

`PTR记录`：IP.in-addr.arpa. IN PTR Value; 示例：1.1.168.192.in-addr.arpa. IN PTR www.anyisalin.com. #PTR记录的写法比较诡异，我们在后面进行叙述

`AAAA记录`：和A记录相似，只是将IPv4地址换为IPv6

## 实例
named.conf的zone

zone "." IN {
    type hint;
    file "named.root";

};

zone "htop.me" IN {
  type master;  
  file "htop.me.zone";
  allow-update {none;};
  allow-transfer {10.0.0.2;};
  notify yes;
  also-notify {10.0.0.2;};   
};

zone  "0.0.10.in-addr.arpa" IN{
    type master;
    file "0.0.10.zone";
}

## DNS view

## 安全设置

bind安全配置：
    
```
访问控制命令：
allow-query {}; 允许查询的主机, 白名单
allow-transfer {}; 允许区域传送主机, 白名单
allow-recursion {}; 允许递归的主机
allow-update {}; 允许更新区域数据库中的内容
```



[sss](http://anyisalin.blog.51cto.com/10917514/1753638)
