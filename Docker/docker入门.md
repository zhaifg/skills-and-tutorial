# Docker 入门
---

## 相关技术
go
cgroup
lxc
namespace
aufs
iptables
网络
firewalld
systemd
upstart
etcd
ip
brctl
编排
Flannel
CI/CD

docker machine
swarm
k8s
moess
google/cadvisor
https://github.com/google/cadvisor


Docker组件:
镜像image
容器 Container
仓库 Repository


镜像管理
容器管理
网络访问
镜像管理
存储


## docker 安装

`uname -r`: `3.10.0-229.el7.x86_64`


1. 使用epel
```
yum install docker-io

server docker-io start
```

2. 使用官方
```
tee /etc/yum.repos.d/docker.repo <<-'EOF'
[dockerrepo]
name=Docker Repository
baseurl=https://yum.dockerproject.org/repo/main/centos/7/
enabled=1
gpgcheck=1
gpgkey=https://yum.dockerproject.org/gpg
EOF

$ sudo yum install docker-engine

$ sudo systemctl enable docker.service

$ sudo systemctl start docker
```



## 简单的实例
### 1. 运行Hello World
```
docker run ubuntu /bin/echo "Hello World"
```
1. docker 运行一个容器
2. ubuntu 是要运行的image名称, 比如这个表示为ubuntu 的系统. 当指定一个image时, docker首先会搜索本地该名字的image, 如果没有则会在到DOcker Hub上寻找.
3. `/bin/echo "Hello World"` 会在新建的容器里运行.

### 2. 运行一个交互性容器
```
docker run -i -t ubuntu /bin/bash
```

`-i`: 
`-t`: 

### 3. 在后台运行一个容器
```
docker run -d -t -i ubuntu /bin/sh -c "while true;do hello world; sleep 1; done;"
1e5535038e285177d5214659a068137486f96ee5c2e85a4ac52dc83f2ebe4147 # container ID
```


## 镜像image

`docker search centos`: 从官方仓库里搜索名称有centos 的镜像
`docker pull centos` : 从官方仓库里拉取镜像
`docker images centos`: 查看本地镜像
`docker rmi centos`: 删除镜像
docker rmi


### 保存和加载镜像
1. 保存镜像 docker save
  `docker save -o ubuntu_14.04.tar ubuntu:14.04`

2. 加载镜像
  `docker load --input ubutun_14.04.tar` or
  `docker load < ubuntu_14.04.tar`


### 移除本地镜像
1. `docker -rmi training/sinatra`

> *注意：在删除镜像之前要先用 docker rm 删掉依赖于这个镜像的所有容器。

### 清理所有未打过标签的本地镜像
` sudo docker -rmi $(docker images -q -f "dangling=true")`

`-q`: --quit
`f`: --filter

## 镜像构建

### 手动构建

1. 使用现有的镜像进行修改
  1. 启动一个镜像
  `docker run -t -i centos /bin/bash`
  2. 在容器中安装一个程序,然后exit退出
  `yum install mysql-server`
  3. 使用docker commit提交变更为新副本
```
docker commit -m "install mysqld" -a "Docker ss" a82aa5362768 centos:v2
```
  其中，-m 来指定提交的说明信息，跟我们使用的版本控制工具一样；-a 可以指定更新的用户信息；之后是用来创建镜像的容器的 ID(a82aa5362768)；最后指定目标镜像的仓库名和 tag 信息。创建成功后会返回这个镜像的 ID 信息。

  4. 使用docker images 查看


### 使用Dockerfile创建镜像
类型:
1. 基础镜像信息
2. 维护者信息
3. 镜像操作指令
4. 容器启动时执行指令

手动安装nginx
`mkdir /opt/docker-file/nginx -pv`
`cd /opt/docker-file/nginx`

`vim Dockerfile`
```
# This is my first docker file
# Version 0.1
# Author:

# Base image
FROM centos
MAINTAINER zhaifengguo@gmail.com
ADD pcre-8.37.tar.gz /usr/local/src
ADD nginx-1.9.3.tar.gz /usr/local/src

RUN yum install -y wget gcc gcc-c++ make openssl-devel 
RUN useradd  -s /sbin/nologin -M www

WORKDIR /usr/local/src/nginx-1.9.3

RUN ./configure --prefix=....&& make && make install
RUN echo "daemon off;" >> /usr/local/nginx/conf/nginx.conf

VOLUME

EXPOSE 80

ENV PATH /usr/local/nginx/sbin:$PATH 

CMD ["nginx"]

```

`docker build -t nginx-file:v1 .`

#### 设置 tag 的方式
`docker tag image_id ... `

#### Image Digests
`docker images --digests | head`

### push an image to docker hub
```
docker push ourour/ssss
```

## 容器

简单的说，容器是独立运行的一个或一组应用，以及它们的运行态环境。对应的，虚拟机可以理解为模拟运行的一整套操作系统（提供了运行态环境和其他系统环境）和跑在上面的应用。

### 启动容器
1. 基于镜像新建一个容器并启动
2. 将在终止状态(stopped)的容器重新启动

#### 新建并启动(docker run)

- 1.下面的命令输入一个"Hello World", 之后终止容器
```
docker run ubuntu:14.04 /bin/echo "hello world"
```

- 2.启动一个bash终端, 用户可以交互
`docker run -it centos /bin/bash`

`-t`: Docker分配一个伪终端并绑定的容器的标准输入上
`-i`: 让容器的标准输入保持打开

当利用`docker run`来创建容器时, Docker在后台运行标准操作包括:
1. 检查本地是否存在指定的镜像, 不存在就从共有仓库下载
2. 利用镜像创建并启动一个容器
3. 分配一个文件系统, 并在只读的镜像层外面挂载一层可读写层
4. 从宿主主机配置的网桥接口中桥接一个虚拟接口到容器中去.
5. 从地址池配置一个IP地址给容器
6. 执行用户指定应用程序
7. 执行完毕容器被终止.

- 3.启动已被终止的容器(docker start)

### 后台运行(docker run -d)

容器是否长久运行与run的命令有关, 与-d参数没有关系
```
docker run -d nginx /bin/bash -c "while 1; do echo 'hello world'; sleep 1; done"

# 查看contianier
[root@mag ~]# docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
6348c99dca5b        nginx               "/bin/bash -c 'while "   2 minutes ago       Up 2 minutes        80/tcp, 443/tcp     hungry_wilson

# 查看log
docker logs 6348c99dca5b

# or
docker logs hungry_wilson
```


### 终止容器(docker stop)
当Docker容器中指定的应用终结时, 容器也自动终止. 或者用户通过`exit`和`ctrl + d` 退出终端时.


### 进入容器
在使用`-d`参数时, 容器启动后进入后台. 某些时候需要进入容器进行操作,  方法有
1. docker attch
2. nsenter工具等

#### attach命令
```
[root@mag ~]# docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
6348c99dca5b        nginx               "/bin/bash -c 'while "   7 minutes ago       Up 7 minutes        80/tcp, 443/tcp     hungry_wilson
9cfd194b99a9        nginx               "nginx -g 'daemon off"   21 hours ago        Up 21 hours         80/tcp, 443/tcp     mynginx
[root@mag ~]# 
[root@mag ~]# docker attch hungry_wilson
docker: 'attch' is not a docker command.
See 'docker --help'.
[root@mag ~]# docker attach hungry_wilson
hello world
hello world
hello world
^Chello world

```

> 使用attach命令有时候不方便, 当多个窗口同时attach到同一个容器的时候, 所有窗口都会同步显示. 当某个窗口因命令阻塞时, 其他窗口也无法执行操作了.

#### nesenter命令
安装:
工具在`util-linux`包

nsenter的可以方位另一个进程的命名空间. nsenter要正常要有root权限.

为了连接到容器, 需要找到容器的第一个进程的PID, 可以通过下面命令获取:
```
PID=$(docker inspect --format "{{ .State.Pid }}" <container>)
```

通过这个PID, 连接容器:
`nsenter --target $PID --mount --uts --ipc --net --pid`

总结成一个脚本命令:
```
#!/bin/bash
CNAME=$1
CPID=$(docker inspect --format "{{.State.Pid}}" $CNAME)
nsenter --target "$CPID"  --mount --uts --ipc --net --pid
```

#####  实例
`indocker` 是上面的脚本
```
[root@mag ~]# docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
9cfd194b99a9        nginx               "nginx -g 'daemon off"   21 hours ago        Up 21 hours         80/tcp, 443/tcp     mynginx

[root@mag ~]# indocker mynginx
root@9cfd194b99a9:/# ls
bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var

root@9cfd194b99a9:/# ip add show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default 
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
9: eth0@if10: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default 
    link/ether 02:42:ac:11:00:02 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.2/16 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:acff:fe11:2/64 scope link 
       valid_lft forever preferred_lft forever


```

更简单的，建议大家下载 .bashrc_docker，并将内容放到 .bashrc 中。
```
$ wget -P ~ https://github.com/yeasy/docker_practice/raw/master/_local/.bashrc_docker;
$ echo "[ -f ~/.bashrc_docker ] && . ~/.bashrc_docker" >> ~/.bashrc; source ~/.bashrc
```
这个文件中定义了很多方便使用 Docker 的命令，例如 docker-pid 可以获取某个容器的 PID；而 docker-enter 可以进入容器或直接在容器内执行命令。
```
$ echo $(docker-pid <container>)
$ docker-enter <container> ls
```

### 导出和导入容器

#### 导出 docker export


#### 导入 docker import
```
cat ubuntu.tar | docker imprt - test/ubuntu:v1.0
docker images
```

此外，也可以通过指定 URL 或者某个目录来导入，例如

`$sudo docker import http://example.com/exampleimage.tgz example/imagerepo`

>注：用户既可以使用 docker load 来导入镜像存储文件到本地镜像库，也可以使用 docker import 来导入一个容器快照到本地镜像库。这两者的区别在于容器快照文件将丢弃所有的历史记录和元数据信息（即仅保存容器当时的快照状态），而镜像存储文件将保存完整记录，体积也要大。此外，从容器快照文件导入时可以重新指定标签等元数据信息。

### 删除容器

可以使用 docker rm 来删除一个处于终止状态的容器。 例如
```
$sudo docker rm  trusting_newton
trusting_newton
```
如果要删除一个运行中的容器，可以添加 `-f `参数。Docker 会发送 SIGKILL 信号给容器。

#### 清理所有处于终止状态的容器

用 `docker ps -a` 命令可以查看所有已经创建的包括终止状态的容器，如果数量太多要一个个删除可能会很麻烦，用 `docker rm $(docker ps -a -q)` 可以全部清理掉。

>这个命令其实会试图删除所有的包括还在运行中的容器，不过就像上面提过的 docker rm 默认并不会删除运行中的容器。


## 仓库
仓库（Repository）是集中存放镜像的地方。

一个容易混淆的概念是注册服务器（Registry）。实际上注册服务器是管理仓库的具体服务器，每个服务器上可以有多个仓库，而每个仓库下面有多个镜像。从这方面来说，仓库可以被认为是一个具体的项目或目录。例如对于仓库地址 dl.dockerpool.com/ubuntu 来说，dl.dockerpool.com 是注册服务器地址，ubuntu 是仓库名。

```
docker search
docker pull

```

### 私有仓库

#### Docker方式
```
docker run -d -p 5000:5000 registry

dockerr run -d -p 5000:5000 -v /opt/data/registry:/tmp/registry registry
```

#### 
```
# ubuntu
sudo apt-get install -y build-essential python-dev libevent-dev python-pip limlzma-dev libssl-dev liblzma-dev libffi-dev

# centos
yum install python-devl libevent-devel python-pip gcc xz-devel


pip install docker-registry

cp config/config_sample.yml config/config.yml

gunicorn -c contrib/gunicorn.py docker_registry.wsgi:application

# or
gunicorn --acess-logifle - --error-logfile - -k gevent -b 0.0.0.0:5000 -w 4 --max-requests 100 docker_registry.wsgi:applicaiton

```

#### 上传下载
建好私有仓库之后, 就可以使用docker tag 来标记一个镜像, 然后推送它到仓库, 别的机器上的就可可以下载下来了. 如192.168.8.91:5000
```
docker tag ba58 192.168.8.91:5000/test
docker images

# push
docker push 192.168.8.91:5000/test

# curl http://192.168.8.91:5000/v1/search

docker pull 192.168.8.91:5000/test
```

#### 配置文件


## Docker数据管理
1. 数据卷(Data volumes)
2. 数据卷容器(Data volume containers)

### 数据卷
数据卷提供了持久性或共享数据的几个有用的功能:
1. 数据卷的初始化在container创建时进行. 如果container基础image包含了挂载点和数据, 那么已经存在的数据会初始化复制到新的数据卷中. 
2. 数据卷可以在容器之间共用.
3. 直接对数据进行更改
4. 更改image是不会对数据卷进行更改
5. 数据卷是独立存在, container删除与否不影响数据卷

#### 添加一个数据卷在容器中

`docker run -it --name volume-test1 -v /data nginx`
把宿主机的/data关在容器中,并且也是`/data`

使用一下命令可查看挂载
```
docker inspect -f {{.Volumes }} volume-test1
docker inspect container
```

#### 挂载主机的目录作为 数据卷
```
 docker run -d -P --name web -v /src/webapp:/webapp training/webapp python app.py 
```

`/src/webapp`: 是host 目录.
`/webapp`: 容器中目录, 如果容器中的这个目录已经挂载会被覆盖,而不是被删除.

挂载目录的名称是应该是 字母数据_-等_
`docker run -v c:\<path>:/c:\<container path>`

#### 挂载时指定权限
` docker run -d -P --name web -v /src/webapp:/webapp:ro training/webapp python app.py`

#### 挂载一个共享存储(ISCSI,NFS, FC)
docker plugin支持
使用共享卷的一个好处是它们是独立于主机的。这意味着，一个卷可以在任何主机上，一个容器开始，只要它有访问共享存储后端，并已安装插件。

通过docker run来使用volume 驱动. Volume驱动创建一个volumes命名name,来代替上面路径形式.

下面命令创建一个命名的volume, 为my-named-volume, 通过flocker 的volume 驱动, 使其在container激活.

```
docker run -d -P --volume-driver=flocker \
-v my-named-volume:/webpp --name web training/webapp python app.py
```

也可以使用`docker volume create`命令提前创建一个volume.
```
docker  volume create -d flocker -o size=10GB my-named-volume
docker run -d -P -v my-named-volume:/webapp --name web training/webapp python app.py
```

### 卷标 Volume Label

### 挂载一个host文件到数据卷
`docker run --rm -it -v ~/.bash_history:/root/.bash_history ubuntu /bin/bash`

>Note: Many tools used to edit files including vi and sed --in-place may result in an inode change. Since Docker v1.1.0, this will produce an error such as “sed: cannot rename ./sedKdJ9Dy: Device or resource busy”. In the case where you want to edit the mounted file, it is often easiest to instead mount the parent directory.

### 数据卷容器
`docker create -v /dbdata --name dbstore training/postgres /bin/true`

使用`--volumes-from` 挂载/dbdata 卷到另一个容器
`docker run -d --volumes-from dbstore --name db1 training/postgres`

另一个:
`$ docker run -d --volumes-from dbstore --name db2 training/postgres`


如果删除dbstore的volume, 后面的db1,db2则不会受影响. 如果从磁盘上删除, 必须在最后一台挂载的容器上,明确使用`docker rm -v`删除,.

### 备份,恢复和合并数据卷

#### 备份
```
docker run --rm --volumes-from dbstore -v $(pwd):/backup ubuntu tar cvf /backup/backup.tar /dbdata
```
这个命令是使用dbstore的数据卷新建了一个容器, 并且还挂载了一个本地目录到新建的 容器的/backup上; 最后通过tar命令把/dbdata 备份到了/backup/中的backup.tar文件.

#### 恢复
- 1.新建容器
`docker run -v /dbdata --name dbstore2 ubuntu /bin/bash`

- 2.挂载并恢复
`$ docker run --rm --volumes-from dbstore2 -v $(pwd):/backup ubuntu bash -c "cd /dbdata && tar xvf /backup/backup.tar --strip 1"`

### 删除卷
docker 数据卷在删除后还会存在在主机中. 可以创建匿名或者命名的数据卷. 命名的数据卷通过指定来自外部容器, 例如`awesome:/bar`. 匿名卷不会指定源目录.当容器删除时, 会用Docker引擎的来清理匿名卷.

`docker run --rm -v foo -v awesome:/bar busybox top`

### 使用共享卷的注意事项
当使用共享数据卷时, 多个容器对数据卷写会造成, 数据的破坏.





## Docker 网络管理

### 1. 使用 -P 指定一个宿主机的随机端口与container的端口对应
`docker run -P --name mynginx1 nginx`

### 2. 使用-p 91:80 指定1:1对应端口
```
docker run -d -p 91:80 --name mynginx2 nginx
# 91 是宿主机端口
# 80 是容器的端口

```

`docker port` 查看容器的端口对应情况
`docker port mynginx 5000`
```
[root@mag ~]# docker port mynginx1
443/tcp -> 0.0.0.0:32768
80/tcp -> 0.0.0.0:32769
[root@mag ~]# docker port mynginx1 443
0.0.0.0:32768

```

### docker network
```
[root@mag ~]# docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
10a0085d0d0d        bridge              bridge              local               
985c4c264919        host                host                local               
901fa9e0f07a        none                null                local   
```

```
docker run -itd --name=networktest ubuntu
```

```bash
[root@mag ~]# docker network inspect bridge
[
    {
        "Name": "bridge",
        "Id": "10a0085d0d0dc6117dd28fdcfd8472db8c1f434e2aebdd4a5b3ca24c474c442a",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "172.17.0.0/16"
                }
            ]
        },
        "Internal": false,
        "Containers": {
            "1709406be2e3d572a97ee767a5969c75c17a8f082b30bc165ed9a82fa0fbee29": {
                "Name": "mynginx1",
                "EndpointID": "5693d0e258dda0dec08a0c73b9cec3d7f21f720dae8011bfcda9c8c5addae3d6",
                "MacAddress": "02:42:ac:11:00:02",
                "IPv4Address": "172.17.0.2/16",
                "IPv6Address": ""
            }
        },
        "Options": {
            "com.docker.network.bridge.default_bridge": "true",
            "com.docker.network.bridge.enable_icc": "true",
            "com.docker.network.bridge.enable_ip_masquerade": "true",
            "com.docker.network.bridge.host_binding_ipv4": "0.0.0.0",
            "com.docker.network.bridge.name": "docker0",
            "com.docker.network.driver.mtu": "1500"
        },
        "Labels": {}
    }
]

```

### docker network disconnect bridge bridgename
端口bridgename 连接

### 创建桥接网络
```
docker network create -d bridge my-bridge-network 
$ docker network ls

NETWORK ID          NAME                DRIVER
7b369448dccb        bridge              bridge              
615d565d498c        my-bridge-network   bridge              
18a2866682b8        none                null                
c288470c46f6        host                host


docker network inspect my-bridge-network
```

### 添加容器到一个网络
`docker run -d --network=my-bridge-network --name db training/postgres`
```
$ docker inspect --format='{{json .NetworkSettings.Networks}}'  web


{"bridge":{"NetworkID":"7ea29fc1412292a2d7bba362f9253545fecdfa8ce9a6e37dd10ba8bee7129812",
"EndpointID":"508b170d56b2ac9e4ef86694b0a76a22dd3df1983404f7321da5649645bf7043","Gateway":"172.17.0.1","IPAddress":"172.17.0.2","IPPrefixLen":16,"IPv6Gateway":"","GlobalIPv6Address":"","GlobalIPv6PrefixLen":0,"MacAddress":"02:42:ac:11:00:02"}}
```



## 高级网络管理

### 快速配置指南
下面是一些与Docker网络有关的命令, 其中有些命令选项只有在Docker服务启动时才能配置, 而且不能马上生效.

`-b BRIDGE --bridge=BRIDGE` 指定容器挂载的网桥
`--bip=CIDR`: 定制所在的网桥的子网掩码
`-H SOCKET  --host=SOCKET`: Docker服务端接受命令的通道
`--icc=true| false` 是否支持容器之间的通信.
`--ip-forward=true| false` 
`--iptables=true|false` 是否允许Docker添加iptables规则
`--mtu=BYTES`

下面2个命令选项既可以在启动时服务时指定, 也可以Docker启动容器(docker run)时指定. 在Docker服务启动的时候会指定成为默认值, 后面的docker run可以覆盖默认值.
`--dns=IP`
`--dns-search=domain`

下面的命令只能在 docker run 时执行, 因为他是针对容器的特性内容.
`-h HOSTNAME --host=HOSTNAME` 配置容器主机名
`--link=CONTAINER_NAME:ALIAS` 添加到另一个容器的连接
`--net=bridge|none|container:NAME_or_ID|host` 配置容器的桥接模式
`-p SPEC --publish=SPEC` 映射容器端口到宿主主机
`-P --publish-all=true|false` 映射容器所有端口到宿主机


### 配置DNS
在容器中使用mount命令可以看到挂在信息:
```
mount

/dev/mapper/centos_kvm1-root on /run/secrets type xfs (rw,relatime,attr2,inode64,noquota)
/dev/mapper/centos_kvm1-root on /etc/resolv.conf type xfs (rw,relatime,attr2,inode64,noquota)
/dev/mapper/centos_kvm1-root on /etc/hostname type xfs (rw,relatime,attr2,inode64,noquota)
/dev/mapper/centos_kvm1-root on /etc/hosts type xfs (rw,relatime,attr2,inode64,noquota)
```

这种机制可以让宿主主机DNS信息发生变更后, 所有Docker容易的dns配置通过/etc/resolv.conf文件立刻得到更新.

使用手动指定容器的配置, 可以时可以使用如下:
`-h HOSTNAME --host=HOSTNAME` 设定容器主机名, 它会被写入容器内的/etc/hostname 和 /etc/hosts. 但他在容器外看不到, 既不会docker ps中显示, 也不会在其他容器中的/etc/hosts中看到.

`--link=CONTAINER_NAME:ALIAS`: 选项会在创建容器的时候, 添加一个其他的容器的主机名到/etc/hosts文件中, 让新容器的进程可以用主机名ALIAS就可以连接他.

`--dns=IP_ADDRESS` 添加 DNS 服务器到容器的 /etc/resolv.conf 中，让容
器用这个服务器来解析所有不在 /etc/hosts 中的主机名。


`--dns-search=DOMAIN` 设定容器的搜索域，当设定搜索域为 .example.com
时，在搜索一个名为 host 的主机时，DNS 不仅搜索host，还会搜索
host.example.com 。 注意：如果没有上述最后 2 个选项，Docker 会默认用主
机上的 /etc/resolv.conf 来配置容器。


### 容器的访问控制
容器的访问控制在Linux上主要由iptables防火墙进行管理和实现.

#### 容器访问外部网络
访问外部网络时需要在本地打开ip转发
```
net.ipv4.ip_forward = 1

sysctl -p
```
如果启动Docker服务时就设定 `--ip-forward=true`, Dokcer就会自动设定系统的 ip_forward = 1

#### 容器之间的访问
容器之间相互访问，需要两方面的支持:
1. 容器的网络拓扑是否已经互联。默认情况下，所有容器都会被连接到
docker0 网桥上。

2. 本地系统的防火墙软件 -- iptables 是否允许通过。

#### 访问所有端口
当Docker服务启动时,默认会添加一条转发策略到iptables的 FORWARD链上. 策略为ACCEPT还是DROP拒绝于配置--cc=true还是false. 当然, 手动指定 --iptables = false 则不会添加 iptables 规则.

此时, 系统中的 iptables 规则可能是类似:
```
iptables -nL
...
Chain FORWARD (policy ACCEPT)
target     prot opt source               destination
DROP       all  --  0.0.0.0/0            0.0.0.0/0
...
```
之后，启动容器（docker run ） 时使用 --link=CONTAINER_NAME:ALIAS 选
项。Docker 会在 iptable 中为 两个容器分别添加一条 ACCEPT 规则，允许相
互访问开放的端口（ 取决于 Dockerfile 中的 EXPOSE 行） 。
当添加了 `--link=CONTAINER_NAME:ALIAS` 选项后，添加了 iptables 规则。
```
$ sudo iptables -nL
...
Chain FORWARD (policy ACCEPT)
target     prot opt source               destination
ACCEPT     tcp  --  172.17.0.2           172.17.0.3           tcp spt:80
ACCEPT     tcp  --  172.17.0.3           172.17.0.2           tcp dpt:80
DROP       all  --  0.0.0.0/0            0.0.0.0/0
```

>注意: --link=CONTAINER_NAME:ALIAS 中的 CONTAINER_NAME 目前必须是 Docker 分配的名字，或使用 --name 参数指定的名字。主机名则不会被识别


### 端口映射

默认情况下，容器可以主动访问到外部网络的连接，但是外部网络无法访问到容器。

#### 容器访问外部实现

容器所有到外部网络的连接，源地址都会被NAT成本地系统的IP地址。这是使用 iptables 的源地址伪装操作实现的。

查看主机的 NAT 规则。
```
$ sudo iptables -t nat -nL
...
Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination
MASQUERADE  all  --  172.17.0.0/16       !172.17.0.0/16
...
```
其中，上述规则将所有源地址在 172.17.0.0/16 网段，目标地址为其他网段（外部网络）的流量动态伪装为从系统网卡发出。MASQUERADE 跟传统 SNAT 的好处是它能动态从网卡获取地址。

#### 外部访问容器实现

容器允许外部访问，可以在 docker run 时候通过 -p 或 -P 参数来启用。

不管用那种办法，其实也是在本地的 iptable 的 nat 表中添加相应的规则。

- 1 使用 -P 时：
```
$ iptables -t nat -nL
...
Chain DOCKER (2 references)
target     prot opt source               destination
DNAT       tcp  --  0.0.0.0/0            0.0.0.0/0            tcp dpt:49153 to:172.17.0.2:80
```
- 2.使用 -p 80:80 时：
```
$ iptables -t nat -nL
Chain DOCKER (2 references)
target     prot opt source               destination
DNAT       tcp  --  0.0.0.0/0            0.0.0.0/0            tcp dpt:80 to:172.17.0.2:80
```

>注意：
这里的规则映射了 0.0.0.0，意味着将接受主机来自所有接口的流量。用户可以通过 -p IP:host_port:container_port 或 -p IP::port 来指定允许访问容器的主机上的 IP、接口等，以制定更严格的规则。
如果希望永久绑定到某个固定的 IP 地址，可以在 Docker 配置文件 /etc/default/docker 中指定 DOCKER_OPTS="--ip=IP_ADDRESS"，之后重启 Docker 服务即可生效。

### 网桥配置和自定义网桥
#### 网桥的配置
默认的情况下, Docker安装完成后会有一个docker0的网桥, 他在内核层联通了其他的物理或者虚拟网卡, 这就将所有容器和本地主机放到了同一个物理网络.

Docker 默认指定了 docker0 接口 的 IP 地址和子网掩码，让主机和容器之间可以通过网桥相互通信，它还给出了 MTU（接口允许接收的最大传输单元），通常是 1500 Bytes，或宿主主机网络路由上支持的默认值。这些值都可以在服务启动的时候进行配置。

`--bip=CIDR` -- IP 地址加掩码格式，例如 192.168.1.5/24
`--mtu=BYTES` -- 覆盖默认的 Docker mtu 配置

也可以在配置文件中配置 DOCKER_OPTS，然后重启服务。 由于目前 Docker 网桥是 Linux 网桥，用户可以使用 brctl show 来查看网桥和端口连接信息。

#### 自定义网桥
除了默认的 docker0 网桥, 用户也可以指定网桥来连接各个容器

在启动 Docker 服务的时候，使用 -b BRIDGE或--bridge=BRIDGE 来指定使用的网桥。

- 1.如果服务已经运行，那需要先停止服务，并删除旧的网桥。
```
$ sudo service docker stop
$ sudo ip link set dev docker0 down
$ sudo brctl delbr docker0
```
- 2.然后创建一个网桥 bridge0。
```
$ sudo brctl addbr bridge0
$ sudo ip addr add 192.168.5.1/24 dev bridge0
$ sudo ip link set dev bridge0 up
```

- 3.查看确认网桥创建并启动。
```
$ ip addr show bridge0
4: bridge0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state UP group default
    link/ether 66:38:d0:0d:76:18 brd ff:ff:ff:ff:ff:ff
    inet 192.168.5.1/24 scope global bridge0
       valid_lft forever preferred_lft forever
```

- 4.配置 Docker 服务，默认桥接到创建的网桥上。
```
$ echo 'DOCKER_OPTS="-b=bridge0"' >> /etc/default/docker
$ sudo service docker start
```

- 5.启动 Docker 服务。 新建一个容器，可以看到它已经桥接到了 bridge0 上。


可以继续用 brctl show 命令查看桥接的信息。另外，在容器中可以使用 ip addr 和 ip route 命令来查看 IP 地址配置和路由信息。

### 工具和示例


在介绍自定义网络拓扑之前，你可能会对一些外部工具和例子感兴趣：

[pipework](https://github.com/jpetazzo/pipework)

Jérôme Petazzoni 编写了一个叫 pipework 的 shell 脚本，可以帮助用户在比较复杂的场景中完成容器的连接。

[playground](https://github.com/brandon-rhodes/fopnp/tree/m/playground)

Brandon Rhodes 创建了一个提供完整的 Docker 容器网络拓扑管理的 Python库，包括路由、NAT 防火墙；以及一些提供 HTTP, SMTP, POP, IMAP, Telnet, SSH, FTP 的服务器。


Docker 1.2.0 开始支持在运行中的容器里编辑 /etc/hosts, /etc/hostname 和 /etc/resolve.conf 文件。

但是这些修改是临时的，只在运行的容器中保留，容器终止或重启后并不会被保存下来。也不会被 docker commit 提交。

### 示例 创建一个点到点的连接

默认情况下，Docker 会将所有容器连接到由 docker0 提供的虚拟子网中。
用户有时候需要两个容器之间可以直连通信，而不用通过主机网桥进行桥接。
解决办法很简单：
创建一对 peer 接口，分别放到两个容器中，配置成点到点链
路类型即可。

- 1.首先启动 2 个容器：
```bash
$ sudo docker run -i -t --rm --net=none base /bin/bash
root@1f1f4c1f931a:/#
$ sudo docker run -i -t --rm --net=none base /bin/bash
root@12e343489d2f:/#
```

- 2.找到进程号，然后创建网络名字空间的跟踪文件。
```bash
$ sudo docker inspect -f '{{.State.Pid}}' 1f1f4c1f931a
2989
$ sudo docker inspect -f '{{.State.Pid}}' 12e343489d2f
3004
$ sudo mkdir -p /var/run/netns
$ sudo ln -s /proc/2989/ns/net /var/run/netns/2989
$ sudo ln -s /proc/3004/ns/net /var/run/netns/3004
```
- 3.创建一对 peer 接口，然后配置路由
```bash
$ sudo ip link add A type veth peer name B
$ sudo ip link set A netns 2989
$ sudo ip netns exec 2989 ip addr add 10.1.1.1/32 dev A
$ sudo ip netns exec 2989 ip link set A up
$ sudo ip netns exec 2989 ip route add 10.1.1.2/32 dev A
$ sudo ip link set B netns 3004
$ sudo ip netns exec 3004 ip addr add 10.1.1.2/32 dev B
$ sudo ip netns exec 3004 ip link set B up
$ sudo ip netns exec 3004 ip route add 10.1.1.1/32 dev B
```

现在这 2 个容器就可以相互 ping 通，并成功建立连接。点到点链路不需要子网和
子网掩码。

此外，也可以不指定 --net=none 来创建点到点链路。这样容器还可以通过原先
的网络来通信。

利用类似的办法，可以创建一个只跟主机通信的容器。但是一般情况下，更推荐使
用 --icc=false 来关闭容器之间的通信。

```
sudo mkdir -p /var/run/netns
$ sudo ln -s /proc/$pid/ns/net /var/run/netns/$pid


ip addr show docker0

$ sudo ip link add A type veth peer name B
$ sudo brctl addif docker0 A
$ sudo ip link set A up

ip link set B netns $pid
ip netns exec $pid ip link set dev B name eth0
ip netns exec $pid ip link set eth0 up
ip netns exec $pid ip addr add 172.17.42.99/16 dev eth0
ip netns exec $pid ip route add default via 172.17.42.1
```


## 常用命令
### `docker ps`: 查看 containers

### `docker logs`: 查看container的stdout

```
[root@mag ~]# docker logs -f mynginx1   # 类似 tail -f
172.17.0.1 - - [27/Oct/2016:08:02:36 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.29.0" "-"
192.168.8.102 - - [01/Nov/2016:06:03:32 +0000] "GET / HTTP/1.1" 200 612 "-" "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36" "-"
192.168.8.102 - - [01/Nov/2016:06:03:32 +0000] "GET /favicon.ico HTTP/1.1" 404 571 "http://192.168.8.85:32769/" "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36" "-"
2016/11/01 06:03:32 [error] 5#5: *2 open() "/usr/share/nginx/html/favicon.ico" failed (2: No such file or directory), client: 192.168.8.102, server: localhost, request: "GET /favicon.ico HTTP/1.1", host: "192.168.8.85:32769", referrer: "http://192.168.8.85:32769/"
```

### `docker inspect `:  检查容器

```
[root@mag ~]# docker inspect mynginx1
[
    {
        "Id": "1709406be2e3d572a97ee767a5969c75c17a8f082b30bc165ed9a82fa0fbee29",
        "Created": "2016-10-27T08:00:26.813372295Z",
        "Path": "nginx",
        "Args": [
            "-g",
            "daemon off;"
        ],
        "State": {
            "Status": "running",
            "Running": true,
            "Paused": false,
            "Restarting": false,
            "OOMKilled": false,
            "Dead": false,
            "Pid": 4866,
            "ExitCode": 0,
            "Error": "",
            "StartedAt": "2016-10-27T08:00:27.488219601Z",
            "FinishedAt": "0001-01-01T00:00:00Z"
        },
        "Image": "sha256:e43d811ce2f4986aa69bc8ba6c92f0789537f604d1601e0b6ec024e1c38062b4",
        "ResolvConfPath": "/var/lib/docker/containers/1709406be2e3d572a97ee767a5969c75c17a8f082b30bc165ed9a82fa0fbee29/resolv.conf",
        "HostnamePath": "/var/lib/docker/containers/1709406be2e3d572a97ee767a5969c75c17a8f082b30bc165ed9a82fa0fbee29/hostname",
        "HostsPath": "/var/lib/docker/containers/1709406be2e3d572a97ee767a5969c75c17a8f082b30bc165ed9a82fa0fbee29/hosts",
        "LogPath": "/var/lib/docker/containers/1709406be2e3d572a97ee767a5969c75c17a8f082b30bc165ed9a82fa0fbee29/1709406be2e3d572a97ee767a5969c75c17a8f082b30bc165ed9a82fa0fbee29-json.log",
        "Name": "/mynginx1",
        "RestartCount": 0,
        "Driver": "devicemapper",
        "MountLabel": "",
        "ProcessLabel": "",
        "AppArmorProfile": "",
        "ExecIDs": null,
        "HostConfig": {
            "Binds": null,
            "ContainerIDFile": "",
            "LogConfig": {
                "Type": "json-file",
                "Config": {}
            },
            "NetworkMode": "default",
            "PortBindings": {},
            "RestartPolicy": {
                "Name": "no",
                "MaximumRetryCount": 0
            },
            "AutoRemove": false,
            "VolumeDriver": "",
            "VolumesFrom": null,
            "CapAdd": null,
            "CapDrop": null,
            "Dns": [],
            "DnsOptions": [],
            "DnsSearch": [],
            "ExtraHosts": null,
            "GroupAdd": null,
            "IpcMode": "",
            "Cgroup": "",
            "Links": null,
            "OomScoreAdj": 0,
            "PidMode": "",
            "Privileged": false,
            "PublishAllPorts": true,
            "ReadonlyRootfs": false,
            "SecurityOpt": null,
            "UTSMode": "",
            "UsernsMode": "",
            "ShmSize": 67108864,
            "Runtime": "runc",
            "ConsoleSize": [
                0,
                0
            ],
            "Isolation": "",
            "CpuShares": 0,
            "Memory": 0,
            "CgroupParent": "",
            "BlkioWeight": 0,
            "BlkioWeightDevice": null,
            "BlkioDeviceReadBps": null,
            "BlkioDeviceWriteBps": null,
            "BlkioDeviceReadIOps": null,
            "BlkioDeviceWriteIOps": null,
            "CpuPeriod": 0,
            "CpuQuota": 0,
            "CpusetCpus": "",
            "CpusetMems": "",
            "Devices": [],
            "DiskQuota": 0,
            "KernelMemory": 0,
            "MemoryReservation": 0,
            "MemorySwap": 0,
            "MemorySwappiness": -1,
            "OomKillDisable": false,
            "PidsLimit": 0,
            "Ulimits": null,
            "CpuCount": 0,
            "CpuPercent": 0,
            "IOMaximumIOps": 0,
            "IOMaximumBandwidth": 0
        },
        "GraphDriver": {
            "Name": "devicemapper",
            "Data": {
                "DeviceId": "13",
                "DeviceName": "docker-253:0-36087184-37ed41006d01a29e66735412ce1a2d9ba44ea1c0f55c22caaef693e73e4a9b48",
                "DeviceSize": "10737418240"
            }
        },
        "Mounts": [],
        "Config": {
            "Hostname": "1709406be2e3",
            "Domainname": "",
            "User": "",
            "AttachStdin": false,
            "AttachStdout": false,
            "AttachStderr": false,
            "ExposedPorts": {
                "443/tcp": {},
                "80/tcp": {}
            },
            "Tty": false,
            "OpenStdin": false,
            "StdinOnce": false,
            "Env": [
                "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                "NGINX_VERSION=1.11.5-1~jessie"
            ],
            "Cmd": [
                "nginx",
                "-g",
                "daemon off;"
            ],
            "Image": "nginx",
            "Volumes": null,
            "WorkingDir": "",
            "Entrypoint": null,
            "OnBuild": null,
            "Labels": {}
        },
        "NetworkSettings": {
            "Bridge": "",
            "SandboxID": "da5ab748b396abd1ad3ed35b5dc7489aa3d8e160c0f460c2413011bfed17ac8c",
            "HairpinMode": false,
            "LinkLocalIPv6Address": "",
            "LinkLocalIPv6PrefixLen": 0,
            "Ports": {
                "443/tcp": [
                    {
                        "HostIp": "0.0.0.0",
                        "HostPort": "32768"
                    }
                ],
                "80/tcp": [
                    {
                        "HostIp": "0.0.0.0",
                        "HostPort": "32769"
                    }
                ]
            },
            "SandboxKey": "/var/run/docker/netns/da5ab748b396",
            "SecondaryIPAddresses": null,
            "SecondaryIPv6Addresses": null,
            "EndpointID": "5693d0e258dda0dec08a0c73b9cec3d7f21f720dae8011bfcda9c8c5addae3d6",
            "Gateway": "172.17.0.1",
            "GlobalIPv6Address": "",
            "GlobalIPv6PrefixLen": 0,
            "IPAddress": "172.17.0.2",
            "IPPrefixLen": 16,
            "IPv6Gateway": "",
            "MacAddress": "02:42:ac:11:00:02",
            "Networks": {
                "bridge": {
                    "IPAMConfig": null,
                    "Links": null,
                    "Aliases": null,
                    "NetworkID": "10a0085d0d0dc6117dd28fdcfd8472db8c1f434e2aebdd4a5b3ca24c474c442a",
                    "EndpointID": "5693d0e258dda0dec08a0c73b9cec3d7f21f720dae8011bfcda9c8c5addae3d6",
                    "Gateway": "172.17.0.1",
                    "IPAddress": "172.17.0.2",
                    "IPPrefixLen": 16,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "MacAddress": "02:42:ac:11:00:02"
                }
            }
        }
    }
]

```

```
 docker inspect  -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'   mynginx1
172.17.0.2

```
docker ps -a

docker run  --name test1  centos /bin/bash
docker run -d --name test1  centos /bin/bash


## Docker监控

## Docker中的日志处理

## docker machine
```
sudo http_proxy=http://localhost:8123 "curl -L https://github.com/docker/machine/releases/download/v0.9.0-rc2/docker-machine-`uname -s`-`uname -m` >/tmp/docker-machine && chmod +x /tmp/docker-machine && sudo cp /tmp/docker-machine /usr/local/bin/docker-machine"
```

## Docker的服务的管理
`dockerd`
### 配置Docker守护进程
```

Flag                Description
-D, --debug=false   Enable or disable debug mode. By default, this is false.
-H,--host=[]        Daemon socket(s) to connect to.
--tls=false         Enable or disable TLS. By default, this is false.
```

`dockerd -D --tls=true --tlscert=/var/docker/server.pem --tlskey=/var/docker/serverkey.pem -H tcp://192.168.59.3:2376`


### ubuntu
从14.04使用upstart, 会查找`/etc/init/`, so ` /etc/init/docker.conf.`
15.04使用systemd, `/etc/default/docker`
通过制定变量`DOCKER_OPTS`.

`DOCKER_OPTS="-D --tls=true --tlscert=/var/docker/server.pem --tlskey=/var/docker/serverkey.pem -H tcp://192.168.59.3:2376"`

### CentOS
`systemctl status docker`
1. 使用具有root权限的用户登录
2. 创建`/etc/systemd/system/docker.service.d` 目录.
  `sudo mkdir /etc/systemd/system/docker.service.d`
3. 创建`/etc/systemd/system/docker.service.d/docker.conf`文件
  `sudo vi /etc/systemd/system/docker.service.d/docker.conf`
4. 覆盖ExecStart配置在上面文件中,用来定制docker守护进程. 设置环境变量文件
```
vi /etc/sysconfig/docker
OPTIONS='-H tcp://0.0.0.0:4243 -H unix:///var/run/docker.sock'
```
```
[Service]
EnvironmentFile=-/etc/sysconfig/docker
EnvironmentFile=-/etc/sysconfig/docker-storage
EnvironmentFile=-/etc/sysconfig/docker-network
ExecStart=
ExecStart=/usr/bin/dockerd $OPTIONS \
          $DOCKER_STORAGE_OPTIONS \
          $DOCKER_NETWORK_OPTIONS \
          $BLOCK_REGISTRY \
          $INSECURE_REGISTRY376
```
  选项:
    * 启用 -D debug模式
    * 设置tls为true用证书来连接
    * 监听在192.168.59.3:2376
5. 保存
6. 同步配置文件
  `sudo systemctl daemon-reload`
7. 重启docker进程
  `sudo systemctl restart docker`
8. 验证docker运行情况

9. 查看日志
`sudo journalctl -u docker`


### 使用systemd管理docker

- 启动docker
`sudo systemctl start docker`
`sudo service docker start`

`sudo systemctl enable docker| sudo chkconfig docker on`

- 定制docker守护进程的参数
有很多方法可以为您的Docker守护进程配置守护进程标志和环境变量。
推荐方式通过在systemd中添加配置文件, 在目录`/etc/systemd/system/docker.service.d `命名为<something>.conf.
这也可以是`/etc/systemd/system/docker.service`，它也可以覆盖`/lib/systemd/system/docker.service`的默认值。

但是，如果以前使用过具有EnvironmentFile（通常指向`/etc/sysconfig/docker`）的程序包，则为了向后兼容性，请将具有.conf扩展名的文件放入`/etc/systemd/system/docker.service.d`目录包括以下内容：
```
[Service]
EnvironmentFile=-/etc/sysconfig/docker
EnvironmentFile=-/etc/sysconfig/docker-storage
EnvironmentFile=-/etc/sysconfig/docker-network
ExecStart=
ExecStart=/usr/bin/dockerd $OPTIONS \
          $DOCKER_STORAGE_OPTIONS \
          $DOCKER_NETWORK_OPTIONS \
          $BLOCK_REGISTRY \
          $INSECURE_REGISTRY
```

如果是用了EnvironmentFile, 则要检查配置
`systemctl show docker | grep EnvironmentFile`
`EnvironmentFile=-/etc/sysconfig/docker (ignore_errors=yes)`

或者, 找到服务文件所在的位置：
```
$ systemctl show --property=FragmentPath docker

FragmentPath=/usr/lib/systemd/system/docker.service

$ grep EnvironmentFile /usr/lib/systemd/system/docker.service

EnvironmentFile=-/etc/sysconfig/docker
```

您可以使用覆盖文件定制Docker守护程序选项，如下面的HTTP代理示例中所述。位于`/usr/lib/systemd/system`或`/lib/systemd/system`中的文件包含默认选项，不应进行编辑。

### 运行时目录和存储驱动程序
您可能希望通过将Docker镜像，容器和卷移动到单独的分区来控制用于Docker镜像，容器和卷的磁盘空间。在这个例子中，我们假设你的docker.service文件看起来像：
```
[Unit]
Description=Docker Application Container Engine
Documentation=https://docs.docker.com
After=network.target

[Service]
Type=notify
# the default is not to use systemd for cgroups because the delegate issues still
# exists and systemd currently does not support the cgroup feature set required
# for containers run by docker
ExecStart=/usr/bin/dockerd
ExecReload=/bin/kill -s HUP $MAINPID
# Having non-zero Limit*s causes performance problems due to accounting overhead
# in the kernel. We recommend using cgroups to do container-local accounting.
LimitNOFILE=infinity
LimitNPROC=infinity
LimitCORE=infinity
# Uncomment TasksMax if your systemd version supports it.
# Only systemd 226 and above support this version.
#TasksMax=infinity
TimeoutStartSec=0
# set delegate yes so that systemd does not reset the cgroups of docker containers
Delegate=yes
# kill only the docker process, not all processes in the cgroup
KillMode=process

[Install]
WantedBy=multi-user.target
```

这将允许我们通过放置文件（如上所述）通过在`/etc/systemd/system/docker.service.d`目录中放置一个包含以下内容的文件来添加额外的标志：
```
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd --graph="/mnt/docker-data" --storage-driver=overlay
```
您还可以在此文件中设置其他环境变量，例如，下面描述的HTTP_PROXY环境变量。要修改ExecStart配置，请指定空配置，然后指定新配置，如下所示：

```
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd --bip=172.17.42.1/16
```
如果无法指定空配置，Docker会报告错误，如：
`docker.service has more than one ExecStart= setting, which is only allowed for Type=oneshot services. Refusing.`

### HTTP proxy
此示例覆盖默认的docker.service文件。如果您在HTTP代理服务器后面，例如在公司设置中，您将需要在Docker systemd服务文件中添加此配置。

1. Create a systemd drop-in directory for the docker service:
`$ mkdir /etc/systemd/system/docker.service.d`
2. Create a file called /etc/systemd/system/docker.service.d/http-proxy.conf that adds the HTTP_PROXY environment variable:
```
[Service]
Environment="HTTP_PROXY=http://proxy.example.com:80/"
```
3. If you have internal Docker registries that you need to contact without proxying you can specify them via the NO_PROXY environment variable:
```
Environment="HTTP_PROXY=http://proxy.example.com:80/" "NO_PROXY=localhost,127.0.0.1,docker-registry.somecorporation.com"
```
4. Flush changes:
`$ sudo systemctl daemon-reload`
5. Verify that the configuration has been loaded:
```
$ systemctl show --property=Environment docker
Environment=HTTP_PROXY=http://proxy.example.com:80/
```
6. Restart Docker:
`$ sudo systemctl restart docker`
