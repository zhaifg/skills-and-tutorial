# Keepalived 的是实例实践
---

## Keeplived MySQL 主从


## Keepalived nginx

## Keepalived haproxy
### master
```
global_defs {
   notification_email {
        acassen@firewall.loc
        failover@firewall.loc
        sysadmin@firewall.loc   
        }  
        
        notification_email_from Alexandre.Cassen@firewall.loc
        smtp_server 192.168.200.1
        smtp_connect_timeout 30 
        router_id HAProxy_DEVEL
    }

    vrrp_script check_haproxy {
        script "killall -0 haproxy"     #设置探测HAProxy服务运行状态的方式，这里的“killall
        #-0 haproxy”仅仅是检测HAProxy服务状态
         interval 2
          weight 21    
    }

    vrrp_instance HAProxy_HA {
        state BACKUP                        #在haproxy-server和backup-haproxy上均配置为BACKUP
        
        interface eth0 
        virtual_router_id 80
        priority 100
        advert_int 2 
        nopreempt   #不抢占模式，只在优先级高的机器上设置即可，优先级低的机器可不设置 
        authentication {
                auth_type PASS 
                auth_pass 1111   
        }
        notify_master "/etc/keepalived/mail_notify.py master "    notify_backup "/etc/keepalived/mail_notify.py backup" 
        notify_fault "/etc/keepalived/mail_notify.py falut"
        track_script {    
            check_haproxy    
        }    
        virtual_ipaddress {
                192.168.66.10/24 dev eth0       #HAProxy的对外服务IP，即VIP    }
        }


```

其中，/etc/keepalived/mail_notify.py文件是一个邮件通知程序，当Keepalived进行Master、Backup、Fault状态切换时，将会发送通知邮件给运维人员，这样可以及时了解高可用集群的运行状态， 以便在适当的时候认为介入故障。
mail_notify.py
```py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sysreload(sys)
from email.MIMEText 
import MIMETextimport smtplibimport MySQLdb
sys.setdefaultencoding('utf-8')
import socket, fcntl, struct
def send_mail(to_list,sub,content):
    mail_host="smtp.163.com"    #设置验证服务器，这里以163.com为例 
    mail_user="username"        #设置验证用户名
    mail_pass="xxxxxx"          #设置验证口令
    mail_postfix="163.com"      #设置邮箱的后缀
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content)
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = to_list
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False
    
def get_local_ip(ifname = 'eth0'):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))
    ret = socket.inet_ntoa(inet[20:24])
    return ret

if sys.argv[1]!="master" and sys.argv[1]!="backup" and sys.argv[1]!="fault":
    sys.exit()
else:
    notify_type = sys.argv[1]

if __name__ == '__main__':
    strcontent = get_local_ip()+ " " +notify_type+状态被激活，确认HAProxy服务运行状态！"

    #下面这段是设置接收报警信息的邮件地址列表，可设置多个
        mailto_list = ['xxxxxx@163.com', xxxxxx@qq.com']
        for mailto in mailto_list:
            send_mail(mailto, "HAProxy状态切换报警", strcontent.encode('utf-8'))
```


## Keepalived lvs