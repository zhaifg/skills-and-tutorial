# Docker 的编排软件--Docker-compose
---

## Compose
Compose是用来定义和运行一个或者多个容器应用的工具. 使用Compose可以简化容器镜像的建立以及运行的. Compose使用Python语言开发, 非常适合在单机环境里部署一个或者多个容器, 并自动把多个容器互相关联起来.

## Compose的使用步骤
Compose的使用基本上遵循以下三步:
1. 用Dockerfile文件定义应用的运行环境, 以便应用在任何地方都可以复制; 基于这个Dockerfile, 可以构建出一个Docker 镜像.
2. 用docker-compose.yml文件定义应用的各个服务, 以便这些服务可以作为应用的组件一起运行.
3. 执行docker-compose up命令, 就可以Compose就会创建和运行整个应用了.


## Compose配置简介
Compose是对docker命令的封装, 默认使用docker-compose.yml来指定docker各个命令中所需要的参数.

以下是一个docker-compose.yml文件的简单示例:
```
web:
  build: ./web
  ports:
  - "5000:5000"
  volumes:
  - .:/code
  links:
  - redis
redis:
  image: redis
```

此docker-compose.yml文件定义了两个服务: Web和Redis, 服务的名称是由用户定义
的.提供Web服务的镜像是通过在Web子目录下调用docker build命令得到的. Web服
务运行后监听的端口是5000, 并且把容器里的5000端口映射到主机的5000端口上; 其所
使用的"/code"目录是通过挂载当前目录得到的. Web服务通过连接Redis容器来访问后
台的Redis数据库, 而Redis数据库服务则是通过运行Redis镜像来提供的.


在docker-compose.yml文件中, 每个定义的服务都至少要包含build或者image两个命令中
的一个, 其他命令都是可选的.

## 环境变量文件
Compose 支持定义默认的环境变量, 可以使用.env的格式存放在docker-compose.yml目录下


### 代替的环境变量
```yaml
web:
  image: "webapp:${TAG}"
```

### 在容器中设置环境变量
```yaml
web: 
  environment:
    - DEBUG=1
```

### 将环境变量传递给容器
`docker run -e VARIABLE...`
```yaml
web:
  environment:
    - DEBUG

```

###  使用env_file配置
运行时:`docker run --env-file=FILE...`

```yaml
web:
  env_file:
    - web-variables.env
```


### 使用docker-compose 色织环境变量

```
$ docker-compose run -e DEBUG=1 web python console.py
#You can also pass a variable through from the shell by not giving it a value:

$ docker-compose run -e DEBUG web python console.py

```

### 环境变量文件".env"

```
$ cat .env
TAG=v1.5

$ cat docker-compose.yml
version: '2.0'
services:
  web:
    image: "webapp:${TAG}"
```

`docker-compose config`: 打印当前的配置后信息.

使用export来设置运行的环境变量
```
$ export TAG=v2.0

$ docker-compose config
version: '2.0'
services:
  web:
    image: 'webapp:v2.0'
```

## 使用多个Compose file
默认的情况下,Compose可以读取两个文件,一个docker-compose.yml和可选的docker-compose.override.yml. docker-compose.yml基础的配置, docker-compose.override.yml:可选的可以覆盖docker-compose.yml的配置.

### 实例
**docker-compose.yml**
```yaml
web:
  image: example/my_web_app:latest
  links:
    - db
    - cache

db:
  image: postgres:latest

cache:
  image: redis:latest
```

**docker-compose.override.yml**
```yaml
web:
  build: .
  volumes:
    - '.:/code'
  ports:
    - 8883:80
  environment:
    DEBUG: 'true'

db:
  command: '-d'
  ports:
    - 5432:5432

cache:
  ports:
    - 6379:6379
```

当使用docker-compose up时, 会读取override来取代基础配置文件.

现在, 我们使用compose创建一个生产环境的, 创建另外一个配置文件,比如(存储了不同的git repo等):
`docker-compose.prod.yml`

```yaml
web:
  ports:
    - 80:80
  environment:
    PRODUCTION: 'true'

cache:
  environment:
    TTL: '500'
```

部署时使用`docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d`

## Docker 的扩展服务
Docker可以使用extends关键字,来使用公共的配置文件, 重用配置文件
> Note: `links`, `volumes_from`, and `depends_on` are never shared between services using >extends. These exceptions exist to avoid implicit dependencies—you always define links and `volumes_from` locally. This ensures dependencies between services are clearly visible when reading the current file. Defining these locally also ensures changes to the referenced file don’t result in breakage.
<!-- 
> links, volumes_from, depends_on 不能使用 -->


### 理解extends配置
- 1.当你在docker-compose.yml定义一些服务时, 可以定义一些扩展的给别的服务的设置
`docker-compose.yml`

```yaml
web:
  extends:
    file: common-services.yml
    service: webapp
```
这段配置,重用的`webapp`服务, 定义webapp服务的文件是`common-services.yml`

`common-services.yml`

```yaml
webapp:
  build: .
  ports:
    - "8000:8000"
  volumes:
    - "/data"
```

You can go further and define (or re-define) configuration locally in docker-compose.yml:
```
web:
  extends:
    file: common-services.yml
    service: webapp
  environment:
    - DEBUG=1
  cpu_shares: 5

important_web:
  extends: web
  cpu_shares: 10
```
You can also write other services and link your web service to them:
```
web:
  extends:
    file: common-services.yml
    service: webapp
  environment:
    - DEBUG=1
  cpu_shares: 5
  links:
    - db
db:
  image: postgres
```

### 示例
下面的实例包括2个服务,1个web应用和1个queue worker. 两个服务都依赖于同一个代码库和共享的配置文件

`common.yml`

```yaml
app:
  build: .
  environmeent:
    CONFIG_FILE_PATH: /code/config
    API_KEY: xxxyyyyy
  cpu_shares: 5
```


` docker-compose.yml `

```yaml
webapp:
  extends:
    file: common.yml
    service: app
  command: /code/run_web_app
  ports:
    - 8080:8080
  links:
    - queue
    - db
queue_worker:
  extends:
    file: common.yml
    service: app
  command: /code/run_worker
  links:
    - queue
```

[官网](https://docs.docker.com/compose)
[docker-composefile语法](https://docs.docker.com/compose/compose-file/)
