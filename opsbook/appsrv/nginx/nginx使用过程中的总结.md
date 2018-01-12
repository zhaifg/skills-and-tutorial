# nginx使用过程中的总结

标签（空格分隔）： Nginx

---

https://serversforhackers.com/nginx-caching/

## Q1, 当nginx反向代理多台tomcat时,不能登录.
>  nginx默认的upstream默认使用的是轮训,当提交请求时可能会分发到不同的后端app,所以会不能登录.

## Q2, 当nginx反向代理并且使用proxy_cache时,不想对某些请求缓存的操作方法.
> 1. 使用location,i系统的变量,正则取得相应的文件,通过添加add_header,或者自定义`set $no_cache`,
     proxy_no_cache $no_cache; (自己总结,需要实验)
  2. 使用proxy_cache_bypass 与proxy_no_cache两个结合使用.
  语法: proxy_cache_bypass string ...;
  默认值: -
  上下文: http, server, location
  定义 nignx不从缓存取响应的条件.如果至少一个字符串条件非空而且非"o",nginx就不会从缓存中去响应:
  ```
  proxy_cache_bypass $cookie_nocache $arg_nocahe$arg_comment
  proxy_cache_bypass $http_pragma $http_authorization;
  ```
  本指令可与proxy_no_cache一起使用.
  语法: proxy_no_cache string ...
  默认值: -
  上下文: http, server, location
  定义nginx不将响应写入缓存的条件.如果至少一个字符串条件非空而且非"o",nginx就不将响应写入缓存:
  ```
  proxy_cache_bypass $cookie_nocache $arg_nocahe$arg_comment
  proxy_cache_bypass $http_pragma $http_authorization;
  ```
  
  ## Q3, nginx的location一个目录转发,后端不存在此目录时的操作?
  
  







