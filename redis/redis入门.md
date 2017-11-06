# redis 入门
---
## 什么redis
K:V

java Map
python  Dict

### 数据结构
strings
Blobs
Bitmaps

Hash Tables(object!)
Linked Lists
Sets
Sorted Sets
### 特性
1. 速度快
2. 持久化
3. 多种数据结构
4. 支持多种编程语言
5. 功能丰富
6. simple
7. 主从
8. 高可用,分布式

### 应用场景
1. 缓存系统
2. 排行榜应用
3. 计数器应用
4. 社交网络
5. 消息多列系统
6. 实时系统

## 安装
### Linux安装方法和原则
1. 软件包
2. 源码安装
3. 最稳定原则

```shell
tar -xf redis-x.x.tar.gz
cd redis-x.x
make
make install
```

### 可执行文件
`redis-server`: redis-server
`redis-cli`: cmd
`redis-benchmark`: performance Test Tools
`redis-check-aof`: AOF文件修复工具
`redis-check-dump`: RDB文件检查工具
`redis-sentinel`: Sentinel服务器(2.8以后)

### 启动等
- 1) `redis-server`
- 2) 验证
`ps -ef |grep redis` `netstat -antpl |grep redis` 
`redis-cli -h ip -p port ping`

- 3)动态参数启动
`redis-server --port port`

- 4) 配置启动
`redis-server configPath`


- 5) init.d 设置

- 6) 客户端
redis-cli -h -p port

- 7) 常用配置
`daemoniz`: 是否守护进程(no|yes)
`port`: Redis对外端口号
`logfile`: Redis 系统日志
`pidfile`: 保存进程号的文件


## Java 工具Jedis

## 数据结构


keys:
* 不能太长或太短
* 最好坚持一种模式: object-type:field  user:1000:password
### String 字符串
* 字符串键值, 二进制安全的, redis的string可以包含任何数据, 比如图片或者序列化对象
k: hello  v: world
场景: 缓存,计数器,分布式锁
* 重要的API
  get key
  set key value o(1)
  del key

```
incr key  # key自增1, 如果key不存在, 自增后get(key)=1

decr key # key自减, 如果key不存在, 自减后get(key)=-1

incrby key k 
#key 自增k, 如果keybucunz,自增后get(key)=k

decr key k
#key自减, 如果不存在key,自减后get(key) = -k


```
#### 记录网站每个用户个人主页的访问量
`incr userid:pageview`

### Hash(哈希)
是一个键名对集合
Redis hash 是一个string类型的field 和value
的映射表, hash 特别适用于存储对象.
```
127.0.0.1:6379>  HMSET user:1 username runoob password runoob points 200
OK
127.0.0.1:6379> HGETALL user:1
1) "username"
2) "runoob"
3) "password"
4) "runoob"
5) "points"
6) "200"
127.0.0.1:6379> 

```

### List 列表
Redis 列表是简单的字符串列表, 按照插入顺序排序. 你可以添加一个元素到表的头部(左边)或者 尾部 右边
```
127.0.0.1:6379> lpush runoob redis
(integer) 1
127.0.0.1:6379> lpush runoob mongodb
(integer) 2
127.0.0.1:6379> lpush runoob rabitmq
(integer) 3
127.0.0.1:6379> lrange runoob 0 10
1) "rabitmq"
2) "mongodb"
3) "redis"
```

### Set 集合
是string类型无序集合
集合通过哈希表实现, 所以添加, 删除, 查找的复杂度都是o(1)
sadd
sadd key member
```
127.0.0.1:6379> sadd runoobs mongodb
(integer) 1
127.0.0.1:6379> sadd runoobs redis
(integer) 1
127.0.0.1:6379> sadd runoobs rabimq
(integer) 1
127.0.0.1:6379> semembers runoobs
(error) ERR unknown command 'semembers'
127.0.0.1:6379> smembers runoobs
1) "redis"
2) "rabimq"
3) "mongodb"
```

### ZSet 有序集合

Redis Zset 和set 一样也是string 类型元素的集合, 且不允许有重复成员
不同的是每个元素都会关联一个double类型的分数. redis 正是通过分数来为集合中的成员进行从小到大的拍讯. zset 成员唯一, 分数不唯一

zadd
zadd key score member
```
127.0.0.1:6379> zadd runb 0 redis
(integer) 1
127.0.0.1:6379> zadd runb 0 mongodb
(integer) 1
127.0.0.1:6379> zadd runb 0 rabmq
(integer) 1
127.0.0.1:6379> zrangebyscore runb 0 1000
1) "mongodb"
2) "rabmq"
3) "redis"

```

Redis数据库
### 单个键管理
### 遍历键管理
### 数据库管理

## Redis-2 种新的数据结构
### HyperLogLog(since 2.8)
### GEO(future 3.2)

