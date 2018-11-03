# supervisor
---
Supervisor is a client/server system that allows its users to monitor and control a number of processes on UNIX-like operating systems.

## 组成
**supervisord**: supervisor server 端的进程. 它启动好管理子进程

**supervisorctl**: 命令行管理程序

**web server** ` [inet_http_server]`

**xml rpc interface**

## install
```
pip install supervisor
yum /apt-get
```

## 使用
### 添加一个程序
```
[program:foo]
command=/bin/cat

```

### 运行
```
supervisord -c supervisord.conf
```

```
supervisorctl
> start xxx
> start all
> stop all
```

