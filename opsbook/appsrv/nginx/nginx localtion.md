# Nginx location
---

```
location [ = | ~ | ~* | ^~ ] uri {
 ... 
}
```


|模式 | 含义|
|---|---|
|location = /uri| = 表示精确匹配，只有完全匹配上才能生效|
|location ^~ /uri|    ^~ 开头对URL路径进行前缀匹配，并且在正则之前。|
|location ~ pattern|  开头表示区分大小写的正则匹配|
|location ~* pattern| 开头表示不区分大小写的正则匹配|
|location /uri|   不带任何修饰符，也表示前缀匹配，但是在正则匹配之后|
|location /|  通用匹配，任何未匹配到其它location的请求都会匹配到，相当于switch中的default|

前缀匹配时，Nginx 不对 url 做编码，因此请求为 /static/20%/aa，可以被规则 ^~ /static/ /aa 匹配到（注意是空格）
多个 location 配置的情况下匹配顺序为（参考资料而来，还未实际验证，试试就知道了，不必拘泥，仅供参考）:

1. 首先精确匹配 =
2. 其次前缀匹配 ^~
3. 其次是按文件中顺序的正则匹配
4. 然后匹配不带任何修饰的前缀匹配。
5. 最后是交给 / 通用匹配
6. 当有匹配成功时候，停止匹配，按当前匹配规则处理请求

例子，有如下匹配规则：
```

location = / {
   echo "规则A";
}
location = /login {
   echo "规则B";
}
location ^~ /static/ {
   echo "规则C";
}
location ^~ /static/files {
    echo "规则X";
}
location ~ \.(gif|jpg|png|js|css)$ {
   echo "规则D";
}
location ~* \.png$ {
   echo "规则E";
}
location /img {
    echo "规则Y";
}
location / {
   echo "规则F";
}
```

那么产生的效果如下：
* 访问根目录 /，比如 http://localhost/ 将匹配 规则A
* 访问 http://localhost/login 将匹配 规则B，http://localhost/register 则匹配 规则F
* 访问 http://localhost/static/a.html 将匹配 规则C
* 访问 http://localhost/static/files/a.exe 将匹配 规则X，虽然 规则C 也能匹配到，但因为最大匹配原则，最终选中了 规则X。你可以测试下，去掉规则 X ，则当前 URL 会匹配上 规则C。
* 访问 http://localhost/a.gif, http://localhost/b.jpg 将匹配 规则D 和 规则 E ，但是 规则 D 顺序优先，规则 E 不起作用，而 http://localhost/static/c.png 则优先匹配到 规则 C
* 访问 http://localhost/a.PNG 则匹配 规则 E ，而不会匹配 规则 D ，因为 规则 E 不区分大小写。
* 访问 http://localhost/img/a.gif 会匹配上 规则D,虽然 规则Y 也可以匹配上，但是因为正则匹配优先，而忽略了 规则Y。
* 访问 http://localhost/img/a.tiff 会匹配上 规则Y。

> 访问 http://localhost/category/id/1111 则最终匹配到规则 F ，因为以上规则都不匹配，这个时候应该是 Nginx 转发请求给后端应用服务器，比如 FastCGI（php），tomcat（jsp），Nginx 作为反向代理服务器存在


所以实际使用中，笔者觉得至少有三个匹配规则定义，如下：
```
# 直接匹配网站根，通过域名访问网站首页比较频繁，使用这个会加速处理，官网如是说。
# 这里是直接转发给后端应用服务器了，也可以是一个静态首页
# 第一个必选规则
location = / {
    proxy_pass http://tomcat:8080/index
}

# 第二个必选规则是处理静态文件请求，这是 nginx 作为 http 服务器的强项
# 有两种配置模式，目录匹配或后缀匹配，任选其一或搭配使用
location ^~ /static/ {
    root /webroot/static/;
}
location ~* \.(gif|jpg|jpeg|png|css|js|ico)$ {
    root /webroot/res/;
}

# 第三个规则就是通用规则，用来转发动态请求到后端应用服务器
# 非静态文件请求就默认是动态请求，自己根据实际把握
# 毕竟目前的一些框架的流行，带.php、.jsp后缀的情况很少了
location / {
    proxy_pass http://tomcat:8080/
}
```



## 案例
https://blog.coding.net/blog/tips-in-configuring-nginx-location

https://moonbingbing.gitbooks.io/openresty-best-practices/ngx/pitfalls_and_common_mistakes.html


0 0,12 * * * python -c 'import random; import time; time.sleep(random.random() * 3600)' && /etc/nginx/let_ssl/certbot-auto renew 
