# kubernetes 入门

## 组件

### Master 组件
集群的管理控制中星

ETCD: 是Kubernetes 提供默认的存储系统, 保存所有集群数据, 使用时需要为etcd 数据提供备份计划

* kube-controller-manager
  - 运行管理控制器, 他们是集群中处理常规任务的后台线程. 逻辑上, 每个控制器是一个单独的进程, 但是为了降低复杂性, 他们都会编译成单个二进制文件, 并在单个进程中运行
  - 这些控制器包括:
    * 节点(Node)控制器
    * 副本(Replication)控制器: 负责维护系统中每个副本中的pod
    * 端点(Endpoints) 控制器: 填充Endpoints 对象(即连接Services & Pods).
    * Servce Account 和 Token控制器: 为新的Namespace 创建默认账户访问API Token
* cloud-controller-manager: 云控制器负责与底层提供商的平台交互. 云控制器管理器是Kubernetes 版本1.6 引入的.
 - 云控制器管理器仅运行云提供商特定的(controller loops) 控制器循环. 可以通过 `--cloud-provider flag` 设置为external 启动kube-controller-manager, 来禁用控制器循环
 - 具体功能:
  * 节点(Node) 控制器
  * 路由 (Route) 控制器
  * Service控制器
  * 卷 (Volume) 控制器

* kube-scheduler: 见识新创建没有分配到Node的Pod, 为Pod 选择一个Node
* 插件 addons:
  - 插件 (addon) 是实现集群pod 和 service 功能的. Pod 由Deployment, ReplicationController等进行管理. Namespace 插接件对象是kube-system Namespace 中创建.
* DNS
  - 虽然不严格要求使用插件, 但是 Kubernetes 集群都应该具有集群DNS
  - 群集DNS 是一个DNS服务器, 能够为 Kubernetes Services 提供DNS记录
  - 由Kubernetes 启动的容器自动将这个DNS服务器包含在他们的DNS Searches 中

* 用户界面: kube-ui
* 容器资源监测
* CLuster-level Logging: 负责保存容器日志.

### 节点组件
节点组件运行咋iNode ,提供Kuberneters 运行时 环境, 以及维护Pod.

* kubelet: 是主要的节点代理, 它会见识已分配给节点的Pod, 具体功能:
  - 安装Pod 所需要的volumen
  - 下载Pod的Secrets
  - Pod 中运行Docker (rkt) 容器
  - 定期执行容器健康检查
  - Reports the status of the pod back to the rest of the system, by creating a mirror pod if necessary.
  - Reports the status of the node back to the rest of the system.
* kube-proxy 通过在主机上维护网络规则并执行连接转发来实现Kubernetes服务抽象
* docker|rkt
* fluentd: fluentd是一个守护进程，可提供cluster-level logging.。



## 1. create a cluster


minikube version
minikube start

kubectl version

### cluster detail

kubectl cluster-info

kubectl get nodes

## 2 using kubectl to create a deployment
kubectl get nodes
### deplpy our app

kubectl run kubernets-bootcamp --image=gcr.io/google-samples/kubernetes-bootcamp:v1 --port=8080
kubectl get deployments

view our app
kubctl proxy
```
export POD_NAME=$(kubectl get pods -o go-template --template '{{range.items}}{{.metadata.name}}{{"\n"}}{{end}}')
echo Name of the Pod: $POD_NAME
export POD_NAME=$(kubectl get pods -o go-template --template '{{range.items}}{{.metadata.name}}{{"\n"}}{{end}}')
echo Name of the P

curl http://localhost:8001/api/v1/namespaces/default/pods/$POD_NAME/proxy/
```

### viewing pods and nodes
1. check application configuration
kubectl get pods
kubectl describe pods

2. show the app in the terminial
kubectl proxy

export POD_NAME=$(kubectl get pods -o go-template --template '{{range.items}}{{.metadata.name}}{{"\n"}}{{end}}')echo Name of the Pod: $POD_NAME

3. view the container logs 
kubectl logs $POD_NAME

4, Executing command on the container
kubectl exec $POD_NAME env

kubectl exec -ti $POD_NAME bash
cat server.js

curl localhost:8080
exit

## using a service to expose your app

1, create a new service
kubectl get pods
kubectl get services
kubectl expose deployment/kubernets-bootcamp --type="NodePort" --port 8080
kubectl get services

kubectl describe services/kubernetes-bootcamp
export NODE_PORT=$(kubectl get services/kubernetes-bootcamp -o go-template='{{(index .spec.ports 0).nodePort}}')
echo NODE_PORT=$NODE_PORT

curl $(minikube ip):$NODE_PORT

2, using labels
kubectl describe deployment

kubectl get pods -l run=kubernetes-bootcamp
kubectl get services -l run=kubernets-bootcamp

export POD_NAME=$(kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}')
echo Name of the Pod: $POD_NAME

kubectl label pod $POD_NAME app=v1

kubectl describe pods $POD_NAME

kubectl get pods -l app=v1

3, deleting  a servcie
kubectl delete service -l run=kubernetes-bootcamp

kubectl get services
curl $(minikube ip):$NODE_PORT
kubectl exec -ti $POD_NAME curl localhost:8080

### running multiple instances of your app
kubectl get deployments
kubectl scale deployments/kubernetes-bootcamp --replicas=4
kubectl get deployments
kubectl get pods -o wide
kubecetl describe deployment/kubernetes-bootcamp 

2. load balancing
kubectl describe services/kubernets-bootcamp
export NODE_PORT=$(kubectl get service/kubernets-bootcamp -o go-template='{{(index .spec.ports 0).nodePort}}')
echo NODE_PORT=$NODE_PORT
curl $(minikube ip):$NODE_PORT

3, scale down

kubectl scale deployments/kubernetes-bootcamp --replicas=2
kubectl get deployments
kubectl get pods -o wide

## 6 performing a rolling update
1, update the version of the app
kubectl get deployments
kubectl get pods
kubectl describe pods
kubectl set image deployments/kubernetes-bootcamp kubernetes-bootcamp=jocatalin/kubernetes-bootcamp:v2
kubectl get pods
2, verify an update
kubectl describe services/kubernetes-bootcamp
export NODE_PORT=$(kubectl get services/kubernetes-bootcamp -o go-template='{{(index .spec.ports 0).nodePort}}')
echo NODE_PORT=$NODE_PORT

curl $(minikube ip):$NODE_PORT

kubectl rollout status deployments/kubernetes-bootcamp
kubectl describe pods

3, rollback an update
kubectl set image deployments/kubernetes-bootcamp kubernetes-bootcamp=gcr.io/google-samples/kubernetes-bootcamp:v10
kubectl get deployments
kubectl get pods
kubectl describe pods
kubectl rollout undo deployments/kubernetes-bootcamp
kubectl get pods
kubectl describe pods

20880


 minikube start --docker-env="HTTP_PROXY=http://192.168.8.104:1080 "--docker-env="HTTPS_PROXY=http://192.168.8.104:1080 "
 export no_proxy=$no_proxy,$(minikube ip)

  minikube start --docker-env="HTTP_PROXY=http://127.0.0.1:1080 "--docker-env="HTTPS_PROXY=http://127.0.0.1:1080 "
 export no_proxy=$no_proxy,$(minikube ip)


 minikube start --vm-driver=kvm2 --docker-env http_proxy=http://192.168.8.104:1080 --docker-env https_proxy=http://192.168.8.104:1080 --docker-env no_proxy=localhost,127.0.0.1,::1,192.168.0.0/16


 https://blog.frognew.com/2018/03/kubeadm-install-kubernetes-1.10.html

 kubeadmin init --kubernetes-version=v.10.0  --pod-network-cidr=10.244.0.0/16 \
  --apiserver-advertise-address=192.168.61.11    --ignore-preflight-errors=Swap



----


https://www.jianshu.com/p/9c7e1c957752

kubeadm init
```
kubeadm init --kubernetes-version=v1.10.4 --pod-network-cidr=10.244.0.0/16 

```


To start using your cluster, you need to run the following as a regular user:
```
  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config
  kubectl apply -f kube-flannel.yaml
```
You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

You can now join any number of machines by running the following on each node
as root:
nodes
```
kubeadm join 192.168.8.91:6443 --token nrt6xl.zlqdg2i65sz1bney --discovery-token-ca-cert-hash sha256:1551d4168f105127dcb88b1f0cc9b2a6cc2aa22c17e6afebd278ccb723a4650e

```


kubectl get pods --all-namespaces

nodes


failed to run Kubelet: cannot create certificate signing request: Unauthorized
