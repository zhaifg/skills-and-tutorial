# Nginx与php

标签（空格分隔）： Nginx

---

##１. nginx与php的上传文件修改
对于nginx+php的一些网站，上传文件大小会受到多个方面的限制，一个是nginx本身的限制，限制了客户端上传文件的大小，一个是php.ini文件中默认了多个地方的设置。下面我们来看看如何修改这些限制
1. 修改PHP配置文件中的三项：`vim /usr/local/php/etc/php.ini`
　　（1）`post_max_size = 50M`　　　　　　#PHP可接受的最大POST数据
　　（2）`upload_max_filesize = 50M`　　　#文件上传允许的最大值
　　（3）`max_execution_time = 300`　　　#每个脚本的最大执行时间，秒钟（0则不限制，不建议设0）
2. 修改Nginx配置文件：`vim /usr/local/nginx/conf/nginx.conf`　(如果忘了配置文件的具体位置，可以使用 locate nginx.conf 查找)
　　（1）`client_max_body_size 50m`　　　#客户端最大上传大小 50M
3. 重启PHP：`/etc/init.d/php-fpm restart`
4. 平滑重启Nginx：`/usr/local/nginx/sbin/nginx -s reload`





