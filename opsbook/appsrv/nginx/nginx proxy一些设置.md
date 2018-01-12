# nginx proxy一些设置

标签（空格分隔）： Nginx

---

语法:	`proxy_buffer_size size`;
默认值:	
proxy_buffer_size 4k|8k;
上下文:	http, server, location
设置缓冲区的大小为size。nginx从被代理的服务器读取响应时，使用该缓冲区保存响应的开始部分。这部分通常包含着一个小小的响应头。该缓冲区大小默认等于proxy_buffers指令设置的一块缓冲区的大小，但它也可以被设置得更小。

语法:	`proxy_buffering on | off;`
默认值:	
proxy_buffering on;
上下文:	http, server, location
代理的时候，开启或关闭缓冲后端服务器的响应。

当开启缓冲时，nginx尽可能快地从被代理的服务器接收响应，再将它存入proxy_buffer_size和proxy_buffers指令设置的缓冲区中。如果响应无法整个纳入内存，那么其中一部分将存入磁盘上的临时文件。proxy_max_temp_file_size和proxy_temp_file_write_size指令可以控制临时文件的写入。

当关闭缓冲时，收到响应后，nginx立即将其同步传给客户端。nginx不会尝试从被代理的服务器读取整个请求，而是将proxy_buffer_size指令设定的大小作为一次读取的最大长度。

响应头“X-Accel-Buffering”传递“yes”或“no”可以动态地开启或关闭代理的缓冲功能。 这个能力可以通过proxy_ignore_headers指令关闭。


语法:	`proxy_cache_bypass string ...;`
默认值:	—
上下文:	http, server, location
定义nginx不从缓存取响应的条件。如果至少一个字符串条件非空而且非“0”，nginx就不会从缓存中去取响应：

proxy_cache_bypass $cookie_nocache $arg_nocache$arg_comment;
proxy_cache_bypass $http_pragma    $http_authorization;
本指令可和与proxy_no_cache一起使用。

语法:	`proxy_cache_key string;`
默认值:	
proxy_cache_key $scheme$proxy_host$request_uri;
上下文:	http, server, location
定义如何生成缓存的键，比如

proxy_cache_key "$host$request_uri $cookie_user";
这条指令的默认值类似于下面字符串

proxy_cache_key $scheme$proxy_host$uri$is_args$args;



语法:`	proxy_cache_path path [levels=levels] keys_zone=name:size [inactive=time] [max_size=size] [loader_files=number] [loader_sleep=time] [loader_threshold=time];`
默认值:	—
上下文:	http
设置缓存的路径和其他参数。缓存数据是保存在文件中的，缓存的键和文件名都是在代理URL上执行MD5的结果。 levels参数定义了缓存的层次结构。比如，下面配置

proxy_cache_path /data/nginx/cache levels=1:2 keys_zone=one:10m;
缓存中文件名看起来是这样的：

/data/nginx/cache/c/29/b7f54b2df7773722d382f4809d65029c
被缓存的响应首先写入一个临时文件，然后进行重命名。从0.8.9版本开始，临时文件和缓存可以放在不同的文件系统。但请注意，这将导致文件在这两个文件系统中进行拷贝，而不是廉价的重命名操作。因此，针对任何路径，都建议将缓存和proxy_temp_path指令设置的临时文件目录放在同一文件系统。

此外，所有活动的键和缓存数据相关的信息都被存放在共享内存中。共享内存通过keys_zone参数的name和size来定义。被缓存的数据如果在inactive参数指定的时间内未被访问，就会被从缓存中移除，不论它是否是刚产生的。inactive的默认值是10分钟。

特殊进程“cache manager”监控缓存的条目数量，如果超过max_size参数设置的最大值，使用LRU算法移除缓存数据。

nginx新启动后不就，特殊进程“cache loader”就被启动。该进程将文件系统上保存的过去缓存的数据的相关信息重新加载到共享内存。加载过程分多次迭代完成，每次迭代，进程只加载不多于loader_files参数指定的文件数量（默认值为100）。此外，每次迭代过程的持续时间不能超过loader_threshold参数的值（默认200毫秒）。每次迭代之间，nginx的暂停时间由loader_sleep参数指定（默认50毫秒）。


语法:`	proxy_http_version 1.0 | 1.1;`
默认值:	
proxy_http_version 1.0;
上下文:	http, server, location
这个指令出现在版本 1.1.4.
设置代理使用的HTTP协议版本。默认使用的版本是1.0，而1.1版本则推荐在使用keepalive连接时一起使用。

语法:`	proxy_no_cache string ...;`
默认值:	—
上下文:	http, server, location
定义nginx不将响应写入缓存的条件。如果至少一个字符串条件非空而且非“0”，nginx就不将响应存入缓存：

proxy_no_cache $cookie_nocache $arg_nocache$arg_comment;
proxy_no_cache $http_pragma    $http_authorization;


语法:	`proxy_pass URL;`
默认值:	—
上下文:	location, if in location, limit_except
设置后端服务器的协议和地址，还可以设置可选的URI以定义本地路径和后端服务器的映射关系。 这条指令可以设置的协议是“http”或者“https”，而地址既可以使用域名或者IP地址加端口（可选）的形式来定义：

proxy_pass http://localhost:8000/uri/;
又可以使用UNIX域套接字路径来定义。该路径接在“unix”字符串后面，两端由冒号所包围，比如：

proxy_pass http://unix:/tmp/backend.socket:/uri/;
如果解析一个域名得到多个地址，所有的地址都会以轮转的方式被使用。当然，也可以使用服务器组来定义地址。

请求URI按下面规则传送给后端服务器：

如果proxy_pass使用了URI，当传送请求到后端服务器时，规范化以后的请求路径与配置中的路径的匹配部分将被替换为指令中定义的URI：
location /name/ {
    proxy_pass http://127.0.0.1/remote/;
}
如果proxy_pass没有使用URI，传送到后端服务器的请求URI一般客户端发起的原始URI，如果nginx改变了请求URI，则传送的URI是nginx改变以后完整的规范化URI：
location /some/path/ {
    proxy_pass http://127.0.0.1;
}
在1.1.12版以前，如果proxy_pass没有使用URI，某些情况下，nginx改变URI以后，会错误地将原始URI而不是改变以后的URI发送到后端服务器。
某些情况下，无法确定请求URI中应该被替换的部分：

使用正则表达式定义路径。
这种情况下，指令不应该使用URI。

在需要代理的路径中，使用rewrite指令改变了URI，但仍使用相同配置处理请求(break)：
location /name/ {
    rewrite    /name/([^/]+) /users?name=$1 break;
    proxy_pass http://127.0.0.1;
}
这种情况下，本指令设置的URI会被忽略，改变后的URI将被发送给后端服务器。

后端服务器的地址，端口和URI中都可以使用变量：

proxy_pass http://$host$uri;
甚至像这样：

proxy_pass $request;
这种情况下，后端服务器的地址将会在定义的服务器组中查找。如果查找不到，nginx使用resolver来查找该地址。

语法:	`proxy_redirect default;`
proxy_redirect off;
proxy_redirect redirect replacement;
默认值:	
proxy_redirect default;
上下文:	http, server, location
设置后端服务器“Location”响应头和“Refresh”响应头的替换文本。 假设后端服务器返回的响应头是 “Location: http://localhost:8000/two/some/uri/”，那么指令

proxy_redirect http://localhost:8000/two/ http://frontend/one/;
将把字符串改写为 “Location: http://frontend/one/some/uri/”。

replacement字符串可以省略服务器名：

proxy_redirect http://localhost:8000/two/ /;
此时将使用代理服务器的主域名和端口号来替换。如果端口是80，可以不加。

用default参数指定的默认替换使用了location和proxy_pass指令的参数。因此，下面两例配置等价：

location /one/ {
    proxy_pass     http://upstream:port/two/;
    proxy_redirect default;
location /one/ {
    proxy_pass     http://upstream:port/two/;
    proxy_redirect http://upstream:port/two/ /one/;
而且因为同样的原因，proxy_pass指令使用变量时，不允许本指令使用default参数。

replacement字符串可以包含变量：

proxy_redirect http://localhost:8000/ http://$host:$server_port/;
而redirect字符串从1.1.11版本开始也可以包含变量：

proxy_redirect http://$proxy_host:8000/ /;
同时，从1.1.11版本开始，指令支持正则表达式。使用正则表达式的话，如果是大小写敏感的匹配，redirect以“~”作为开始，如果是大小写不敏感的匹配，redirect以“~*”作为开始。而且redirect的正则表达式中可以包含命名匹配组和位置匹配组，而在replacement中可以引用这些匹配组的值：

proxy_redirect ~^(http://[^:]+):\d+(/.+)$ $1$2;
proxy_redirect ~*/user/([^/]+)/(.+)$      http://$1.example.com/$2;
除此以外，可以同时定义多个proxy_redirect指令：

proxy_redirect default;
proxy_redirect http://localhost:8000/  /;
proxy_redirect http://www.example.com/ /;
另外，off参数可以使所有相同配置级别的proxy_redirect指令无效：

proxy_redirect off;
proxy_redirect default;
proxy_redirect http://localhost:8000/  /;
proxy_redirect http://www.example.com/ /;
最后，使用这条指令也可以为地址为相对地址的重定向添加域名：

proxy_redirect / /;




{
        set $no_cache 1;
    }

    location ~ ^/(index)\.php(/|$) {
            fastcgi_cache fideloper;
            fastcgi_cache_valid 200 60m; # Only cache 200 responses, cache for 60 minutes
            fastcgi_cache_methods GET HEAD; # Only GET and HEAD methods apply
            add_header X-Fastcgi-Cache $upstream_cache_status;
            fastcgi_cache_bypass $no_cache;  # Don't pull from cache based on $no_cache
            fastcgi_no_cache $no_cache; # Don't save to cache based on $no_cache

            # Regular PHP-FPM stuff:
            include fastcgi.conf; # fastcgi_params for nginx < 1.6.1
            fastcgi_split_path_info ^(.+\.php)(/.+)$;
            fastcgi_pass unix:/var/run/php5-fpm.sock;
            fastcgi_index index.php;
            fastcgi_param LARA_ENV production;
    }
}


location /private {
    expires -1;
    add_header Cache-Control "no-store";
}
