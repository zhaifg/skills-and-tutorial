# Ｎgnix代理负载均衡缓存

标签（空格分隔）： Nginx

---

##一、配置反向代理
**1.nginx配置反向代理只需要`proxy_pass` 一个命令即可。**

```
location / {
        proxy_pass      http://192.168.18.201;
        proxy_set_header  X-Real-IP  $remote_addr; #加上这一行
}
```
指令说明：`proxy_pass`
语法：`proxy_pass UR`L
默认值：no       
使用字段：`location, location中的if字段   `    
这个指令设置被代理服务器的地址和被映射的URI，地址可以使用主机名或IP加端口号的形式，例如：proxy_pass http://localhost:8000/uri/;

指令说明：`proxy_set_header`
语法：`proxy_set_header header value `
默认值： `Host and Connection `
使用字段：`http, server, location `
这个指令允许将发送到被代理服务器的请求头重新定义或者增加一些字段。这个值可以是一个文本，变量或者它们的组合。proxy_set_header在指定的字段中没有定义时会从它的上级字段继承。

**2.httpd取得真实IP的配置**
`yum -y install mod_rapf`

`LogFormat "{X-Real-IP}i %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined`


##二、负载均衡

**1.upstream 负载均衡模块说明**
案例：
下面设定负载均衡的服务器列表。
```
upstream test.net{
ip_hash;
server 192.168.10.13:80;
server 192.168.10.14:80  down;
server 192.168.10.15:8009  max_fails=3  fail_timeout=20s;
server 192.168.10.16:8080;
}
server {
  location / {
    proxy_pass  http://test.net;
  }
}
```
upstream是Nginx的HTTP Upstream模块，这个模块通过一个简单的调度算法来实现客户端IP到后端服务器的负载均衡。在上面的设定中，通过upstream指令指定了一个负载均衡器的名称test.net。这个名称可以任意指定，在后面需要用到的地方直接调用即可。

**2.upstream 支持的负载均衡算法**
Nginx的负载均衡模块目前支持4种调度算法，下面进行分别介绍，其中后两项属于第三方调度算法。  
`轮询（默认）`。每个请求按时间顺序逐一分配到不同的后端服务器，如果后端某台服务器宕机，故障系统被自动剔除，使用户访问不受影响。Weight 指定轮询权值，Weight值越大，分配到的访问机率越高，主要用于后端每个服务器性能不均的情况下。
`ip_hash`。每个请求按访问IP的hash结果分配，这样来自同一个IP的访客固定访问一个后端服务器，有效解决了动态网页存在的session共享问题。
`fair`。这是比上面两个更加智能的负载均衡算法。此种算法可以依据页面大小和加载时间长短智能地进行负载均衡，也就是根据后端服务器的响应时间来分配请求，响应时间短的优先分配。Nginx本身是不支持fair的，如果需要使用这种调度算法，必须下载Nginx的upstream_fair模块。
`url_hash`。此方法按访问url的hash结果来分配请求，使每个url定向到同一个后端服务器，可以进一步提高后端缓存服务器的效率。Nginx本身是不支持url_hash的，如果需要使用这种调度算法，必须安装Nginx 的hash软件包。

**3.upstream 支持的状态参数**
在HTTP Upstream模块中，可以通过server指令指定后端服务器的IP地址和端口，同时还可以设定每个后端服务器在负载均衡调度中的状态。常用的状态有：      
`down`，表示当前的server暂时不参与负载均衡。
`backup`，预留的备份机器。当其他所有的非backup机器出现故障或者忙的时候，才会请求backup机器，因此这台机器的压力最轻。
`max_fails`，允许请求失败的次数，默认为1。当超过最大次数时，返回proxy_next_upstream 模块定义的错误。
`fail_timeout`，在经历了max_fails次失败后，暂停服务的时间。max_fails可以和fail_timeout一起使用。
注，当负载调度算法为ip_hash时，后端服务器在负载均衡调度中的状态不能是weight和backup。

4.实验拓扑
nginx --->apache01
      |----> apache02

**5.配置nginx负载均衡**
```
[root@nginx ~]# vim /etc/nginx/nginx.conf
upstream webservers {
      server 192.168.18.201 weight=1;
      server 192.168.18.202 weight=1;
  }
  server {
      listen       80;
      server_name  localhost;
      #charset koi8-r;
      #access_log  logs/host.access.log  main;
      location / {
              proxy_pass      http://webservers;
              proxy_set_header  X-Real-IP  $remote_addr;
      }
}
```
注，upstream是定义在server{ }之外的，不能定义在server{ }内部。定义好upstream之后，用proxy_pass引用一下即可。

**6.重新加载一下配置文件**
```
[root@nginx ~]# service nginx reload
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
重新载入 nginx：                                           [确定]
```

**7.测试一下**

注，大家可以不断的刷新浏览的内容，可以发现web1与web2是交替出现的，达到了负载均衡的效果。


**8.配置nginx进行健康状态检查**
`max_fails`，允许请求失败的次数，默认为1。当超过最大次数时，返回proxy_next_upstream 模块定义的错误。
`fail_timeout`，在经历了max_fails次失败后，暂停服务的时间。max_fails可以和fail_timeout一起使用，进行健康状态检查。
```
[root@nginx ~]# vim /etc/nginx/nginx.conf
upstream webservers {
        server 192.168.18.201 weight=1 max_fails=2 fail_timeout=2;
        server 192.168.18.202 weight=1 max_fails=2 fail_timeout=2;
    }
```

**9.配置backup服务器**
```
[root@nginx ~]# vim /etc/nginx/nginx.conf
server {
                listen 8080;
                server_name localhost;
                root /data/www/errorpage;
                index index.html;
        }
upstream webservers {
        server 192.168.18.201 weight=1 max_fails=2 fail_timeout=2;
        server 192.168.18.202 weight=1 max_fails=2 fail_timeout=2;
        server 127.0.0.1:8080 backup;
    }
[root@nginx ~]# mkdir -pv /data/www/errorpage
[root@nginx errorpage]# cat index.html
<h1>Sorry......</h1>
```

**10.配置ip_hash负载均衡**
`ip_hash`，每个请求按访问IP的hash结果分配，这样来自同一个IP的访客固定访问一个后端服务器，有效解决了动态网页存在的session共享问题。（一般电子商务网站用的比较多）
```
[root@nginx ~]# vim /etc/nginx/nginx.conf
upstream webservers {
        ip_hash;
        server 192.168.18.201 weight=1 max_fails=2 fail_timeout=2;
        server 192.168.18.202 weight=1 max_fails=2 fail_timeout=2;
        #server 127.0.0.1:8080 backup;
    }
```
注，当负载调度算法为ip_hash时，后端服务器在负载均衡调度中的状态不能有backup。（有人可能会问，为什么呢？大家想啊，如果负载均衡把你分配到backup服务器上，你能访问到页面吗？不能，所以了不能配置backup服务器）



## 三、Nginx之页面缓存
**1.指令说明**
`proxy_cache_path`
语法：`proxy_cache_path path [levels=number] keys_zone=zone_name:zone_size [inactive=time] [max_size=size]; ` 
默认值：`None`  
使用字段：`http  `
指令指定缓存的路径和一些其他参数，缓存的数据存储在文件中，并且使用代理url的哈希值作为关键字与文件名。levels参数指定缓存的子目录数，例如：
```
proxy_cache_path  /data/nginx/cache  levels=1:2   keys_zone=one:10m;
```
文件名类似于：
```
/data/nginx/cache/c/29/b7f54b2df7773722d382f4809d65029c
```
levels指定目录结构，可以使用任意的1位或2位数字作为目录结构，如 X, X:X,或X:X:X 例如: “2”, “2:2”, “1:1:2“，但是最多只能是三级目录。  
所有活动的key和元数据存储在共享的内存池中，这个区域用keys_zone参数指定。`one指的是共享池的名称`，`10m指的是共享池的大小`。  
注意每一个定义的内存池必须是不重复的路径，例如：
```
proxy_cache_path  /data/nginx/cache/one    levels=1      keys_zone=one:10m;
proxy_cache_path  /data/nginx/cache/two    levels=2:2    keys_zone=two:100m;
proxy_cache_path  /data/nginx/cache/three  levels=1:1:2  keys_zone=three:1000m;
```
如果在inactive参数指定的时间内缓存的数据没有被请求则被删除，默认inactive为10分钟。一个名为cache manager的进程控制磁盘的缓存大小，它被用来删除不活动的缓存和控制缓存大小，这些都在max_size参数中定义，当目前缓存的值超出max_size指定的值之后，超过其大小后最少使用数据（LRU替换算法）将被删除。内存池的大小按照缓存页面数的比例进行设置，一个页面（文件）的元数据大小按照操作系统来定，如FreeBSD/i386下为64字节，FreeBSD/amd64下为128字节。

`proxy_cache`
语法：`proxy_cache zone_name; ` 
默认值：None  
使用字段：`http, server, location ` 
设置一个缓存区域的名称，一个相同的区域可以在不同的地方使用。  
在0.7.48后，缓存遵循后端的”Expires”, “Cache-Control: no-cache”, “Cache-Control: max-age=XXX”头部字段，0.7.66版本以后，”Cache-Control:“private”和”no-store”头同样被遵循。nginx在缓存过程中不会处理”Vary”头，为了确保一些私有数据不被所有的用户看到，后端必须设置 “no-cache”或者”max-age=0”头，或者proxy_cache_key包含用户指定的数据如`$cookie_xxx`，使用cookie的值作为proxy_cache_key的一部分可以防止缓存私有数据，所以可以在不同的location中分别指定proxy_cache_key的值以便分开私有数据和公有数据。  
缓存指令依赖代理缓冲区(buffers)，`如果proxy_buffers设置为off，缓存不会生效。`

`proxy_cache_valid`
语法：`proxy_cache_valid reply_code [reply_code …] time;`  
默认值：None  
使用字段：`http, server, location`  
为不同的应答设置不同的缓存时间，例如：
```
proxy_cache_valid  200 302  10m;
proxy_cache_valid  404      1m;
```
为应答代码为200和302的设置缓存时间为10分钟，404代码缓存1分钟。  
如果只定义时间：
```
proxy_cache_valid 5m;
```
那么只对代码为200, 301和302的应答进行缓存。  
同样可以使用any参数任何应答。
```
proxy_cache_valid  200 302 10m;
proxy_cache_valid  301 1h;
proxy_cache_valid  any 1m;
```
**2.定义一个简单nginx缓存服务器**
```
[root@nginx ~]# vim /etc/nginx/nginx.conf
proxy_cache_path /data/nginx/cache/webserver levels=1:2 keys_zone=webserver:20m max_size=1g;

   server {
       listen       80;
       server_name  localhost;
       #charset koi8-r;
       #access_log  logs/host.access.log  main;
       location / {
               proxy_pass      http://webservers;
               proxy_set_header  X-Real-IP  $remote_addr;
               proxy_cache webserver;
               proxy_cache_valid 200 10m;
               proxy_cache_keys $host$uri$is_args$args;
               proxy_set_header Host  $host;
               expires      1d;
                #如果后端的服务器返回502、504、执行超时等错误，自动将请求转发到upstream负载均衡池中的另一台服务器，实现故障转移。
         proxy_next_upstream http_502 http_504 error timeout invalid_header;
        
       }
}
```

**3.新建缓存目录**
`[root@nginx ~]# mkdir -pv /data/nginx/cache/webserver`

**4.重新加载一下配置文件**
```
[root@nginx webserver]# service nginx reload
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
重新载入 nginx：                                           [确定]
```

**5.下面我们来测试一下（谷歌浏览器）**

注，大家用谷歌浏览器测试的时候，可以按F12调用开发工具，选择Network选项，我们可以看到，Response Headers，在这里我们可以看到，我们请求的是否是缓存，但现在还看不到，下面我们来配置一下，再来测试。

**6. 缓存变量说明**
`$server_addr`
服务器地址，在完成一次系统调用后可以确定这个值，如果要绕开系统调用，则必须在listen中指定地址并且使用bind参数。
`$upstream_cache_status`
0.8.3版本中其值可能为：
`MISS` 未命中
`EXPIRED` - expired。请求被传送到后端。
`UPDATING` - expired。由于proxy/fastcgi_cache_use_stale正在更新，将使用旧的应答。
`STALE` - expired。由于proxy/fastcgi_cache_use_stale，后端将得到过期的应答。
HIT 命中
```
[root@nginx ~]# vim /etc/nginx/nginx.conf
proxy_cache_path /data/nginx/cache/webserver levels=1:2 keys_zone=webserver:20m max_size=1g;
    server {
        listen       80;
        server_name  localhost;
        #charset koi8-r;
        #access_log  logs/host.access.log  main;
       #增加两头部
        add_header X-Via $server_addr;
        add_header X-Cache $upstream_cache_status;
        location / {
                proxy_pass      http://webservers;
                proxy_set_header  X-Real-IP  $remote_addr;
                proxy_cache webserver;
                proxy_cache_valid 200 10m;
        }
}

```
**7.重新加载一下配置文件**

**8.测试一下**


**9.查看一下缓存目录**
```
[root@nginx ~]# cd /data/nginx/cache/webserver/f/63/
[root@nginx 63]# ls
681ad4c77694b65d61c9985553a2763f
```
注，缓存目录里确实有缓存文件。好了，nginx缓存配置就到这边了，更多配置请根据需要看配置文档。下面我们来说一下，URL重写。

**10.缓存清理**

**11.命中率统计**
二、nginx cache命中率统计

即然nginx为我们提供了`$upstream_cache_status`函数，自然可以将命中状态写入到日志中。具体可以如下定义日志格式：
```
log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                  '$status $body_bytes_sent "$http_referer" '
                  '"$http_user_agent" "$http_x_forwarded_for"'
                  '"$upstream_cache_status"';
```
命中率统计方法：用HIT的数量除以日志总量得出缓存命中率：
```
awk '{if($NF==""HIT"") hit++} END {printf "%.2f%",hit/NR}' access.log
```
了解了原理以后，也可以通过crontab脚本将每天的命中率统计到一个日志中，以备查看。
```
# crontab -l
1 0 * * * /opt/shell/nginx_cache_hit >> /usr/local/nginx/logs/hit
```
访脚本的内容为：
```
#!/bin/bash
LOG_FILE='/usr/local/nginx/logs/access.log.1'
LAST_DAY=$(date +%F -d "-1 day")
awk '{if($NF==""HIT"") hit++} END {printf "'$LAST_DAY': %d %d %.2f%n", hit,NR,hit/NR}' $LOG_FILE
```

##四、读写分离
  
   需求分析，前端一台nginx做负载均衡反向代理，后面两台httpd服务器。整个架构是提供BBS(论坛)服务，有一需求得实现读写分离，就是上传附件的功能，我们上传的附件只能上传到Web1，然后在Web1上利用rsync+inotify实现附件同步，大家都知道rsync+inotify只能是主向从同步，不能双向同步。所以Web1可进行写操作，而Web2只能进行读操作，这就带来读写分离的需求，下面我们就来说一下，读写分离怎么实现。
   
**2.WebDAV功能说明**
      ` WebDAV （Web-based Distributed Authoring and Versioning）` 一种基于 HTTP 1.1协议的通信协议。它扩展了HTTP 1.1，在GET、POST、HEAD等几个HTTP标准方法以外添加了一些新的方法，使应用程序可直接对Web Server直接读写，并支持写文件锁定(Locking)及解锁(Unlock)，还可以支持文件的版本控制。这样我们就能配置读写分离功能了，下面我们来具体配置一下。
       
**3.修改配置文件**
```
[root@nginx nginx]# vim /etc/nginx/nginx.conf
server {
        listen       80;
        server_name  localhost;
        #charset koi8-r;
        #access_log  logs/host.access.log  main;
        location / {
                proxy_pass http://192.168.18.202;
                if ($request_method = "PUT"){
                        proxy_pass http://192.168.18.201;
                }
        }
}
```
**4.重新加载一下配置文件**
```
[root@nginx ~]# service nginx reload
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
重新载入 nginx：                                           [确定]
```

**5.配置httpd的WebDAV功能**
```
[root@web1 ~]# vim /etc/httpd/conf/httpd.conf
<Directory "/var/www/html">
Dav on
```
注，在<Directory "/var/www/html">下启用就行。
**6.重新启动一下httpd**
```
[root@web1 ~]# service httpd restart
停止 httpd：                                               [确定]
正在启动 httpd：                                           [确定]
```
**7.测试一下**
```
[root@nginx ~]# curl http://192.168.18.201
<h1>web1.test.com</h1>
[root@nginx ~]# curl http://192.168.18.202
<h1>web2.test.com</h1>
```
注，web1与web2访问都没问题。
```
[root@nginx ~]# curl -T /etc/issue  http://192.168.18.202
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>405 Method Not Allowed</title>
</head><body>
<h1>Method Not Allowed</h1>
The requested method PUT is not allowed for the URL /issue.
<hr>
<address>Apache/2.2.15 (CentOS) Server at 192.168.18.202 Port 80</address>
</body></html>
```
注，我们上传文件到，web2上时，因为web2只人读功能，所以没有开户WebDAV功能，所以显示是405 Method Not Allowed。  
```
[root@nginx ~]# curl -T /etc/issue  http://192.168.18.201
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>403 Forbidden</title>
</head><body>
<h1>Forbidden</h1>
You don't have permission to access /issue
on this server.
<hr>
<address>Apache/2.2.15 (CentOS) Server at 192.168.18.201 Port 80</address>
</body></html>
```
注，我们在Web1开启了WebDAV功能，但我们目录是root目录是不允许apache用户上传的，所以显示的是403 Forbidden。下面我们给apache授权，允许上传。
```
[root@web1 ~]# setfacl -m u:apache:rwx /var/www/html/
```
下面我们再来测试一下，
```
[root@nginx ~]# curl -T /etc/issue  http://192.168.18.201
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>201 Created</title>
</head><body>
<h1>Created</h1>
Resource /issue has been created.
<hr />
<address>Apache/2.2.15 (CentOS) Server at 192.168.18.201 Port 80</address>
</body></html>
```
注，大家可以看到我们成功的上传了文件，说明nginx读写分离功能配置完成。最后，我们来查看一下上传的文件。
```
[root@web1 ~]# cd /var/www/html/
[root@web1 html]# ll
总用量 12
drwxr-xr-x 2 root   root   4096 9月   4 13:16 forum
-rw-r--r-- 1 root   root     23 9月   3 23:37 index.html
-rw-r--r-- 1 apache apache   47 9月   4 14:06 issue
```




