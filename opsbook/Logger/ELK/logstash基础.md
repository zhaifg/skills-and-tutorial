# logstash 手册
---
## Logstash 介绍


## Logstash 安装

Logstash从1.5开始, 将核心代码和插件完全剥离, 并重构了蟾剑架构逻辑, 所有插件都以标准的Ruy Gem包形式发布.

1. 直接到官网下载安装包

直接下载官方发布的二进制包的，可以访问 https://www.elastic.co/downloads/logstash 页面找对应操作系统和版本，点击下载即可。不过更推荐使用软件仓库完成安装。

```
# 安装jdk, 配置jdk环境
export JAVA_HOME=
解压logstash
```

2. yum/apt包
在配置官网提供的yum源或者deb源
```
rpm --import http://packages.elasticsearch.org/GPG-KEY-elasticsearch
cat > /etc/yum.repos.d/logstash.repo <<EOF
[logstash-5.0]
name=logstash repository for 5.0.x packages
baseurl=http://packages.elasticsearch.org/logstash/5.0/centos
gpgcheck=1
gpgkey=http://packages.elasticsearch.org/GPG-KEY-elasticsearch
enabled=1
EOF
yum clean all
yum install logstash
```

## 入门

### Hello World
```
[root@yimiwork_217 logstash]# ./bin/logstash -e 'input{stdin{}}output{stdout{codec=>rubydebug}}'
hello world   
Settings: Default pipeline workers: 2
Pipeline main started
{
       "message" => "hello world",
      "@version" => "1",
    "@timestamp" => "2016-10-21T07:57:49.309Z",
          "host" => "yimiwork_217"
}


```
### 完整实例
使用logstash.conf配置文件来启动logstash
`logstash`

```
input {
    stdin {}
}

output {
    stdout {
        codec ==> rubydebug {}
    }

    elasticsearch {
        embedded ==> true
    }
}
```

`bin/logstash -f logstash.conf`

### 解释
每位系统管理员都肯定写过很多类似这样的命令：`cat randdata | awk '{print $2}' | sort | uniq -c | tee sortdata`。这个管道符 `|` 可以算是 Linux 世界最伟大的发明之一(另一个是“一切皆文件”)。
Logstash 就像管道符一样！

你输入(就像命令行的 cat )数据，然后处理过滤(就像 awk 或者 uniq 之类)数据，最后输出(就像 tee )到其他地方。

当然实际上，Logstash 是用不同的线程来实现这些的。如果你运行 top 命令然后按下 H 键，你就可以看到下面这样的输出：
```
  PID USER      PR  NI  VIRT  RES  SHR S %CPU %MEM    TIME+  COMMAND                          
21401 root      16   0 1249m 303m  10m S 18.6  0.2 866:25.46 |worker                           
21467 root      15   0 1249m 303m  10m S  3.7  0.2 129:25.59 >elasticsearch.                   
21468 root      15   0 1249m 303m  10m S  3.7  0.2 128:53.39 >elasticsearch.                   
21400 root      15   0 1249m 303m  10m S  2.7  0.2 108:35.80 <file                             
21403 root      15   0 1249m 303m  10m S  1.3  0.2  49:31.89 >output                           
21470 root      15   0 1249m 303m  10m S  1.0  0.2  56:24.24 >elasticsearch.
```

>小贴士：logstash 很温馨的给每个线程都取了名字，输入的叫xx，过滤的叫|xx


数据在线程之间以 `事件的形式流传`。`不要叫行`，因为 logstash `可以处理多行事件`。
Logstash 会给事件添加一些额外信息。最重要的就是 `@timestamp`，用来标记事件的发生时间。因为这个字段涉及到 Logstash 的内部流转，所以必须是一个 `joda 对象`，如果你尝试自己给一个字符串字段重命名为 @`timestamp` 的话，Logstash 会直接报错。所以，请使用 `filters/date` 插件 来管理这个特殊字段。
此外，大多数时候，还可以见到另外几个：

1. `host` 标记事件发生在哪里。
2. `type` 标记事件的唯一类型。
3. `tags` 标记事件的某方面属性。这是一个数组，一个事件可以有多个标签。

你可以随意给事件添加字段或者从事件里删除字段。事实上事件就是一个 Ruby 对象，或者更简单的理解为就是一个哈希也行。

>小贴士：每个 logstash 过滤插件，都会有四个方法叫 add_tag, remove_tag, add_field 和 remove_field。它们在插件过滤匹配成功时生效。

## 配置语法

Logstash社区通常习惯用Shipper, Broker 和Index来描述数据流中不同进程各自的角色, 如下图

![logstash-arch.jpg](../../images/logstash-arch.jpg)


Logstash 设计了自己的DSL, 包括区域, 注释, 数据类型(布尔值, 字符串数值, 数组, 哈希), 条件判断, 字段引用等.

### 区域(setection) {}
使用`{}`来定义区域. 区域内可以包括插件区域定义, 可以在一个区域内定义多个插件. 如:
```
input {
    stdin {}
    syslog {}
}
```

### 数据类型
1. 布尔型(bool)
```
debug ==> true
```

2. 字符串(String)
```
host => "hostname"
```

3. 数值(number)
```
port => 513
```

4. 数组(array)
```
match => ["datetime", "UNIX", "ISO0861"]
```

5. 哈希(hash)
```
options => {
    key1 => "value1",
    key2 => "value2"
}
```
如果版本低于1.2, 哈希语法跟数组一样
```
match => ["field1", "pattern1", "field2", "pattern2"]
```

### 字段引用(field reference)
字段引用 Logstash:Event对象属性.我们之前提过事件就像一个哈希一样，所以你可以想象字段就像一个键值对。

> 小贴士：我们叫它字段，因为 Elasticsearch 里是这么叫的。

如果想在Logstash配置中使用字段的值, 只需要把字段的名字写在`[]`中就可以了. 比如可以从geoip里这样获取 "longitude"值.

`[geoip][location][0]`
小贴士：logstash 的数组也支持倒序下标，即` [geoip][location][-1] `可以获取数组最后一个元素的值

Logstash 还支持变量内插，在字符串里使用字段引用的方法是这样：
`"the longitude is %{[geoip][location][0]}"`

### 条件判断(condition)

表达式支持下面的这些操作:

1. ==(等于), !=(不等于), <,>, <=, >=
2. =~(匹配正则), !~(不匹配正则)
3. in(包含), not in(包含)
4. and(与), or, nand(非与), xor(非或)
5. ()符合表达式, !()对复合表达式结果取反

通常来说, 都会在表达式里用到字段引用. 为了尽量全面展示各种表达式. 下面虚拟一个示例.
```
if "_grokparsesefailure" not in [tags] {

    }
else if [status] !~ /^2\d\d/ or ([url] == "/noc.gif") nand [geoip][city] != "beijing" {}

```

### 命令行参数

Logstash提供了一个shell脚本叫logstash方便快速运行.

- `-e`: 执行, 
- `-f --config`: 从文件里读取配置
此外，logstash 还提供一个方便我们规划和书写配置的小功能。你可以直接用 bin/`logstash -f /etc/logstash.d/` 来运行。logstash 会自动读取 /etc/logstash.d/ 目录下所有 *.conf 的文本文件，然后在自己内存里拼接成一个完整的大配置文件，再去执行。+

> 注意：
logstash 列出目录下所有文件时，是字母排序的。而 logstash 配置段的 filter 和 output 都是顺序执行，所以顺序非常重要。采用多文件管理的用户，推荐采用数字编号方式命名配置文件，同时在配置中，严谨采用 if 判断限定不同日志的动作。

` `--configtest 或 -t`
意即`测试`。用来测试 Logstash 读取到的配置文件语法是否能正常解析。Logstash 配置语法是用 grammar.treetop 定义的。尤其是使用了上一条提到的读取目录方式的读者，尤其要提前测试。

- `--log 或 -l`
意即日志。Logstash 默认输出日志到标准错误。生产环境下你可以通过 bin/logstash `-l logs/logstash.log` 命令来统一存储日志。
`--pipeline-workers 或 -w`
运行 filter 和 output 的 pipeline 线程数量。默认是 CPU 核数。

- `--pipeline-batch-size 或 -b`
每个 Logstash pipeline 线程，在执行具体的 filter 和 output 函数之前，最多能累积的日志条数。默认是 125 条。越大性能越好，同样也会消耗越多的 JVM 内存。

- `--pipeline-batch-delay 或 -u`
每个 Logstash pipeline 线程，在打包批量日志的时候，最多等待几毫秒。默认是 5 ms。
- `--pluginpath 或 -P`
可以写自己的插件，然后用 `bin/logstash --pluginpath /path/to/own/plugins` 加载它们。

- `--verbose`
输出一定的调试日志。
- `--debug`
输出更多的调试日志。


## 配置文件
`config/logstash.yml`
从 Logstash 5.0 开始，新增了 $LS_HOME/config/logstash.yml 文件，可以将所有的命令行参数都通过 YAML 文件方式设置。同时为了反映命令行配置参数的层级关系，参数也都改成用.而不是-了。

## 插件安装

使用plugin命令进行管理插件
```
[root@yimiwork_217 logstash]# ./bin/logstash-plugin 
Usage:
    bin/logstash-plugin [OPTIONS] SUBCOMMAND [ARG] ...

Parameters:
    SUBCOMMAND                    subcommand
    [ARG] ...                     subcommand arguments

Subcommands:
    install                       Install a plugin
    uninstall                     Uninstall a plugin
    update                        Update a plugin
    pack                          Package currently installed plugins
    unpack                        Unpack packaged plugins
    list                          List all installed plugins
    generate                      Create the foundation for a new plugin

Options:
    -h, --help                    print help

```

插件的列表url: https://github.com/logstash-plugins

### 本地安装插件
`logstash-plugin install /path/do/logstash-for-crash.gem`

### 后台运行

1. 标准的service 方式
  如果采用rpm或者deb包安装时, 支持这种方式.

2. 使用nohup

3. screen方式
4. 使用supervisord, god等方式运行.


## 插件配置

### 输入插件
基于shipper端场景, 主要介绍STDIN, TCP,File

### 编码插件
- 1. 标准输入(stdin)

实例:
```
input {
    stdin {
        add_field => {"key"=>"value"}
        coedc => "plain"
        tags => ["add"]
        type => "std"
    }
}
```

`logstash -f logstash.conf` 输入Hello World
输出
```
{
       "message" => "Hello World",
      "@version" => "1",
    "@timestamp" => "2016-10-21T08:14:45.563Z",
          "type" => "std",
           "key" => "value",
          "tags" => [
        [0] "add"
    ],
          "host" => "yimiwork_217"
}

```
`type` 和 `tag` 是logstash 事件中两个特殊的字段. 通常来说, 我们会在"输入区段"中通过type来标记时间类型, 前提我们知道输于什么类型, 而tags则是在处理数据过程中, 有具体的插件添加或者删除的.
最常见用法:
```
input {
    stdin{
        type => "web"
    }
}
filter {
    if [type] == "web"{
        grok {
            match =>["message", %{COMBINEADPACHELOG}]
        }
    }
}
output {
    if "_grokparsefailure" in [tags] {
        nagios_nsca {
            nagios_status => "1"
        }
        else{
            elasticsearch {

            }
        }
    }
}
```

- 2.文件输入
 Logstash 通过FileWatch的来监听文件的变化. 这个库支持glob文件展开, 而且会记录一个叫.sincedb的数据库文件来跟踪日志变化, 并读取位置.

```
input {
    file {
        path => ["/var/log/*.log", "/var/log/messages"]
        type => "system"
        start_position => "beginning"
    }
}
```

有一些比较有用的配置项，可以用来指定 FileWatch 库的行为：
`discover_interval`
logstash 每隔多久去检查一次被监听的 path 下是否有新文件。默认值是 15 秒。

`exclude`
不想被监听的文件可以排除出去，这里跟 path 一样支持 glob 展开。

`close_older`
一个已经监听中的文件，如果超过这个值的时间内没有更新内容，就关闭监听它的文件句柄。默认是 3600 秒，即一小时。

`ignore_older`
在每次检查文件列表的时候，如果一个文件的最后修改时间超过这个值，就忽略这个文件。默认是 86400 秒，即一天。

`sincedb_path`
如果你不想用默认的 $HOME/.sincedb(Windows 平台上在 C:\Windows\System32\config\systemprofile\.sincedb)，可以通过这个配置定义 sincedb 文件到其他位置。

`sincedb_write_interval`
logstash 每隔多久写一次 sincedb 文件，默认是 15 秒。

`stat_interval`
logstash 每隔多久检查一次被监听文件状态（是否有更新），默认是 1 秒。

`start_position`
logstash 从什么位置开始读取文件数据，默认是结束位置，也就是说 logstash 进程会以类似 tail -F 的形式运行。如果你是要导入原有数据，把这个设定改成 "beginning"，logstash 进程就从头开始读取，类似 less +F 的形式运行。
注意

通常你要导入原有数据进 Elasticsearch 的话，你还需要 `filter/date 插件来修改默认的"@timestamp" 字段值`。稍后会学习这方面的知识。

`FileWatch 只支持文件的绝对路径`，而且会不自动递归目录。所以有需要的话，请用数组方式都写明具体哪些文件。
LogStash::Inputs::File 只是在进程运行的注册阶段初始化一个 FileWatch 对象。所以`它不能支持类似 fluentd 那样的 path => "/path/to/%{+yyyy/MM/dd/hh}.log"` 写法。达到相同目的，你`只能写成 path => "/path/to/*/*/*/*.log"`。FileWatch 模块提供了一个稍微简单一点的写法：`/path/to/**/*.log`，用` **` `来缩写表示递归全部子目录`。

`start_position` 仅在该文件从未被监听过的时候起作用。如果 sincedb 文件中已经有这个文件的 inode 记录了，那么 logstash 依然会从记录过的 pos 开始读取数据。所以重复测试的时候每回需要删除 sincedb 文件(官方博客上提供了另一个巧妙的思路：将 sincedb_path 定义为 /dev/null，则每次重启自动从头开始读)。

因为 windows 平台上没有 inode 的概念，Logstash 某些版本在 windows 平台上监听文件不是很靠谱。windows 平台上，推荐考虑使用 nxlog 作为收集端，参阅本书稍后章节。

- 3.TCP输入
未来你可能会用 Redis 服务器或者其他的消息队列系统来作为 logstash broker 的角色。不过 Logstash 其实也有自己的 TCP/UDP 插件，在临时任务的时候，也算能用，尤其是测试环境。
小贴士：虽然 LogStash::Inputs::TCP 用 Ruby 的 Socket 和 OpenSSL 库实现了高级的 SSL 功能，但 Logstash 本身只能在 SizedQueue 中缓存 20 个事件。这就是我们建议在生产环境中换用其他消息队列的原因。
配置示例
```
input {
    tcp {
        port => 8888
        mode => "server"
        ssl_enable => false
    }
}
```
#### 常见场景

目前来看，LogStash::Inputs::TCP 最常见的用法就是配合 nc 命令导入旧数据。在启动 logstash 进程后，在另一个终端运行如下命令即可导入数据：
`# nc 127.0.0.1 8888 < olddata`
这种做法比用 LogStash::Inputs::File 好，因为当 nc 命令结束，我们就知道数据导入完毕了。而用 input/file 方式，logstash 进程还会一直等待新数据输入被监听的文件，不能直接看出是否任务完成了。

- 4.syslog

syslog可能是运维领域最流行的数据传输协议了。当你想从设备上收集系统日志的时候，syslog 应该会是你的第一选择。尤其是网络设备，比如思科 —— syslog 几乎是唯一可行的办法。

我们这里不解释如何配置你的 syslog.conf, rsyslog.conf 或者 syslog-ng.conf 来发送数据，而只讲如何把 logstash 配置成一个 syslog 服务器来接收数据。
有关 rsyslog 的用法，稍后的类型项目一节中，会有更详细的介绍。

配置示例
```
input {
  syslog {
    port => "514"
  }
}
```
运行结果

作为最简单的测试，我们先暂停一下本机的 syslogd (或 rsyslogd )进程，然后启动 logstash 进程（这样就不会有端口冲突问题）。现在，本机的 syslog 就会默认发送到 logstash 里了。我们可以用自带的 logger 命令行工具发送一条 "Hello World"信息到 syslog 里（即 logstash 里）。看到的 logstash 输出像下面这样：
```
{
           "message" => "Hello World",
          "@version" => "1",
        "@timestamp" => "2014-08-08T09:01:15.911Z",
              "host" => "127.0.0.1",
          "priority" => 31,
         "timestamp" => "Aug  8 17:01:15",
         "logsource" => "raochenlindeMacBook-Air.local",
           "program" => "com.apple.metadata.mdflagwriter",
               "pid" => "381",
          "severity" => 7,
          "facility" => 3,
    "facility_label" => "system",
    "severity_label" => "Debug"
}
```
解释

Logstash 是用 `UDPSocket`, `TCPServer` 和` LogStash::Filters::Grok` 来实现 `LogStash::Inputs::Syslog` 的。所以你其实可以直接用 logstash 配置实现一样的效果：
```
input {
  tcp {
    port => "8514"
  }
}
filter {
  grok {
    match => ["message", "%{SYSLOGLINE}" ]
  }
  syslog_pri { }
}
```

#### 最佳实践
> 建议在使用 `LogStash::Inputs::Syslog` 的时候走 TCP 协议来传输数据。

因为具体实现中，UDP 监听器只用了一个线程，而 TCP 监听器会在接收每个连接的时候都启动新的线程来处理后续步骤。
如果你已经在使用 UDP 监听器收集日志，用下行命令检查你的 UDP 接收队列大小：
```
# netstat -plnu | awk 'NR==1 || $4~/:514$/{print $2}'
Recv-Q
228096
```
228096 是 UDP 接收队列的默认最大大小，这时候 linux 内核开始丢弃数据包了！

>强烈建议使用LogStash::Inputs::TCP和 LogStash::Filters::Grok 配合实现同样的 syslog 功能！

虽然 LogStash::Inputs::Syslog 在使用 TCPServer 的时候可以采用多线程处理数据的接收，但是在同一个客户端数据的处理中，其 grok 和 date 是一直在该线程中完成的，这会导致总体上的处理性能几何级的下降 —— 经过测试，TCPServer 每秒可以接收 50000 条数据，而在同一线程中启用 grok 后每秒只能处理 5000 条，再加上 date 只能达到 500 条！
才将这两步拆分到 filters 阶段后，logstash 支持对该阶段插件单独设置多线程运行，大大提高了总体处理性能。在相同环境下， logstash -f tcp.conf -w 20 的测试中，总体处理性能可以达到每秒 30000 条数据！
注：测试采用 logstash 作者提供的 `yes "<44>May 19 18:30:17 snack jls: foo bar 32" | nc localhost 3000 `命令。出处见：https://github.com/jordansissel/experiments/blob/master/ruby/jruby-netty/syslog-server/Makefile

- 5.collect

collectd 是一个守护(daemon)进程，用来收集系统性能和提供各种存储方式来存储不同值的机制。它会在系统运行和存储信息时周期性的统计系统的相关统计信息。利用这些信息有助于查找当前系统性能瓶颈（如作为性能分析 performance analysis）和预测系统未来的 load（如能力部署capacity planning）等
下面简单介绍一下: collectd的部署以及与logstash对接的相关配置实例
collectd的安装

解决依赖
```
rpm -ivh "http://dl.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm"
yum -y install libcurl libcurl-devel rrdtool rrdtool-devel perl-rrdtool rrdtool-prel libgcrypt-devel gcc make gcc-c++ liboping liboping-devel perl-CPAN net-snmp net-snmp-devel
```
源码安装collectd
```
wget http://collectd.org/files/collectd-5.4.1.tar.gz
tar zxvf collectd-5.4.1.tar.gz
cd collectd-5.4.1
./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var --libdir=/usr/lib --mandir=/usr/share/man --enable-all-plugins
make && make install
```
安装启动脚本
```
cp contrib/redhat/init.d-collectd /etc/init.d/collectd
chmod +x /etc/init.d/collectd
```
启动collectd

`service collectd start`
collectd的配置

以下配置可以实现对服务器基本的CPU、内存、网卡流量、磁盘 IO 以及磁盘空间占用情况的监控:
```
Hostname "host.example.com"
LoadPlugin interface
LoadPlugin cpu
LoadPlugin memory
LoadPlugin network
LoadPlugin df
LoadPlugin disk
<Plugin interface>
    Interface "eth0"
    IgnoreSelected false
</Plugin>
<Plugin network>
    <Server "10.0.0.1" "25826"> ## logstash 的 IP 地址和 collectd 的数据接收端口号
    </Server>
</Plugin>
```
#### logstash的配置

以下配置实现通过 logstash 监听 25826 端口，接收从 collectd 发送过来的各项检测数据。注意 logstash-filter-collectd 插件本身需要单独安装，logstash 插件安装说明之前已经讲过：
bin/plugin install logstash-filter-collectd
示例一：
```
input {
    collectd {
        port => 25826 ## 端口号与发送端对应
        type => collectd
    }
}
```
#### 示例二：（推荐）
```
udp {
    port => 25826
    buffer_size => 1452
    workers => 3          # Default is 2
    queue_size => 30000   # Default is 2000
    codec => collectd { }
    type => "collectd"
}
```

运行结果

下面是简单的一个输出结果：
```
{
  "_index": "logstash-2014.12.11",
  "_type": "collectd",
  "_id": "dS6vVz4aRtK5xS86kwjZnw",
  "_score": null,
  "_source": {
    "host": "host.example.com",
    "@timestamp": "2014-12-11T06:28:52.118Z",
    "plugin": "interface",
    "plugin_instance": "eth0",
    "collectd_type": "if_packets",
    "rx": 19147144,
    "tx": 3608629,
    "@version": "1",
    "type": "collectd",
    "tags": [
      "_grokparsefailure"
    ]
  },
  "sort": [
    1418279332118
  ]
}
```
#### 参考资料

collectd支持收集的数据类型： http://git.verplant.org/?p=collectd.git;a=blob;hb=master;f=README
collectd收集各数据类型的配置参考资料： http://collectd.org/documentation/manpages/collectd.conf.5.shtml
collectd简单配置文件示例： https://gist.github.com/untergeek/ab85cb86a9bf39f1fc6d


### 编解码配置
Codec 是 logstash 从 1.3.0 版开始新引入的概念(Codec 来自 Coder/decoder 两个单词的首字母缩写)。

在此之前，logstash只支持纯文本形式输入，然后以过滤器处理它。但现在，我们可以在输入 期处理不同类型的数据，这全是因为有了 codec 设置。
所以，这里需要纠正之前的一个概念。Logstash 不只是一个input | filter | output 的数据流，而是一个 `input | decode | filter | encode | output` 的数据流！codec 就是用来 decode、encode 事件的。

codec 的引入，使得 logstash 可以更好更方便的与其他有自定义数据格式的运维产品共存，比如 graphite、fluent、netflow、collectd，以及使用 msgpack、json、edn 等通用数据格式的其他产品等。
事实上，我们在第一个 "hello world" 用例中就已经用过 `codec` 了 —— `rubydebug` 就是一种 codec！虽然它`一般只会用在 stdout 插件中`，作为配置测试或者调试的工具。

小贴士：这个五段式的流程说明源自 Perl 版的 Logstash (后来改名叫 Message::Passing 模块)的设计。本书最后会对该模块稍作介绍。

#### 采用 JSON 编码

在早期的版本中，有一种降低 logstash 过滤器的 CPU 负载消耗的做法盛行于社区(在当时的 cookbook 上有专门的一节介绍)：直接输入预定义好的 JSON 数据，这样就可以省略掉 filter/grok 配置！
这个建议依然有效，不过在当前版本中需要稍微做一点配置变动 —— 因为现在有专门的 codec 设置。

配置示例

社区常见的示例都是用的 Apache 的 customlog。不过我觉得 Nginx 是一个比 Apache 更常用的新型 web 服务器，所以我这里会用 nginx.conf 做示例：
```
logformat json '{"@timestamp":"$time_iso8601",'
               '"@version":"1",'
               '"host":"$server_addr",'
               '"client":"$remote_addr",'
               '"size":$body_bytes_sent,'
               '"responsetime":$request_time,'
               '"domain":"$host",'
               '"url":"$uri",'
               '"status":"$status"}';
access_log /var/log/nginx/access.log_json json;
```
注意：在` $request_time` 和` $body_bytes_sent` 变量两头没有双引号 "，这两个数据在 JSON 里应该是数值类型！

重启 nginx 应用，然后修改你的 input/file 区段配置成下面这样：
```
input {
    file {
        path => "/var/log/nginx/access.log_json""
        codec => "json"
    }
}
```
运行结果

下面访问一下你 nginx 发布的 web 页面，然后你会看到 logstash 进程输出类似下面这样的内容：
```
{
      "@timestamp" => "2014-03-21T18:52:25.000+08:00",
        "@version" => "1",
            "host" => "raochenlindeMacBook-Air.local",
          "client" => "123.125.74.53",
            "size" => 8096,
    "responsetime" => 0.04,
          "domain" => "www.domain.com",
             "url" => "/path/to/file.suffix",
          "status" => "200"
}
```

**小贴士**
对于一个 web 服务器的访问日志，看起来已经可以很好的工作了。不过如果 Nginx 是作为一个代理服务器运行的话，访问日志里有些变量，比如说 `$upstream_response_time`，可能不会一直是数字，它也可能是一个 `"-" `字符串！这会直接导致 logstash 对输入数据验证报异常。
有两个办法解决这个问题：
用 sed 在输入之前先替换 - 成 0。
运行 logstash 进程时不再读取文件而是标准输入，这样命令就成了下面这个样子：
```
tail -F /var/log/nginx/proxy_access.log_json \
    | sed 's/upstreamtime":-/upstreamtime":0/' \
    | /usr/local/logstash/bin/logstash -f /usr/local/logstash/etc/proxylog.conf
```
日志格式中统一记录为字符串格式(即都带上双引号 ")，然后再在 logstash 中用 filter/mutate 插件来变更应该是数值类型的字符字段的值类型。
有关 LogStash::Filters::Mutate 的内容，本书稍后会有介绍。

#### 合并多行数据(Multiline)

有些时候，应用程序调试日志会包含非常丰富的内容，为一个事件打印出很多行内容。这种日志通常都很难通过命令行解析的方式做分析。
而 logstash 正为此准备好了 codec/multiline 插件！
小贴士：multiline 插件也可以用于其他类似的堆栈式信息，比如 linux 的内核日志。

配置示例
```
input {
    stdin {
        codec => multiline {
            pattern => "^\["
            negate => true
            what => "previous"
        }
    }
}
```
运行结果

运行 logstash 进程，然后在等待输入的终端中输入如下几行数据：
```
[Aug/08/08 14:54:03] hello world
[Aug/08/09 14:54:04] hello logstash
    hello best practice
    hello raochenlin
[Aug/08/10 14:54:05] the end
```
你会发现 logstash 输出下面这样的返回：
```
{
    "@timestamp" => "2014-08-09T13:32:03.368Z",
       "message" => "[Aug/08/08 14:54:03] hello world\n",
      "@version" => "1",
          "host" => "raochenlindeMacBook-Air.local"
}
{
    "@timestamp" => "2014-08-09T13:32:24.359Z",
       "message" => "[Aug/08/09 14:54:04] hello logstash\n\n    hello best practice\n\n    hello raochenlin\n",
      "@version" => "1",
          "tags" => [
        [0] "multiline"
    ],
          "host" => "raochenlindeMacBook-Air.local"
}
```
你看，后面这个事件，在 "message" 字段里存储了三行数据！
小贴士：你可能注意到输出的事件中都没有最后的"the end"字符串。这是因为你最后输入的回车符 `\n` 并不匹配设定的 `^\[` 正则表达式，logstash 还得等下一行数据直到匹配成功后才会输出这个事件。
解释

其实这个插件的原理很简单，就是把当前行的数据添加到前面一行后面，，直到新进的当前行匹配 `^\[` 正则为止。
这个正则还可以用 grok 表达式，稍后你就会学习这方面的内容。

#### Log4J 的另一种方案

说到应用程序日志，log4j 肯定是第一个被大家想到的。使用 codec/multiline 也确实是一个办法。
不过，如果你本身就是开发人员，或者可以推动程序修改变更的话，logstash 还提供了另一种处理 log4j 的方式：input/log4j。与 codec/multiline 不同，这个插件是直接调用了 org.apache.log4j.spi.LoggingEvent 处理 TCP 端口接收的数据。稍后章节会详细讲述 log4j 的用法。
推荐阅读

https://github.com/logstash-plugins/logstash-patterns-core/blob/master/patterns/java

### 网络流编码 netflow
NetFlow是Cisco发明的饿一种数据交换方式. NetFlow提供网络流量的会话级视图, 记录下每个TCP/IP事物信息.

```
input {
    udp {
      port => 9995
      codec => netflow {
        definitions => "/home/administrator/logstash-1.4.2/lib/logstash/codecs/netflow/netflow.yaml"
        versions => [5]
      }
    }
  }

  output {
    stdout { codec => rubydebug }
    if ( [host] =~ "10\.1\.1[12]\.1" ) {
      elasticsearch {
        index => "logstash_netflow5-%{+YYYY.MM.dd}"
        host => "localhost"
      }
    } else {
      elasticsearch {
        index => "logstash-%{+YYYY.MM.dd}"
        host => "localhost"
      }
    }
  }
```
由于该插件生成字段较多, 所以建议对应的Elasticsearch索引模板也需要单独提交
```
curl -XPUT localhost:9200/_template/logstash_netflow5 -d '{
    "template" : "logstash_netflow5-*",
    "settings": {
      "index.refresh_interval": "5s"
    },
    "mappings" : {
      "_default_" : {
        "_all" : {"enabled" : false},
        "properties" : {
          "@version": { "index": "analyzed", "type": "integer" },
          "@timestamp": { "index": "analyzed", "type": "date" },
          "netflow": {
            "dynamic": true,
            "type": "object",
            "properties": {
              "version": { "index": "analyzed", "type": "integer" },
              "flow_seq_num": { "index": "not_analyzed", "type": "long" },
              "engine_type": { "index": "not_analyzed", "type": "integer" },
              "engine_id": { "index": "not_analyzed", "type": "integer" },
              "sampling_algorithm": { "index": "not_analyzed", "type": "integer" },
              "sampling_interval": { "index": "not_analyzed", "type": "integer" },
              "flow_records": { "index": "not_analyzed", "type": "integer" },
              "ipv4_src_addr": { "index": "analyzed", "type": "ip" },
              "ipv4_dst_addr": { "index": "analyzed", "type": "ip" },
              "ipv4_next_hop": { "index": "analyzed", "type": "ip" },
              "input_snmp": { "index": "not_analyzed", "type": "long" },
              "output_snmp": { "index": "not_analyzed", "type": "long" },
              "in_pkts": { "index": "analyzed", "type": "long" },
              "in_bytes": { "index": "analyzed", "type": "long" },
              "first_switched": { "index": "not_analyzed", "type": "date" },
              "last_switched": { "index": "not_analyzed", "type": "date" },
              "l4_src_port": { "index": "analyzed", "type": "long" },
              "l4_dst_port": { "index": "analyzed", "type": "long" },
              "tcp_flags": { "index": "analyzed", "type": "integer" },
              "protocol": { "index": "analyzed", "type": "integer" },
              "src_tos": { "index": "analyzed", "type": "integer" },
              "src_as": { "index": "analyzed", "type": "integer" },
              "dst_as": { "index": "analyzed", "type": "integer" },
              "src_mask": { "index": "analyzed", "type": "integer" },
              "dst_mask": { "index": "analyzed", "type": "integer" }
            }
          }
        }
      }
    }
  }'
```
### 过滤插件: 

#### date 时间处理
Logstash-filter-date 插件可以用来转换你的日志的时间字符串, 变成LogStash::Timestamp, 然后存入到@timestamp字段里.

注意：因为在稍后的 outputs/elasticsearch 中常用的 %{+YYYY.MM.dd} 这种写法必须读取 @timestamp 数据，所以一定不要直接删掉这个字段保留自己的字段，而是应该用 filters/date 转换后删除自己的字段！+

这在导入旧数据的时候固然非常有用，而在实时数据处理的时候同样有效，因为一般情况下数据流程中我们都会有缓冲区，导致最终的实际处理时间跟事件产生时间略有偏差。
小贴士：个人强烈建议打开 Nginx 的 access_log 配置项的 buffer 参数，对极限响应性能有极大提升！


**logstash-filter-date的时间格式**:
1. ISO8601: 
  类似 "2011-04-19T03:44:01.103Z" 这样的格式。具体Z后面可以有 "08:00"也可以没有，".103"这个也可以没有。常用场景里来说，Nginx 的 log_format 配置里就可以使用 $time_iso8601 变量来记录请求时间成这种格式

2. UNIX: UNIX时间戳格式, 记录从1970年起至今的秒数, squid默认的格式
3. UNIX_MS :这个时间戳则是从 1970 年起始至今的总毫秒数。据我所知，JavaScript 里经常使用这个时间格式
4. TAI64N: TAI64N 格式比较少见，是这个样子的：@4000000052f88ea32489532c。我目前只知道常见应用中， qmail 会用这个格式。
5. Joda-Time 库:Logstash 内部使用了 Java 的 Joda 时间库来作时间处理。所以我们可以使用 Joda 库所支持的时间格式来作具体定义。


下面我们写一个 Joda 时间格式的配置作为示例：
```
filter {
    grok {
        match => ["message", "%{HTTPDATE:logdate}"]
    }
    date {
        match => ["logdate", "dd/MMM/yyyy:HH:mm:ss Z"]
    }
}
```
注意：时区偏移量只需要用一个字母 Z 即可。

时区问题


#### grok 正则捕获
grok是Logstash最重要的插件, 可以在grok预定义号命名的正则表达式, 以后引用

##### 正则表达式语法
grok里可以写标准正则,如:
`\s+(?<request_time>\d+(?:\.\d+)?)\s+`

现在给我们的配置文件添加第一个过滤器区段配置。配置要添加在输入和输出区段之间(logstash 执行区段的时候并不依赖于次序，不过为了自己看得方便，还是按次序书写吧)：
```
input {
    stdin{
        }
}

filter{
    grok {
        match => {
            "message" => "\s+(?<request_time>\d+(?:\.\d+)?)\s+"
        }
    }
}
output {
    stdout {
        codec => rubydebug
    }
}
```

运行logstash进程输入 "begin 123.456 end", 会输出:
```
{
         "message" => "begin 123.456 end",
        "@version" => "1",
      "@timestamp" => "2014-08-09T11:55:38.186Z",
            "host" => "raochenlindeMacBook-Air.local",
    "request_time" => "123.456"
}
```
漂亮！不过数据类型好像不太满意……request_time 应该是数值而不是字符串。
我们已经提过稍后会学习用 LogStash::Filters::Mutate 来转换字段值类型，不过在 grok 里，其实有自己的魔法来实现这个功能！

**Grok表达式语法**:
**最佳实践**:
实际运用中，我们需要处理各种各样的日志文件，如果你都是在配置文件里各自写一行自己的表达式，就完全不可管理了。所以，我们建议是把所有的 grok 表达式统一写入到一个地方。然后用 filter/grok 的 `patterns_dir` 选项来指明。
如果你把 "message" 里所有的信息都 grok 到不同的字段了，数据实质上就相当于是重复存储了两份。所以你可以用 `remove_field` 参数来删除掉 message 字段，或者用 `overwrite` 参数来重写默认的 message 字段，只保留最重要的部分。
重写参数的示例如下：
```
filter {
    grok {
        patterns_dir => "/path/to/your/own/patterns"
        match => {
            "message" => "%{SYSLOGBASE} %{DATA:message}"
        }
        overwrite => ["message"]
    }
}
```


**多行匹配**

在和` codec/multiline` 搭配使用的时候，需要注意一个问题，grok 正则和普通正则一样，默认是不支持匹配回车换行的。就像你需要 `=~ //m `一样也需要单独指定，具体写法是在表达式开始位置加 (?m) 标记。如下所示：
```
match => {
    "message" => "(?m)\s+(?<request_time>\d+(?:\.\d+)?)\s+"
}
```
**多项选择**

有时候我们会碰上一个日志有多种可能格式的情况。这时候要写成单一正则就比较困难，或者全用 `|` 隔开又比较丑陋。这时候，logstash 的语法提供给我们一个有趣的解决方式。
文档中，都说明 logstash/filters/grok 插件的 match 参数应该接受的是一个 Hash 值。但是因为早期的 logstash 语法中 Hash 值也是用 [] 这种方式书写的，所以其实现在传递 Array 值给 match 参数也完全没问题。所以，我们这里其实可以传递多个正则来匹配同一个字段：
```
match => [
    "message", "(?<request_time>\d+(?:\.\d+)?)",
    "message", "%{SYSLOGBASE} %{DATA:message}",
    "message", "(?m)%{WORD}"
]
```
logstash 会按照这个定义次序依次尝试匹配，到匹配成功为止。虽说效果跟用 | 分割写个大大的正则是一样的，但是可阅读性好了很多。

#### GeoIP地址查询
GeoIP 是最常见的免费 IP 地址归类查询库，同时也有收费版可以采购。GeoIP 库可以根据 IP 地址提供对应的地域信息，包括国别，省市，经纬度等，对于可视化地图和区域统计非常有用。

**配置示例**
```
filter {
    geoip {
        source => "message"
    }
}
```

```json
{
       "message" => "183.60.92.253",
      "@version" => "1",
    "@timestamp" => "2014-08-07T10:32:55.610Z",
          "host" => "raochenlindeMacBook-Air.local",
         "geoip" => {
                      "ip" => "183.60.92.253",
           "country_code2" => "CN",
           "country_code3" => "CHN",
            "country_name" => "China",
          "continent_code" => "AS",
             "region_name" => "30",
               "city_name" => "Guangzhou",
                "latitude" => 23.11670000000001,
               "longitude" => 113.25,
                "timezone" => "Asia/Chongqing",
        "real_region_name" => "Guangdong",
                "location" => [
            [0] 113.25,
            [1] 23.11670000000001
        ]
    }
}
```


**配置说明**

GeoIP 库数据较多，如果你不需要这么多内容，可以通过 `fields` 选项指定自己所需要的。下例为全部可选内容：
```
filter {
    geoip {
        fields => ["city_name", "continent_code", "country_code2", "country_code3", "country_name", "dma_code", "ip", "latitude", "longitude", "postal_code", "region_name", "timezone"]
    }
}
```
需要注意的是：`geoip.location` 是 logstash 通过 latitude 和 longitude 额外生成的数据。所以，如果你是想要经纬度又不想重复数据的话，应该像下面这样做：
```
filter { 
    geoip { 
        fields => ["city_name", "country_code2", "country_name", "latitude", "longitude", "region_name"] 
        remove_field => ["[geoip][latitude]", "[geoip][longitude]"]
         } 
} 
```

geoip 插件的 "source" 字段可以是任一处理后的字段，比如 "client_ip"，但是字段内容却需要小心！geoip 库内只存有公共网络上的 IP 信息，查询不到结果的，会直接返回 null，而 logstash 的 geoip 插件对 null 结果的处理是：不生成对应的 geoip.字段。+

所以读者在测试时，如果使用了诸如 127.0.0.1, 172.16.0.1, 182.168.0.1, 10.0.0.1 等内网地址，会发现没有对应输出！

#### Json编码

#### key-value切分

#### metrics统计

#### mutate数据修改

#### 使用ruby处理

#### split切分事件


### 输出插件

#### 保存进 Elasticsearch
Logstash 可以使用不同的协议实现完成将数据写入 Elasticsearch 的工作。在不同时期，也有不同的插件实现方式。本节以最新版为准，即主要介绍 HTTP 方式。同时也附带一些原有的 node 和 transport 方式的介绍。

配置实例:
```
output{
    elasticsearch {
        hosts => ["192.168.8.12:9200"]
        index => "logstash-%{type}-%{+YYYY.MM.dd}"
        document_type => "%{type}"
        workers => 1
        flush_size => 20000
        idle_flush_time => 10
        template_overwrite => true
    }
}
```
解释

**批量发送**
`flush_size` 和 `idle_flush_time` 共同控制 Logstash 向 Elasticsearch 发送批量数据的行为。以上面示例来说：Logstash 会努力攒到 20000 条数据一次性发送出去，但是如果 10 秒钟内也没攒够 20000 条，Logstash 还是会以当前攒到的数据量发一次。

默认情况下，flush_size 是 500 条，`idle_flush_time` 是 1 秒。这也是很多人改大了 flush_size 也没能提高写入 ES 性能的原因——Logstash 还是 1 秒钟发送一次。
索引名

写入的 ES 索引的名称，这里可以使用变量。为了更贴合日志场景，Logstash 提供了 `%{+YYYY.MM.dd}` 这种写法。在语法解析的时候，看到以` + `号开头的，就会自动认为后面是时间格式，尝试用时间格式来解析后续字符串。所以，之前处理过程中不要给自定义字段取个加号开头的名字

此外，注意索引名中`不能有大写字母`，否则 ES 在日志中会报 `InvalidIndexNameException`，但是 Logstash 不会报错，这个错误比较隐晦，也容易掉进这个坑中。


input {
  file {
     path => "/var/log/messages"
     type => "system"
     start_position => "begining"
}
}

output{
  elasticsearch {
     host => [""]
     index => "system-%{}"
}

}




