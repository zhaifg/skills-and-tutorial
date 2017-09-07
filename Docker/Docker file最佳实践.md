# Docker file最佳实践
---

通常情况下, 最好的方式,在一个空目录下建立一个Dockerfile. 要增加构建的性能，您可以通过将.dockerignore文件添加到该目录来排除文件和目录。语法类似.gitignore

1. 避免安装不必须的包
2. 每一个容器只关注一个功能
3. 最小化镜像层数.
4. 排序多行参数.
5. 构建缓存
  1. 在`docker build`指定`--no-cache=true`, 避免使用缓存
6. APT-GET
  1. 你应该避免RUN apt-get升级或dist升级
  2. 始终将RUN apt-get update 与apt-get install组合在同一RUN语句中，例如：

## 关键字
### FROM
指定基础镜像, 在Docker file的第一行

```
from <image>  
from <image>:<tag> 
from <image>@<digest>
```

### LABEL
使用label来组织工程中的镜像, label用来记录license信息, 注释,以及其他的信息. 
每一个label占据一行, 以LABEL开始, 使用一个或者多可键值对的形式.

添加元数据到镜像, 键值对形式, 使用空格分隔, 使用引用和反斜杠进行续行.

```
LABEL com.example.version="0.0.1-beta"
LABEL com.example.release-date="2015-02-12"
LABEL com.example.version.is-production=""

# Set multiple labels on one line
LABEL com.example.version="0.0.1-beta" com.example.release-date="2015-02-12"

# Set multiple labels at once, using line-continuation characters to break long lines
LABEL vendor=ACME\ Incorporated \
      com.example.is-beta= \
      com.example.is-production="" \
      com.example.version="0.0.1-beta" \
      com.example.release-date="2015-02-12"
```



### MAINTAINER:
  维护者信息
`MAINTAINER <name>`

### RUN
在执行时, 会在最顶层新建一层并提交结果.
运行的命令, 两种格式, 默认的使用`/bin/sh -c` ` cmd /S /C` 
`RUN ["executable", "param1", "param2"]` execform

`RUN <command>`
在windows,可以执行多条命令
`RUN <command>` `/bin/sh -c` 默认执行的sh
`RUN /bin/bash -c 'source $HOME/.bashrc ;\ echo $HOME'`  使用全局参数

`RUN ["executable", "param1", "param2"]`: 这是一个json数组, 必须使用双引号
`["/bin/bash", "-c", "echo hello"]`

```
RUN /bin/bash -c 'source $HOME/.bashrc; \
   echo $HOME'
# or

RUN ["/bin/bash", "-c", "echo hello"]

RUN apt-get update && apt-get install -y \
  bzr \
  cvs \
  git \
  mercurial \
  subversion
```
RUN: Build cache
>  使用execform不会调用一个shell, 平常的shell过程将不会发生, 如: RUN ["echo", "$HOME"]将什么也没有. 要调用shell过程, 使用shellform 或者使用RUN ["sh", "-c" "echo $HOME"]
>  


### CMD
一个Dockerfile中, 只能一条cmd
一次执行一条命令
格式:
```
CMD ["executable","param1","param2"] (execform, 这是首选行形式)
CMD ["param1","param2"] (as default parameters to ENTRYPOINT) # 默认参数在ENTRYPOINT 设置
CMD command param1 param2 (shell form)
```
> 如果CMD如果CMD用于为ENTRYPOINT指令提供默认参数, 则CMD和ENTRYPOINT必须是JSON格式.



```
CMD echo "This is a test." | wc -
CMD ["/usr/bin/wc","--help"]
```


### RUN与CMD区别
RUN: 运行命令并提交结果
CMD: 在build阶段不会执行, 但是会在image里执行.

### EXPOSE

`EXPOSE <port> [<port>...]`




### ENV
设置环境变量
```
ENV <key> <value>
ENV <key>=<value> ...
```

```
ENV myName="John Doe" myDog=Rex\ The\ Dog \
    myCat=fluffy


ENV myName John Doe
ENV myDog Rex The Dog
ENV myCat fluffy
```

### ADD
构建时, 复制本地文件,远程的文件等到docke image里
```
ADD <src>... <dest>
ADD ["<src>",... "<dest>"] (this form is required for paths containing whitespace)
```

- 1.如果多个src资源, 必须在上下文中, 
```
ADD hom* /mydir/
ADD hom?.txt /mydir/
```

- 2.dest 必须是绝对路径或者相对于WORKDIR路径. 
- 3.如果src是远程地址
  1. 下载后的权限是600
  2. 如果远程文件是HTTP协议,且header中有Last-Modified, 那么目标文件的mtime 为这个时间
- 4.如果在Dockerfile中使用标准输入时, 请使用docker build - < somefile
- 5.如果远程开启了验证时, 使用wget, curl等工具
- 6. 遵守以下规则
  1. 如果src必须在build上下文中, 不能使用` ADD ../something /something`.
  2. 如果src是url, dest不是以斜杠结尾, 则下载后使url后复制到dest
  3. 如果src是URL并且dest以尾部斜杠结尾，则从URL中推断文件名，并将文件下载到`<dest> / <filename>`。例如，`ADD http://example.com/foobar /`会创建文件`/foobar。`
  4. 如果src是目录, 复制目录的全部内容，包括文件系统元数据。不包括目录, 只复制内容
  5. 如果src是本地tar压缩(gzip, bzip2, xz), 会被解压. 如果是远程的压缩文件, 则需要用`tar -x`解压
  6. 如果src是别的类型文件, 则复制文件和原信息.
  7. 如果src是多个资源, 只用的正则等, 则dest必须是目录且以/结尾
  8. 如果dest没有使用/结尾, 则src被复制为dest
  9. 如果dest不存在,则创建


### COPY

```
COPY <src>... <dest>
COPY ["<src>",... "<dest>"] 对于包含空格的路径，此表单是必需的
```

```
COPY hom* /mydir/        # adds all files starting with "hom"
COPY hom?.txt /mydir/    # ? is replaced with any single character, e.g., "home.txt"
```


### ENTRYPOINT
```
ENTRYPOINT ["executable", "param1", "param2"] (exec form, preferred)
ENTRYPOINT command param1 param2 (shell form)
```
ENTRYPOINT允许您配置将作为可执行文件运行的容器。
`docker run  -it --rm -p 80:80 nginx`
`docker run <image>`的命令行参数将附加在exec形式的ENTRYPOINT中的所有元素之后，并将覆盖使用CMD指定的所有元素。您可以使用docker run --entrypoint标志覆盖ENTRYPOINT指令。
在Dockerfile中只有最后一个ENTRYPOINT才会生效.

#### exec 形式的ENTRYPOINT
您可以使用ENTRYPOINT的exec形式设置相当稳定的默认命令和参数，然后使用任一形式的CMD设置更可能更改的其他默认值。
```
FROM ubuntu
ENTRYPOINT ["top", "-b"]
CMD ["-c"]

#---
# 当您运行容器时，您可以看到top是唯一的进程：
$ docker run -it --rm --name test  top -H
top - 08:25:00 up  7:27,  0 users,  load average: 0.00, 0.01, 0.05
Threads:   1 total,   1 running,   0 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.1 us,  0.1 sy,  0.0 ni, 99.7 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem:   2056668 total,  1616832 used,   439836 free,    99352 buffers
KiB Swap:  1441840 total,        0 used,  1441840 free.  1324440 cached Mem

  PID USER      PR  NI    VIRT    RES    SHR S %CPU %MEM     TIME+ COMMAND
    1 root      20   0   19744   2336   2080 R  0.0  0.1   0:00.04 top

# To examine the result further, you can use docker exec:
$ docker exec -it test ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  2.6  0.1  19752  2352 ?        Ss+  08:24   0:00 top -b -H
root         7  0.0  0.1  15572  2164 ?        R+   08:25   0:00 ps aux

```

#### Shell form ENTRYPOINT example
您可以为ENTRYPOINT指定一个纯字符串，它将在/ bin / sh -c中执行。
这种形式将使用shell处理来替换shell环境变量，并且将忽略任何CMD或docker运行命令行参数。要确保docker停止将正确地发出任何长时间运行的ENTRYPOINT可执行文件，您需要记住用exec启动它：
```
FROM ubuntu
ENTRYPOINT exec top -b
```
When you run this image, you’ll see the single PID 1 process:
```
$ docker run -it --rm --name test top
Mem: 1704520K used, 352148K free, 0K shrd, 0K buff, 140368121167873K cached
CPU:   5% usr   0% sys   0% nic  94% idle   0% io   0% irq   0% sirq
Load average: 0.08 0.03 0.05 2/98 6
  PID  PPID USER     STAT   VSZ %VSZ %CPU COMMAND
    1     0 root     R     3164   0%   0% top -b

# Which will exit cleanly on docker stop:
$ /usr/bin/time docker stop test
test
real    0m 0.20s
user    0m 0.02s
sys 0m 0.04s

# If you forget to add exec to the beginning of your ENTRYPOINT:
FROM ubuntu
ENTRYPOINT top -b
CMD --ignored-param1

# You can then run it (giving it a name for the next step):
$ docker run -it --name test top --ignored-param2
Mem: 1704184K used, 352484K free, 0K shrd, 0K buff, 140621524238337K cached
CPU:   9% usr   2% sys   0% nic  88% idle   0% io   0% irq   0% sirq
Load average: 0.01 0.02 0.05 2/101 7
  PID  PPID USER     STAT   VSZ %VSZ %CPU COMMAND
    1     0 root     S     3168   0%   0% /bin/sh -c top -b cmd cmd2
    7     1 root     R     3164   0%   0% top -b
```

#### 了解CMD和ENTRYPOINT如何交互
CMD和ENTRYPOINT指令定义在运行容器时执行什么命令。有很少的规则描述他们的合作。

1. Dockerfile应该至少指定一个CMD或ENTRYPOINT命令。
2. 当使用容器作为可执行文件时，应该定义ENTRYPOINT。
3. CMD应该用作定义ENTRYPOINT命令的默认参数或在容器中执行ad-hoc命令的一种方法
4. 当运行带有替代参数的容器时，CMD将被覆盖。
5. 


### VOLUME
`VOLUME ["/data"]`

### USER
`USER daemon`

### WORKDIR
`WORKDIR /path/to/workdir`

```
WORKDIR /a
WORKDIR b
WORKDIR c
RUN pwd
# /a/b/c

ENV DIRPATH /path
WORKDIR $DIRPATH/$DIRNAME
RUN pwd
# /path/$DIRNAME
```

### ARG
`ARG <name>[=<default value>]`
ARG指令定义一个变量，用户可以使用docker build命令使用--build-arg <varname> = <value>标志，在构建时将其传递给构建器。如果用户指定未在Dockerfile中定义的构建参数，构建将输出警告。
```
[Warning] One or more build-args [foo] were not consumed.
```
Dockerfile作者可以通过指定ARG一次或多个变量，通过多次指定ARG来定义单个变量。例如，一个有效的Dockerfile：
```
FROM busybox
ARG user1
ARG buildno
...
```



### STOPSIGNAL
`STOPSIGNAL signal`

### ONBUILD
`ONBUILD [INSTRUCTION]`ONBUILD指令将image添加到稍后执行的触发指令，当image用作另一个构建的基础时.
触发器将在下游构建的上下文中执行，就好像它已经在下游Dockerfile中的FROM指令之后立即插入。


example:
```
# golang
FROM buildpack-deps:jessie-scm

# gcc for cgo
RUN apt-get update && apt-get install -y --no-install-recommends \
        g++ \
        gcc \
        libc6-dev \
        make \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

ENV GOLANG_VERSION 1.7.5
ENV GOLANG_DOWNLOAD_URL https://golang.org/dl/go$GOLANG_VERSION.linux-amd64.tar.gz
ENV GOLANG_DOWNLOAD_SHA256 2e4dd6c44f0693bef4e7b46cc701513d74c3cc44f2419bf519d7868b12931ac3

RUN curl -fsSL "$GOLANG_DOWNLOAD_URL" -o golang.tar.gz \
    && echo "$GOLANG_DOWNLOAD_SHA256  golang.tar.gz" | sha256sum -c - \
    && tar -C /usr/local -xzf golang.tar.gz \
    && rm golang.tar.gz

ENV GOPATH /go
ENV PATH $GOPATH/bin:/usr/local/go/bin:$PATH

RUN mkdir -p "$GOPATH/src" "$GOPATH/bin" && chmod -R 777 "$GOPATH"
WORKDIR $GOPATH

COPY go-wrapper /usr/local/bin/
```


## 摘自
[官网 Docker file最佳实践.md](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/)
[docker file 语法](https://docs.docker.com/engine/reference/builder/)


docker run -d swarm join --addr=192.168.8.87:2375 token://8d4aa70668b725a41565f3ab74319a8f
