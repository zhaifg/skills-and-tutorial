# Nginx常用技巧和配置

标签（空格分隔）： Nginx

---
##一、root与alias区别
nginx指定文件路径有两种方式root和alias，这两者的用法区别，使用方法总结了下，方便大家在应用过程中，快速响应。root与alias主要区别在于nginx如何解释location后面的uri，这会使两者分别以不同的方式将请求映射到服务器文件上。

    [root]

语法：`root path`
默认值：`root html`
配置段：`http、server、location、if`

[alias]
语法：`alias path`
配置段：`location`

实例：
```
location ~ ^/weblogs/ {
        root /data/weblogs/www.ttlsa.com;
        autoindex on;
        auth_basic            "Restricted";
        auth_basic_user_file  passwd/weblogs;
}
```
如果一个请求的URI是/weblogs/httplogs/www.ttlsa.com-access.log时，web服务器将会返回服务器上的/data/weblogs/www.ttlsa.com/weblogs/httplogs/www.ttlsa.com-access.log的文件。

root会根据完整的URI请求来映射，也就是/path/uri。[/info]
因此，前面的请求映射为path/weblogs/httplogs/www.ttlsa.com-access.log。
```
location ^~ /binapp/ { 
        limit_conn limit 4;
        limit_rate 200k;
        internal; 
        alias /data/statics/bin/apps/;
}
```
alias会把location后面配置的路径丢弃掉，把当前匹配到的目录指向到指定的目录。如果一个请求的URI是/binapp/a.ttlsa.com/favicon时，web服务器将会返回服务器上的/data/statics/bin/apps/a.ttlsa.com/favicon.jgp的文件。

1. 使用alias时，目录名后面一定要加”/”。
2. alias可以指定任何名称。
3. alias在使用正则匹配时，必须捕捉要匹配的内容并在指定的内容处使用。
4. alias只能位于location块中。[/warning]


## 二、 HTTP Keepalives
在nginx与upstream之间启用HTTP Keepalives有助于提供性能，减少连接的等待时间，并可以减少对端口的占用，避免大流量情况下，端口耗尽。

HTTP协议使用TCP连接传输的HTTP请求和接收HTTP响应的。HTTP Keepalive 允许对这些TCP连接的复用，从而避免了创建和销毁的每个请求连接的开销。

![httphttp][1]

HTTP使用这个过程被称为“存活”的保持TCP连接。如果客户端需要进行另一次HTTP事务，它可以利用这个闲置的“存活连接”，而不是创建一个新的TCP连接。

Nginx是一个完整的代理，管理从客户端（前端存活的连接）到服务端（上游存活连接）的连接。

![http][2]

NGINX保持“存活连接高速缓存”，一套闲置的保活连接到上游服务器，当它需要转发一个请求到上游，它会从缓存中已经建立的连接，而不是创建一个新的TCP连接。这就减少了NGINX和上游服务器之间等待时间，并减少端口使用。所以NGINX能够吸收和负载平衡​​大量的流量。在突发大流量下，高速缓存可能被耗尽，在这种情况下NGINX将与上游服务器建立新的HTTP连接。

这种技术有时被称为“复用”，“连接池”，“连接复用”，或在传统的负载均衡术语中称为“OneConnect”。

keepalive连接缓存配置如下：
```
server {
   listen 80;
   location / {
      proxy_pass http://backend;
      proxy_http_version 1.1;
      proxy_set_header Connection ""
   }
}
 
upstream backend {
   server webserver1;
   server webserver2;
 
   
# maintain a maximum of 20 idle connections to each upstream server
   keepalive 20;
}

```

##三、 SSL的反向代理
Nginx反向代理，用的场景非常之多。Nginx反向代理配置可以参见下本博客内容。那么，nginx的SSL反向代理该如何配置呢？SSL配置请站内搜索，这里就不累述了。

修改nginx.conf配置
```
server {
        listen          443 ssl;
        server_name     www.ttlsa.com;
 
        ssl_certificate      ssl/www.ttlsa.com.crt;
        ssl_certificate_key  ssl/www.ttlsa.com.key;
        ssl_prefer_server_ciphers on;
        keepalive_timeout    60;
    ssl_session_cache    shared:SSL:10m;
        ssl_session_timeout  10m;
  
        location / {
            proxy_pass  http://www.ttlsa.com;
            proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
                proxy_set_header        Accept-Encoding   "";
            proxy_set_header        Host            $host;
            proxy_set_header        X-Real-IP       $remote_addr;
            proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header        X-Forwarded-Proto $scheme;
        add_header              Front-End-Https   on;
            proxy_redirect     off;
      }
}
```
重启服务
```
# /usr/local/nginx/sbin/nginx -t
# /usr/local/nginx/sbin/nginx -s reload
```

## 四、nginx proxy_pass指令’/’注意事项
nginx代理配置完之后,nginx配置proxy_pass，需要注意转发的路径配置.

### 1. proxy_pass配置说明

**不带/**
```
location /test/
{
                proxy_pass http://t6:8300;
}
``` 

 **带/**
```

```
location /test/
{
                proxy_pass http://t6:8300/;
 }
```
上面两种配置，区别只在于proxy_pass转发的路径后是否带 “/”

**针对情况1，如果访问url =** http://server/test/test.jsp，则被nginx代理后，请求路径会便问http://proxy_pass/test/test.jsp，将test/ 作为根路径，请求test/路径下的资源

**针对情况2，如果访问url =** http://server/test/test.jsp，则被nginx代理后，请求路径会变为 http://proxy_pass/test.jsp，直接访问server的根资源

### 2. 典型实例

同一个域名下，根据根路径的不同，访问不同应用及资源
例如：A应用` http://server/a ` ; B应用` http://server/b`

A 应用和 B应用共同使用访问域名` http://server；`
配置nginx代理转发时，如果采用情况2的配置方式，则会导致访问`http://server/a/test.jsp`时，代理到`http://proxy_pass/test.jsp`，导致无法访问到正确的资源，页面中如果有对根资源的访问，也都会以`http://server` 做为根路径访问资源，导致资源失效

针对此类情况，需要采用情况1，分别针对不用应用，设置不同的根资源路径，并保证代理后的根路径也依然有效.

## nginx apache lighthttpd 禁止某个目录执行PHP文件

安全问题无小事，死生之地，存亡之道，不可不察也。有关web站点安全设置可以参见：nginx安全配置、Linux下Apache安全配置策略、lnmp架构下php安全配置分享、确保nginx安全的10个技巧、Linux系统必备安全配置。

本文主要讲述针对nginx、Apache、lighthttpd三大web容器的针对某个特定的目录禁止执行PHP等程序。

**nginx**
```
location /upload/ {
    location ~ .*\.(php)?$
    {
        deny all;
    }
}
location ~* ^/(upload|images)/.*\.(php|php5)$
{
    deny all;
}
```
**Apache**
```
<Directory /webroot/attachments>
    php_flag engine off
</Directory>
```
**lighthttpd**
```
$HTTP["url"] =~ "^/(forumdata|templates|upload|images)/" {
    fastcgi.server = ()
}
```

## nginx禁止访问目录中可执行文件
某些网站系统需要用户上传图片等文件到某些目录下,难免程序有些漏洞,导致用户上传了php、cgi等等可执行的文件，导致网站陷入非常为难的境地. 此时我们可以通过nginx来禁止用户访问这些目录下的可执行文件。

nginx配置

```
location ~* /(images|cache|media|logs|tmp)/.*.(php|pl|py|jsp|sh|cgi)$ {
 return 403;
 error_page 403 /403_error.html;
 }
```
作用：在目录images、cache、media、logs、tmp目录下面的所有php、pl、py、jsp、sh、cgi都不能访问。

重启nginx

`/usr/local/nginx-1.7.0/sbin/nginx -s reload`

## ngnix的status配置

1. 查找有没有编译stub模块
```
nginx -V | grep --color -o http_stub_status
```
`with-http_stub_status_module`
2. 在某个`server{}`模块里
```
    # Turn on nginx stats
        stub_status on;
        # I do not need logs for stats
        access_log   off;
        # Security: Only allow access from 192.168.1.100 IP #
        allow 192.168.1.100;
        # Send rest of the world to /dev/null #
        deny all;
   }
 
```
> 
Active connections: 43 
server accepts handled requests
 7368 7368 10993 
Reading: 0 Writing: 5 Waiting: 38
Interpretation

`Active connections` – Number of all open connections. This doesn’t mean number of users. A single user, for a single pageview can open many concurrent connections to your server.

`Server accepts handled requests` – This shows three values.
- First is total accepted connections.
- Second is total handled connections. Usually first 2 values are same.
- Third value is number of and handles requests. This is usually greater than second value.
- Dividing third-value by second-one will give you number of requests per connection handled by Nginx. In above example, 10993/7368, 1.49 requests per connections.

`Reading` – nginx reads request header
`Writing` – nginx reads request body, processes request, or writes response to a client
`Waiting` – keep-alive connections, actually it is `active – (reading + writing)`.This value depends on keepalive-timeout. Do not confuse non-zero waiting value for poor performance. It can be ignored.

Although, you can force zero waiting by setting `keepalive_timeout 0`;


## 如何防止处理未定义主机名的请求
如果不允许请求中缺少“Host”头，可以定义如下主机，丢弃这些请求：
```
server {
    listen       80;
    server_name  "";
    return       444;
}
```
在这里，我们设置主机名为空字符串以匹配未定义“Host”头的请求，而且返回了一个nginx特有的，非http标准的返回码444，它可以用来关闭连接。

##虚拟主机名的匹配规则
1. 确切的名字；
2. 最长的以星号起始的通配符名字：*.example.org；
3. 最长的以星号结束的通配符名字：mail.*；
4. 第一个匹配的正则表达式名字（按在配置文件中出现的顺序）。

##虚拟主机名
1. 确切的名字
2. 通配符*.example.com,只能以*开头或结尾，且*后面或者前面跟着“.”
3. 正则表达式的形式，必须以“～”为开头，且“.”需要用加"\".。
正则的形式可以表示引用`server_name  "~^(?<name>\w\d{1,3}+)\.example\.net$";`
```
命名的正则表达式捕获组在后面可以作为变量使用：

server {
    server_name   ~^(www\.)?(?<domain>.+)$;

    location / {
        root   /sites/$domain;
    }
}
PCRE使用下面语法支持命名捕获组：

?<name> 从PCRE-7.0开始支持，兼容Perl 5.10语法
?'name' 从PCRE-7.0开始支持，兼容Perl 5.10语法
?P<name>  从PCRE-4.0开始支持，兼容Python语法
```
##servername 定义大量名字报错时
如果定义了大量名字，或者定义了非常长的名字，那可能需要在http配置块中使用`server_names_hash_max_size`和`server_names_hash_bucket_size`指令进行调整。`server_names_hash_bucket_size`的默认值可能是32，或者是64，或者是其他值，取决于CPU的缓存行的长度。如果这个值是32，那么定义“too.long.server.name.example.org”作为虚拟主机名就会失败，而nginx显示下面错误信息：
```
could not build the server_names_hash,
you should increase server_names_hash_bucket_size: 32
出现了这种情况，那就需要将指令的值扩大一倍：

http {
    server_names_hash_bucket_size  64;
    ...
如果定义了大量名字，得到了另外一个错误：

could not build the server_names_hash,
you should increase either server_names_hash_max_size: 512
or server_names_hash_bucket_size: 32
```
那么应该先尝试设置`server_names_hash_max_size`的值差不多等于名字列表的名字总量。如果还不能解决问题，或者服务器启动非常缓慢，再尝试提高`server_names_hash_bucket_size`的值。

[以上出处][1]


-------

##nginx开启debug模式
[开启debug模式方法][2]

## nginx 访问认证
```
location / {
    auth_basic "close site";
     auth_basic_user_file conf/htpasswd；
}
```

```
# comment
name1：password1
name2：password2：comment
name3：password3
```


## 防盗链

```
location ~* \.(gif|jpg|swf)$ {
    valid_referers none blocked start.igrow.cn sta.igrow.cn;
    if ($invalid_referer) {
       rewrite ^/ http://$host/logo.png;
    }
}
```

## gzip

## 浏览器缓存

  [1]: http://nginx.org/cn/docs/http/server_names.html
  [2]: http://nginx.org/cn/docs/debugging_log.html

  [1]: http://imglf2.ph.126.net/Y6MxCo0Zb2TXHYrqKNVGmw==/808959083166896375.png
  [2]: http://imglf1.ph.126.net/_r0KYYG8oj_w4-xWwmCRDQ==/2388878127361437373.png
  
 
