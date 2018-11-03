# redis 入门与实战
---


## redis API的使用和理解

### 通用命令
keys: 遍历出所有的key
一般不在生产环境使用, o(n)命令, key 比较多的时比较慢

    keys *
    keys [pattern] keys he* keys he[hl]


dbsize: 计算key 的总数

exist: exist key 检查key 是否存在, 存在返回1 , 不存在返回0

del key: 删除指定的key-value

expire key seconds: key 在 seconds 秒后过期
ttl key: 查看剩余的过期时间
persist key: 取消key 过期

type key: 返回key 的类型

#### 时间复杂度:
keys o(n)
dbsize O(1)
del  O(1)
exists  O(1)
expire  O(1)
type  O(1)

### 数据结构和内部编码

string: raw, int, embstr

hash: hashtable
    ziplist

list:  linkedlist
    ziplist
set:  hashtable
intset

zset: 
  skiplist
  ziplist

### 字符串
key: 字符串, 数字(自动转换为str), bits

场景:
* 缓存
* 计数器
* 分布式锁

get:
    get key
set:
    set key value
del:

incr:
decr:
incrby:
decrby:

某个人页面访问量:
incr userid:pageview

缓存视频的基本信息:

分布式id生成器:
incr id


set
    set key value key 不管存不存在,设置
setnx
 setnx key value: key 不存在,才设置
setxx
 setxx key value: key 存在,才设置


mget: mget key1 key2 key3

mset: k v k v

getset key newvalue

* append key value, 
  * 如果key 已经存在并且是一个字符串, append 命令将value 追加到原来的可以结尾.
  * 如果可以不存在, append就简单的将给定的可以设置为 value, 跟, set key value 一样
  * 返回 追加value之后, key中字符串的长度

strlen key

incrbyfloat
getrange key start end
setrange


### hash
key : field value
user:1:info  

hget
hset
hdel

hexists
hlen

hmget
hmset

记录网站每个用户个人主页的访问量?
hincrby user:1:info pageview count


hgetall
hvals 返回hask key 所对应的field的value
hkeys

string vs hash


### list

lpush
lpop
rpop

lrem key count value
ltrim key start end
lrange key start end (包含end)
lindex key index
llen
lset key index newValue

blpop key timeout: 阻塞性pop, timeout=0 永远不阻塞

brpop

LRUSH + LPOP =stackLPUSH + RPOP = queue
LPUSH + LTRIM

TimeLine:


### 集合 set

key: values 

sadd key element
srem key element

scard 计算集合大小
sismember 判断是否在集合中
srandmember
smembers
spop


sdiff 差集
sinter 交集
sunion 并集
sdiff|sinter|suion + store key
标签:


### zset 有序集合

key: value (score, value)

zadd key score element 分数可以重复, element 不能重复

zrem key element 可以多个
zscore key clement
zincrby key increScore element 增加减少元素分数
zcard key 

zrank 获取排名

zrange ley start end (withscore) 放回指定索引范围内的升序元素(分值)
zcount key minScore maxScore


zrevrank

排行榜

## 

### 慢查询
slowlog-max-len
  1. 先进先出
  2. 固定长度
  3. 保存在内存中
  4. 默认10ms, 通常1ms

 slowlog-log-slower-than
 1. 慢查询阙值 微秒
 2. slowlog-log-slower-than=0 记录所有命令 
 3. 不要设置过小, 通常设置1000 左右
 4. 理解命令的声明周期
 5. 定期持久化慢查询

### pipeline

一次pipeline的 时间 = 1次网络时间 + n 次命令执行时间
1. Redis的命令时间是微秒级别
2. PIpleline 每次条数要控制

## 发布订阅
角色
* 发布者 publisher
* 订阅者 subscriber
* 频道 channel

命令
publish channel message
subscriber \[channel\] 一个或者多个
unsubscriber 


## 消息队列

## bimap
位图

相关命令
setbit key offset value
getbit
bitcount key \[start end\]
bitop op deskey key \[key ...\]
bitpos key targetBit \[start\]  \[end\]

## HyperLogLog
1. 用极小的空间完成队里数量统计
2. 本质还是字符串

pfadd key element \[element ...\] 添加用户
浦发countkey \[key ...\]

pfmerge key key

## GEO

geoadd key longitude laititude memeber

geopos key member \[member...\]
geodist key member1 member2 \[unit\]
georadius key ....

## redis持久化的取舍和选择

### 持久化的作用

### RDB
快照
rdb 二进制文件 

1. save 同步命令
2. bgsave 异步命令
3. 自动

### AOF
binlog


## redis复制原理与优化
