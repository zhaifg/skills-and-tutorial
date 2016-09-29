# openldap
---
http://opjasee.com/2014/03/28/openldap-use-sudo.html
https://wiki.archlinux.org/index.php/OpenLDAP_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)
https://www.ibm.com/developerworks/cn/linux/1312_zhangchao_opensslldap/
http://www.ibm.com/developerworks/cn/linux/l-openldap/
http://wangzan18.blog.51cto.com/8021085/1843801
http://wangzan18.blog.51cto.com/8021085/1834219
https://linux.cn/article-6934-1.html  book

http://seanlook.com/2015/01/21/openldap-install-guide-ssl/
https://www.ibm.com/developerworks/cn/linux/l-openldap/
http://crashedbboy.blogspot.com/2015/08/centos-7-open-ldap.html
http://www.jslink.org/linux/openldap-ssl-sssd.html
globally-unique Distinguished Name (DN) :  uid=babs,ou=People,dc=example,dc=com

slapd-->server


②安装openssl openssl-devel以及cyrus-sasl
1
yum install openssl openssl-devel gnutls cyrus-sasl
③安装Heimdal
1
2
3
4
5
yum install libedit-devel
tar -zxvf heimdal-1.5.3.tar.gz
cd heimdal-1.5.3
./configure --without-ipv6 --with-openldap
make && make install
④安装Berkeley DB
1
2
3
4
tar -zxvf db-6.0.20.tar.gz
cd db-6.0.20/build_unix/
../dist/configure --prefix=/usr/local/BerkeleyDB
make && make install
⑤安装OpenLDAP
1
2
3
4
5
6
7
8
9
10
11
12
gunzip -c openldap-2.4.36.tgz | tar xf -
cd openldap-2.4.36
vim /etc/ld.so.conf
/usr/local/BerkeleyDB/lib
ldconfig
./configure --prefix=/usr/local/openldap --with-tls=openssl --enable-bdb \
CPPFLAGS="-I/usr/local/BerkeleyDB/include" \
LDFLAGS="-L/usr/local/BerkeleyDB/lib"
make depend
make
make test
make install
6、启动前配置
①修改主配置文件
载入需要使用的schema
1
2
3
4
5
6
7
8
9
10
11
12
13
14
vim /usr/local/openldap/etc/openldap/slapd.conf
include         /usr/local/openldap/etc/openldap/schema/core.schema
include         /usr/local/openldap/etc/openldap/schema/collective.schema
include         /usr/local/openldap/etc/openldap/schema/corba.schema
include         /usr/local/openldap/etc/openldap/schema/cosine.schema
include         /usr/local/openldap/etc/openldap/schema/duaconf.schema
include         /usr/local/openldap/etc/openldap/schema/dyngroup.schema
include         /usr/local/openldap/etc/openldap/schema/inetorgperson.schema
include         /usr/local/openldap/etc/openldap/schema/java.schema
include         /usr/local/openldap/etc/openldap/schema/misc.schema
include         /usr/local/openldap/etc/openldap/schema/nis.schema
include         /usr/local/openldap/etc/openldap/schema/openldap.schema
include         /usr/local/openldap/etc/openldap/schema/pmi.schema
include         /usr/local/openldap/etc/openldap/schema/ppolicy.schema
更改默认根域名
1
2
3
4
5
6
7
vim /usr/local/openldap/etc/openldap/slapd.conf
suffix          "dc=my-domain,dc=com"
rootdn         "cn=Manager,dc=my-domain,dc=com"
rootpw          secret
注：rootpw可以是MD5值也可以是明文
生成加密密码：
/usr/local/openldap/sbin/slappasswd

②创建根dc
1
2
3
4
5
6
7
8
vim root.ldif
dn: dc=flame100,dc=cn
objectclass: top
objectClass: dcObject
objectClass: organizationalUnit
dc: flame100
ou: flame100.com
ldapadd -x -D "cn=Manager,dc=flame100,dc=cn" -W -f root.ldif
③启动测试
为了方便使用命令，加入相关路径到环境变量里

1
2
3
vim ~/.bash_profile
PATH=$PATH:$HOME/bin:/usr/local/openldap/bin
source~/.bash_profile
启动之前需要复制一下数据存储的配置文件
1
cp /usr/local/openldap/var/openldap-data/DB_CONFIG.example /usr/local/openldap/var/openldap-data/DB_CONFIG
调试模式启动服务观察是否有报错
1
/usr/local/openldap/libexec/slapd -d 1
