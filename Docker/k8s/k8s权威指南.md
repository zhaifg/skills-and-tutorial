# K8S 权威指南
---

Service:
   分布式集群的核心
   * 拥有一个唯一指定的名字.
   * 拥有一个虚拟IP(Cluster IP, Service IP 或VIP) 和端口
   * 能够提供某种远程服务能力
   * 被映射到了提供这种服务能力的一组容器应用上.
   
Service 的服务进程目前都是基于SOcket 通信方式对外提供服务.

## POD
Pod Ip
* Pod 运行在一个我们称之为节点(Node)的环境中, 这个节点既可以是物理机, 也可以是私有云或者公有云中虚拟机, 通常在一个节点运行几百个POD
* 每个Pod里运行着一个特殊的被称之为Pause 的容器, 其他的容器则为业务容器; 这些业务容器共享Pause 容器的网络栈和Volume挂载卷, 因此他们之间的通信和数据交换更为高效, 在设计是我们可以充分利用这一特性将一组密切相关的服务进程放到同一个Pod中;

## Master节点和工作节点
Master 运行着集群管理相关的一组进程:
* kube-apiserver
* kube-controller-manager
* kube-scheduler
* 这些进程实现了整个集群的资源管理, Pod调度, 弹性伸缩, 安全控制, 系统监控和纠错等管理, 并且都是全自动完成.

Node: 运行真正的应用程序, 最小运行单元是Pod
* kubeelet: 负责Pod对应的容器的创建,启停等任务, 同事与Master节点密切协作, 实现集群管理的基本功能.
* kube-proxy: 实现Kubernets Service 的通信与负载均衡机制的重要组件.
* Docker Engine: 负责本机的容器创建和管理工作

负责Pod的创建, 启动, 监控, 重启, 销毁, 以及实现软件模式的负载均衡器
