#cobbler
---
## 环境准备;
### Cobbler/Cobblerd
First and foremost, cobbler requires Python. Any version over 2.6 should work. Cobbler also requires the installation of the following packages:
>>
createrepo
httpd (apache2 for Debian/Ubuntu)
mkisofs
mod_wsgi (libapache2-mod-wsgi for Debian/Ubuntu)
mod_ssl (libapache2-mod-ssl)
python-cheetah
python-netaddr
python-simplejson
python-urlgrabber
PyYAML (python-yaml for Debian/Ubuntu)
rsync
syslinux
tftp-server (atftpd for Debian/Ubuntu, though others may work)
yum-utils


## Cobbler-Web
Cobbler web only has one other requirement besides cobbler itself:
> 
Django (python-django for Debian/Ubuntu)


```
yum install  cobbler-web 
```
## Koan
Koan can be installed apart from cobblerd, and has only the following requirement (besides python itself of course):
>
python-simplejson

## Source Prerequisites
Installation from source requires the following additional packages:
```
git
make
python-devel
python-setuptools
python-cheetah
openssl
```

```bash
yum install -y createrepo httpd mkisofs mod_wsgi  mod_ssl python-cheetah python-netaddr python-simplejson python-urlgrabber PyYAML rsync syslinux tftp-server yum-utils

yum install -y git make python-devel python-setuptools python-cheetah openssl openssl-devel

yum install -y cobbler 
setenforce 0;


```

## 配置Cobbler
Cobbler的配置文件`/etc/cobbler/settings`

`vim  /etc/cobbler/settings` 

* 1.设置`default_password_crypted`
```bash 
openssl passwd -1

vim /etc/cobbler/settings 
default_password_crypted: "passwd"
```

* 2.配置`server:`, `next_server`;
server: Cobbler服务器的IP地址, 不能使用`0.0.0.0`
`next_server`: 为将要建立的httpd, dhcpd等地址.

* 3.配置dhcp, dns, ftp等地址
```
#default 0, 修改为1, 表示生成dhcpd.conf ,使用dhcpd.template模板
manage_dhcp:0;
```

manage_dhcp：1  dhcpd/dnsmasq
manage_dns：1 dhcpd/dnsmasq
manage_tftpd：1
restart_dhcp：1
restart_dns：1
pxe_just_once：1

```
/etc/cobbler/modules.conf：
清单 1. 配置设置
[dns]
module = manage_dnsmasq

[dhcp]
module = manage_dnsmasq

[tftpd]
module = manage_in_tftpd
```

* 4.修改dhcpd.templage
```
vim /etc/cobbler/dhcp.template 
ddns-update-style interim;

allow booting;
allow bootp;

ignore client-updates;
set vendorclass = option vendor-class-identifier;

option pxe-system-type code 93 = unsigned integer 16;

subnet 192.168.20.0 netmask 255.255.255.0 {
     option routers             192.168.20.1;
     option domain-name-servers 192.168.20.1;
     option subnet-mask         255.255.255.0;
     range dynamic-bootp        192.168.20.100 192.168.20.254;
     default-lease-time         21600;
     max-lease-time             43200;
     next-server                $next_server;
     class "pxeclients" {
          match if substring (option vendor-class-identifier, 0, 9) = "PXEClient";
          if option pxe-system-type = 00:02 {
                  filename "ia64/elilo.efi";
          } else if option pxe-system-type = 00:06 {
                  filename "grub/grub-x86.efi";
          } else if option pxe-system-type = 00:07 {
                  filename "grub/grub-x86_64.efi";
          } else {
                  filename "pxelinux.0";
          }
     }

}

#for dhcp_tag in $dhcp_tags.keys():
    ## group could be subnet if your dhcp tags line up with your subnets
    ## or really any valid dhcpd.conf construct ... if you only use the
    ## default dhcp tag in cobbler, the group block can be deleted for a
    ## flat configuration
# group for Cobbler DHCP tag: $dhcp_tag
group {
        #for mac in $dhcp_tags[$dhcp_tag].keys():
            #set iface = $dhcp_tags[$dhcp_tag][$mac]
    host $iface.name {
        hardware ethernet $mac;
        #if $iface.ip_address:
        fixed-address $iface.ip_address;
        #end if
        #if $iface.hostname:
        option host-name "$iface.hostname";
        #end if
        #if $iface.netmask:
        option subnet-mask $iface.netmask;
        #end if
        #if $iface.gateway:
        option routers $iface.gateway;
        #end if
        #if $iface.enable_gpxe:
        if exists user-class and option user-class = "gPXE" {
            filename "http://$cobbler_server/cblr/svc/op/gpxe/system/$iface.owner";
        } else if exists user-class and option user-class = "iPXE" {
            filename "http://$cobbler_server/cblr/svc/op/gpxe/system/$iface.owner";
        } else {
            filename "undionly.kpxe";
        }
        #else
        filename "$iface.filename";
        #end if
        ## Cobbler defaults to $next_server, but some users
        ## may like to use $iface.system.server for proxied setups
        next-server $next_server;
        ## next-server $iface.next_server;
    }
        #end for
}
        

```

## 建立配置cobbler默认的镜像目录
```
mkdir -pv /var/www/cobbler/ks_mirror
```

## 通过cobbler check命令检测配置并修复
```
cobbler check
```
提示, 比如,修改xintd.d/下的rsync,tftp的启动等
```
yum install dhcp
vim  /etc/xinetd.d/rsync 

cobbler check

/etc/init.d/dhcpd start
vim  /etc/xinetd.d/tftp
/etc/init.d/xinetd restart

cobbler get-loaders

# vim /usr/lib/python2.6/site-packages/cobbler/action_dlcontent.py
# vim /usr/lib/python2.6/site-packages/cobbler/settings.py

cobbler get-loaders
cobbler check
/etc/init.d/iptables stop

yum install pykickstart
yum install fence-agents 

/etc/init.d/cobblerd restart

cobbler check
yum install rsync
vim /etc/xinetd.d/rsync 

yum install debmirror
```

## 同步cobbler的配置
```
cobbler sync
less /etc/dhcp/dhcpd.conf 
/etc/init.d/dhcpd status
```


##导入第一个镜像

### 1. 建立挂载目录并挂载镜像
```bash
mkdir /mnt/iso/centos7 -pv
mount -t iso9660 -o loop,ro  CentOS-7-x86_64-DVD-1511.iso /mnt/iso/centos7/
ll /mnt/iso/centos7/
```

### 2. 导入镜像到cobbler
```bash
cobbler import --name=centos7 --arch=x86_64 --path=/mnt/iso/centos7/
cobbler distro list
cobbler distro report --name=centos7-x86_64
```

### 3. 查看镜像信息
* 1.镜像的profile
```
cobbler profile  list
```

* 2.对象详情查看
```
cobbler distro report --name=centos7-x86_64

Name                           : centos7-x86_64
Architecture                   : x86_64
TFTP Boot Files                : {}
Breed                          : redhat
Comment                        : 
Fetchable Files                : {}
Initrd                         : /var/www/cobbler/ks_mirror/centos7-x86_64/images/pxeboot/initrd.img
Kernel                         : /var/www/cobbler/ks_mirror/centos7-x86_64/images/pxeboot/vmlinuz
Kernel Options                 : {}
Kernel Options (Post Install)  : {}
Kickstart Metadata             : {'tree': 'http://@@http_server@@/cblr/links/centos7-x86_64'}
Management Classes             : []
OS Version                     : rhel7
Owners                         : ['admin']
Red Hat Management Key         : <<inherit>>
Red Hat Management Server      : <<inherit>>
Template Files                 : {}
```

* 3.自定义kickstart文件,
默认的情况下, cobbler会自动建立一个kickstart文件, 存放在`/var/lib/cobbler/kickstarts/sample_end.ks`, 我们可以根据详情自定义kickstart.ks文件.

上传自定义的kickstart文件到/var/lib/cobbler/kickstarts/our.cfg

修改profile
```
cobbler edit --name=centos7-x86_64 --kickstart=/var/lib/cobbler/kickstarts/our.cfg
```


```
 修改安装系统的内核参数，在CentOS7系统有一个地方变了，就是网卡名变成eno16777736这种形式，但是为了运维标准化，我们需要将它变成我们常用的eth0，因此使用下面的参数。但要注意是CentOS7才需要下面的步骤，CentOS6不需要。
[root@linux-node1 ~]# cobbler profile edit --name=CentOS-7.1-x86_64 --kopts='net.ifnames=0 biosdevname=0'
[root@linux-node1 ~]# cobbler profile report CentOS-7.1-x86_64
Name                           : CentOS-7.1-x86_64
TFTP Boot Files                : {}
Comment                        : 
DHCP Tag                       : default
Distribution                   : CentOS-7.1-x86_64
Enable gPXE?                   : 0
Enable PXE Menu?               : 1
Fetchable Files                : {}
Kernel Options                 : {'biosdevname': '0', 'net.ifnames': '0'}
Kernel Options (Post Install)  : {}
Kickstart                      : /var/lib/cobbler/kickstarts/CentOS-7.1-x86_64.cfg
Kickstart Metadata             : {}
Management Classes             : []
Management Parameters          : <<inherit>>
Name Servers                   : []
Name Servers Search Path       : []
Owners                         : ['admin']
Parent Profile                 : 
Internal proxy                 : 
Red Hat Management Key         : <<inherit>>
Red Hat Management Server      : <<inherit>>
Repos                          : []
Server Override                : <<inherit>>
Template Files                 : {}
Virt Auto Boot                 : 1
Virt Bridge                    : xenbr0
Virt CPUs                      : 1
Virt Disk Driver Type          : raw
Virt File Size(GB)             : 5
Virt Path                      : 
Virt RAM (MB)                  : 512
Virt Type                      : kvm
```

* 4.修改新建系统的banner
```
#修改Cobbler提示
[root@linux-node1 ~]# vim /etc/cobbler/pxe/pxedefault.template
MENU TITLE Cobbler | http://www.example.com
[root@linux-node1 ~]# cobbler sync # 修改配置都要同步
```

## 定制要安装的系统
```
cobbler system add --name=centos71 --profile=centos7-x86_64

cobbler system edit --name=centos71 --interface=eth1 --mac=00:0C:29:34:E8:87 --ip-address=192.168.20.1 --netmask=255.255.255.0 --static=1 --dns-name=192.168.20.1
```
hostname...


比如定制mac, ip,dns,

## 配置cobbler-web
```
/etc/cobbler/users.conf       # Web服务授权配置文件
/etc/cobbler/users.digest     # 用于web访问的用户名密码配置文件
[root@linux-node1 ~]# cat /etc/cobbler/users.digest
cobbler:Cobbler:a2d6bae81669d707b72c0bd9806e01f3
# 设置Cobbler web用户登陆密码
# 在Cobbler组添加cobbler用户，提示输入2遍密码确认
[root@linux-node1 ~]# htdigest /etc/cobbler/users.digest "Cobbler" cobbler
Changing password for user cobbler in realm Cobbler
New password: 123456
Re-type new password:123456
[root@linux-node1 ~]# cobbler sync
[root@linux-node1 ~]# /etc/init.d/httpd restart
停止 httpd：                                               [确定]
正在启动 httpd：                                           [确定]
[root@linux-node1 ~]# /etc/init.d/cobblerd restart
Stopping cobbler daemon:                                   [确定]
Starting cobbler daemon:                                   [确定]
```

## 使用api编程



## Cobbler自定义安装

1.将新服务器划入装机vlan
2.根据资产清单上的mac地址，自定义安装
    A、机房
    B、机房区域
    C、机柜
    D、服务器位置
    E、服务器网线接入端口
    F、该端口mac地址
    G、profile 操作系统 分区等 预分配的IP地址 主机名 子网 网关 dns 角色
3.自动化装机平台，安装
    新建一台虚拟机
    设置如下
    00:50:56:3A:07:6F
    linux-node3.oldboyedu.com
    255.255.255.0
    192.168.56.2
    192.168.56.2
添加一台主机指定mac（虚拟机可以生成一个mac地址），IP，主机名
```
cobbler system add --name=linux-node3.oldboyedu.com --mac=00:50:56:3A:07:6F --profile=CentOS-7-x86_64 \
--ip-address=192.168.56.120 --subnet=255.255.255.0 --gateway=192.168.56.2 --interface=eth0 \
--static=1 --hostname=linux-node3.oldboyedu.com --name-servers="192.168.56.2" \
--kickstart=/var/lib/cobbler/kickstarts/CentOS-7-x86_64.cfg
```
执行cobbler system list查看添加的system
```
[root@linux-node2 kickstarts]# cobbler system list
   linux-node3.oldboyedu.com
```
注意：一定要执行cobbler sync进行同步配置，否则不生效

通过cat /etc/dhcp/dhcpd.conf可以查看到配置信息已添加
```
group {
    host generic1 {
        hardware ethernet 00:50:56:3A:07:6F;
        fixed-address 192.168.56.120;
        option host-name "linux-node3.oldboyedu.com";
        option subnet-mask 255.255.255.0;
        option routers 192.168.56.2;
        filename "/pxelinux.0";
        next-server 192.168.56.12;
    }
}
```
最后，启动刚才创建的虚拟机，无需任何人工干预，即可啪啪啪装机了。

## cobbler的API
API定义文件所在目录

/etc/httpd/conf.d/,此目录下的文件
```
[root@linux-node2 conf.d]# ll
total 36
-rw-r--r-- 1 root root 2926 May 12 18:27 autoindex.conf
-rw-r--r-- 1 root root 1087 Jan 24 22:40 cobbler.conf
-rw-r--r-- 1 root root 1165 Jan 24 22:40 cobbler_web.conf
-rw-r--r-- 1 root root  366 May 12 18:28 README
-rw-r--r-- 1 root root 9438 May 12 18:16 ssl.conf
-rw-r--r-- 1 root root 1252 May 12 18:16 userdir.conf
-rw-r--r-- 1 root root  824 May 12 18:16 welcome.conf
```
API：
ProxyPass /cobbler_api http://localhost:25151/
ProxyPassReverse /cobbler_api http://localhost:25151/
通过编写python来自动化安装系统
```python
#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import xmlrpclib 

class CobblerAPI(object):
    def __init__(self,url,user,password):
        self.cobbler_user= user
        self.cobbler_pass = password
        self.cobbler_url = url
    
    def add_system(self,hostname,ip_add,mac_add,profile):
        '''
        Add Cobbler System Infomation
        '''
        ret = {
            "result": True,
            "comment": [],
        }
        #get token
        remote = xmlrpclib.Server(self.cobbler_url) 
        token = remote.login(self.cobbler_user,self.cobbler_pass) 
        
        #add system
        system_id = remote.new_system(token) 
        remote.modify_system(system_id,"name",hostname,token) 
        remote.modify_system(system_id,"hostname",hostname,token) 
        remote.modify_system(system_id,'modify_interface', { 
            "macaddress-eth0" : mac_add, 
            "ipaddress-eth0" : ip_add, 
            "dnsname-eth0" : hostname, 
        }, token) 
        remote.modify_system(system_id,"profile",profile,token) 
        remote.save_system(system_id, token) 
        try:
            remote.sync(token)
        except Exception as e:
            ret['result'] = False
            ret['comment'].append(str(e))
        return ret

def main():
    cobbler = CobblerAPI("http://192.168.56.12/cobbler_api","cobbler","cobbler")
    ret = cobbler.add_system(hostname='cobbler-api-test',ip_add='192.168.56.121',mac_add='00:50:56:28:3D:4F',profile='CentOS-7-x86_64')
    print ret

if __name__ == '__main__':
    main()
```

这个脚本中addsystem方法中需要四个参数:主机名，IP地址，mac地址和profile。 注意：mac地址可以通过创建一台虚拟机时生成而获得 执行脚本python cobblerapi.py，脚本执行成功会有如下提示：
```
[root@linux-node2 ~]# python cobbler_api.py 
{'comment': [], 'result': True}
通过cobbler system list查看

[root@linux-node2 ~]# cobbler system list
   cobbler-api-test
   linux-node3.oldboyedu.com
```
最后，打开电源，就可以啪啪啪装机了，无需人工干预。

## 通过koan重装系统
假如某台机器需要重装系统，使用cobbler也可以完成。这里要用到koan这个工具，这个工具安装在需要重装的那个操作系统上，我用上面刚装完的系统做一下测试。

首先，更新一下yum源
```
[root@cobbler-api-test ~]# wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
```
执行
```
[root@cobbler-api-test ~]# yum install -y koan
```
指定cobbler所在服务器的IP地址
```
[root@cobbler-api-test ~]# koan --replace-self --server=192.168.56.12 --profile=CentOS-7-x86_64

- looking for Cobbler at http://192.168.56.12:80/cobbler_api
- reading URL: http://192.168.56.12/cblr/svc/op/ks/profile/CentOS-7-x86_64
install_tree: http://192.168.56.12/cblr/links/CentOS-7-x86_64
downloading initrd initrd.img to /boot/initrd.img_koan
url=http://192.168.56.12/cobbler/images/CentOS-7-x86_64/initrd.img
- reading URL: http://192.168.56.12/cobbler/images/CentOS-7-x86_64/initrd.img
downloading kernel vmlinuz to /boot/vmlinuz_koan
url=http://192.168.56.12/cobbler/images/CentOS-7-x86_64/vmlinuz
- reading URL: http://192.168.56.12/cobbler/images/CentOS-7-x86_64/vmlinuz
- ['/sbin/grubby', '--add-kernel', '/boot/vmlinuz_koan', '--initrd', '/boot/initrd.img_koan', '--args', '"ksdevice=link lang= text net.ifnames=0 ks=http://192.168.56.12/cblr/svc/op/ks/profile/CentOS-7-x86_64 biosdevname=0 kssendmac "', '--copy-default', '--make-default', '--title=kick1465316032']
- ['/sbin/grubby', '--update-kernel', '/boot/vmlinuz_koan', '--remove-args=root']
- reboot to apply changes
```
可以看到最后提示reboot让改动生效。执行reboot。

接下来，通过虚拟机的界面可以看到系统开始重装，啪啪啪，无需人工干预。其实是在grub上新增了一条安装项

生产环境中，专门划分一个装机vlan。
