# openstack

主机名          角色              IP     安装软件
mag.htop.me     manager   192.168.8.85   mysql   glance cinder mesq nts keystone image compute manage 
A                         192.168.20.9

kvm1.htop.me              192.168.8.87    nova neutron 
B                         192.168.20.10
                          br0 192.168.40.11

```
yum install ntp
# set ntp
yum install yum-plugin-priorities
vim /etc/resolv.conf 
yum update -y
yum install https://repos.fedorapeople.org/repos/openstack/openstack-mitaka/rdo-release-mitaka-5.noarch.rpm
yum upgrade
yum install openstack-selinux

```
A:
```
yum install mariadb mariadb-server MySQL-python
```

```

[mysqld]

bind-address = 10.0.0.11
default-storage-engine = innodb
innodb_file_per_table
collation-server = utf8_general_ci
init-connect = 'SET NAMES utf8'
character-set-server = utf8
 
```

```
systemctl enable mariadb.service
systemctl start mariadb.service

mysql_secure_installation
```

```
yum install rabbitmq-server
```

```
systemctl enable rabbitmq-server.service
systemctl start rabbitmq-server.service
```

```
Replace RABBIT_PASS with a suitable password.

# rabbitmqctl change_password guest RABBIT_PASS
```

```
 mysql -u root -p


CREATE DATABASE keystone;
Grant proper access to the keystone database:

GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'localhost' \
  IDENTIFIED BY 'KEYSTONE_DBPASS';
GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'%' \
  IDENTIFIED BY 'KEYSTONE_DBPASS';

openssl rand -hex 10
8afd174bfb984ee78217



```


Passwords
Password name   Description
Database password (no variable used)    Root password for the database
ADMIN_PASS  Password of user admin
CEILOMETER_DBPASS   Database password for the Telemetry service
CEILOMETER_PASS Password of Telemetry service user ceilometer
CINDER_DBPASS   Database password for the Block Storage service
CINDER_PASS Password of Block Storage service user cinder
DASH_DBPASS Database password for the dashboard
DEMO_PASS   Password of user demo
GLANCE_DBPASS   Database password for Image service
GLANCE_PASS Password of Image service user glance
HEAT_DBPASS Database password for the Orchestration service
HEAT_DOMAIN_PASS    Password of Orchestration domain
HEAT_PASS   Password of Orchestration service user heat
KEYSTONE_DBPASS Database password of Identity service
NEUTRON_DBPASS  Database password for the Networking service
NEUTRON_PASS    Password of Networking service user neutron
NOVA_DBPASS Database password for Compute service
NOVA_PASS   Password of Compute service user nova
RABBIT_PASS Password of user guest of RabbitMQ
SWIFT_PASS  Password of Object Storage service user swift

```
# controller
10.0.0.11       controller

# compute1
10.0.0.31       compute1

# block1
10.0.0.41       block1

# object1
10.0.0.51       object1

# object2
10.0.0.52       object2
```



keystone-manage bootstrap --bootstrap-password 111111 \
  --bootstrap-admin-url http://mag.htop.me:35357/v3/ \
  --bootstrap-internal-url http://mag.htop.me:35357/v3/ \
  --bootstrap-public-url http://mag.htop.me:5000/v3/ \
  --bootstrap-region-id RegionOne


keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone

```
export OS_TOKEN=8afd174bfb984ee78217
export OS_URL=http://controller:35357/v3
export OS_IDENTITY_API_VERSION=3


export OS_TOKEN="5780572edf661edef9fb"
export OS_URL="http://mag.htop.me:35357/v3"
export OS_IDENTITY_API_VERSION=3



openstack  service create --debug --name keystone --description "OpenStack Identity" identity 

openstack endpoint create --region RegionOne identity public http://mag.htop.me:5000/v3


openstack endpoint create --region RegionOne identity internal http://mag.htop.me:5000/v3
 
openstack endpoint create --region RegionOne identity admin http://mag.htop.me:5000/v3


openstack endpoint create --region RegionOne identity public http://mag.htop.me:5000/v3


openstack endpoint create --region RegionOne identity internal http://mag.htop.me:5000/v3

openstack endpoint create --region RegionOne identity admin http://mag.htop.me:5000/v3


openstack --os-auth-url http://mag.htop.me:35357/v3 \
  --os-project-domain-name default --os-user-domain-name default \
  --os-project-name admin --os-username admin token issue


openstack --os-auth-url http://mag.htop.me:5000/v3 \
  --os-project-domain-name default --os-user-domain-name default \
  --os-project-name demo --os-username demo token issue


  GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'localhost' \
  IDENTIFIED BY '111111';
GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'%' \
  IDENTIFIED BY '111111';
GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'localhost' \
  IDENTIFIED BY '111111';
GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'%' \
  IDENTIFIED BY '111111'; 

```


GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'localhost' \
  IDENTIFIED BY '111111';
GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'%' \
  IDENTIFIED BY '111111';

  GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'localhost' \
  IDENTIFIED BY '111111';
GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'%' \
  IDENTIFIED BY '111111';
GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'localhost' \
  IDENTIFIED BY '111111';
GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'%' \
  IDENTIFIED BY '111111';
  flush privileges;



systemctl stop openstack-nova-api.service \
  openstack-nova-consoleauth.service openstack-nova-scheduler.service \
  openstack-nova-conductor.service openstack-nova-novncproxy.service

  systemctl start openstack-nova-api.service \
  openstack-nova-consoleauth.service openstack-nova-scheduler.service \
  openstack-nova-conductor.service openstack-nova-novncproxy.service


  GRANT ALL PRIVILEGES ON neutron.* TO 'neutron'@'localhost' \
  IDENTIFIED BY '111111';
GRANT ALL PRIVILEGES ON neutron.* TO 'neutron'@'%' \
  IDENTIFIED BY '111111';
    flush privileges;


`错误：创建网络"30"失败: Unable to create the network`
