# 远程执行
---

## Grains
* 信息查询
  * salt  '*' grains.ls items
* 匹配执行, 匹配minion
  - salt -G os:CentOS cmd.run 'w'
* 通过配置文件, 自定义grains
* 在 client 端设置

## pillar
给 minion 指定 想要的数据, 在master配置
`salt `

master
pillar_roots:
  base:
    - /srv/pillar

## Grains 与 Pillar 区别
* grains minion 端 静态数据, minion 启动时手机, 存储基本数据
* Pillar Master 动态数据, saltutil.refresh_pillar 刷新, 用于敏感数据







salt 目标 模块 命令
```
salt '<target>' <function> [arguments]
```

##  目标
salt '*' [ options ] sys.doc

salt -E '.*' [ options ] sys.doc cmd

salt -G 'os:Arch.*' [ options ] test.ping

salt -C 'G@os:Arch.* and webserv* or G@kernel:FreeBSD' [ options ] test.ping

```

salt '*' test.ping
salt '*.example.net' test.ping
salt '*.example.*' test.ping

salt 'web?.example.net' test.ping
salt 'web[1-5]' test.ping
salt 'web[1,3]' test.ping
salt 'web-[x-z]' test.ping

## pcre
salt -E 'web1-(prod|devel)' test.ping

base:
  'web1-(prod|devel)':
  - match: pcre
  - webserver

## List
salt -L 'web1,web2,web3' test.ping

## grains
salt -G 'os:CentOS' test.ping
salt -G 'cpuarch:x86_64' grains.item num_cpus
salt -G 'ec2_tags:environment:*production*'


## pillar
salt -I 'somekey:specialvalue' test.ping
salt -I 'foo:bar:baz*' test.ping

## ipcdr

salt -S 192.168.40.20 test.ping
salt -S 10.0.0.0/24 test.ping

salt -C 'S@10.0.0.0/24 and G@os:Debian' test.ping

'172.16.0.0/12':
   - match: ipcidr
   - internal
```




Target Selection
-E, --pcre
       The target expression will be interpreted as a PCRE regular expression rather than a shell glob.

-L, --list
       The target expression will be interpreted as a comma-delimited list; example: server1.foo.bar,server2.foo.bar,example7.quo.qux

-G, --grain
       The target expression matches values returned by the Salt grains system on the minions. The target expression is in the format of '<grain value>:<glob expression>'; example: 'os:Arch*'

       This was changed in version 0.9.8 to accept glob expressions instead of regular expression. To use regular expression matching with grains, use the --grain-pcre option.

--grain-pcre
    The target expression matches values returned by the Salt grains system on the minions. The target expression is in the format of '<grain value>:< regular expression>'; example: 'os:Arch.*'

-N, --nodegroup
       Use a predefined compound target defined in the Salt master configuration file.

-R, --range
       Instead of using shell globs to evaluate the target, use a range expression to identify targets. Range expressions look like %cluster.

       Using the Range option requires that a range server is set up and the location of the range server is referenced in the master configuration file.

-C, --compound
       Utilize many target definitions to make the call very granular. This option takes a group of targets separated by and or or. The default matcher is a glob as usual. If something other than a
       glob is used, preface it with the letter denoting the type; example: 'webserv* and G@os:Debian or E@db*' Make sure that the compound target is encapsulated in quotes.

-I, --pillar
       Instead of using shell globs to evaluate the target, use a pillar value to identify targets. The syntax for the target is the pillar key followed by a glob expression: "role:production*"

-S, --ipcidr
              Match based on Subnet (CIDR notation) or IPv4 address.


### 复合指定
关键词 `and`, `or`, `not`


|Letter  |Match Type|  实例：|是否支持分割?|
|---|----|---|---|
|G |  Grains glob |G@os:Ubuntu |Yes|
|E |  PCRE Minion ID | E@web\d+\.(dev|qa|prod)\.loc|    No|
|P |  Grains PCRE |P@os:(RedHat|Fedora|CentOS)| Yes|
|L |  List of minions |L@minion1.example.com,minion3.domain.com or bl*.domain.com|  No|
|I |  Pillar glob| I@pdata:foobar|  Yes|
|J |  Pillar PCRE |J@pdata:^(foo|bar)$ |Yes|
|S|   Subnet/IP address |  S@192.168.1.0/24 or S@192.168.1.100| No|
|R |  Range cluster  | R@%foo.bar | No|

```bash
salt -C 'webserv* and G@os:Debian or E@web-dc1-srv.*' test.ping

base:
  'webserv* and G@os:Debian or E@web-dc1-srv.*':
    - match: compound
    - webserver

salt -C 'not web-dc1-srv' test.ping
salt -C '* and not G@kernel:Darwin' test.ping
salt -C '* and not web-dc1-srv' test.ping
```

### 优先匹配
```bash
salt -C '( ms-1 or G@id:ms-3 ) and G@id:ms-3' test.ping

```

### 交替分隔符
```
salt -C 'J|@foo|bar|^foo:bar$ or J!@gitrepo!https://github.com:example/project.git' test.ping
```

### 正则表达式

`salt -E '(httpd|java)_serv'  test.ping `

top.sls:
```
base:
   (httpd|java)_serv:
     - match: pcre
```

### List

## grains

## pillar

salt '*' saltutil.refresh_pillar

设置pillar值

salt '*' state.highstate pillar={'cheese': 'spam'}

pillar的主目录下的top.sls
```yaml
#top.sls
base:      # 指定环境
  '*':     # target
    - packages  # 引用packages.sls或者packages/init.sls
    - service  #引用services.sls 或者servives/init.sls


#packages.sls
zabbix:
  package-name: zabbix
  version: 2.2.4

# services.sls
zabbix:
  port: 10050
  user: admin
```

###  查看pillar 的相关模块
`salt '*' sys.list_functions pillar`
`salt '*' sys.doc pillar`


### 查看刚定义的pillar
`salt 'Minion' pillar.item zabbix`



## states
states 模块列表
```
salt '*' sys.list_state_modules
```

```yaml
#cat /src/salt/top.sls
base:              #base环境
  '*':           #Target(代表所有Traget)
    - one      #引用one.sls或者one/init.sls states文件
  'Minion':      #Target(代表匹配Minion)        
    - tow      #引用tow.sls或者tow/init.sls states文件    
  'Minion1':     #Target(代表批量Minion1)        
    - three    #引用three.sls或者three/init.sls states
```

然后我们新建三个states文件：one.sls、tow.sls、three.sls，最后我们就可以使用state.highstate命令同时对Minion和Min-ion1两台机器进行配置管理了。

## 节点组的配置
`master`

```
nodegroups:
  group1: 'L@foo.domain.com,bar.domain.com,baz.domain.com or bl*.domain.com'
  group2: 'G@os:Debian and foo.domain.com'
  group3: 'G@os:Debian and N@group1'
  group4:
    - 'G@foo:bar'
    - 'or'
    - 'G@foo:baz'
```

```
salt -N group1 test.ping
base:
  group1:
    - match: nodegroup
    - webserver

```


## 批量更新, 每次更新多少
```
salt '*' -b 10 test.ping

salt -G 'os:RedHat' --batch-size 25% apache.signal restart
```


 salt '*' state.highstate

