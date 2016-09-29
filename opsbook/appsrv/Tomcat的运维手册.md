# Tomcat 运维手册
---

## Tomcat的安装

这里使用的tomcat是使用[官网][http://tomcat.apache.org]上下载的Tomcat, 不是通过YUM或者APT安装的方式

### Linux下的安装

1. 直接使用
直接下载Tomcat的源码包(tar或者zip), 解压到/opt目录下.
```bash
wget http://mirror.bit.edu.cn/apache/tomcat/tomcat-7/v7.0.69/bin/apache-tomcat-7.0.69.tar.gz

tar -xf apache-tomcat-7.0.69.tar.gz -C /opt
ln -s /opt/apache-tomcat-7.0.69 /opt/tomcat

```

### Windows的安装

1. 使用安装包安装.
   使用官网上的带有服务的安装包安装.(略)

2. 使用源码安装包安装
  1. 从官网上下载源码包
  2. 在相应系统的目录里解压
  3. 如果需要安装成windows服务模式(避免用户注销时,tomcat的退出)
  4. 在cmd下进入Tomcat的bin目录下,运行`services.bat install` ,这样可以在windows的服务里找到tomcat

## Tomcat的结构介绍

- bin, 启动,关闭,以及其他的脚本程序
- conf, 配置文件目录, 主要是`server.xml`
- logs, 日志文件路径,主要是access_log和catalina.out
- webapps, 默认的代码路径, 实际情况下不会放在这个下面
- lib, 确保目录下的 JAR-file 对于所有 webapp 都有效。默认安装包括 servlet-api.jar（Servlet），jasper.jar（JSP）和 jasper-el.jar（EL）。外部的 JAR 文件也可以放在这里，如 MySQL JDBC 驱动（mysql-connector-java-5.1.{xx}-bin.jar )和 JSTL（jstl.jar 和 standard.jar）
- work, 运行的用户的程序,JSP编译的路径, 有时停止是需要清理
- temp, 临时文件目录


## Tomcat相关文件的介绍
- bin/{startup.sh, shutdown.sh, startup.bat, shutdown.bat}, Linux,Windows下相应的启动关闭问价
- bin/catalina.sh/bat, Tomcat主要的启动文件, `startup`主要是调用此文件,一些相关启动配置可以在这个文件中配置.

- conf/server.xml, tomcat主要的配置文件
- conf/tomcat-user.xml, 授权和访问控制用户名，密码和角色数据库
- conf/catalina.policy 提供特殊的安全策略

### server.xml介绍
详情建`tomcat的server.xml文件介绍`.

## Tomcat的一般配置


## Tomcat的优化
如何修改配置呢，在/tomcat的/bin/下面有个脚本文件catailna.sh。 如果 windows 是bat设置tomcat的使用内存，其实就是设置jvm的使用参数。

###　Tomcat内存优化
Tomcat内存优化主要是对 tomcat 启动参数优化，我们可以在 tomcat 的启动脚本 catalina.sh 中设置 JAVA_OPTS 参数。

1.JAVA_OPTS参数说明
>
 `-server`   启用jdk 的 server 版；
 `-Xms`      java虚拟机初始化时的最小内存；
 `-Xmx`      java虚拟机可使用的最大内存；
 `-XX:PermSize`    内存永久保留区域
 `-XX:MaxPermSize`   内存最大永久保留区域

设置Tomcat启动的初始内存，其初始空间(即-Xms)是物理内存的1/64，最大空间(-Xmx)是物理内存的1/4。可以利用JVM提供的-Xmn -Xms -Xmx等选项，要加`m`说明是`MB`，否则就是KB了，在启动tomcat时会报内存不足。

> -Xms：初始值  【初始化内存大小】
 -Xmx：最大值  【可以使用的最大内存】
 -Xmn：最小值

 >JVM堆的设置是指java程序运行过程中JVM可以调配使用的内存空间的设置.JVM在启动的时候会自动设置Heap size的值，其初始空间(即-Xms)是物理内存的1/64，最大空间(-Xmx)是物理内存的1/4。可以利用JVM提供的-Xmn -Xms -Xmx等选项可进行设置。Heap size 的大小是Young Generation 和Tenured Generaion 之和。 

提示：`在JVM中如果98％的时间是用于GC且可用的Heap size 不足2％的时候将抛出此异常信息。`

__提示__：`Heap Size` 最大不要超过可用物理内存的80％，一般的要将`-Xms`和`-Xmx`选项设置为相同，而`-Xmn`为1/4的`-Xmx值`。 这两个值的大小一般根据需要进行设置。初始化堆的大小执行了虚拟机在启动时向系统申请的内存的大小。一般而言，这个参数不重要。但是有的应用 程序在大负载的情况下会急剧地占用更多的内存，此时这个参数就是显得非常重要，如果虚拟机启动时设置使用的内存比较小而在这种情况下有许多对象进行初始化，虚拟机就必须重复地增加内存来满足使用。由于这种原因，我们一般把`-Xms和-Xmx设为一样大，而堆的最大值受限于系统使用的物理内存`。一般使用数 据量较大的应用程序会使用持久对象，内存使用有可能迅速地增长。当应用程序需要的内存超出堆的最大值时虚拟机就会提示内存溢出，并且导致应用服务崩溃。因 此一般建议`堆的最大值设置为可用内存的最大值的80%`。

- 如果系统花费很多的时间收集垃圾,请减小堆大小。一次完全的垃圾收集应该不超过 3-5 秒。如果垃圾收集成为瓶颈，那么需要指定代的大小，检查垃圾收集的详细输出，研究 垃圾收集参数对性能的影响。一般说来，你应该使用物理内存的 80% 作为堆大小。当增加处理器时，记得增加内存，因为分配可以并行进行，而垃圾收集不是并行的。
- 在重启你的Tomcat服务器之后，这些配置的更改才会有效。

Windows在文件`{tomcathome}/bin/catalina.bat`，Unix在文件`{tomcathome}/bin/catalina.sh`的前面，增加如下设置：
服务器参数配置
tomcat默认：
```bash
 -Xms1024m -Xmx1024m -Xss1024K -XX:PermSize=128m -XX:MaxPermSize=256m
```
__Java_OPTS参数__
```
JAVA_OPTS="-Djava.awt.headless=true -Dfile.encoding=UTF-8
-server -Xms2048m -Xmx2048m
-XX:NewSize=512m -XX:MaxNewSize=512m -XX:PermSize=512m
-XX:MaxPermSize=512m -XX:+DisableExplicitGC"
```

配置完成后可重启Tomcat ，通过以下命令进行查看配置是否生效：

1.首先查看Tomcat 进程号：
   `ps -ef | grep tomcat`
  我们可以看到Tomcat 进程号是 `9217` 

2.查看是否配置生效：
  `sudo jmap –heap 9217`
  我们可以看到`MaxHeapSize` 等参数已经生效。


### Tomcat并发优化

#### Tomcat连接相关参数
在Tomcat配置文件conf下面 server.xml 中的配置中和连接数相关的参数有

`minProcessors`：最小空闲连接线程数，用于提高系统处理性能，默认值为10
`maxProcessors`：最大连接线程数，即：并发处理的最大请求数，默认值为75
`acceptCount`：允许的最大连接数，应大于等于maxProcessors，默认值为100
`enableLookups`：是否反查域名，取值为：true或false。为了提高处理能力，应设置为false
`connectionTimeout`：网络连接超时，单位：毫秒。设置为0表示永不超时，这样设置有隐患的。通常可设置为30000毫秒。


一般设置为:

```
<Connector port=“8080" protocol="org.apache.coyote.http11.Http11NioProtocol"
  maxThreads="600"
  minSpareThreads="100"
  maxSpareThreads="500"
  acceptCount="700"
  connectionTimeout="20000"
  redirectPort="8443" />
```
这样设置以后，基本上没有再当机过。
`protocol="org.apache.coyote.http11.Http11NioProtocol`"使用java的异步io护理技术,no blocking IO

`maxThreads="600"` 表示最多同时处理600个连接 最大线程数
minSpareThreads=`100` 表示即使没有人使用也开这么多空线程等待  初始化时创建的线程数
`maxSpareThreads="500"` 表示如果最多可以空500个线程，例如某时刻有505人访问，之后没有人访问了，则tomcat不会保留505个空线程，而是关闭505个空的。  一旦创建的线程超过这个值，Tomcat就会关闭不再需要的socket线程。

`acceptCount="700"` 指定当所有可以使用的处理请求的线程数都被使用时，可以放到处理队列中的请求数，超过这个数的请求将不予处理

这里是http connector的优化，如果使用apache和tomcat做集群的负载均衡，并且使用ajp协议做apache和tomcat的协议转发，那么还需要优化ajp connector。
```
<Connector port="8009" protocol="AJP/1.3" maxThreads="600" minSpareThreads="100" maxSpareThreads="500" acceptCount="700" connectionTimeout="20000" redirectPort="8443" />
```

### 与nginx和或者httpd结合使用
  使用ngnix或者httpd结合使用, 把静态文件交给nginx或者httpd处理, tomcat只负责处理香瓜你的动态请求, 减小Tomcat的压力.

  具体见`tomcat与httpd的整合配置`, `tomcat与nginx整合配置`

### 使用 Server JRE 替代JDK

服务器上不要安装JDK，请使用 Server JRE. 服务器上根本不需要编译器，代码应该在Release服务器上完成编译打包工作。

理由：`一旦服务器被控制，可以防止在其服务器上编译其他恶意代码并植入到你的程序中。`

### 虚拟主机
不要使用Tomcat的虚拟主机，每个站点一个实例。即，启动多个tomcat.

这也是PHP运维在这里常犯的错误，PHP的做法是一个Web下面放置多个虚拟主机，而不是每个主机启动一个web服务器。Tomcat 是多线程,共享内存，任何一个虚拟主机中的应用出现崩溃，会影响到所有应用程序。采用多个实例方式虽然开销比较大，但保证了应用程序隔离与安全。

## 安全配置
1. 安装后初始化配置
  当Tomcat完成安装后你首先要做的事情如下：
  首次安装完成后立即删除webapps下面的所有代码
  `rm -rf /srv/apache-tomcat/webapps/*`
            
  注释或删除 tomcat-users.xml 所有用户权限，看上去如下：

``` xml
# cat conf/tomcat-users.xml
<?xml version='1.0' encoding='utf-8'?>
<tomcat-users>
</tomcat-users>
```

2.隐藏版本信息

```xml
vim $CATALINA_HOME/conf/server.xml

    <Connector port="80" protocol="HTTP/1.1"
               connectionTimeout="20000"
               redirectPort="8443"
                maxThreads="8192"
                minSpareThreads="64"
                maxSpareThreads="128"
                acceptCount="128"
                enableLookups="false"
                server="Neo App Srv 1.0"/>
```
```
# curl -I http://localhost:8080/
HTTP/1.1 400 Bad Request
Transfer-Encoding: chunked
Date: Thu, 20 Oct 2011 09:51:55 GMT
Connection: close
Server: Neo App Srv 1.0
```

  服务器信息已经被改为 Server: Neo App Srv 1.0

3. 应用程序安

关闭war自动部署 `unpackWARs="false" autoDeploy="false"`。防止被植入木马等恶意程序

关闭 `reloadable="false"` 也用于防止被植入木马

4. 启动Tomcat帐号
  建议建立一个Tomcat帐号,专门用来启动tomcat, 禁止使用root用户

5. 修改`shutdown`端口, 禁止外面的访问


## Tomcat使用中常见的故障

### Tomcat的JVM提示内存溢出
查看`%TOMCAT_HOME%\logs`文件夹下，日志文件是否有内存溢出错误

### 修改Tomcat的JVM

1. 错误提示：`java.lang.OutOfMemoryError: Java heap space`
  Tomcat默认可以使用的内存为128MB，在较大型的应用项目中，这点内存是不够的，有可能导致系统无法运行。常见的问题是报Tomcat内存溢出错误，`Out of Memory`(系统内存不足)的异常，从而导致客户端显示500错误，一般调整Tomcat的使用内存即可解决此问题。

  1. windows环境下修改
   `%TOMCAT_HOME%\bin\catalina.bat`文件，在文件开头增加如下设置：`JAVA_OPTS=-Xms2048m -Xmx2048m`
  
  2. Linux环境下修改
  `%TOMCAT_HOME%\bin\catalina.sh`文件，在文件开头增加如下设置：`JAVA_OPTS=-Xms2048m -Xmx2048m`
  
  其中，-Xms设置初始化内存大小，-Xmx设置可以使用的最大内存。


2. 错误提示：`java.lang.OutOfMemoryError: PermGen space`
  PermGen space的全称是Permanent Generation space,是指内存的永久保存区域，这块内存主要是被JVM存
  放Class和Meta信息的,Class在被Loader时就会被放到PermGen space中，它和存放类实例(Instance)的Heap区域不同,GC(Garbage Collection)不会在主程序运行期对PermGen space进行清理，所以如果你的应用中有很CLASS的话,就很可能出现PermGen space错误，这种错误常见在web服务器对JSP进行pre compile的时候。如果你的WEB APP下都用了大量的第三方jar, 其大小超过了jvm默认的大小(4M)那么就会产生此错误信息了。

  1. 解决方法：
  在catalina.bat/catalina.bat的第一行增加：
`set JAVA_OPTS=-Xms64m -Xmx256m -XX:PermSize=128M -XX:MaxNewSize=256m - XX:MaxPermSize=256m`
  在catalina.sh的第一行增加：
`JAVA_OPTS=-Xms64m -Xmx256m -XX:PermSize=128M -XX:MaxNewSize=256m  XX:MaxPermSize=256m`

3.不能使用80端口问题
  3.1. 使用nginx, 或者httpd结合处理
  3.2. 使用iptables转发`iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080`

4.windows tomcat `java.net.SocketException: select failed`
>  
java.net.SocketException: select failed
at java.net.PlainSocketImpl.socketAccept(Native Method)
at java.net.PlainSocketImpl.accept(PlainSocketImpl.java:384)
at java.net.ServerSocket.implAccept(ServerSocket.java:453)
at java.net.ServerSocket.accept(ServerSocket.java:421)
at org.apache.tomcat.util.net.DefaultServerSocketFactory.acceptSocket(DefaultServerSocketFactory.java:61)
at org.apache.tomcat.util.net.JIoEndpoint$Acceptor.run(JIoEndpoint.java:317)
at java.lang.Thread.run(Thread.java:619)

这一串启动异常,而且是刷屏的出现,网上也有很多解决方法,比如卸载IPV6,重装TCP/IP协议啊,依旧不行,卸载网卡重装了也不行.有个`修复LSP的功能,点击修复后,异常解除.`
需要为tomcat添加额外的启动参数：`-Djava.net.preferIPv4Stack=true` .

## Linux把tomcat做成服务


[http://tomcat.apache.org]: 


[][参考]
[参考]: http://www.sysopen.cn/20165012/

