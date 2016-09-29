# KVM的基础基于CentOS7
---

## 安装
```
@virtualization-hypervisor
@virtualization-client
@virtualization-platform
@virtualization-tools

 yum install qemu-kvm qemu-img libvirt

```
### 推荐的包
`python-virtinst`: virt-install

`libvirt-python`
`virt-manager`
`libvirt-client`

```
 yum install virt-install libvirt-python virt-manager python-virtinst libvirt-client
```

## KVM安装系统
安装系统可以是图形界面, 也可以使用命令. 主要是命令为主.

### 使用virt-install 安装

virt-install 命令介绍:
`--name`: 虚拟机的名称
`--disk`: 指定虚拟机安装的虚拟磁盘
`--graphics`: 指定安装虚拟机时的界面, 比如vnc, spice, none(自动安装)
`--vcpus`: 指定的cpu的个数
`--ram`: 指定分配的内存大小,单位MB
`--location`: 指定ISO安装镜像的url, 可以http,ftp, nfs等, 使用光驱时不使用这个
`--extra-args`: 当时使用`--location`时, 使用此参数指定额外的属性. 例如指定console.
`--network bridge`: 使用哪个网桥
`--os-type`: 操作系统类型, linux, winxp
`--os-variant`: 操作系统的版本, 如rhel7
`--cd-rom`: 使用光驱挂载iso, 
`--hvm `: 指定为全虚拟化
` --nographics`
`--pxe`
`--file`: 
`--nodisks`
`--filesystem`




- 1.实例1
```
virt-install \
   --name=guest1-rhel7-64 \
   --disk path=/var/lib/libvirt/images/guest1-rhel7-64.dsk,size=8,sparse=false,cache=none \
   --graphics spice \
   --vcpus=2 --ram=2048 \
   --location=http://example1.com/installation_tree/RHEL7.2-Server-x86_64/os \
   --network bridge=br0 \
   --os-type=linux \
   --os-variant=rhel7
```

- 2.实例2, 使用virtio-scsi控制器安装
```
 virt-install \
   --name=guest1-rhel7 \
   --controller type=scsi,model=virtio-scsi \
   --disk path=/var/lib/libvirt/images/guest1-rhel7.dsk,size=8,sparse=false,cache=none,bus=scsi \
   --graphics spice \
   --vcpus=2 --ram=2048 \
   --location=http://example1.com/installation_tree/RHEL7.1-Server-x86_64/os \
   --network bridge=br0 \
   --os-type=linux \
   --os-variant=rhel7
```

> --os-type 确保这个参数与安装系统一致, 优化驱动

- 3.实例3.pxe安装
默认情况下，如果没有网络，客户虚拟机将尝试从其他启动设备(bootable)启动。如果没有其他的启动设备, 安装被暂停. 可以尝试使用qemu-kvm的启动`reboot-timeout`, 超时重试;
`qemu-kvm -boot reboot-timeout=1000`

全虚拟化安装guest os
```
virt-install --hvm --connect qemu:///system \
--network=bridge:br0 --pxe --graphics spice \
--name=rhel7-machine --ram=756 --vcpus=4 \
--os-type=linux --os-variant=rhel7 \
--disk path=/var/lib/libvirt/images/rhel7-machine.img,size=10
```

使用kickstart 安装
```
virt-install -n rhel7ks-guest -r 1024 --file=/var/lib/libvirt/images/rhel7ks-guest.img --file-size=10 \
 --location /var/lib/libvirt/images/rhel-server-7.1-x86_64-dvd.iso --nographics \
 --extra-args="ks=http://192.168.122.1/ks.cfg ip=dhcp \
console=tty0 console=ttyS0,115200n8” --os-variant=rhel7.0

```

- 4.使用Text模式安装
```
virt-install -n rhel7anaconda-guest -r 1024 --disk=path=/path/to/rhel7anaconda-guest.img,size=10 \
--location /mnt/RHEL7DVD --nographics \
--extra-args=”console=tty0 console=ttyS0,115200n8” \
--disk=path=/path/to/rhel7-dvd.iso,device=cdrom
```

- 5.使用nat的network方式安装
```
 virt-install --network=default \
      --name=rhel7-machine --ram=756 --vcpus=4 \
      --os-type=linux --os-variant=rhel7
```

- 6.指定dhcp的安装
```
virt-install --network=br0 \
        --name=rhel7-machine --ram=756 --vcpus=4 \
        --os-type=linux --os-variant=rhel7
```

- 7.指定IP地址安装
```
virt-install
        --network=br0 \
        --name=rhel7-machine --ram=756 --vcpus=4 \
        --os-type=linux --os-variant=rhel7 \
        --extra-args=”ip=192.168.1.2::192.168.1.1:255.255.255.0:test.example.com:eth0:none”
```

`ip=[ip]::[gateway]:[netmask]:[hostname]:[interface]:[autoconf]`

### 优雅的关闭guest os方式

- 1.通过修改libvirt-guests服务配置参数来实现
  - 1.1 `vim /etc/sysconfig/libvirt-guests`
   Edit the file, remove the comment mark (#) and change the ON_SHUTDOWN=suspend to ON_SHUTDOWN=shutdown. Remember to save the change.

  - 1.2 启动libvirt-guests服务

## 半虚拟化驱动 virtio

### 已存在的设备进行半虚拟化的添加

1. 确保已经正确的安装了正确的驱动(viostor)
2. 使用virsh edit修改相应的guest os. 使用root用户, 要修改的guest的配置文件的存储路径在 /etc/libvirt/qemu下, 使用virsh修改
3. 下面的配置文件的是默认情况下(使用的virtual ide), 没有使用virtio的.
```xml
<disk type='file' device='disk'>
   <source file='/var/lib/libvirt/images/disk1.img'/>
   <target dev='hda' bus='ide'/>
</disk>
```
4. 修改`bus`属性为`virtio` ,同时修改`dev`属性从如hda, hdb, hdc修改为相应的vda, vdb, vdc.
```xml
<disk type='file' device='disk'>
   <source file='/var/lib/libvirt/images/disk1.img'/>
   <target dev='vda' bus='virtio'/>
</disk>
```

5. 删除disk标签内的address标签。这步必须做, libvirt会在适当时间重新生成新的address


> virt-manager, virsh attach-disk or virsh attach-interface 可以使用virto新建新的磁盘

### 新设备使用virto
#### 使用virt-manager


## 网络配置
rhel7 支持的虚拟网络为
1. 使用nat
2. 直接使用物理网卡
3. 直接分配的使用PCIe SR-IOV的虚拟网卡
4. 桥接


### 使用nat(默认的方式)
查看kvm的网络形式
`virsh net-list --all`
```
virsh net-list --all
 Name                 State      Autostart     Persistent
----------------------------------------------------------
 default              active     yes           yes


ll /etc/libvirt/qemu/
total 4
drwx------ 3 root root   40 Sep 21 14:36 networks
-rw------- 1 root root 3776 Sep 22 17:04 test01.xml
```


自动启动默认的网络
```
virsh net-autstart default
#手动启动
virsh net-start default
```

一旦libvrit启动了默认的网络, 会看到一个桥接的网卡, 这个网卡不是真实的物理网卡, 这个 设备用来转发与真实的网卡与guest os 的数据. 宿主机需要打开ip 的转发.

libvirt 添加一条iptables规则用于guest os与桥接网卡的通信, INPUT, OUTPUT, POSTROUTING链

guest os的配置文件
```
<interface type='network'>
   <source network='default'/>
</interface>
```
mac地址是可选定义的, 可以自动生成.
```
<interface type='network'>
  <source network='default'/>
  <mac address='00:16:3e:1a:b3:4a'/>
</interface>
```


### virt-net

virt-net 的zero-copy

### 桥接网络
创建桥接网络的方式:
- 1.使用nmtui
- 2.使用nmcli
```bash
# 新建桥接
~]# nmcli con add type bridge ifname br0
Connection 'bridge-br0' (6ad5bba6-98a0-4f20-839d-c997ba7668ad) successfully added.


~]$ nmcli con show
NAME        UUID                                  TYPE            DEVICE
bridge-br0  79cf6a3e-0310-4a78-b759-bda1cc3eef8d  bridge          br0
eth0        4d5c449a-a6c5-451c-8206-3c9a4ec88bca  802-3-ethernet  eth0

~]# nmcli con modify bridge-br0 bridge.stp no

~]# nmcli con modify bridge-br0 bridge.stp yes

~]$ nmcli con add type bridge ifname br5 stp yes priority 28672
Connection 'bridge-br5' (86b83ad3-b466-4795-aeb6-4a66eb1856c7) successfully added.


~]$ nmcli connection modify bridge-br5 bridge.priority 36864

~]$ nmcli -f bridge con show bridge-br0

~]$ nmcli connection edit bridge-br0

nmcli> set bridge.priority 4096
nmcli> save
Connection 'bridge-br0' (79cf6a3e-0310-4a78-b759-bda1cc3eef8d) successfully saved.
nmcli> quit
```

3. 使用ip命令与brctl
```
brctl show
brctl addbr br0
brctl addif eth0

ip link add br0 type bridge
ip 
```


4. 编辑配置文件
```
DEVICE=br0
TYPE=Bridge
IPADDR=192.168.1.1
PREFIX=24
BOOTPROTO=none
ONBOOT=yes
DELAY=0
```



#### bond网卡的桥接

`/etc/sysconfig/network-scripts/ifcfg-bond0`
```
DEVICE=brbond0
ONBOOT=yes
TYPE=Bridge
IPADDR=192.168.1.1
PREFIX=24
```

#### 激活桥接网卡
```
ifup
ip  link set  br0 up

service network restart
```

### libvirt 桥接网卡
`<bridge name='br0' macTableManager='libvirt'/>`



### KVM 半虚拟化
提高guest windows 性能
`yum install virt-win`
配置win客户系统

## KVM的过量私用资源

### 超量使用内存
实例1
server1, 32GB ram, 被分配给50个虚拟机, 每个guest为1GB,宿主机自身需要4G内存以及需要4GBswap(最小量);

在宿主机需要分配多大的swap才能保证超量使用内存呢:

1. 计算每个虚拟机所需的内存的综合, 如: 50*1G=50G
2. 计算宿主机的所欲要的内存,swap的总量和: 50G +　4G + 4G=58G;
3. 以上可以算出来要运行这么多虚拟机时需要的总内存数为:58G, 现在只有32GB(物理内存), 要保证可以运行时, 还需要的内存为: 58G-32G=26G, 需要建立swap的大小为26G.

### 超量使用cpu


## KVM 客户机的时间管理
KVM的虚拟机中断不是真实的中断, 而是模拟出来的.
KVM-clock
ntpd
TSC:   cat /proc/cpuinfo | grep constant_tsc


## libvirt的网络启动

### 设置libvirt的私有网络的pxe  server启动

- 1.设置是PXE启动镜像, 配置目录 /var/lib/tftp
- 2. 设置
```
virsh net-destroy default
virsh net-edit default
```

- 3.编辑<ip>元素, 包括合适的IP, 掩码,dhcp的范围和启动的镜像文件`BOOT_FILENAME`.
```
<ip address='192.168.122.1' netmask='255.255.255.0'>
   <tftp root='/var/lib/tftp' />
   <dhcp>
      <range start='192.168.122.2' end='192.168.122.254' />
      <bootp file='BOOT_FILENAME' />
   </dhcp>
</ip>
```

- 4.run: `virsh net-start default`

- 5.`virt-install --pxe --network bridge=breth0 --prompt` 

### 从pxe启动一个guest

#### 1 使用桥接网络
```
virt-install --pxe --network bridge=breth0 --prompt
```
编辑配置文件的方法
```
<os>
   <type arch='x86_64' machine='rhel6.2.0'>hvm</type>
   <boot dev='network'/>  <!--启动方式-->
   <boot dev='hd'/>
</os>
<interface type='bridge'>       
   <mac address='52:54:00:5a:ad:cb'/>
   <source bridge='breth0'/>     
   <target dev='vnet0'/>
   <alias name='net0'/>
   <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
</interface>
```
#### 2 使用私有libvirt网络

```
virt-install --pxe --network network=default --prompt
```
or
```
<os>
   <type arch='x86_64' machine='rhel6.2.0'>hvm</type>
   <boot dev='network'/>         
   <boot dev='hd'/>
</os>
```

还可以确保虚拟机连接到专用网络

```
<interface type='network'>     
   <mac address='52:54:00:66:79:14'/>
   <source network='default'/>      
   <target dev='vnet0'/>
   <alias name='net0'/>
   <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
</interface>
```

## 使用QEMU agent与SPICE agent

### QEMU agent
QEMU agent运行在客户机, 允许宿主机使用libvirt发送指令来操作客户机的操作系统, 如用来冻结和解冻文件系统, 客户机给予相应的响应.
相关的软件`qemu-guest-agent`

比如在线修改cpu的核数等,在线激活.

### 建立qemu agent 与宿主机的通信

####  使用virsh设置一个shutdown状态下linux  guest os

* 1 Shut down the virtual machine

Ensure the virtual machine (named rhel7 in this example) is shut down before configuring the QEMU guest agent:
`# virsh shutdown rhel7 `

* 2.Add the QEMU guest agent channel to the guest XML configuration

Edit the guest's XML file to add the QEMU guest agent details:
`# virsh edit rhel7`

Add the following to the guest's XML file and save the changes:
```
<channel type='unix'>
   <target type='virtio' name='org.qemu.guest_agent.0'/>
</channel>
```
* 3 Start the virtual machine

`# virsh start rhel7`

* 4 Install the QEMU guest agent on the guest

Install the QEMU guest agent if not yet installed in the guest virtual machine:
`# yum install qemu-guest-agent`

* 5 Start the QEMU guest agent in the guest

Start the QEMU guest agent service in the guest:
`# systemctl start qemu-guest-agent`

#### 在线添加通信(LINUX 客户机)

- 1 Create an XML file for the QEMU guest agent
```
# cat agent.xml
<channel type='unix'>
   <target type='virtio' name='org.qemu.guest_agent.0'/>
</channel>
```

- 2.Attach the QEMU guest agent to the virtual machine

Attach the QEMU guest agent to the running virtual machine (named rhel7 in this example) with this command:
`# virsh attach-device rhel7 agent.xml`

- 3 Install the QEMU guest agent on the guest

Install the QEMU guest agent if not yet installed in the guest virtual machine:
`# yum install qemu-guest-agent`

- 4.Start the QEMU guest agent in the guest

Start the QEMU guest agent service in the guest:
`# systemctl start qemu-guest-agent`

[windows见 kvm文档](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Virtualization_Deployment_and_Administration_Guide/chap-QEMU_Guest_Agent.html)

### 使用 qemu agent
```
virsh shutdown --mode=agent

```
