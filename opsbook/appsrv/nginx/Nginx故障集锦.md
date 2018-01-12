# Nginx故障集锦

标签（空格分隔）： Nginx

---

## connect() failed (111: Connection refused) while connecting to upstream解决

有时候nginx运行很正常，但是会发现错误日志中依旧有报错`connect() failed (111: Connection refused) while connecting to upstream.`

1. 一般情况下我们的upstream都是fastcgi://127.0.0.1:9000. 造成这个问题的原因大致有两个

` php-fpm没有运行`

执行如下命令查看是否启动了php-fpm，如果没有则启动你的php-fpm即可

`netstat -ant | grep 9000`
 

1. php-fpm队列满了

php-fpm.conf配置文件`pm.max_children`修改大一点,重启php-fpm并观察日志情况

##二、 nginx上传错误413 Request Entity Too Large
默认情况下使用nginx反向代理上传超过2MB的文件，会报错413 Request Entity Too Large,解决这个方法很简单,修改配置client_max_body_size值即可

修改nginx.conf
```
#cat /usr/local/nginx-1.7.0/conf/nginx.conf | grep client_max_body_size
 client_max_body_size 10M;
```
如果需要上传更大的文件，那么client_max_body_size改成更大的值即可,这边改成了10MB

重启nginx

`# /usr/local/nginx-1.7.0/sbin/nginx -s reload`

## 三、大文件下载优化
nginx大文件下载优化
2014年7月16日凉白开
默认情况下`proxy_max_temp_file_size`值为`1024MB`,也就是说后端服务器的文件不大于1G都可以缓存到nginx代理硬盘中，如果超过1G，那么文件不缓存，而是直接中转发送给客户端.如果`proxy_max_temp_file_size`设置为0，表示不使用临时缓存。

在大文件的环境下，如果想启用临时缓存，那么可以修改配置，值改成你想要的。

修改nginx配置
```
location /
 {
 ...
 proxy_max_temp_file_size 2048m;
 ...
 }
```
重启nginx

`# /usr/local/nginx-1.7.0/sbin/nginx -s reload`

## 四、nginx反向代理proxy_set_header自定义header头无效

公司使用nginx作为负载均衡，有时候需要自定义header头发送给后端的真实服务器. 想过去应该是非常的简单的事情.

例子如下：

设置代理服务器ip头
`proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;`

然后自己在自定义个header，remote_header_test，如下：
`proxy_set_header remote_header_test "123123123";`
接着后端真实服务器打开`www.ttlsa.com/nginx_header.php`

源代码是简单的phpinfo
```
<?php
 
phpinfo();
 
?>
```
在phpinfo结果页面中搜索刚才设置的头部，发现没有找到,网上查找资料,才发现原来nginx会忽略掉下划线的头部变量.于是改成如下：
`proxy_set_header remoteheadertest "123123123";`

再次打`开www.ttlsa.com/nginx_header.php`,搜索`remoteheadertest`,有内容. 看来果真不能用下划线. 然后改成’`-`‘，如下：
`proxy_set_header remote-header-test "123123123";`

打开页面,搜索到的头部是`remote_header_test`. 自动转换成下划线了.

如果想要支持下划线的话，需要增加如下配置：
`underscores_in_headers on;`
可以加到http或者server中

语法：`underscores_in_headers on|off`
默认值：`off`
使用字段：http, server
`是否允许在header的字段中带下划线`

##nginx强制缓存（解决no-store）

nginx代理做好了，缓存也配置好了，但是发现css、js、jpg这些静态文件统统都cached成功。但是偏偏页面文件依旧到源服务器取。

1. nginx不缓存原因

默认情况下，nginx是否缓存是由nginx缓存服务器与源服务器共同决定的, 缓存服务器需要严格遵守源服务器响应的header来决定是否缓存以及缓存的时常。header主要有如下：
`Cache-control：no-cache、no-store`
如果出现这两值，nginx缓存服务器是绝对不会缓存的
`Expires：1980-01-01`
如果出现日期比当前时间早，也不会缓存。

2. 解决不缓存方案

2.1 方法一：
修改程序或者源服务器web程序响应的header



2.2 方法二：

nginx代理直接加上如下一句：

`proxy_ignore_headers X-Accel-Expires Expires Cache-Control Set-Cookie;`
3. 结束

最后，强烈推荐去看《nginx缓存优先级》


## 启动Nginx时有如下报错“nginx：[emerg]getpw-nam（"nginx"）failed”。

解答：这是因为没有对应的Nginx服务用户，执行useraddnginx-s/sbin/nologin-M创建Nginx用户即可。为了让读者理解问题，



