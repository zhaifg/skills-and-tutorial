# yimi 腾讯云测试环境

## 所涉及的应用
- memcached
- mongodb
- mysql
- nginx
- tomcat
- java

`JAVA_HOME=/usr/java/jdk1.7.0_45/`

## memcached
```
/usr/local/memcached/bin/memcached -u daemon -d -m 256 -l 127.0.0.1 -p 11211 -vv
```


## mongodb 

`/usr/local/mongodb/bin`
`start.sh`
```
/usr/local/mongo
./mongod --dbpath /mnt/xvdb1/mongodata --logpath /mnt/xvdb1/yimilogs/mongodb/logs --fork --port 27017 --auth
```


## activemq

`/disk/activemq`

```
/usr/java/jdk1.7.0_45//bin/java -Xms1G -Xmx1G -Djava.util.logging.config.file=logging.properties -Dcom.sun.management.jmxremote -Djava.io.tmpdir=/mnt/xvdb1/activemq/tmp -Dactivemq.classpath=/mnt/xvdb1/activemq/conf; -Dactivemq.home=/mnt/xvdb1/activemq -Dactivemq.base=/mnt/xvdb1/activemq -Dactivemq.conf=/mnt/xvdb1/activemq/conf -Dactivemq.data=/mnt/xvdb1/activemq/data -jar /mnt/xvdb1/activemq/bin/activemq.jar start
```

## openfire

```
/usr/java/jdk1.7.0_45/bin/java -server -Dinstall4j.jvmDir=/usr/java/jdk1.7.0_45 -Dexe4j.moduleName=/mnt/xvdb1/openfire0716/bin/openfire -DopenfireHome=/mnt/xvdb1/openfire0716/bin/../ -Dopenfire.lib.dir=/mnt/xvdb1/openfire0716/lib -Dinstall4j.launcherId=22 -Dinstall4j.swt=false -Di4j.vmov=true -Di4j.vmov=true -Di4j.vmov=true -Di4j.vmov=true -Di4j.vmov=true -Xmx1600M -Xms1600M -Xmn600M -XX:PermSize=64M -
XX:MaxPermSize=64M -Xss256K -XX:+DisableExplicitGC -XX:SurvivorRatio=8 -XX:+UseConcMarkSweepGC -XX:+UseParNewGC -XX:CMSInitiatingOccupancyFraction=80 -Di4j.v
pt=true -classpath /mnt/xvdb1/openfire0716/.install4j/i4jruntime.jar:/mnt/xvdb1/openfire0716/lib/activation.jar:/mnt/xvdb1/openfire0716/lib/bcpg-jdk15on.jar:
/mnt/xvdb1/openfire0716/lib/bcpkix-jdk15on.jar:/mnt/xvdb1/openfire0716/lib/bcprov-jdk15on.jar:/mnt/xvdb1/openfire0716/lib/bouncycastle.jar:/mnt/xvdb1/openfir
e0716/lib/commons-el.jar:/mnt/xvdb1/openfire0716/lib/hsqldb.jar:/mnt/xvdb1/openfire0716/lib/jasper-compiler.jar:/mnt/xvdb1/openfire0716/lib/jasper-runtime.ja
r:/mnt/xvdb1/openfire0716/lib/jdic.jar:/mnt/xvdb1/openfire0716/lib/jtds.jar:/mnt/xvdb1/openfire0716/lib/mail.jar:/mnt/xvdb1/openfire0716/lib/mysql.jar:/mnt/x
vdb1/openfire0716/lib/openfire.jar:/mnt/xvdb1/openfire0716/lib/postgres.jar:/mnt/xvdb1/openfire0716/lib/servlet.jar:/mnt/xvdb1/openfire0716/lib/slf4j-log4j12
.jar:/mnt/xvdb1/openfire0716/lib/startup.jar com.install4j.runtime.launcher.Launcher start org.jivesoftware.openfire.starter.ServerStarter
```



## iptables

```

*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT DROP [0:0]
#qiniu 七牛
-A INPUT -p tcp -m multiport --sport 80,6060 -j ACCEPT
-A OUTPUT -p tcp -m multiport --dport 80,6060 -j ACCEPT


#internet to 7070,6060
-A INPUT -p tcp -m multiport --dport 8080,6060,6070,81,7090,5678,11098 -j ACCEPT
-A OUTPUT -p tcp -m multiport --sport 8080,6060,6070,81,7090,5678,11098 -j ACCEPT

#local to baidu map
-A OUTPUT -d api.map.baidu.com -p tcp -m tcp --dport 80 -j ACCEPT
-A INPUT -s api.map.baidu.com -p tcp -m tcp --sport 80 -j ACCEPT


#console to 10096
-A OUTPUT -d 58.241.9.230/32 -p tcp -m multiport --sport 10096,10097 -j ACCEPT
-A INPUT -s 58.241.9.230/32 -p tcp -m multiport --dport 10096,10097 -j ACCEPT
-A OUTPUT -d 58.241.21.58/32 -p tcp -m multiport --sport 10096,10097 -j ACCEPT
-A INPUT -s 58.241.21.58/32 -p tcp -m multiport --dport 10096,10097 -j ACCEPT


#DNS
-A INPUT -p udp -m udp --sport 53 -j ACCEPT
-A OUTPUT -p udp -m udp --dport 53 -j ACCEPT

#ping
-A OUTPUT -p icmp -j ACCEPT
-A INPUT -p icmp -j ACCEPT

#loopback
-A INPUT -i lo -j ACCEPT
-A OUTPUT -o lo -j ACCEPT

#log mail
-A INPUT -p tcp -m tcp --sport 25 -j ACCEPT
-A OUTPUT -p tcp -m tcp --dport 25 -j ACCEPT
-A INPUT -p tcp -m tcp --sport 456 -j ACCEPT
-A OUTPUT -p tcp -m tcp --dport 456 -j ACCEPT
COMMIT

```
