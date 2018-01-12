# Nginx rewrite

标签（空格分隔）： Nginx

---

## 1.相关命令
**1） break**
默认，none   server，location，if
完成当前的设置的规则，停止执行其他的重写指令。
```
if ($slow)
{
     limit_rate 10k;
     break;
}
```

**2)if**
`if(condition){...}`
注意:在使用if指令之前请看if is evil page 并且尽量考虑用 `try_files代替`。http://wiki.nginx.org/IfIsEvil 
判断一个条件，如果条件成立，则后面的大括号内的语句将执行，相关配置从上级继承。
可以再判断语句中指定下列值：
* 一个变量的名称；不成立的值为：空字符串“ ”或者一些用“0”开始的字符串。
* 一个使用=或者！=运算符的比较语句。

使用附后~*和~模式匹配的正则表达式：
* ~ 为区分大小写的匹配。
* ~*部区分大小写的匹配（firefox匹配FireFox）。
* ！和！~* 不匹配
* 使用-f 和！-f检查一个文件是否存在。
* 使用-d和!-d检查一个目录是否存在。
* 使用-e和!-e检查一个文件，目录或者软链接是否存在。
* 使用-x和!-x检查一个文件是否为可执行文件。
* 正则表达式的一部分可以用圆括号，方便之后按照顺序用$1-$9来引用。  
     
 实例：
```
 if ($http_user_agent ~  MSIE) {
     rewrite ^(.*)$ /msie/$1 break;
 }
 if ($http_cookie ~* "id=([^;]+)(?;:|$)") {
     set $id   $1;
 }

 if (!-f $request_filename){
     break;
     proxy_pass http://127.0.0.1;
 }
 if ($slow) {
     limit_rate 10k;
 }
 if ($invalid_referer){
    return 403;
 }

 if ($args ~ post =140){
    rewrite ^ http://example.com/ permanent;
 }
```

内置变量$invalid_referer用指令valid_referers指定。


**3）return**
` return code`

**4）rewrite**
`rewrite regex replacement flag`
按照相关的正则表达式与字符创修改URI，指令按照在配置文件中出现顺序执行。
可以在重写指令后面添加标记。
如果替换的字符串以http://开头，请求将被重定向，并且不在执行多余的rewrite指令。
    
尾部的标记（flag）可以是一下的值：
**last** -  完成重写指令，之后搜索相应的URI或location。
**break** - 完成重写指令。
**redirect** - 返回302临时重定向，如果替换字段用http://开头则被使用。
**permanent** - 返回301永久重定向。
     
注意如果一个重定向是相对的（没有主机部分），nginx将在重定向的过程中使用匹配server_name指令的“Host”头或者server_name指令指定的第一个名称，如果头不匹配或不存在，如果没有设置server_name，将使用本地主机名，如果你总是想让nginx使用“Host”头，可以再
server_name使用“*”通配符（查看http核心模块中的server_name）。例如：
```
      rewrite ^(/download/.*)/media/(.*)\..*$ $1/mp3/$2.mp3 break;
      rewrite ^(/download/.*)/audio/(.*)\..*$ $1/mp3/$2.ra break;
```
  但是如果我们将其放入一个名为/download/的location中，则需要将last标记为break，否则nginx将执行10次循环并返回500错误。
```
     location /download/ {
         rewrite ^(/download/.*)/media/(.*)\..*$ $1/mp3/$2.mp3 break;
         rewrite ^(/download/.*)/audio/(.*)\..*$ $1/mp3/$2.ra break;
         return 403;
     }
```
 如果替换字段中包含参数，那么其余的请求参数将附加到后面，为了防止附加，可以在最后一个字符后面跟一个问号：
         
`rewrite   ^/user/(.*)$ /show?user=$1? last;`
 注意：大括号（{ 和 }），可以同时用在正则表达式和配置块中，为了防止冲突，正则表达式使用括号需要用双引号（或者单引号）。

例如要重写以下的URL：
`  /photos/123456 `
为：
`  /path/to/photos/12/1234/123456.png`
则使用以下正则表达式（注意引号）：
`  rewrite "/photos/([0-9]{2})([0-9]{2})([0-9]{2})"            /path/to/photos/$1/$1$2/$1$2$3.png;`

如果指定一个“`？`”在重写的结尾，Nginx将丢弃请求中的参数，即变量$args,当使用`$request_uri`或者`$uri` & `$args`时可以在rewrite结
尾使用“`？`”以避免Nginx处理两次参数串。

在rewrite中使用`$request_uri`将`www.example.com`重写到`example.com`；
```
     server {
         server_name www.example.com ;
         rewrite ^ http://example.com$request_uri? parmanent;
     }
```
同样，重写只对路径进行操作，而不是参数，如果要重写一个带参数的URL，可以使用以下代替：
```
     if ($args ^~post =100 ) {
         rewrite ^ http://example.com/new-address.html? permanent;
     }
```
注意`$args`变量不会被编译，与location过程中的URI不同。

**5） rewrite_log**   
    `    rewrite_log off | on`
     启用时将在error log中记录notice标记的重写日志。


 **6） set**  
   ` set variable value`
    指令设置一个变量并为其赋值，其值可以是文本，变量和它们的结合。
    你可以使用定义一个新的变量，但是不能使用set设置$http_xxx头部变量的值。
   
**7）uninitialized_variable_warn   on|off**
    开启或者关闭在未初始化变量中记录警告日志。
    事实上，rewrite指令在配置文件加载时已经编译到内部代码，在解释器产生请求时使用。
 这个解释器是一个简单的堆栈虚拟机，如下列指令：
```
        location  /download/ {
            if ($forbidden) {
                return 403;
            }
            if ($slow) {
                limit_rate 10k;
            }
            rewrite ^/(download/.*)/media/(.*)\..*$ /$1/mp3/$2.mp3 break;
        }
```
将被编译成一下顺序：

           variable $forbidden
           checking to zero
           recovery 403
           completion of entire code
           variable $slow
           checking to zero
           checking of regular excodession
           copying "/"
           copying $1
           copying "/mp3/"
           copying  $2
           copying ".mp3"
           completion of regular excodession
           completion of entire sequece

注意并没有关于`limit_rate`的代码，因为它没有提及`ngx_http_rewrite_modul`e模块，`“if”`块可以类似”`location`”指令在配置文件的相同部分同时存在。  

如果`$slow`为真，对应的`if`块将生效，在这个配置中`limit_rate`的值为10k。  
指令：
` rewrite  ^/(download/.*)/media/(.*)\..*$  /$1/mp3/$2.mp3  break;`
         
如果我们将第一个斜杠括入圆括号，则可以减少执行顺序：
` rewrite  ^(/download/.*)/media/(.*)\..*$  $1/mp3/$2.mp3  break;`

之后的顺序类似如下：

            checking regular excodession
            copying $1
            copying "/mp3/"
            copying $2
            copying ".mp3"
            completion of regular excodession
            completion of entire code

注，由于配置文件内容较多，为了让大家看着方便，我们备份一下配置文件，打开一个新的配置文件。

```
      server {
          listen       80;
          server_name  localhost;
          #charset koi8-r;
          #access_log  logs/host.access.log  main;
          location / {
             root   html;
             index  index.html index.htm;
             rewrite ^/bbs/(.*)$ http://192.168.18.201/forum/$1;
          }
     }
```
注，大家可以从图中看出，`status code 302`指的是临时重定向，那就说明我们rewrite重写配置成功。大家知道`302是临时重定向`而`301是永久重定向`，那么怎么实现永久重定向呢。一般服务器与服务器之间是临时重定向，服务器内部是永久重定向。下面我们来演示一下永久重定向。
    
**8)  配置永久重定向**

`  vim /etc/nginx/nginx.conf`
```
     server {
        listen       80;
        server_name  localhost;
        #charset koi8-r;
        #access_log  logs/host.access.log  main;
        location / {
            root   html;
            index  index.html index.htm;
            rewrite ^/bbs/(.*)$ /forum/$1;
        }
      }
```
准备forum目录与测试文件

注，大家从图中可以看到，我们访问bbs/是直接帮我们跳转到forum/下，这种本机的跳转就是永久重定向也叫隐式重定向。好了，rewrite重定向我们就说到这里了，想要查询更多关于重定向的指令请参考官方文档。最后，我们来说一下读写分离。

## 域名跳转







