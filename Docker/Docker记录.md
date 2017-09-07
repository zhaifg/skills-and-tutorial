# Docker 记录
---

## Docker swarm
Docker Swarm独立版：
用于创建Docker主机(运行Docker守护进程的服务器)集群工具.
> 这是旧的版本, docker 1.12以后, 使用swarm mode

## swarmkit
Docker集群管理和容器编排工具SwarmKit，其主要功能包括节点发现、基于raft算法的一致性和任务调度等

## Docker swarm mode
Docker Engine 1.12及后续版本集成了Swarmkit编排服务, 即Swarm Mode. 他将服务对象引入到Docker中, 提供了swarm集群管理的原生支持并实现了scaling,rolling update, service discovery, load balance, routing mesh等.。

```
docker swarm init --advertise-addr 192.168.8.91
```

```
[root@docker_001 ~]# docker swarm init --advertise-addr 192.168.8.91
Swarm initialized: current node (3rsvbcoacj39rjxymgttl8j43) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-2y4klyhrv78k9wqi4cua4hio7kvqinc9tcssnyxbgudz174vpy-4ic0yk2haz79c9rwtz478vrms \
    192.168.8.91:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
```

```
    docker swarm join \
    --token SWMTKN-1-2y4klyhrv78k9wqi4cua4hio7kvqinc9tcssnyxbgudz174vpy-4ic0yk2haz79c9rwtz478vrms \
    192.168.8.91:2377

```

### deploy a service
```
docker service create --replicas 1 --name helloworld alpine ping docker.com

[root@docker_001 ~]# docker service ls
ID            NAME        REPLICAS  IMAGE   COMMAND
6lf4p6xdntjx  helloworld  1/1       alpine  ping docker.com

docker service inspect --pretty helloworld


[root@docker_001 ~]# docker service ps helloworld
ID                         NAME              IMAGE   NODE        DESIRED STATE  CURRENT STATE            ERROR
73hcyn8ysvb70s8du5cpb7y1h  helloworld.1      alpine  docker_003  Running        Preparing 5 seconds ago  
ba7wsr9bm2zxyyerz04yalsg8   \_ helloworld.1  alpine  docker_001  Shutdown       Failed 6 seconds ago     "task: non-zero exit (1)"


# 横向扩展container为5个
[root@docker_001 ~]# docker service scale helloworld=5
helloworld scaled to 5

[root@docker_001 ~]# docker service ps helloworld
ID                         NAME              IMAGE   NODE        DESIRED STATE  CURRENT STATE               ERROR
73hcyn8ysvb70s8du5cpb7y1h  helloworld.1      alpine  docker_003  Running        Running about a minute ago  
ba7wsr9bm2zxyyerz04yalsg8   \_ helloworld.1  alpine  docker_001  Shutdown       Failed about a minute ago   "task: non-zero exit (1)"
9oz72m16lr81cm44tc3fcqn4c  helloworld.2      alpine  docker_001  Running        Running 3 seconds ago       
b061fk1a1u2nk5xt7w4r19sdg  helloworld.3      alpine  docker_002  Running        Running 2 seconds ago       
09eg7r7pwewmtjuw3m58eb583  helloworld.4      alpine  docker_002  Running        Running 2 seconds ago       
7ddpv2jtci35mbl26steu5tmp  helloworld.5      alpine  docker_003  Running        Preparing 7 seconds ago  

# 删除 swarm 服务
docker service rm helloworld
docker service inspect helloworld
docker ps
```

使用滚动更新一个服务,

1. 登录Docker swarm 管理端
2. 部署 redis 3.0.6 服务在swarm里, 使用10秒的延迟更新集群.
```
docker service create --replicas 3 --name redis --update-delay 10s redis:3.0.6
```
`--update-delay`: 配置进集群的延迟时间,
  - `-s` 秒
  - `m`: 分钟
  - `h`: 小时
  - `10m30s`, 10分钟30秒
默认情况下，调度程序一次更新1个任务。您可以传递`--update-parallelism`标志来配置调度程序同时更新的最大服务任务数。

默认情况下，当对单个任务的更新返回RUNNING状态时，调度程序会调度另一个任务进行更新，直到所有任务都更新. 如果在更新期间的任何时间任务返回FAILED，则调度程序暂停更新。您可以使用`--update-failure-action`标志控制docker服务创建或docker服务更新的行为。

3. 检查redis 服务
`docker service inspect --pretty redis`

4. 更新redis 镜像, swarm管理器根据UpdateConfig策略将更新应用于节点：
`docker service update image redis:3.0.7 redis`
  更新的过程默认:
    1. stop the first task
    2. 调度器更新停止的容器的镜像
    3. 启动更新后的容器
    4. 如果更新成功, 则等待设置的延迟时间后, 再更新下一个
    5. 如果任何一个更新出现failed则暂停更新.

5. 使用`docker service inspect --pretty redis` 查看更新后的镜像状态
6. 重新启动暂停的更新`docker service update redis`
7. 使用`docker service ps <service-id>` 查看更新过程


```
docker service create \
  --mode global \
  --mount type=bind,source=/,destination=/rootfs,ro=1 \
  --mount type=bind,source=/var/run,destination=/var/run \
  --mount type=bind,source=/sys,destination=/sys,ro=1 \
  --mount type=bind,source=/var/lib/docker/,destination=/var/lib/docker,ro=1 \
  --publish mode=host,target=8080,published=8080 \
  --name=cadvisor \
  google/cadvisor:latest
```
