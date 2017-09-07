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


## 目录服务LDAP
轻型目录存取协定（英文：Lightweight Directory Access Protocol，缩写：LDAP，/ˈɛldæp/）是一个开放的，中立的，工业标准的应用协议，通过IP协议提供访问控制和维护分布式信息的目录信息。

目录服务在开发内部网和与互联网程序共享用户、系统、网络、服务和应用的过程中占据了重要地位。[2]例如，目录服务可能提供了组织有序的记录集合，通常有层级结构，例如公司电子邮件目录。同理，也可以提供包含了地址和电话号码的电话簿。

LDAP由互联网工程任务组（IETF）的文档RFC定义，使用了描述语言ASN.1定义。最新的版本是版本3，由RFC 4511所定义。例如，一个用语言描述的LDAP的搜索如：“在公司邮件目录中搜索公司位于那什维尔名字中含有“Jessy”的有邮件地址的所有人。请返回他们的全名，电子邮件，头衔和简述。”[3]

LDAP的一个常用用途是单点登录，用户可以在多个服务中使用同一个密码，通常用于公司内部网站的登录中（这样他们可以在公司电脑上登录一次，便可以自动在公司内部网上登录）。[3]
LDAP基于X.500标准的子集。因为这个关系，LDAP有时被称为X.500-lite。



### LDAP的特点

* LDAP的结构用树来表示，而不是用表格。正因为这样，就不能用SQL语句了
* LDAP可以很快地得到查询结果，不过在写方面，就慢得多
* LDAP提供了静态数据的快速查询方式
* Client/server模型，Server 用于存储数据，Client提供操作目录信息树的工具
* 这些工具可以将数据库的内容以文本格式（LDAP 数据交换格式，LDIF）呈现在您的面前
* LDAP是一种开放Internet标准，LDAP协议是跨平台的Interent协议

## LDAP 协议

LDAP目录的条目(entry)由属性(attribute)的一个聚集组成, 并由一个唯一性的名字引用, 即专有名称(distinguished name,DN). 例如, DN能取这样的值:`ou=groups, ou=people, dc=wikipedia, dc=org`.

        dc =wikipedia,dc=org
            |
       /        \
  ou=people     ou=groups

ldap目录和普通数据库的主要不同之处在于数据的组织方式, 它是一种有层次的, 树形结构. 所有条目的属性的定义是对象类object class的组成不服, 并组成在一起构成schema; 那么些在组织内代表个人的schema并命名为white pages schema. 数据库内的每个条目都与若干对象类联系, 而这些对象类决定了一个属性是否为可选和它保存哪些类型的信息, 属性的名字一般是易于记忆的字符串, 例如用cn为通用名(common name)命名, 而"mail"代表e-mail地址. 属性取值依赖于其类型, 并且LDAPv3中一般非二进制都遵从UTF-8字符串语法. 例如, mail属性包含值"user@exmaple.com"; jpegPhotos属性一般包含JPEG/JFIF格式的图片.

### 基本概念

### Entry
条目, 也叫记录项, 是LDAP中的基本组成单元, 像字典里中的词条, 或者数据库中的记录. 通常对LDAP的添加, 删除, 更改,检索都是以条目为基本对象.

`Base DN`：LDAP目录树的最顶部就是根，也就是所谓的“Base DN"，如"dc=mydomain,dc=org"。

`dn`: distringuished 唯一辨别名 uid=zhaig, ou=market,dc=example, dc=com
`rdn`: relative dn 相对辨别名



### Attribue

每个条目都是有很多属性(Attribute), 比如常见的人都有姓名, 地址, 电话等属性. 每个属性都有名称以及对应的值, 属性值可以有单个, 多个, 比如有多个邮箱.

属性不是随便定义的, 需要符合一定的规则, 而这个规则可以通过schema指定, 比如, 如果entry没有包含在 inetorgperson 这个schema中的`objectClass: inetOrgPerson`, 那么就不能为它指定employeeNumber属性, 因为emplyeeNumber是在 `inetorgperson`中定义的.

`dc`: domain componet 域名部分, example.com dc=example,dc=com
`uid`: user id 用户id 如zhaifg
`ou`: oganization unit 组织单位, 如 teach
`cn`: common name 公共名称,
`sn`:surname 姓
`c`: country 
`o`: organization

### ObjectClass
对象类是属性的集合, LDAP预想了很多人员组织机构中常见的对象, 并将其封装成对象类. 比如人员(Person)含有姓(sn),名(cn),电话(telephoneNumber)、密码(userPassword)等属性，单位职工(organizationalPerson)是人员(person)的继承类，除了上述属性之外还含有职务（title）、邮政编码（postalCode）、通信地址(postalAddress)等属性。

通过对象类可以方便的定义条目类型。每个条目可以直接继承多个对象类，这样就继承了各种属性。如果2个对象类中有相同的属性，则条目继承后只会保留1个属性。对象类同时也规定了哪些属性是基本信息，必须含有(Must 活Required，必要属性)：哪些属性是扩展信息，可以含有（May或Optional，可选属性）。

对象类有三种类型：结构类型（Structural）、抽象类型(Abstract)和辅助类型（Auxiliary）。结构类型是最基本的类型，它规定了对象实体的基本属性，每个条目属于且仅属于一个结构型对象类。抽象类型可以是结构类型或其他抽象类型父类，它将对象属性中共性的部分组织在一起，称为其他类的模板，条目不能直接集成抽象型对象类。辅助类型规定了对象实体的扩展属性。每个条目至少有一个结构性对象类。

对象类本身是可以相互继承的，所以对象类的根类是top抽象型对象类。以常用的人员类型为例，他们的继承关系：

!(../images/openldap_objectclass.jpg)

下面是inetOrgPerson对象类的在schema中的定义，可以清楚的看到它的父类SUB和可选属性MAY、必要属性MUST(继承自organizationalPerson)，关于各属性的语法则在schema中的attributetype定义

```
# inetOrgPerson
# The inetOrgPerson represents people who are associated with an
# organization in some way.  It is a structural class and is derived
# from the organizationalPerson which is defined in X.521 [X521].
objectclass     ( 2.16.840.1.113730.3.2.2
    NAME 'inetOrgPerson'
        DESC 'RFC2798: Internet Organizational Person'
    SUP organizationalPerson
    STRUCTURAL
        MAY (
                audio $ businessCategory $ carLicense $ departmentNumber $
                displayName $ employeeNumber $ employeeType $ givenName $
                homePhone $ homePostalAddress $ initials $ jpegPhoto $
                labeledURI $ mail $ manager $ mobile $ o $ pager $
                photo $ roomNumber $ secretary $ uid $ userCertificate $
                x500uniqueIdentifier $ preferredLanguage $
                userSMIMECertificate $ userPKCS12 )
        )
```

### Schema
d对象类(ObjectClass), 属性类型(Attribute Type), 语法(Syntax)分别约定了条目, 属性, 值, 他们之间的关系如下图所示. 所以这些构成了模式(Schema)---对象类的集合. 条目数据在导入时通常需要接受模式检查, 它确保了目录中所有的条目数据结构都是一致的.

!(../images/openladap_schema.jpg)[等等]

### backend & database

ldap的后台进程slapd接收、响应请求，但实际存储数据、获取数据的操作是由Backends做的，而数据是存放在database中，所以你可以看到往往你可以看到backend和database指令是一样的值如 bdb 。一个 backend 可以有多个 database instance，但每个 database 的 suffix 和 rootdn 不一样。openldap 2.4版本的模块是动态加载的，所以在使用backend时需要moduleload back_bdb指令。

bdb是一个高性能的支持事务和故障恢复的数据库后端，可以满足绝大部分需求。许多旧文档里（包括官方）说建议将bdb作为首选后端服务（primary backend），但2.4版文档明确说hdb才是被首先推荐使用的，这从 2.4.40 版默认安装后的配置文件里也可以看出。hdb是基于bdb的，但是它通过扩展的索引和缓存技术可以加快数据访问，修改entries会更有效率，有兴趣可以访问上的链接或slapd.backends。

### TLS & SASL
分布式LDAP 是以明文的格式通过网络来发送信息的，包括client访问ldap的密码（当然一般密码已然是二进制的），SSL/TLS 的加密协议就是来保证数据传送的保密性和完整性。

SASL （Simple Authenticaion and Security Layer）简单身份验证安全框架，它能够实现openldap客户端到服务端的用户验证，也是ldapsearch、ldapmodify这些标准客户端工具默认尝试与LDAP服务端认证用户的方式（前提是已经安装好 Cyrus SASL）。SASL有几大工业实现标准：Kerveros V5、DIGEST-MD5、EXTERNAL、PLAIN、LOGIN。

Kerveros V5是里面最复杂的一种，使用GSSAPI机制，必须配置完整的Kerberos V5安全系统，密码不再存放在目录服务器中，每一个dn与Kerberos数据库的主体对应。DIGEST-MD5稍微简单一点，密码通过saslpasswd2生成放在sasldb数据库中，或者将明文hash存到LDAP dn的userPassword中，每一个authid映射成目录服务器的dn，常和SSL配合使用。参考将 LDAP 客户端配置为使用安全性

EXTERNAL一般用于初始化添加schema时使用，如ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/core.ldif。

### LDIF

LDIF（LDAP Data Interchange Format，数据交换格式）是LDAP数据库信息的一种文本格式，用于数据的导入导出，每行都是“属性: 值”对，见 openldap ldif格式示例

#### LDIF 编写时注意的事项

* LDIF 文件每行的结尾不允许有空格或者制表符
* LDIF 文件允许相关属性可以重复赋值并使用
* LDIF 文件以.ldif为结尾命名
* LDIF 文件中以# 为开头的一行为注释, 可以作为解释使用
* LDIF 文件所有的赋值方式为: 属性:[空格]属性值
* LDIF 文件通过空行定义一个条目, 空格前为一个条目, 空格后卫另一个条目点开始.

#### LDIF格式语法

```
# 注释, 用于对条目进行解释

dn: 条目名称
objectClass (对象类): 属性值
objectClass (对象类): 属性值
...
```
如
```
dn: uid=zhaifg,ou=people,dc=example,dc=com
objectClass: top
objectClass: posixAccount
objectClass: shadowAccount
objectClass: person
objectClass: inetOrgPerson
objectClass: hostObject
sn: zhai
cn: zhaifg
telephoneNumber: 1xxxxxxxxx
mail: zhaifengguo@gmail.com
```

## Server端安装CentOS 6

### YUM方式

* 1.配置epel源, 以及设置时间同步
```

yum install openldap openldap-servers openldap-clients openldap-devel compat-openldap 
```
* 2.初始化OpenLDAP配置
```
cp /usr/share/openldap-servers/DB_CONFIG.example /var/lib/ldap/DB_CONFIG
cp /usr/share/openldap-servers/slapd.conf.obsolete /etc/openldap/slapd.conf
chown -R ldap.ldap  /var/lib/ldap/DB_CONFIG /etc/openldap
```

* 3.启动LDAP的主进程slapd
```
unimedsci.com
service slapd restart
```

* 4.获取OpenLDAP的默认的监控端口
```
netstat -antpl|grep -i: 389
```


### 配置文件信息
* `/etc/openldap/slapd.conf`: 主配置文件, 记录根域名称, 管理员名称, 密码,日志, 权限等相关信息
* `/var/lib/ldap/*`: 数据文件的存放的位置
* `/etc/openldap/slapd.d/*`: 
* `/usr/share/openldap-servers/DB_CONFIG.example`: 模板配置文件
* `/usr/share/openldap-servers/slapd.conf.obsolete`: 模板数据库配置文件
* `/etc/openldap/schema/*`: OpenLDAP schema 规范存放位置
* 默认的监控端口 389, 明文
* 加密监听端口: 636

#### slapd.conf的文件
配置文件的里以#开头的为注释说明

- 1.引入schema文件
```
include  /etc/openldap/schema/corba.schema
include         /etc/openldap/schema/core.schema
include         /etc/openldap/schema/cosine.schema
include         /etc/openldap/schema/duaconf.schema
include         /etc/openldap/schema/dyngroup.schema
include         /etc/openldap/schema/inetorgperson.schema
include         /etc/openldap/schema/java.schema
include         /etc/openldap/schema/misc.schema
include         /etc/openldap/schema/nis.schema
include         /etc/openldap/schema/openldap.schema
include         /etc/openldap/schema/ppolicy.schema
include         /etc/openldap/schema/collective.schema
include         /etc/openldap/schema/samba.schema
```

`allow bind_v2`: 允许2.0版本的连接
`pidfile /var/run/openldap/slapd.pid`: pid文件
`argsfile /var/run/openldap/slapd.args`: OpenLDAP参数存放的路径
`modulepath /usr/lib(64)/openldap`  模块的存放路径

```
TLSCACertificatePath /etc/openldap/certs
TLSCertificateFile "\"OpenLDAP Server\""
TLSCertificateKeyFile /etc/openldap/certs/password
```
证书传输时的证书的保存路径

`database bdb`: OpenLDAP数据库类型
`suffix "dc=htop,dc=me"`: 指定服务域名DN
`rootdn "cn=admin,dc=htop,dc=me"`: 管理员指定
`root 123456`: 明文指定管理员密码
`rootpw {SSHA}4Z3xsU4KL/fo364XLxyjOlAPGl1jCyhf`: 加密指定管理员密码

* 通过cn=config来实现管理员的修改以及密码的修改
```
cat << EOF | ldapadd -Y EXTERNAL -H ldapi:///
dn: olcDatabase={0}config,cn=config
changetype: modify
delete: olcRootDN

dn: olcDatabase={0}config,cn=config
changetype: modify
add: olcRootDN
olcRootDN: cn=zhaifg,cn=config

dn: olcDatabase={0}config,cn=config
changetype: modify
add: olcRootPW
olcRootPW: {SSHA}4Z3xsU4KL/fo364XLxyjOlAPGl1jCyhf
EOF

```
此时把管理员由admin改为了zhaifg, 

`directory /var/lib/ldap` 数据库文件存放目录

```
index objectClass                       eq,pres
index ou,cn,mail,surname,givenname      eq,pres,sub
index uidNumber,gidNumber,loginShell    eq,pres
index uid,memberUid                     eq,pres,sub
index nisMapName,nisMapEntry            eq,pres,sub
```
OpenLDAP索引

#### 生成同步数据

* 语法验证
```
slapdtest -f /etc/openldap/slapd.conf 
```

* 删除 slapd.d/下的所有文件, 使用slapdtest同步数据
```
rm -fr /etc/openldap/slpad.d/*
slaptest -f /etc/openldap/slapd.conf -F /etc/openldap/slapd.d
chown -R ldap.ldap /etc/openldap/slapd.d
/etc/init.d/slapd restart
```

#### OpenLDAP日志日志

* 获取日志级别
`slapd -d ?`

* 配置rsyslog,
`vim /etc/rsyslog.conf`
添加
```
local4.*                                                /var/log/slapd.log
```
重启
`/etc/init.d/rsyslog restart`


* 设置slapd.conf  的日志
```
loglevel 256
cachesize 1000
checkpoint 2048 10
```

* 重新生成slpad.d
```
rm -fr /etc/openldap/slpad.d/*
slaptest -f /etc/openldap/slapd.conf -F /etc/openldap/slapd.d
chown -R ldap.ldap /etc/openldap/slapd.d
/etc/init.d/slapd restart
```

#### 防火墙和selinux的配置
pass

### OpenLDAP目录规划

- 1)将规划的DN天剑的OpenLDAP目录树中, 建立base.ldif
```
dn: dc=htop,dc=me
dc: htop
objectClass: top
objectClass: domain

dn: ou=people,dc=htop,dc=me
ou: people
objectClass: top
objectClass: organizationalUnit

dn: ou=group, dc=htop,dc=me
ou: group
objectClass: top
objectClass: organizationalUnit
```

- 2)使用lapdadd导入
```
lapdadd -x -w 123456 -D cn=admin,dc=htop,dc=me -f base.ldif
```

- 3)使用ldapsearch查看当前目录数结构
```
ldapsearch -x -LLL
```

- 4) 故障分析: 当ldapsearch -x -LLL, 如出现如下
```
No such object(32)
```
配置:
```
cat >>/etc/openldap/ldap.conf<<EOF
BASE dc=htop,dc=me
URI ldap://IP
EOF
```

### OpenLDAP用户以及与用户组相关的配置
添加用户和用户组有两种方式:
1. 将系统用户通过migrationtools工具生成LDIF文件并结合ldapadd命令导入OpenLDAP目录树中,生成OpenLDAP用户.
2. 通过自定义LDIF文件并通过OpenLDAP命令进行添加或者修改操作.

#### 通过migrationtools实现OpenLDAP用户以及用户组的添加
migrationtools开源工具通过查找/etc/passwd, /etc/shadow, /etc/groups生成LDIF, 并通过ldapadd命令更新数据库数据, 完成用户添加.

* 1) 安装migrationtools工具
`yum install migrationtools -y`

* 2) 创建OpenLDAP 根域条目
`/usr/share/migrationtools/migrate_base.pl > base.ldif`
可以修改base.ldif里的内容, 去掉不需要的条目, 然后使用ldapadd导入

* 3) 添加用户用户生成OpenLDAP用户
  * 比如先添加系统用户user01-user05
  * useradd user01  passwd user01

* 4) 配置migrationtools配置文件`/usr/share/migrationtools/migrate_common.ph`
```
# Default DNS domain
$DEFAULT_MAIL_DOMAIN = "htop.me";

# Default base 
$DEFAULT_BASE = "dc=htop,dc=me";

```

* 5) 通过migrationtools 工具生成LDIF模板文件并生成用户以及组LDIF文件
```
grep "user" /etc/passwd > system
/usr/share/migrationtools/migrate_passwd.pl system people.ldif

grep "某些组" /etc/group > group
/usr/share/migrationtools/migrate_group.pl group group.ldif
```

* 6) 查看生成的数据
```
例如使用zhaifg单个用户
# people.ldif
dn: uid=zhaifg,ou=People,dc=htop,dc=me
uid: zhaifg
cn: zhaifg
objectClass: account
objectClass: posixAccount
objectClass: top
objectClass: shadowAccount
userPassword: {crypt}$6$CqHKtpgX$rqaqDawaPrrEJ.2HcFwHiOGgD0zEQpY5hh8fEnxRlT1F8Sr2PG/pZJOi.u9NezTt2T13bkZ/mKC7Zosr8FYBi1
shadowLastChange: 17065
shadowMin: 0
shadowMax: 99999
shadowWarning: 7
loginShell: /bin/bash
uidNumber: 501
gidNumber: 502
homeDirectory: /home/zhaifg


# group
dn: cn=zhaifg,ou=Group,dc=htop,dc=me
objectClass: posixGroup
objectClass: top
cn: zhaifg
userPassword: {crypt}x
gidNumber: 502
```

* 7) 利用ldapadd导入模板文件中的内容
`ldapadd -x -W -D "cn=admin,dc=htop,dc=me" -f people.ldif`
`ldapadd -x -W -D "cn=admin,dc=htop,dc=me" -f group.ldif`


* 8) 查看导入信息
```
ldapsearch -x -LLL


ldapsearch -LLL -D "cn=admin,dc=htop,dc=me" -W -b 'dc=htop,dc=me' 'uid=zhaifg'
```

#### 自定义LDIF文件添加用户以及用户组条目

* 1) 定义LDIF用户文件
如zhaifg.ldif
```
dn: uid=zhaifg,ou=People,dc=htop,dc=me
objectClass: person
objectClass: posixAccount
objectClass: top
objectClass: shadowAccount
cn: zhaifg
sn: zhai
giveName: 凤国
displayNmae: 翟凤国
uid: zhaifg
userPassword: {crypt}$6$CqHKtpgX$rqaqDawaPrrEJ.2HcFwHiOGgD0zEQpY5hh8fEnxRlT1F8Sr2PG/pZJOi.u9NezTt2T13bkZ/mKC7Zosr8FYBi1
gecos: System Mananger
shadowLastChange: 17065
shadowMin: 0
shadowMax: 99999
shadowWarning: 7
shadowExpire: -1
loginShell: /bin/bash
uidNumber: 501
gidNumber: 502
homeDirectory: /home/zhaifg
employeeNumber: xxxxx
homePhone: 000000
mobile: xxxxx
mail: zhaifengguo@gmail.com
postalAddress: shanghai
initials: 上海
```

### 索引

* 1) 通过ldapsearch 命令查看当前olcDatabase={2}bdb 有哪些索引
```
[root@yimiwork_212 openldap]# ldapsearch -Q -LLL -Y EXTERNAL -H ldapi:/// -b cn=config '(olcDatabase={2}bdb)' olcDbIndex

dn: olcDatabase={2}bdb,cn=config
olcDbIndex: objectClass pres,eq
olcDbIndex: cn pres,eq,sub
olcDbIndex: uid pres,eq,sub
olcDbIndex: uidNumber pres,eq
olcDbIndex: gidNumber pres,eq
olcDbIndex: sn pres,eq,sub
olcDbIndex: mail pres,eq,sub
olcDbIndex: ou pres,eq,sub
olcDbIndex: memberUid pres,eq,sub
olcDbIndex: givenName pres,eq,sub
olcDbIndex: loginShell pres,eq
olcDbIndex: nisMapName pres,eq,sub
olcDbIndex: nisMapEntry pres,eq,sub
```
上述结果显示当前数据库文件没有关于"sn pres, eq,sub"的索引信息

* 2) 创建一个ldif文件, 用于存放索引命令
```
vim hdb-index.ldif

dn: olcDatabase={2}bdb,cn=config
changetype: modify
add: olcDbIndex
olcDbIndex: sn pres, eq, sub
```

* 3) 通过ldapmodify 命令创建olcDatabase={2}hdb数据库相关索引条目
```
ldapmodify -Q -LLL -Y EXTERNAL -H ldapi:/// -f hdb-index.ldif
```

* 4) 通过ldapsearch 进行验证, 是否"sn pres, eq sub" 添加成功.
```
ldapsearch -Q -LLL -Y EXTERNAL -H ldapi:/// -b cn=config '(olcDatabase={2}bdb)' olcDbIndex | grep -i "sn"
```

### 通过slpad.conf定义用户策略控制

默认的情况下, 不允许普通用户更改自身密码, 只允许管理员更改.

* 1) 定义访问控制策略, 允许修改自身密码
```
access  to attrs=shadowLastChange, userPassword
  by self write # 只允许自身修改
  by * auth
access to * 
  by * read # 允许授权用户查看信息
```

* 2) 重新加载slapd.conf文件
```
rm -fr /etc/openldap/slpad.d/*
slaptest -f /etc/openldap/slapd.conf -F /etc/openldap/slapd.d
chown -R ldap.ldap /etc/openldap/slapd.d
/etc/init.d/slapd restart
```


## 与Linux客户端集成

### Linux账号登录的系统流程

* 客户端输入账号密码提交后
* 系统根据/etc/nsswitch.conf文件获取账号的查找顺序,然后再根据PAM配置文件调用相关模块, 对账号(/etc/passwd)以及密码(/etc/shadow)进行查找并进行匹配.
* 当本地匹配不成功时, 会通过后端认证服务器进行验证,如openldap
* 匹配成功后则进行授权用户登录并根据相关权限获取不同用户特权

### RHEL系统登录的验证配置文件如下

5.x:
/etc/ldap.conf /etc/nsswitch.conf /etc/pam.d/system-auth

6.x:
/etc/openldap.conf/etc/autoconfig/ldap  /etc/pam_ldap.conf  /etc/nslcd.conf /etc/sudo-ldap.conf

7.x
/etc/openldap.conf/etc/autoconfig/ldap  /etc/pam_ldap.conf  /etc/nslcd.conf /etc/sudo-ldap.conf

`/etc/nsswitch.conf`: glibc包里的 主要用于名称转换服务

`/etc/sysconfig/autoconfig`: 该文件由autoconfig 软件包提供, 主要用于身份验证之LDAP功能

`/etc/pam.d/system-auth`: pam软件包生成. 主要用于实现用户账号身份验证

`/etc/pam_ldap.conf`: nss-pam-ldapd 软件包生成, 实现客户端与服务端的交互.

`/etc/openldap/ldap.conf`: openldap主要用于查询OpenLDAP服务器所有条目
 

### 配置方式

* 图形: setup
* 配置文件
* authconfig

rhel 6.x为例

* 1) 配置时间同步
* 2) 域名解析
* 3) 安装OpenLDAP客户端软件
```
yum install openldap-clients nss-pam-ldapd 
```
* 4) 修改配置文件实现客户端的部署
setup方式

* 5) 修改nslc.conf
cp /etc/nslcd.conf /etc/nslcd.conf.bak
vi
```
uri ldap://xxxxx
base dc=htop,dc=me
ssl no
tls_cacertdir /etc/openldap/cacerts
```
* 6)修改pam_ldap.conf
cp
```
base dc=htop,dc=me

uri ldap://xxxxx
ssl no
tls_cacertdir /etc/openldap/cacerts
bind_policy soft
```

* 7) 修改system-auth认证文件

添加
```
auth        sufficient    pam_ldap.so use_first_pass
account     [default=bad success=ok user_unknown=ignore] pam_ldap.so
password    sufficient    pam_ldap.so use_authtok
session     optional      pam_ldap.so
# session     optional      pam_mkhomedir.so                                   
```

* 8) 修改nsswitch.conf
```
passwd:     files ldap
shadow:     files ldap
group:      files ldap
```

* 9) 修改authconfig 认证文件
```
USESHADOW=yes
USELDAPAUTH=yes
USELOCAUTHORIZE=yes
USELDAP=yes
```

* 10) 重新启动nslcd进程
```
/etc/init.d/nslcd restart
```

* 11) 客户端验证
```
getent passwd zhaifg
```

* 12) 登录验证
提示时
```
Last login: Thu Apr 20 17:34:19 2017 from 192.168.8.103
Could not chdir to home directory /home/zhaifg: No such file or directory
-bash-4.1$ 

```
解决方式: you 

1. autofs + NFS
2. 在/etc/pam.d/system-auth添加pam模块
```
cat >>/etc/pam.d/system-auth<<EOF
session optional pam_mkhomedir.so skel=/etc/skel umask=0022
EOF
```
3. `authconfig --enablemkhomedir --update`


#### authconfig 命令介绍

`authconfig -h`

* authconfig备份恢复案例
  1. 使用authconfig命令备份系统文件
    * authconfig -savebackup=systemconfig.bak
  2. 使用authconfig指令恢复初始配置参数
    * authconfig --restorebackup=systemconfig.bak  # 指定恢复文件
    * authconfig --restorelastbackup  # 恢复在上次配置更改前配置文件的备份

* 使用authocnifg 把当前系统加入openldap
```
authconfig --enablemkhomedir --disableldaptls -enableldap  --enableldapauth --ldapserver=ldap://ip  --ldapbasedn="dc=htop,dc=me"  --enableshadow --update
```

参考[https://segmentfault.com/a/1190000002607140](等等)


