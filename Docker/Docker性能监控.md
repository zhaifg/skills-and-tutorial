# Docker性能监控
---

容器的监控与传统的监控不同, 容器是动态的, 生命周期短, 特别是在微服务的分布式架构下, 容器个数, IP地址随时可能变化. 如果采取传统监控的方案, 则会增加监控的复杂度. 

## 常用的监控工具

### Docker stats
默认的情况下的Docker的性能监控是:`docker stats`
`docker stats contianer1 container2 ...`

```
docker stats
CONTAINER           CPU %               MEM USAGE / LIMIT       MEM %               NET I/O               BLOCK I/O           PIDS
1e3993b07ea8        0.04%               832 KiB / 1.789 GiB     0.04%               1.089 MB / 59.44 MB   1.565 MB / 0 B      1
95116c66a919        105.37%             196.3 MiB / 1.789 GiB   10.72%              476 MB / 464.1 MB     0 B / 12.32 MB      4
abc8c6eaa69b        0.00%               34.33 MiB / 1.789 GiB   1.87%               342.6 MB / 423.3 MB   42 MB / 117.1 MB    6
5e1011c4ee0c        0.07%               9.691 MiB / 1.789 GiB   0.53%               143.8 MB / 52.67 MB   7.499 MB / 0 B      3

```
`CONTAINER`: 容器名称
`CPU%`: 使用CPU百分比
`MEM USAGE / LIMIT`:
`MEM%`:
`NET I/O `: 网络接收和发送
`BLOCK I/O`: 硬盘的接受和发送
`PIDS`: 

### cAdvisor
是一款图形化的监控页面, 而且，与本文中的其他的工具不一样的是CAdvisor是免费的，并且还开源。另外，它的资源消耗也比较低。但是，它有它的局限性，它只能监控一个Docker主机。因此，如果你是多节点的话，那就比较麻烦了，你得在所有的主机上都安装一个CAdvisor，者肯定特别不方便。值得注意的是，如果你使用的是Kubernetes，你可以使用heapster来监控多节点集群。另外，在图表中的数据仅仅是时长一分钟的移动窗口，并没有方法来查看长期趋势。如果资源使用率在危险水平，它却没有生成警告的机制。如果在Docker节点的资源消耗方面，你没有任何可视化界面，那么CAdvisor是一个不错的开端来带你步入容器监控，然而如果你打算在你的容器中运行任何关键任务，那你就需要一个更强大的工具或者方法。

```
docker run                                      \
--volume=/:/rootfs:ro                         \
--volume=/var/run:/var/run:rw                 \
--volume=/sys:/sys:ro                         \
--volume=/var/lib/docker/:/var/lib/docker:ro  \
--publish=8080:8080                           \
--detach=true                                 \
--name=cadvisor                               \
google/cadvisor:latest
```

### Scout(第三方)

### Data Dog(第三方)

### Sensu Monitoring Framework

### 监控宝等

## 多机监控

###  cAdvisor+ Influxdb+grafana
可以在每台主机上运行一个cAdvisor容器负责数据采集，再将采集后的数据都存到时序型数据库influxdb中，再通过图形展示工具grafana定制展示面板

### Kubernetes上容器的监控
在Kubernetes的新版本中已经集成了cAdvisor，所以在Kubernetes架构下，不需要单独再去安装cAdvisor，可以直接使用节点的IP加默认端口4194就可以直接访问cAdvisor的监控面板。而Kubernetes还提供一个叫heapster的组件用于聚合每个node上cAdvisor采集的数据，再通过Kubedash进行展示

### Prometheus 




http://dockone.io/article/1643
http://dockone.io/article/2040

http://dockone.io/article/171
