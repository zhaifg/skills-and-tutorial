# openstack的组成
---

## keystone
用户认证,服务目录

/etc/keystone.keystone.conf
使用keystone客户端进行配置
认证的概念
Authenticaition
credentials
Domain
EndPoint
Group
OpenStackClient
Project
Region
Role
Service
Token
User

管理的实例
openstack user create --password-prompt --email alice@example.com alice


## glance
glance-api : 接受云系统的创建删除,读取请求
glance-registry: 云系统的镜像注册服务
image store: 

## Nutron (网络)
公共网络
管理网络
存储网络
服务网络

应用层: lbaas
传输层: Lbaas haproxy vpnaas
网络层: iptables ,ip route
数据链里层: Linux birdge


## Nova
API: 负责接收和响应外部请求, 支持OpenStack API, EC2API

Cert:负责身份认证
Scheduler: 用于云主机调用
Conductor: 计算节点访问数据的中间件
Consoleauth: 用于控制台的授权认证
Novncproy: vnc代理

## Cinder块存储服务

### 块存储
1. 物理硬盘
2. LVM设备
3. FC-SAN, IP-SAN

### 文件存储
1. nas
2. nfs,
3.  ceph_fs
### 对象存储
1. ceph rbd

### 存储的选择
本地存储(Cinder默认)

NFS

GlusterFS

iSCSI

Ceph

MooseFS

## 虚拟机新建过程
1. 界面或者命令行通过RESTful API向keystone获取认证信息
2. keystone 通过用户请求认证信息, 并生成auth-token返回给对应的认证请求
3. 界面或者命令通过RESTful API向nova-api发送一个boot instance的请求(携带auth-token).
4. nova-api接受请求后向keystone发送认证求情, 查看token是否为有效用户和token
5. keystone验证token时候有效,如果有效则返回有效的认证和对应的角色(注:有些操作需要角色权限才能操作.).
6. 通过认证后nova-api和数据通讯(mq).
7. 初始化新建虚拟机的数据库记录
8. nova-api通过rpc.call 想nova-scheduler请求是否有创建虚拟机的资源(Host ID).
9. nova-scheduler进程监听消息队列, 获取nova-api的请求.
10. nova-scheduler通过查询nova数据库中计算资源的情况, 并通过调度算法计算符合虚拟机创建需要的主机.
11. 对于有符合虚拟机创建的主机,nova-scheduler更新数据库中虚拟机对应的物理主机信息.
12. nova-scheduler通过rpc.cast想nova-computer发送对应的 创建虚拟机的请求信息.
13. nova-compute 会从对应的消息队列中获取创建虚拟机请求的消息.
14. nova-compute通过rpc.call想nova-conductor请求获取虚拟机的消息(Flavoer)
15. nova-conductor会从消息队列中拿到nova-compute请求信息.
16. nova-conductor根据消息查询虚拟机对应的信息.
17. nova-conductor从数据库中获得虚拟机对应的信息.
18. nova-conductor吧虚拟机信息通过消息的方式发送到消息队列中.
19. nova-comptue从队形的消息队列中获取虚拟机信息消息.
20. nova-compute通过keystone的RESTful API拿到认证的token, 并通过HTTP请求glance-api获取创建虚拟机所需要的镜像.
21. glance-api向keystone认证token是否有效, 并返回结果.
22. token验证通过, nova-compute获得虚拟机镜像信息(URI).
23. nova-compute通过keystone的REST ful API拿到认证的token, 并通过HTTP请求neutron-server获取创建虚拟机所需要的网络信息.
24. neutron-server想keystone验证token的有效性, 并返回验证结果.
25. token验证通过, nova-compute获得虚拟机网络信息.
26. nova-compute通过keystone 的REST ful API拿到认证token, 并通过HTTP请求cinder-api获取创建虚拟机所需要的持久化存储的信息.
27. conder-api想keystone认证token是否有效, 并返回验证结果.
28. token通过验证, nova-compute获得虚拟机持久化存储信息.
29. nova-compute根据instance的信息调用配置的虚拟化驱动来创建虚拟机.


