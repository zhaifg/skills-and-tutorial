# Nginx的流量控制

标签（空格分隔）： Nginx

---

## nginx限制请求数ngx_http_limit_req_module模块

请求数的限制该怎么做呢？这就需要通过`ngx_http_limit_req_module` 模块来实现，该模块可以通过定义的 键值来限制请求处理的频率。特别的，可以限制来自单个IP地址的请求处理频率。 限制的方法如同漏斗，每秒固定处理请求数，推迟过多请求。

**二. ngx_http_limit_req_module模块指令**
`limit_req_zone`
语法: `limit_req_zone $variable zone=name:size rate=rate;`
默认值: `none`
配置段: `http`
设置一块共享内存限制域用来保存键值的状态参数。 特别是保存了当前超出请求的数量。 键的值就是指定的变量（空值不会被计算）。如

    limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;

说明：
> 区域名称为one，大小为10m，平均处理的请求频率不能超过每秒一次。
键值是客户端IP。
使用`$binary_remote_addr`变量， 可以将每条状态记录的大小减少到64个字节，这样1M的内存可以保存大约1万6千个64字节的记录。
如果限制域的存储空间耗尽了，对于后续所有请求，服务器都会返回 503 (Service Temporarily Unavailable)错误。

速度可以设置为每秒处理请求数和每分钟处理请求数，其值必须是整数，所以如果你需要指定每秒处理少于1个的请求，2秒处理一个请求，可以使用 “30r/m”。

`limit_req_log_level`
语法: `limit_req_log_level info | notice | warn | error;`
默认值: `limit_req_log_level error;`
配置段: `http, server, location`
设置你所希望的日志级别，当服务器因为频率过高拒绝或者延迟处理请求时可以记下相应级别的日志。 延迟记录的日志级别比拒绝的低一个级别；比如， 如果设置“limit_req_log_level notice”， 延迟的日志就是info级别。

`limit_req_status`
语法: `limit_req_status code;`
默认值: `limit_req_status 503;`
配置段: `http, server, location`

该指令在1.3.15版本引入。设置拒绝请求的响应状态码。

`limit_req`
语法: `limit_req zone=name [burst=number] [nodelay];`
默认值: `—`
配置段: `http, server, location`
设置对应的共享内存限制域和允许被处理的最大请求数阈值。 如果请求的频率超过了限制域配置的值，请求处理会被延迟，所以所有的请求都是以定义的频率被处理的。 超过频率限制的请求会被延迟，直到被延迟的请求数超过了定义的阈值，这时，这个请求会被终止，并返回503 (Service Temporarily Unavailable) 错误。这个阈值的默认值为0。如：

    limit_req_zone $binary_remote_addr zone=ttlsa_com:10m rate=1r/s;
    server {
        location /www.ttlsa.com/ {
            limit_req zone=ttlsa_com burst=5;
        }
    }

限制平均每秒不超过一个请求，同时允许超过频率限制的请求数不多于5个。
如果不希望超过的请求被延迟，可以用nodelay参数,如：

    limit_req zone=ttlsa_com burst=5 nodelay;

###三. 完整实例配置
```
http {
 limit_req_zone $binary_remote_addr zone=ttlsa_com:10m rate=1r/s;
 
 server {
 location  ^~ /download/ {  
 limit_req zone=ttlsa_com burst=5;
 alias /data/www.ttlsa.com/download/;
        }
 }
}
```
可能要对某些IP不做限制，需要使用到白名单。名单设置参见后续的文档，我会整理一份以供读者参考。请专注。

## nginx限制连接数ngx_http_limit_conn_module模块

###　**一. 前言**
我们经常会遇到这种情况，服务器流量异常，负载过大等等。对于大流量恶意的攻击访问，会带来带宽的浪费，服务器压力，影响业务，往往考虑对同一个ip的连接数，并发数进行限制。下面说说`ngx_http_limit_conn_module` 模块来实现该需求。`该模块可以根据定义的键来限制每个键值的连接数，如同一个IP来源的连接数。并不是所有的连接都会被该模块计数，只有那些正在被处理的请求（这些请求的头信息已被完全读入）所在的连接才会被计数。`

### 二. ngx_http_limit_conn_module指令解释

`limit_conn_zone`
语法: `limit_conn_zone $variable zone=name:size;`
默认值: `none`
配置段: `http`
该指令描述会话状态存储区域。键的状态中保存了当前连接数，键的值可以是特定变量的任何非空值（空值将不会被考虑）。$variable定义键，zone=name定义区域名称，后面的limit_conn指令会用到的。size定义各个键共享内存空间大小。如：

    limit_conn_zone $binary_remote_addr zone=addr:10m;

注释：客户端的IP地址作为键。注意，这里使用的是$binary_remote_addr变量，而不是$remote_addr变量。
`$remote_addr`变量的长度为7字节到15字节，而存储状态在32位平台中占用32字节或64字节，在64位平台中占用64字节。
`$binary_remote_addr`变量的长度是固定的4字节，存储状态在32位平台中占用32字节或64字节，在64位平台中占用64字节。
1M共享空间可以保存3.2万个32位的状态，1.6万个64位的状态。
如果共享内存空间被耗尽，服务器将会对后续所有的请求返回 503 (Service Temporarily Unavailable) 错误。

`limit_zone` 指令和`limit_conn_zone`指令同等意思，limit_zone已经被弃用，就不再做说明了。

`limit_conn_log_level`
语法：`limit_conn_log_level info | notice | warn | error`
默认值：`error`
配置段：`http, server, location`
当达到最大限制连接数后，记录日志的等级。

`limit_conn`
语法：`limit_conn zone_name number`
默认值：`none`
配置段：`http, server, location`
指定每个给定键值的最大同时连接数，当超过这个数字时被返回503 (Service Temporarily Unavailable)错误。如：

```
limit_conn_zone $binary_remote_addr zone=addr:10m;
server {
    location /www.ttlsa.com/ {
        limit_conn addr 1;
    }
}
```
同一IP同一时间只允许有一个连接。
当多个 limit_conn 指令被配置时，所有的连接数限制都会生效。比如，下面配置不仅会限制单一IP来源的连接数，同时也会限制单一虚拟服务器的总连接数：
```
limit_conn_zone $binary_remote_addr zone=perip:10m;
limit_conn_zone $server_name zone=perserver:10m;
server {
    limit_conn perip 10;
    limit_conn perserver 100;
}
```
> limit_conn指令可以从上级继承下来。

`limit_conn_status`
语法: `limit_conn_status code;`
默认值: `limit_conn_status 503;`
配置段: `http, server, location`
该指定在1.3.15版本引入的。指定当超过限制时，返回的状态码。默认是503。

`limit_rate`
语法：`limit_rate rate`
默认值：`0`
配置段：`http, server, location, if in location`
对每个连接的速率限制。参数rate的单位是字节/秒，设置为0将关闭限速。 按连接限速而不是按IP限制，因此如果某个客户端同时开启了两个连接，那么客户端的整体速率是这条指令设置值的2倍。


### 三. 完整实例配置
```
http {
 limit_conn_zone $binary_remote_addr zone=limit:10m;
 limit_conn_log_level info;
 
 server {
 location  ^~ /download/ {  
 limit_conn limit 4;
 limit_rate 200k;
 alias /data/www.ttlsa.com/download/;
                }
 }
}
```
### 四. 使用注意事项
事务都具有两面性的。`ngx_http_limit_conn_module` 模块虽说可以解决当前面临的并发问题，但是会引入另外一些问题的。如前端如果有做LVS或反代，而我们后端启用了该模块功能，那不是非常多503错误了？这样的话，可以在前端启用该模块，要么就是设置白名单，白名单设置参见后续的文档，我会整理一份以供读者参考。
可以与`ngx_http_limit_req_module` 模块结合起来使用，以达到最好效果


## Nginx对POST的限制方法

对POST方法限制，用ngx_http_limit_req_module是不可以的，这是限制请求的方式；
ngx_conn_limit_req_module模块来限制流量是可以的。

Tengine的配置有些不同。

```
http{
    limit_conn_zone $binary_remote_addr zone=limit:10m;
}

server {
 location = /function/do_voteSZ.json {
    limit_conn limit 1;
    limit_rate 200k;
}
}
```