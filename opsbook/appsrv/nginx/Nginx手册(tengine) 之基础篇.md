# Nginx手册(tengine) 之基础篇

标签（空格分隔）： Nginx 

---

## 一、安装

```
useradd nginx
```

```
yum -y install nginx
apt-get install nginx

yum -y install zlib zlib-devel pcre pcre-devel openssl openssl-devel

./configure   --prefix=/usr   --sbin-path=/usr/sbin/nginx   --conf-path=/etc/nginx/nginx.conf   --error-log-path=/var/log/nginx/error.log   --http-log-path=/var/log/nginx/access.log   --pid-path=/var/run/nginx/nginx.pid    --lock-path=/var/lock/nginx.lock   --user=nginx   --group=nginx   --with-http_ssl_module   --with-http_flv_module   --with-http_stub_status_module   --with-http_gzip_static_module   --http-client-body-temp-path=/var/tmp/nginx/client/   --http-proxy-temp-path=/var/tmp/nginx/proxy/   --http-fastcgi-temp-path=/var/tmp/nginx/fcgi/   --http-uwsgi-temp-path=/var/tmp/nginx/uwsgi   --http-scgi-temp-path=/var/tmp/nginx/scgi   --with-pcre

make 
make install

```

##二. nginx启动脚本
```
#!/bin/sh   
#   
# nginx - this script starts and stops the nginx daemon   
#   
# chkconfig:   - 85 15   
# description:  Nginx is an HTTP(S) server, HTTP(S) reverse \   
#               proxy and IMAP/POP3 proxy server   
# processname: nginx   
# config:      /etc/nginx/nginx.conf   
# config:      /etc/sysconfig/nginx   
# pidfile:     /var/run/nginx.pid   
# Source function library.   
. /etc/rc.d/init.d/functions   
# Source networking configuration.   
. /etc/sysconfig/network   
# Check that networking is up.   
[ "$NETWORKING" = "no" ] && exit 0   
nginx="/usr/sbin/nginx"   
prog=$(basename $nginx)   
NGINX_CONF_FILE="/etc/nginx/nginx.conf"   
[ -f /etc/sysconfig/nginx ] && . /etc/sysconfig/nginx   
lockfile=/var/lock/subsys/nginx   
make_dirs() {   
   # make required directories   
   user=`nginx -V 2>&1 | grep "configure arguments:" | sed 's/[^*]*--user=\([^ ]*\).*/\1/g' -`   
   options=`$nginx -V 2>&1 | grep 'configure arguments:'`   
   for opt in $options; do   
       if [ `echo $opt | grep '.*-temp-path'` ]; then   
           value=`echo $opt | cut -d "=" -f 2`   
           if [ ! -d "$value" ]; then   
               # echo "creating" $value   
               mkdir -p $value && chown -R $user $value   
           fi   
       fi   
   done   
}   
start() {   
    [ -x $nginx ] || exit 5   
    [ -f $NGINX_CONF_FILE ] || exit 6   
    make_dirs   
    echo -n $"Starting $prog: "   
    daemon $nginx -c $NGINX_CONF_FILE   
    retval=$?   
    echo   
    [ $retval -eq 0 ] && touch $lockfile   
    return $retval   
}   
stop() {   
    echo -n $"Stopping $prog: "   
    killproc $prog -QUIT   
    retval=$?   
    echo   
    [ $retval -eq 0 ] && rm -f $lockfile   
    return $retval   
}   
restart() {   
    configtest || return $?   
    stop   
    sleep 1   
    start   
}   
reload() {   
    configtest || return $?   
    echo -n $"Reloading $prog: "   
    killproc $nginx -HUP   
    RETVAL=$?   
    echo   
}   
force_reload() {   
    restart   
}   
configtest() {   
  $nginx -t -c $NGINX_CONF_FILE   
}   
rh_status() {   
    status $prog   
}   
rh_status_q() {   
    rh_status >/dev/null 2>&1   
}   
case "$1" in   
    start)   
        rh_status_q && exit 0   
        $1   
        ;;   
    stop)   
        rh_status_q || exit 0   
        $1   
        ;;   
    restart|configtest)   
        $1   
        ;;   
    reload)   
        rh_status_q || exit 7   
        $1   
        ;;   
    force-reload)   
        force_reload   
        ;;   
    status)   
        rh_status   
        ;;   
    condrestart|try-restart)   
        rh_status_q || exit 0   
            ;;   
    *)   
        echo $"Usage: $0 {start|stop|status|restart|condrestart|try-restart|reload|force-reload|configtest}"   
        exit 2   
esac
```

## 三.nginx状态页面
```
location /NginxStatus {
    stub_status     on;
    access_log             logs/NginxStatus.log;
    auth_basic             "NginxStatus";
    auth_basic_user_file    ../htpasswd;
       }
```
stub_status为“on”表示启用StubStatus的工作状态统计功能；
access_log 用来指定StubStatus模块的访问日志文件；
auth_basic是Nginx的一种认证机制；
auth_basic_user_file用来指定认证的密码文件。
由于Nginx的auth_basic认证采用的是与Apache兼容的密码文件，因此需要用Apache的htpasswd命令来生成密码文件。例如要添加一个webadmin用户，可以使用下面的方式生成密码文件：
```
/usr/local/apache/bin/htpasswd -c  /opt/nginx/conf/htpasswd webadmin
```
要查看Nginx的运行状态，可以输入http://ip/ NginxStatus，然后输入刚刚创建的用户名和密码就可以看到如下信息：
```
Active connections: 1
server accepts handled requests
393411 393411 393799
Reading: 0 Writing: 1 Waiting: 0
```
Active connections表示当前活跃的连接数。
第三行的3个数字表示 Nginx当前总共处理了393411个连接， 成功创建了393 411次握手，总共处理了393 799个请求。
最后一行的Reading表示Nginx读取到客户端Header信息数； Writing表示Nginx返回给客户端的Header信息数；Waiting表示Nginx已经处理完、正在等候下一次请求指令时的驻留连接数。
补充说明：
```
error_page  404              /404.html;
error_page   500 502 503 504  /50x.html;
location = /50x.html {
           root   html;
       }
```
在最后这段设置中，设置了虚拟主机的错误信息返回页面，通过error_page指令可以定制各种错误信息的返回页面。在默认情况下，Nginx会在主目录的html目录中查找指定的返回页面。特别需要注意的是，这些错误信息的返回页面大小一定要超过512KB，否则会被IE浏览器替换为IE默认的错误页面。好了，到这里nginx的配置文件讲解全部完成。下面我们来说一说nginx命令参数。

配置Nginx的访问控制
基于用户的访问控制，
**1.提供测试文件**
```
[root@web run]# cd /data/www/ 
[root@web www]# ll 
总用量 4 
-rw-r--r-- 1 nginx nginx 23 8月  29 20:04 index.html 
[root@web www]# mkdir bbs 
[root@web www]# cd bbs/ 
[root@web bbs]# vim index.html 
[root@web bbs]# cat index.html 
<h1>Auth Page</h1>
```
**2.修改配置文件**
```
location /data { 
           root /www/bbs; 
           index index.html 
           auth_basic             "Auth Page";
           auth_basic_user_file  /etc/nginx/.user; 
       }
```

**3.安装httpd-tools 工具包**

`[root@web bbs]# yum install -y httpd-devel`

**4.生成认证文件**
```
[root@web bbs]# htpasswd -c -m /etc/nginx/.user nginx 
New password: 
Re-type new password: 
Adding password for user nginx 
[root@web bbs]# ls -a /etc/nginx/ 
.                     fastcgi_params          mime.types          nginx.conf.default   .user 
..                    fastcgi_params.default  mime.types.default  .nginx.conf.swp      uwsgi_params 
fastcgi.conf          koi-utf                 nginx.conf          scgi_params          uwsgi_params.default 
fastcgi.conf.default  koi-win                 nginx.conf.bak      scgi_params.default  win-utf
```

**5.重新加载一下nginx配置文件**
```
[root@web bbs]# service nginx reload 
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok 
nginx: configuration file /etc/nginx/nginx.conf test is successful 
重新载入 nginx：                                           [确定]
```

## 四，访问控制
### 基于IP的访问控制，
**1.控制指令**
`allow` 定义允许访问的规则
`deny` 定义拒绝访问的规则
`allow all或deny all` 定义默认规则

**2.案例**
```
[root@web test]# vim /etc/nginx/nginx.conf
location / { 
         root   /data/www; 
         index  index.html index.htm; 
         #auth_basic "Auth Page";           
         #auth_basic_user_file /etc/nginx/.user; 
         deny 192.168.18.138; 
         allow 192.168.18.0/24;
         deny  all; 
     }
```

注，大家可以看到不允许访问。allow与deny指令使用很简单，唯一与httpd不同的是nginx没有定义默认规则，所以默认规则得自己定义。我这里定义是deny all；默认拒绝所有。

##五、配置Nginx提供状态页面
**1.修改配置文件**
```
[root@web test]# vim /etc/nginx/nginx.conf
location /status { 
     root /; 
     stub_status on; 
     auth_basic "NginxStatus";              
     auth_basic_user_file /etc/nginx/.user; 
     }
```

##六、配置Nginx的错误页面
**1.提供404错误页面**
```
[root@web www]# ll 
总用量 8 
drwxr-xr-x 2 root  root  4096 8月  29 20:36 bbs 
-rw-r--r-- 1 nginx nginx   23 8月  29 20:04 index.html 
[root@web www]# vim 404.html 
[root@web www]# cat 404.html 
<h1>404 error</h1>
<h1>404 error</h1>
<h1>404 error</h1>
<h1>404 error</h1>

```
**2.修改配置文件**
```
[root@web test]# vim /etc/nginx/nginx.conf
server {
error_page  404                 /404.html;
}
```

##七、配置Nginx打开目录浏览功能
**1.指令说明**
Nginx默认是不允许列出整个目录的。如需此功能，打开nginx.conf文件，在location server 或 http段中加入autoindex on；另外两个参数最好也加上去，
autoindex_exact_size off；默认为on，显示出文件的确切大小，单位是bytes。改为off后，显示出文件的大概大小，单位是kB或者MB或者GB。
autoindex_localtime on；默认为off，显示的文件时间为GMT时间。改为on后，显示的文件时间为文件的服务器时间。

**2.修改配置文件**
```
server { 
    listen       80; 
    server_name  www.nginx.com; 
    location / { 
    autoindex on; 
    autoindex_exact_size on; 
    autoindex_localtime on; 
    root   /data/www; 
    index  123.html; 
    } 
}
```


##八、配置Nginx基于ssl提供https服务
**1.创建CA自签证书**
```
[root@web ~]# cd /etc/pki/CA/ 
[root@web CA]# ls 
certs  crl  newcerts  private 
[root@web CA]# cd private/ 
[root@web private]# ls 
[root@web private]# (umask 077; openssl genrsa 2048 > cakey.pem) #生成私钥 
Generating RSA private key, 2048 bit long modulus 
...............................+++ 
.............+++ 
e is 65537 (0x10001) 
[root@web CA]# openssl req -new -x509 -key ./private/cakey.pem -out cacert.pem #生成自签证书 
You are about to be asked to enter information that will be incorporated 
into your certificate request. 
What you are about to enter is what is called a Distinguished Name or a DN. 
There are quite a few fields but you can leave some blank 
For some fields there will be a default value, 
If you enter '.', the field will be left blank. 
----- 
Country Name (2 letter code) [XX]:CN 
State or Province Name (full name) []:SH 
Locality Name (eg, city) [Default City]:XH  
Organization Name (eg, company) [Default Company Ltd]:JJHH    
Organizational Unit Name (eg, section) []:Tech 
Common Name (eg, your name or your server's hostname) []:ca.test.com 
Email Address []:caadmin@test.com 
[root@web private]# ll 
总用量 8 
-rw------- 1 root root 1679 8月  29 23:31 cakey.pem 
[root@web CA]# touch serial 
[root@web CA]# echo 01 > serial 
[root@web CA]# touch index.txt
[root@web CA]# ll 
总用量 24 
-rw-r--r--  1 root root 1375 8月  29 23:34 cacert.pem 
drwxr-xr-x. 2 root root 4096 3月   5 06:22 certs 
drwxr-xr-x. 2 root root 4096 3月   5 06:22 crl 
-rw-r--r--  1 root root    0 8月  29 23:35 index.txt 
drwxr-xr-x. 2 root root 4096 3月   5 06:22 newcerts 
drwx------. 2 root root 4096 8月  29 23:49 private 
-rw-r--r--  1 root root    3 8月  29 23:35 serial
```
**2.生成证书申请**
```
[root@web ~]# mkdir /etc/nginx/ssl 
[root@web CA]# cd /etc/nginx/ssl/
[root@web ssl]# (umask 077; openssl genrsa 1024 > nginx.key) #生成私钥 
Generating RSA private key, 1024 bit long modulus 
.........................................++++++ 
..................................++++++ 
e is 65537 (0x10001)
[root@web ssl]# openssl req -new -key nginx.key -out nginx.csr 
You are about to be asked to enter information that will be incorporated 
into your certificate request. 
What you are about to enter is what is called a Distinguished Name or a DN. 
There are quite a few fields but you can leave some blank 
For some fields there will be a default value, 
If you enter '.', the field will be left blank. 
----- 
Country Name (2 letter code) [XX]:CN 
State or Province Name (full name) []:SH 
Locality Name (eg, city) [Default City]:XH 
Organization Name (eg, company) [Default Company Ltd]:JJHH 
Organizational Unit Name (eg, section) []:Tech 
Common Name (eg, your name or your server's hostname) []:www.test.com 
Email Address []:
Please enter the following 'extra' attributes 
to be sent with your certificate request 
A challenge password []: 
An optional company name []:
```
**3. 让CA签名并颁发证书**
```
[root@web ssl]# openssl ca -in nginx.csr -out nginx.crt -days 3650 
Using configuration from /etc/pki/tls/openssl.cnf 
Check that the request matches the signature 
Signature ok 
Certificate Details: 
        Serial Number: 1 (0x1) 
        Validity 
            Not Before: Aug 29 15:51:53 2013 GMT 
            Not After : Aug 27 15:51:53 2023 GMT 
        Subject: 
            countryName               = CN 
            stateOrProvinceName       = SH 
            organizationName          = JJHH 
            organizationalUnitName    = Tech 
            commonName                = www.test.com 
        X509v3 extensions: 
            X509v3 Basic Constraints: 
                CA:FALSE 
            Netscape Comment: 
                OpenSSL Generated Certificate 
            X509v3 Subject Key Identifier: 
                60:87:97:14:D5:A2:23:B9:C5:13:97:5D:0D:B9:D7:C3:C2:66:F0:4B 
            X509v3 Authority Key Identifier: 
                keyid:9E:3E:5B:84:06:BE:68:01:C9:16:7C:08:5F:C5:54:0D:7B:FC:FA:87
Certificate is to be certified until Aug 27 15:51:53 2023 GMT (3650 days) 
Sign the certificate? [y/n]:y
1 out of 1 certificate requests certified, commit? [y/n]y 
Write out database with 1 new entries 
Data Base Updated
```

**4.修改配置文件**
```
server { 
      listen       443; 
      server_name  localhost;
      ssl                  on; 
      ssl_certificate      /etc/nginx/ssl/nginx.crt; 
      ssl_certificate_key  /etc/nginx/ssl/nginx.key;
      ssl_session_timeout  5m;
      ssl_protocols  SSLv2 SSLv3 TLSv1; 
      ssl_ciphers  HIGH:!aNULL:!MD5; 
      ssl_prefer_server_ciphers   on;
      location / { 
          root   html; 
          index  index.html index.htm; 
      } 
  }
```
**5.重新启动一下nginx服务器**
```
[root@web ssl]# service nginx restart 
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok 
nginx: configuration file /etc/nginx/nginx.conf test is successful 
停止 nginx：                                               [确定] 
正在启动 nginx：

[确定]
```

**6.查看一下端口**  
```
[root@web ssl]# netstat -ntlp 
Active Internet connections (only servers) 
Proto Recv-Q Send-Q Local Address               Foreign Address             State       PID/Program name 
tcp        0      0 0.0.0.0:80                  0.0.0.0:*                   LISTEN      10661/nginx       
tcp        0      0 0.0.0.0:22                  0.0.0.0:*                   LISTEN      1033/sshd         
tcp        0      0 127.0.0.1:25                0.0.0.0:*                   LISTEN      1110/master       
tcp        0      0 127.0.0.1:6010              0.0.0.0:*                   LISTEN      9599/sshd         
tcp        0      0 0.0.0.0:443                 0.0.0.0:*                   LISTEN      10661/nginx       
tcp        0      0 127.0.0.1:6012              0.0.0.0:*                   LISTEN      9470/sshd         
tcp        0      0 :::22                       :::*                        LISTEN      1033/sshd         
tcp        0      0 ::1:25                      :::*                        LISTEN      1110/master       
tcp        0      0 ::1:6010                    :::*                        LISTEN      9599/sshd         
tcp        0      0 ::1:6012                    :::*                        LISTEN      9470/sshd
```

