# openvpn
---

## openvpn的简介(出自维基百科)

OpenVPN是一个用于创建虚拟专用网络加密通道的软件包，最早由James Yonan编写。OpenVPN允许创建的VPN使用公开密钥、电子证书、或者用户名／密码来进行身份验证。
它大量使用了OpenSSL加密库中的SSLv3/TLSv1协议函数库。
目前OpenVPN能在Solaris、Linux、OpenBSD、FreeBSD、NetBSD、Mac OS X与Microsoft Windows以及Android和iOS上运行，并包含了许多安全性的功能。它并不是一个基于Web的VPN软件，也不与IPsec及其他VPN软件包兼容。

### 原理
OpenVPN的技术核心是虚拟网卡, 其次是SSL协议实现.

OpenVPN中的虚拟网卡: 虚拟网卡是使用网络底层编程技术实现的一个驱动软件。安装此类程序后主机上会增加一个非真实的网卡，并可以像其它网卡一样进行配置。服务程序可以在应用层打开虚拟网卡，如果应用软件（如网络浏览器）向虚拟网卡发送数据，则服务程序可以读取到该数据。如果服务程序写合适的数据到虚拟网卡，应用软件也可以接收得到。虚拟网卡在很多的操作系统中都有相应的实现，这也是OpenVPN能够跨平台使用的一个重要原因。
在OpenVPN中，如果用户访问一个远程的虚拟地址（属于虚拟网卡配用的地址系列，区别于真实地址），则操作系统会通过路由机制将数据包（TUN模式）或数据帧（TAP模式）发送到虚拟网卡上，服务程序接收该数据并进行相应的处理后，会通过SOCKET从外网上发送出去。这完成了一个单向传输的过程，反之亦然。当远程服务程序通过SOCKET从外网上接收到数据，并进行相应的处理后，又会发送回给虚拟网卡，则该应用软件就可以接收到

### 加密方式
OpenVPN使用OpenSSL库来加密数据与控制信息。这意味着，它能够使用任何OpenSSL支持的算法。它提供了可选的数据包HMAC功能以提高连接的安全性。此外，OpenSSL的硬件加速也能提高它的性能。2.3.0以后版本引入PolarSSL

### 身份验证方式
OpenVPN提供了多种身份验证方式，用以确认连接双方的身份，包括：
* 预享私钥
* 第三方证书
* 用户名／密码组合
预享密钥最为简单，但同时它只能用于创建点对点的VPN；基于PKI的第三方证书提供了最完善的功能，但是需要额外维护一个PKI证书系统。OpenVPN2.0后引入了用户名／口令组合的身份验证方式，它可以省略客户端证书，但是仍需要一份服务器证书用作加密。

### 功能与端口
OpenVPN所有的通信都基于一个单一的IP端口，默认且推荐使用UDP协议通讯，同时也支持TCP。IANA（Internet Assigned Numbers Authority）指定给OpenVPN的官方端口为1194。OpenVPN 2.0以后版本每个进程可以同时管理数个并发的隧道。OpenVPN使用通用网络协议（TCP与UDP）的特点使它成为IPsec等协议的理想替代，尤其是在ISP（Internet service provider）过滤某些特定VPN协议的情况下。

OpenVPN连接能通过大多数的代理服务器，并且能够在NAT的环境中很好地工作。
服务端具有向客户端“推送”某些网络配置信息的功能，这些信息包括：IP地址、路由设置等。

OpenVPN提供了两种虚拟网络接口：通用Tun/Tap驱动，通过它们，可以创建三层IP隧道，或者虚拟二层以太网，后者可以传送任何类型的二层以太网络数据。
传送的数据可通过LZO算法压缩。

### 安全
OpenVPN与生俱来便具备了许多安全特性：它在用户空间运行，无须对内核及网络协议栈作修改；初始完毕后以chroot方式运行，放弃root权限；使用mlockall以防止敏感数据交换到磁盘。
OpenVPN通过PKCS#11支持硬件加密标识，如智能卡

client: 10.0.0.4
Openvpn server 双网卡: 外网: 10.0.8.28 ,gw, dns正常配置, 内网: 172.16.2.18 gw不要配
机房App Server: eth0 172.16.2.33/24

## OpenVPN安装与配置

### Linux
- 1.使用ntp做时间同步
- 2.安装
CentOS 6.x
```
# 设置epel源
yum install easy-rsa openvpn openssl openssl-devel lzo lzo-devel
```

CentOS 7.x
```
# 设置epel源
yun install openssl openssl-devel lzo lzo-devel openvpn easy-rsa
```

Ubuntu
```
sudo  apt-get update
sudo  apt-get install openvpn easy-rsa
```

#### 编译
```
yum install gcc 
编译需要依赖的包openssl-devel lzo-devel pam-devel

tar xfz openvpn-[version].tar.gz
./configure
make
make install
```
### windows

### 生成key
1. copyeasy-rsa包到openvpn下
```
cp -fr /usr/share/easy-rsa/2.0/ /etc/openvpn/easy-rsa
```
2. 配置pki
```
cd /etc/openvpn/easy-rsa
vim vars
#修改最后的部分, 根据自己的自定义

export KEY_COUNTRY="CN" #国家简称
export KEY_PROVINCE="JS" #省份
export KEY_CITY="Wuxi"　# 城市
export KEY_ORG="YimiWork" # 组织名称, 
export KEY_EMAIL="zhaifengguo@1mi.cn" # 管理员email
export KEY_OU="uxindai" # 单元名

# X509 Subject Field
export KEY_NAME="EasyRSA"
```

3. 加载vars中环境变量
```
source vars
 
NOTE: If you run ./clean-all, I will be doing a rm -rf on /etc/openvpn/easy-rsa/keys
```


4. 清空原有的证书
```
./clean-all 
```

5. 生成ca证书
```
./build-ca

Generating a 2048 bit RSA private key
.............................+++
................................................+++
writing new private key to 'ca.key'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [CN]:
State or Province Name (full name) [JS]:
Locality Name (eg, city) [Wuxi]:
Organization Name (eg, company) [BaiChuan]:
Organizational Unit Name (eg, section) [ops]:
Common Name (eg, your name or your server's hostname) [BaiChuan CA]:
Name [EasyRSA]:
Email Address [admin@baichuan.com]:

```

6. 生成服务端证书
```
./build-key-server server

Generating a 2048 bit RSA private key
.......................................................................+++
.........................................+++
writing new private key to 'server.key'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [CN]:
State or Province Name (full name) [JS]:
Locality Name (eg, city) [Wuxi]:
Organization Name (eg, company) [BaiChuan]:
Organizational Unit Name (eg, section) [ops]:
Common Name (eg, your name or your server's hostname) [server]:
Name [EasyRSA]:
Email Address [admin@baichuan.com]:

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:
Using configuration from /etc/openvpn/easy-rsa/openssl-1.0.0.cnf
Check that the request matches the signature
Signature ok
The Subject's Distinguished Name is as follows
countryName           :PRINTABLE:'CN'
stateOrProvinceName   :PRINTABLE:'JS'
localityName          :PRINTABLE:'Wuxi'
organizationName      :PRINTABLE:'BaiChuan'
organizationalUnitName:PRINTABLE:'ops'
commonName            :PRINTABLE:'server'
name                  :PRINTABLE:'EasyRSA'
emailAddress          :IA5STRING:'admin@baichuan.com'
Certificate is to be certified until Apr 15 02:34:47 2027 GMT (3650 days)
Sign the certificate? [y/n]:y  


1 out of 1 certificate requests certified, commit? [y/n]y
Write out database with 1 new entries
Data Base Updated

```
输入y,同意生成证书

7. 生成DH验证文件
```
./buid-dh
```

8. 

9. 生成客户端证书
```
./build-key user_001

Generating a 2048 bit RSA private key
................................................................................................+++
.......................................................+++
writing new private key to 'user_001.key'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [CN]:
State or Province Name (full name) [JS]:
Locality Name (eg, city) [Wuxi]:
Organization Name (eg, company) [BaiChuan]:
Organizational Unit Name (eg, section) [ops]:
Common Name (eg, your name or your server's hostname) [user_001]:
Name [EasyRSA]:
Email Address [admin@baichuan.com]:

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:
Using configuration from /etc/openvpn/easy-rsa/openssl-1.0.0.cnf
Check that the request matches the signature
Signature ok
The Subject's Distinguished Name is as follows
countryName           :PRINTABLE:'CN'
stateOrProvinceName   :PRINTABLE:'JS'
localityName          :PRINTABLE:'Wuxi'
organizationName      :PRINTABLE:'BaiChuan'
organizationalUnitName:PRINTABLE:'ops'
commonName            :T61STRING:'user_001'
name                  :PRINTABLE:'EasyRSA'
emailAddress          :IA5STRING:'admin@baichuan.com'
Certificate is to be certified until Apr 15 02:43:04 2027 GMT (3650 days)
Sign the certificate? [y/n]:y


1 out of 1 certificate requests certified, commit? [y/n]y
Write out database with 1 new entries
Data Base Updated

```
客户端证书用于客户端连接时使用的证书

### 证书的类型以及作用域

|文件名| 作用域 | 作用 |加密|
|----- |-----|----|-----|
|car.crt| 服务端和所有客户端  |root ca证书    | No    |
|car.key| 密钥签名的机  |root ca key   | Yes   |
|dh{n}.pem| 服务端  |Diffie Hellman parameters  | NO   |
|server.crt| 服务端  |服务端证书  | NO   |
|server.key| 服务端  |服务端密钥  | YES   |
|user_001.crt| 客户端(User001)  |客户端证书  | No   |
|user_001.key| 客户端  |客户端密钥  | YES   |

### 服务端配置
- 1.在openvpn下创建server.conf的配置文件,
```
port 1194 # 指定端口
proto tcp  # 指定tcp协议默认是udp协议
dev tun # 使用路由模式
ca ca.crt # 指定 ca证书
cert server.crt # 指定服务端证书
key server.key  # 指定服务端密钥

dh dh2048.pem # 使用Diffie Hellman算法进行加密密钥计算
server 10.8.0.0 255.255.255.0 # 指定tun0, 以及vpn的的网段
ifconfig-pool-persist ipp.txt # 

push "route 192.168.8.0 255.255.255.0" # 推送到客户端的路由
push "dhcp-option DNS 223.5.5.5" # 向客户端推送DNS
push "redirect-gateway def1 bypass-dhcp"  #


client-config-dir ccd # 使用此目录对各个vpn客户端进行细粒度控制
script-security 2

client-to-client # 允许不同客户端进行互相访问, 使用openvpn内部路由
duplicate-cn #

keepalive 10 120 #每10秒发送保活, 120秒内未收到保活信息时想OpenVPN进程发送SIGUSR1信号
;tls-auth ta.key 0 # 防止DDOS

cipher AES-256-CBC

max-clients 100 # 最多登录的客户端
user nobody  # 启动程序的用户和组
group nobody
persist-tun  #收到信息SIGUSR1时不关闭tuno虚拟网口和重新打开
persist-key #收到信号SIGUSR1时不重新读取key文件
status openvpn-status.log # 状态信息位置
log-append  /var/log/openvpn.log

verb 3 # 日志级别

```
- 1.ccd目录下的文件, 必须以客户端证书的Common Name文件命名
- 2.ccd目录可以对每个不同的客户端进行细粒度的控制
-   * 配置实例: 客户端user_001
      * ccd/user_001:
        * `ifconfig-push 10.8.0.11` 定义获取的IP
        * `iroute 192.168.4.0 255.255.255.0` 自定义单台的路由
- 3.iroute是必需的. 在server.conf中的--route指令把包从内核路由到OpenVPn, 进入VPN后, --route指令把路由到该指定的客户端
- 

### 重要的服务端参数
* `server 10.8.0.0 255.255.255.0`
* `push "route-gateway 10.8.0.4"`
* `client-config-dir ccd`
* `route 192.168.4.0 255.255.255.0`
* `iroute 192.168.4.0 255.255.255.0`
* `push "dhcp-option DNS 10.66.0.5"`
* `local host`
* `duplicate-cn`
* `script-security 2`
* `redirect-gateway flags`: 自动执行路由命令, 使所有出站的IP流量通过VPN重定向. 这是一个客户端选项
  * 此操作的过程分三步:
    * 创建一个静态的路由到remote 的服务器上
    * 删除原来的路由
    * 设置新的默认路由
  * 相应的标志为:
    * `local`: 
    * `autolocal` :
    * `def1`: 使用此标志可以使用0.0.0.0/1和128.0.0.0/1而不是0.0.0.0/0来覆盖默认网关。这样做有利于重写，但不会擦除原始的默认网关。
    * `bypass-dhcp`: 添加直接路由到DHCP服务器
    * `bypass-dns`: 
    * `block-local`: 
    
### 启动服务端
/etc/init.d/openvpn

`openvpn --deamon --config /etc/openvpn/server.conf`
### 客户端
一般情况下的使用证书登录的客户端文件
客户端配置文件, 一般以ovpn为扩展名, 文件名一般是用户生成时的common name, 如user_001.ovpn
```
client # 指定角色为客户端
dev tun  # 和服务器一致
proto tcp # 和服务器一致
remote 58.215.212.194 1194 # 指定服务器的IP和端口
resolv-retry infinite # 连接失败重复尝试
nobind # 不指定本地端口
persist-key # 收到信号SIGUSR1不重新读取key
persist-tun # 收到信号SIGUSR1不关闭tun虚拟网口和重新打开

ca "hfca.crt" # 指定CA证书位置
cert "zhaifg.crt" # 指定客户端证书位置
key "zhaifg.key" # 指定客户端密钥位置

comp-lzo # 启用压缩

#ns-cert-type server # 要求服务器端的证书的扩展属性为server
remote-cert-tls server
cipher AES-256-CBC
verb 3

```
#### Linux 系统
1. 终端中登录
```
openvpn --config client.ovpn
```
2. gui客户端

#### windows

安装openvpn-install.exe文件, 把ca证书以及用户证书放在config目录下

## OpenVPN的使用方式

### 使用OpenVPN创建点对点方式
#### 创建不加密的简单的点对点
a server:
```
openvpn --remote b.server.com --dev tun0 --ifconfig 10.8.0.1 10.8.0.2 --verb 9
```

b server
```
openvpn --remote a.server.com --dev tun0 --ifconfig 10.8.0.2 10.8.0.1 --verb 9
```

on a server:
```
tun0      Link encap:UNSPEC  HWaddr 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  
          inet addr:10.8.0.1  P-t-P:10.8.0.2  Mask:255.255.255.255
          UP POINTOPOINT RUNNING NOARP MULTICAST  MTU:1500  Metric:1
          RX packets:12 errors:0 dropped:0 overruns:0 frame:0
          TX packets:12 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:100 
          RX bytes:1008 (1008.0 b)  TX bytes:1008 (1008.0 b)

ping 10.8.0.2
PING 10.8.0.2 (10.8.0.2) 56(84) bytes of data.
64 bytes from 10.8.0.2: icmp_seq=1 ttl=64 time=9.56 ms
^C
--- 10.8.0.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 797ms
rtt min/avg/max/mdev = 9.566/9.566/9.566/0.000 ms

```

b server
```
ifconfig

tcpdump -vvv -nnn -i tun0 icmp

```

#### A tunnel with static-key security 
*  a server 上生成key, 并复制到b server上
```
openvpn --genkey --secret key
```

* on a server
```
openvpn --remote b.server.com --dev tun0 --ifconfig 10.8.0.1 10.8.0.2 --verb 5 --secret key

```

* on b server
```
openvpn --remote a.server.com --dev tun0 --ifconfig 10.8.0.2 10.8.0.1 --verb 5 --secret key
```

####  A tunnel with full TLS-based security
这种方式下使用 server和client方式
* server中创建ca证书
* 创建dh证书
* 创建server证书
* 创建客户端证书
* 在客户端
```
openvpn --remote server.example.com --dev tun1 --ifconfig 10.4.0.1 10.4.0.2 --tls-client --ca ca.crt --cert client.crt --key client.key --reneg-sec 60 --verb 5
```

* 在server端
```
openvpn --remote client.example.com --dev tun1 --ifconfig 10.4.0.2 10.4.0.1 --tls-server --dh dh1024.pem --ca ca.crt --cert server.crt --key server.key --reneg-sec 60 --verb 5
```
* 路由处理
```
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -A FORWARD -i tun+ -j ACCEPT

```

### 使用OpenVPN的远程访问服务
这种方式,通常用于远程办公的方式, 通过vpn拨号入自己的内网

架构如图:


配置过程
* 设置VPN Server的的时间同步, 并且安装openvpn, 详细教程, 如上
* 生成相应的证书, 以及客户端证书user_001
* 配置server.conf
```

```

* 启动OpenVPN 服务器
* 设置防火墙, 放行相应的端口
* 客户端安装openvpn(以linux为例的客户端)
* 下载相应的客户端证书,
* 生成相应的客户端的配置文件 user_001.ovpn
* 客户端连接到VPN Server, 并测试连通性
* 设置OpenVPN Server的IP转发
* 客户端通过VPN连接OpenVPN局域网内的其他的Server
```
在客户端上:
ping 192.168.10.100

在 10.100上抓包

有来没有返回
```

* 解决客户端访问服务端局域网内的问题的方式:
  * 第一种: 把OpenVPN的所在局域网的内的机器的网关全部设置为OpenVPN的这台服务器
  * 第二种: 在各个服务器上添加一个静态路由使10.8.0.0/24端的请求发送到OpenVPN上
  * 第三种: 在OpenVPN上通过iptables进行nat转换的方式
我们选择使用第三种
在OpenVPN上
```
iptables -A FORWARD -i tun0 -j ACCEPT
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE  # eth0为内网的网卡
iptables  -t nat -A POSTROUTING -o tun0 -j MASQUERADE #可选
# or
iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE 
iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eho0 -j SNAT --to-source 10.2.8.10 

```

* 测试连通性
* 
### 构建LAN-to-LAN的方式
站点到站点的VPN, 用于连接两个或者多个地域上的不同局域网. 每一个LAN有一台OpenVPN服务器作为接入点, 组成虚拟专用网络, 使得不同LAN里面的主机和服务器都能互联互通

典型架构如下:

部署注意的事项:
* 在所有VPN的接入点, 把系统路由转发打开
* 在所有VPN的接入点, 在tun0端口和内网端口全部配置成NAT模式, 简化了VPN的路由设置
* 在所有的VPN的接入点, 把iptables转发设置为允许
* 在每个LAN的主机, 通过设置静态路由或者默认路由, 把到对端的访问下一跳指向到本机的LAN的接入点的内网IP.

client端参考
```
clinet
dev tun
proto udp
remote ip port
resolv-retry infinite
nobind
persist-key
persist-tun
ca
cert
key
ns-ceryt-type server
comp-lzp
verb4
route-delay 2
keepalive 10 120
log-append /var/log/openvpn/openvpn.log
```

### 回收客户端证书
```
. ./vars
./revoke-full user_001
#  keys下生成crl.pem, 在server.conf上加入
crl-verfiy crl.pem
```
## OpenVPN的验证方式

### 使用证书验证
上面的都是使用证书的方式

### 使用脚本验证

server端
```
auth-user-pass-verify auth-pam.pl via-file
client-cert-not-required
username-as-common-name
script-security 3 # 改为3
```

client端
去掉客户端的证书以及密钥, 让添加auth-user-pass
```
client
dev tun
proto tcp
remote 115.29.190.115 1194
nobind
persist-key
persist-tun
ns-cert-type server
ca "ca.crt"
cipher AES-256-CBC
verb 3
auth-user-pass
```
### 使用

## 客户端的负载均衡
## 排错

### log

### 客户端与服务端要一致的配置

cipher
ca
dev
proto
comp-lzo

### ip forward的设置

### 检查路由表
1. 时间同步
2. lzo包安装, openvpn
```
cd esay-rsa/
vim vars

export KEY_COUNTRY="CN"
export KEY_PROVINCE="Jiangsu"
export KEY_CITY="Wuxi"
export KEY_ORG="YimiWork"
export KEY_EMAIL="me@admin.com"
export KEY_CN=CN
export KEY_NAME=xxxx
export KEY_OU=xxx

./configure 

./clean-all
./build-ca # 生成ca证书
./build-key-server server # 服务端秘钥文件 server可以自定义
./build-key  user01 #客户端证书
./build-key-pass user01 # 证书加密码

# 生成hellman协议文件, 生成传输进行密钥交换时用到的交换密钥协议
./build-dh

# 生成防止恶意攻击的文件
openvpn --genkey --secret keys/ta.key
```

`vars`: 创建环境变量等等
`clean-all`: 
``
``
`pkitool` 脚本直接使用vars的环境变量设置, 直接生成证书
```
cp -ap keys /etc/openvpn
cp sample-config-files/client.conf,server.conf /etc/openvpn/

```

server.conf

local
port
proto udp
dev tun
ca ca.rt

cert server.crt
key server.key
dh dh1024.pem
server 10.8.0.0 255.255.255.0
ifconfig-poll-persist ipp.txt
push "route 172.16.1.0 255.255.255.0" : 是VPN SERVER所在的内网网段, 如果有多个可以写多个push, 注意, 此命令在vpn客户端生成.

client-to-client: 客户之间是否允许通讯
duplicat-cn: 允许多个客户单使用同一个账号连接
keepalive 10 120
comp-lzp
presist-key
persist-tun
status openvpn-status.log  openvpn日志状态信息
log /var/log/openvpn.log 日志文件
verb3 


有防火墙的话, 要开启
IP转发


eth0

iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE

iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -d 10.2.8.0/24 -o eho0 -j SNAT --to-source 10.2.8.10 
将虚拟网段10.8.0.0/24访问内网10.2.8.0/24都通过内网网卡eth0并且将源地址转换成10.2.8.10转发

iptables -t nat -A POSTROUTING -s 172.16.10.0/24 -j SNAT --to-source 115.29.190.115

1.  vpnserver 做网关
2.  不加网关, 加路由
3.  使用iptables nat 不加网关和路由
  * 内网地址的网卡添加nat使用
  * masque
  * iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth1 -j MASQUERADE
  * to-source 方式
  * iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth1 -j SNAT --to--source 内网网卡地址 eth1 是内网网卡


openldap, openvpn, samba ,[mail], gitlab, zabbix, oa
登录日志, samba,修改日志, 


openvpn 教程, 解决方案, 
