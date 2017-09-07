#CentOS7的常规操作
---

## 1. Register and Enable Red Hat Subscription


## 2. Configure Network with Static IP Address
```
* Two character prefixes based on the type of interface:
*   en -- ethernet
*   sl -- serial line IP (slip)
*   wl -- wlan
*   ww -- wwan
*
* Type of names:
*   b<number>                             -- BCMA bus core number
*   ccw<name>                             -- CCW bus group name
*   o<index>                              -- on-board device index number
*   s<slot>[f<function>][d<dev_port>]     -- hotplug slot index number
*   x<MAC>                                -- MAC address
*   [P<domain>]p<bus>s<slot>[f<function>][d<dev_port>]
*                                         -- PCI geographical location
*   [P<domain>]p<bus>s<slot>[f<function>][u<port>][..][i<interface>]
*                                         -- USB port number chain
```
配置静态IP
安装命令集(ifconfig netstat等命令)
`yum install net-tools`

配置静态IP`/etc/sysconfig/network-script/ifcfg-ethxxx`
```bash
TYPE=Ethernet
BOOTPROTO=none
DEFROUTE=yes
PEERDNS=yes
PEERROUTES=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_PEERDNS=yes
IPV6_PEERROUTES=yes
IPV6_FAILURE_FATAL=no

IPADDR=192.168.8.114
PREFIX=24
GATEWAY=192.168.8.1
DNS1=114.114.114.114

NAME=eno16777736
DEVICE=eno16777736
ONBOOT=yes

```

`service restart network`

`ip addr show`
**改成eth形式的**
原来为eno16667, 改为eth0
修改`/etc/default/grub` 在下面行添加`net.ifnames=0`如下:

`GRUB_CMDLINE_LINUX="crashkernel=auto rd.lvm.lv=centos/root rd.lvm.lv=centos/swap net.ifnames=0  rhgb quiet"`
生成新的grub引导文件`sudo grub2-mkconfig -o /boot/grub2/grub.cfg`

修改或者清除` /etc/udev/rules.d/80-'hostname'.rules`文件, or `/etc/udev/rules.d/90-eno-fix.rules`
修改:
`SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTR{address}=="08:00:27:a9:7a:e1", ATTR{type}=="1", KERNEL=="eth*", NAME="eth0"`

清除时, 如果是虚拟机最好重新生成下mac

修改或者清除

## 3. Set Hostname of Server
```bash
echo $HOSTNAME
vi /etc/hostname

echo $HOSTNAME
```

## 4. Update or Upgrade CentOS Minimal Install

```bash
yum  -y update && yum -y  upgrade
```
## 5. Install Command Line Web Browser
```bash
yum install links
```

## 6. Install Apache HTTP Server
```bash
yum  -y install httpd httpd-devel

firewall-cmd --add-service=http
# firewall-cmd --parmanent -add-port=3221/tcp 

# reload firewall
firewall-cmd --reload

systemctl start httpd.service
systemctl enable httpd.service
```

## 7. Install PHP

```bash
yum -y install php

systemctl restart httpd.service


```

## 8. Install MariaDB Database
```bash
yum install mariadb-server mariadb

systemctl start mariadb.service
systemctl enable mariadb.service

firewall-cmd --add-service=mysql
/usr/bin/mysql_secure_installation
```

## 9. Install and Configure SSH Server
```bash
ssh -V
# /etc/ssh/ssh_config


```

## 10. Install GCC (GNU Compiler Collection)
```bash
yum install gcc
gcc -version
```

## 11. Install Java


## 12. Install Apache Tomcat


## 13. Install Nmap to Monitor Open Ports
```bash
yum install nmap

firewall-cmd --list-ports
```

## 14. FirewallD Configuration
firewalld替换了iptables
```bash
systemctl status firewalld

firewall-cmd --state
firewall-cmd --get-zones
firewall-cmd --zone=work --list-all
firewall-cmd --get-default-zone
firewall-cmd --set-default-zone=work
firewall-cmd --list-services

firewall-cmd --add-service=http
firewall-cmd --reload
firewall-cmd --add-service=http --permanent
firewall-cmd  --remove-service=http
firewall-cmd --zone=work --remove-service=http --permanent
firewall-cmd --add-port=331/tcp
firewall-cmd --add-port=331/tcp --permanent
firewall-cmd --remove-port=331/tcp
firewall-cmd --remove-port=331/tcp --permanent

systemctl stop firewalld
systemctl disable firewalld
firewall-cmd --state

```
