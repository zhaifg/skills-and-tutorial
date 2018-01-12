# nginx命令日志切割平滑升级

标签（空格分隔）： Nginx

---

## 1、 nginx日志切割

`cut_nginx_log.sh`
```
#!/bin/sh
# This script run at 00:00
# The Nginx logs path
logs_path="/usr/local/nginx/logs/"
mkdir -p ${logs_path}$(date -d "yesterday" +"%Y")/$(date -d "yesterday" +"%m")/
mv ${logs_path}access.log ${logs_path}$(date -d "yesterday" +"%Y")/$(date -d "yesterday" +"%m")/access_$(date -d "yesterday" +"%Y%m%d").log
kill -USR1 `cat /usr/local/nginx/logs/nginx.pid`
```  
`Crontab -e 
  00 00 * * * sh  /usr/local/nginx/cut_nginx_log.sh`


##2、Error  No input file specified

1） php.ini（/etc/php5/cgi/php.ini）的配置中这两项
    cgi.fix_pathinfo=1  （这个是自己添加的）
     
2） nginx配置文件/etc/nginx/sites-available/default 中注意以下部分
``` 
location ~ \.php$ {
                fastcgi_pass   127.0.0.1:9000;
                fastcgi_index  index.php;
                fastcgi_param  SCRIPT_FILENAME  /var/www/nginx-default$fastcgi_script_name;
                include               fastcgi_params;
        }
```
/var/www/nginx-default路径需要根据你主机主目录的实际情况填写
配置完以上部分，重启一下nginx和php-fpm


## 3、Nginx的信号命令
`Kill - 信号类型 `cat /xxxx/nginx.pid``
1) 从容的停止Nginx
 `Kill -QUIT Nginx 主进程号`
 
2) 快速停止Nginx
 ` Kill - TERM Nginx主进程号`
 ` Kill - INT Nginx主进程号`

3) 强制停止所有Nginx进程
 `Pkill -9 nginx`

4) 平滑的重启
  `Kill -HUP Nginx主进程号`

5) Nginx信号
`TERM,INT`  快速关闭
`QUIT` 从容关闭  
`HUP`  平滑重启，重新加载配置文件
`USR1` 重新打开配置文件，在切割日志文件时用于较大
`USR2` 平滑升级可执行程序
`WINCH`  从容关闭工作进程


## 4、Nginx平滑升级
  （1）使用新的可执行程序替换旧的可执行程序，对于编译安装的nginx，可以将新版本编译安装到旧版本的安装路径中。替换之前，最好备份一下旧的可执行文件。
  
  （2）发送一下指令 kill USR2 旧版本的Nginx主进程号。
  
  （3）旧版本Nginx的煮即成将重命名它的.pid文件为.oldbin。然后执行新版的的Nginx可执行程序，依次启动新的主进程和新的工作进程。
  
  （4）此时，新、旧版本的Nginx实例会同时运行，共同处理输入的请求。要逐步停止旧版本的Nginx实例，你必须发送WINCH信号给旧的主进程，然后，它的工作进程就将开始从容的关闭。Kill - WINCH 旧版本的NGINX主进程号。
  
  （5）一段时间后，旧的工作进程处理了所有已有连接的请求后退出，由新的工作进程来处理输入的请求。
  
  （6）这时候，我们可以决定使用新版本，还是恢复到旧的版本。





