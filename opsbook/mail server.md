# mail server
---

## 邮件服务器的组成：
1. MUA:(Mail User Agent) 提供用户写信,读信,寄信的软件.寄信时以SMTP协议讲邮件提交给MTA;收信时,以POP或IMAP协议访问服务器上的邮箱.
2. MTA(MailTransfer Agent): 负责接收,递送邮件的服务器软件.决定邮件的递送路径,进行必要的地址改写.应该有本地系统收下的邮件,委托给MDA进行最后的投递操作.
3. MDA(Mail Delivery Agent): 负责投递本地邮件到适当邮箱.MDA可以过滤邮件内容,或是依照用户设定的准则,将邮件分类到适当的邮箱;设置可以将邮件转回给MTA,以寄到另一个邮箱.



## 邮件服务的收发原理


## postfix的安全性
1. 模块化设计
2. shell与进程
3. chroot


## Email概念
RPC (Request for Comments docment) 821, 822.

邮件管理员 postmaster: 保护邮件系统正确运作,适应环境的改变,增加,移除邮箱,过滤垃圾邮件等责任.

'拒收'与'退信':

`信封地址`与`邮件标题`: 
`邮件列表`: Mailing list
`垃圾邮件`:
`别名`:

## SMTP协议:
SMTP指令:
`HELO`,`MAIL FROM`,`RCPT TO`,`DATA`,`QUIT`

## ESMTP协议：
增强版的协议，
STMP指令前加`E`, 如`EHELO`

##Postfix的结构
启动时,首先启动的是 `master daemon`,主导邮件的处理流程,同时也是其他组件的总管.在处理邮件的过程中,master会启动对应功能处理相关事宜,被master启动的组件,在完成交付的工作之余会自行结束;或者,如果组建的处理时间超过时限,或者工作量达到了预定限度,组建也会自行结束;master daemon会常驻在系统中,当管理员启动它时,它从`main.cf`和`master.cf`这两个配置文件取得启动参数.

### 邮件处理流程:
接收邮件-->将邮件排入队列-->递送邮件


各个postfix组件之间的合作全靠队列(queue)交换邮件.

Queue Mananger

## 虚拟别名邮件
寄给虚拟别名地址的邮件,全部都需要转寄到其真实的地址.  虚拟别名的网域名称列
在`virtual_alias_domains`参数中

## LMTP 投递

## Pipe 投递
pipe daemon将邮件传给外部程序.内容过滤,病毒扫描,垃圾邮件分析或者其他通信媒介(传真机).


##　基本配置

`/etc/postfix/`: 配置文件与查询表
`/usr/libexec/postfix`　：　各个服务器程序
`/var/spool/postfix/`：　队列文件
`/usr/sbin`: postfix的工具程序.

- postfix需要完整的hostname, 解析等. postconf -e hostname
- 别名数据库: newaliases

日志:
/var/log/maillog

### 配置文件
`master.cf`
`main.cf`

重载配置文件 `postfix reload`
