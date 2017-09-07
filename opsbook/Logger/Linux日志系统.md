# Linux日志系统
---

相关的rsyslogd
在centos7 里由journald管理rsyslogd服务.




日志切割相关
/etc/logrotate.conf
/etc/logrotate.d/

## rsyslog

### rsyslog 基础配置
/etc/rsyslog.conf
日志分为全局, 模块,规则(过滤filter, 动作action) 组成

#### filter
filter可以过滤出特定的信息, action是对信息的处理.
rsyslog提供各种过滤规则.


Facility/Priority-based filters
Facility确定是哪个一部分的日志, 比如kern (0), user (1), mail (2), daemon (3), auth (4), syslog (5), lpr (6), news (7), uucp (8), cron (9), authpriv (10), ftp (11), and local0 through local7 (16 - 23).

Priority-based: debug (7), info (6), notice (5), warning (4), err (3), crit (2), alert (1), and emerg (0).
```
FACILITY.PRIORITY
```

如果是规则使用"="指定话, 会忽略其他规则, "!为除外的意思.
"*"为全部的规则. 多个规则指定是时, 使用","或者分号.

#### 实例
```
kern.*
mail.crit
cron.!info, !debug

```

#### 基于属性过滤(Property-based filters)

基于属性的规则过滤可以使用任何的属性比如"timegenerated" or "syslogtag"过滤.  可以比较每一个指定特殊值的属性进行比较, 属性比较大小写敏感.

```
:PROPERTY,[!]COMPARE_OPERATION, "STRING"
```

`PROPERTY`: 指定属性
`[!]`: 否定比较
`COMPARE_OPERATION`: 比较操作符: contains(contains_i), isequal(isequal), startswith(startswith_i),regex, ereregex, isempty

#### 基于属性的过滤的实例
```
:msg, contains, "error"

:hostname, isequal, "host1"

:msg, !regex, "fatal .* error"
```
#### 扩展正则
```
if expression then action esle action

$msg startswith 'DEVNAME' or $syslogfacility-text == 'local0'
```

```
if $progoramname = 'prog1' then {
    action(type="omfile" file="/var/log/prog1.log")
    if $msg contains 'test' then
       action(type="omfile" file="/var/log/prog1tet.log")
    else
    action(type="omfile" file="/var/log/pro1notest.log")
}
```

### actions
处理filter匹配的信息

- 1.保存信息到文件
```
filter path
# 
cron.* /var/log/cron.log
```
默认的情况下保存信息到file是同步操作, 可以是时候用"-"来取消同步刷新磁盘

`FILTER ?DynamicFile`: 使用动态文件进行存储.

```
$template DynamicFile,"/var/log/test_logs/%timegenerated%-test.log"
#使用属性timegenerated

*.* ?DynamicFile

```


如果指定文件为终端或者/dev/console设备, 那么信息将会以标准输出方式输出

- 2.通过网络进行保存
`@[(zNUMBER)] HOST:[PORT]`: @表示为使用udp @@为tcp
**zNUMBER** 使用zlib 进行压缩,NUMBER为压缩的级别
```
*.* @192.168.8.1
*.* @@192.168.8.1:6514
*.* @(z9)[2001:db8::1]
```

**输出 Output channel**

`$outchannel NAME, FILE_NAME, MAX_SIZE, ACTION`

`NAME`, channel名称
`FILE_NAME`, 只能是文件, 不能是其他(pipe,终端等)
`MAX_SIZE`, 最大值 bytes

```
FILTER :mfile:$NAME
```
####输出轮训
定义channel
```
$outchannel log_rotation, /var/log/test_log.log, 1048576600, /home/joe/log_ratation_script

```

```
*.* :omfile:$log_rotation
```

- 3.发送到指定用户
- 4.执行程序
`*.* ^test-program;template`
- 5.存储到数据库
`:PLUGIN:DB_HOST,DB_NAME,DB_USER,DB_PASSWORD;[TEMPLATE]`
需要导入ommysql
```
$ModLoad ommysql    # Output module for MySQL support
$ModLoad ompgsql    # Output module for PostgreSQL support
```

- 6.丢弃日志
`FILTER ~`
`cron.* ~`

### 指定多个action
```
FILTER ACTION
& ACTION
& ACTION
```

```
kern.=crit user1
& ^test-program;temp
& @192.168.0.1
```

### 模板 Teamplates
输出模板
定义
```
$teamlate TEAMPLATE_NAME, "text %PROPERTY% more text", [OPTION]
```

`%`
`OPTION` 指定模板修改功能的任何选项, 支持sql或者stdsql

#### 属性Properties
`%PROPERTY_NAME[:FROM_CHAR:TO_CHAR:OPTION]%`
```
%msg%
%msg:1:2%
%msg:::drop-last-lf%
%timegenerated:1:10:date-rfc3339%
```
#### Templates 实例
```
$template verbose,  "%syslogseverity%, %syslogfacility%, %timegenerated%, %HOSTNAME%, %syslogtag%, %msg%\n"

#. A wall message template
$template wallmsg,"\r\n\7Message from syslogd@%HOSTNAME% at %timegenerated% ...\r\n %syslogtag% %msg%\n\r"


$template dbFormat,"insert into SystemEvents (Message, Facility, FromHost, Priority, DeviceReportedTime, ReceivedAt, InfoUnitID, SysLogTag) values ('%msg%', %syslogfacility%, '%HOSTNAME%', %syslogpriority%, '%timereported:::date-mysql%', '%timegenerated:::date-mysql%', %iut%, '%syslogtag%')", sql

# debugformat

"Debug line with all properties:\nFROMHOST: '%FROMHOST%', fromhost-ip: '%fromhost-ip%', HOSTNAME: '%HOSTNAME%', PRI: %PRI%,\nsyslogtag '%syslogtag%', programname: '%programname%', APP-NAME: '%APP-NAME%', PROCID: '%PROCID%', MSGID: '%MSGID%',\nTIMESTAMP: '%TIMESTAMP%', STRUCTURED-DATA: '%STRUCTURED-DATA%',\nmsg: '%msg%'\nescaped msg: '%msg:::drop-cc%'\nrawmsg: '%rawmsg%'\n\n\"


```

### Centos7 新版本的rsyslog语法

#### RainerScript 
input() and ruleset()
