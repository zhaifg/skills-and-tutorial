# Docker网络
---

网络通过namespace进行网络隔离

## Docker网络的类型
1. bridge: 默认的网络驱动. Container通过一对veth pair连接到docker0网桥上, 由Docker为容器动态分配IP以及配置路由, 防火墙规则等.
2. host: 容器与主机共享同一Network Namespace, 共享一套网络协议栈,路由表以及iptables规则等. 容器与主机看到的是相同的网络视图.
3. null/none: --net=none  容器内网配置为空, 需要用户手动为容器配置网络接口以及路由等.
4. remote: Docker网络插件的实现. Remote dirver是的Libnetwork可以通过HTTP RESTful API对接第三方的网络方案, 类似SOcketPlane的SDN方案只要实现了约定HTTP URL处理函数以及底层的网络接口配置方法, 就可以替换Docker原生的网络实现.
5. overlay: Docker原生的跨主机多子网网络方案. 只要通过使用linux bridge和vxlan隧道实现, 底层通过类似于etcd或者consul的KV存储系统实现多机的信息同步. overlay驱动当前还未正式发布, 但是开发者可以通过编译实验班的Docker来尝试使用, Docker实验班同事提供了额外的network和service指明了来进行灵活的网络操作, 不过, 需要内核版本大于等于3.16才正常使用(docker 1.8)

###  none
--net=none
仅有lo

### container: 
与运行中的容器共享Network Namespce, 共享相同网络视图.

如: 以默认网络配置(bridge模式)启动一个容器, 设置hostname为 dockerNet, dns 为8.8.8.8
```
docker run -h dockerNet --dns 8.8.8.8 -itd ubuntu:latest bash

ip addr show

```

### host
与主机共享Root Network Namespace, 容器有完整的权限操作主机的协议栈, ;路由表和防火墙等, 被认为是不安全的
--net=host


### birdge:
NAT网络模型
Docker Daemon启动时会在主机创建一个Linux网桥(,默认为docker0, 可通过-b参数手动指定). 容器启动时, Docker会创建一对veth pair(虚拟网络接口)设备. veth是成对存在一端进入的书会同时出现在另一端.Docker会将一端连接到docker0网桥上, 另一端放入容器的Network Namespace内, 从而实现容器与主机通信的目的.

`-t nat -A POSTROUTING -s 172.17.0.0/16 ! -0 docker0 -j MASQUERADE`

```
docker network create --driver bridge isolated_nw
docker network inspect isolated_nw
docker ls
```

### overlay


### 自定义网络
可以提供 bridge和 overlay network, macvlan network, 或者创建一个network plugin, 或者remote network


### docker_gwbridge 网络 
docker_gwbridge是本地网络网络，由Docker在两种不同的情况下自动创建：
1. 在初始化或者加入一个swarm时, Docker会创建一个, 并且使用他与其他的swarm的nodes之间进行联系, 在不同host之间
2. 当容器的网络都不能提供外部连接时，Docker将容器连接到docker_gwbridge网络以及容器的其他网络，以便容器可以连接到外部网络或其他群节点。

如果需要自定义配置，可以提前创建docker_gwbridge网络，否则Docker会根据需要创建它。以下示例使用一些自定义选项创建docker_gwbridge网络。
```
docker network create --subnet 172.30.0.0/16 \
                        --opt com.docker.network.bridge.name=docker_gwbridge \
            --opt com.docker.network.bridge.enable_icc=false \
            docker_gwbridge
```

##network相关的命令
docker network create
docker network connect
docker network ls
docker network rm
docker network disconnect
docker network inspect


docker network create
可以创建birdge和overlay网络
bridge 只能运行在本机, --subnet指定子网, 只能是一个
overlay可以跨主机运行
创建自定义网络时，可以向驱动程序传递其他选项。桥接驱动程序接受以下选项：

com.docker.network.bridge.name - 
com.docker.network.bridge.enable_ip_masquerade  --ip-masq
com.docker.network.bridge.enable_icc --icc
com.docker.network.bridge.host_binding_ipv4 --ip
com.docker.network.driver.mtu --mtu  也支持overlay

`docker network create -o "com.docker.network.bridge.host_binding_ipv4"="172.23.0.1" my-network`

**docker network connect**
使容器加入某个网络, 每一次加入一个网络, /etc/hosts都会改变
使用6个容器的实例

- 1.创建和运行两个容器, container1和container2
`docker run -itd --name container1 busybox`
`docker run -itd --name container2 busybox`

- 2.创建一个单独bridge网络
`docker network create -d bridge --subnet 172.25.0.0/16 isolated_nw`

- 3.container2加入isolated_nw网络, 然后验证这个连接.
```
docker network connect isolated_nw container2
docker network inspect isolated_nw
```
container2 分配了地址

- 4.启动第三个容器使用--ip来指定一个ip启动连接到isolated_nw网络
```
docker run  --network=isolated_nw --ip=172.25.3.3 -itd --name=container3 busybox

```

- 5.检查container3使用的网络资源。为了简洁，下面的输出被截断。
```
docker inspect --format='' container3
```

- 6.Inspect the network resources used by container2.
```
docker inspect --format='' container2 | python -m json.tool
```

- 7.进入container2测试网络
```
docker attach container2
sudo ifconfig -a
```

- 8.docker嵌入的dnsserver

ping container3 name
ping container1, ip
ctrl+p ctrl+q

- 9.目前，container2连接到bridge和isolated_nw网络，因此它可以与container1和container3通信。但是，container3和container1没有任何公共网络，因此它们无法通信。要验证此，请附加到container3并尝试通过IP地址ping container1。

- 10.创建container4可以连接到isolated_nw, 还可以连击刀container5(暂时不存在)
```
docker run --network=isolated_nw -itd --name=container4 --link container5:c5 busybox
```
这有点棘手，因为container5还不存在。创建container5时，container4将能够将名称c5解析为container5的IP地址。

> 使用旧链接创建的容器之间的任何链接本质上都是静态的，并将容器与别名进行硬绑定。它不容许链接的容器重新启动。用户定义网络中的新链接功能支持容器之间的动态链接，并且允许重新启动和链接容器中的IP地址更改

```
docker attach container4
ping container5
ping c5
```

- 11.创建container5并连接到container4, c4
```
docker run --network=isolated_nw -itd --name=container5 --link container4:c4 busybox

docker attach container4
 ping -w 4 c5
```

**网络别名作用域示例**

此外，如果容器属于多个网络，则给定链接的别名在给定网络内被限定。因此，容器可以链接到不同网络中的不同别名，并且别名不会用于不在同一网络上的容器。

- 1.创建另一个网络local_alias
`docker network create -d bridge --subnet 172.26.0.0./24 local_alias`

- 2.将container4和container5连接到 local_alias
```
docker network connect --link container5:foo local_alias container4
docker network connect --link container4:bar local_alias container5
```
- 3.在container4里ping container4使用的是foo, ping container5使用c5
- 4.从isolated_nw断开container5, 从container4中ping c5
```
docker network disconnect isolated_nw container5

docker attach container4
ping -w 4 c5
ping -w 4 foo

```

**限制docker网络**
虽然docker网络是建议的方式来控制您的容器使用的网络，但它确实有一些限制。
_环境变量注入_
环境变量注入本质上是静态的，并且在容器启动后不能更改环境变量。legacy --link标志将所有环境变量共享到链接的容器，但docker network命令没有等效项.当使用docker网络连接到网络时，容器之间不能动态地存在环境变量。。

*理解network-scoped alias*
传统链接提供了在配置别名的容器内隔离的流出名称解析。 Network-scoped aliases不允许这种单向隔离，但是为网络的所有成员提供别名。

- 1.创建container6 在isolated_nw且给的网络启用别名app
`docker run --network=isolated_nw -itd --name=container6 --network-alias app busybox`

- 2.登录container4, ping container6 和ping app, ip地址是一样的
- 3.把container6加入到local_alias网络中,且网络别名为scoped-app
`docker network connect --alias scoped-app local_alias container6`

- 4.在container4,container5(只在isolated_nw)上使用两个别名分别ping, 

这表明别名限定到定义它的网络，并且只有连接到该网络的容器才能访问别名。

### (将多个容器解析为单个别名)Resolving multiple containers to a single alias

多个容器可以在同一网络中共享同一个网络范围的别名。

- 1.启动一个container7在isolated_nw上, 且使用和container6一样的别名 app
`docker run --network=isolated_nw -itd --name=container7 --network-alias app busybox`
当多个容器被分享为同一个biemingshi,其中一个容器会被解析. 如果这个container不可用, 则另一个container被解析. 这在集群中提供了一种高可用性。

> 当IP地址解析时，选择解析它的容器是随机的。因此，在下面的练习中，您可能会在一些步骤中得到不同的结果。如果该步骤假定返回的结果是container6，但是你得到container7，这就是为什么。

- 2.启动一个持续ping app 在container4
```
docker attach container4
ping app
```
- 3.在另一个终端中停止container6
`docker stop container6`
在连接到container4的终端中，观察ping输出。它会在container6关闭时暂停，因为ping命令在首次调用IP时查找IP，并且该IP不再可访问。但是，ping命令默认情况下具有非常长的超时，因此不会发生错误。

- 4.run agin ping app
- 5.重启container6 docker start container6
- 6.重启ping

### Disconnecting containers
```
$ docker network disconnect isolated_nw container2

$ docker inspect --format=''  container2 | python -m json.tool
```
