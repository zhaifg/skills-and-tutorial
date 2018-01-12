# zabbix的自动注册
---

## zabbix 的自动发现,自动注册等功能
网络发现, 前提是所有服务器都已经安装了agent 或者 snmp, server 扫描配置好的ip段, 自动添加 host, 自动给 host link 模板, 自动添加主机组立等.

### zabbix 网络发现机遇如下信息
* ip 范围
* 可用外部服务(FTP, SSH, WEB, POP3, IMAP, TCP, etc)
* 来自 zabbix agent 的信息
* 来自 snmp agent 信息

网络发现由两个阶段组成:  discovery 和 actions

### Discovery 发现
zabbix 定期扫描网络发现规则中的IP 范围, 么个规则中都定义了一组需要检测的服务, 在这些 IP 范围内 一一扫描网络发现木块每次检测到 service 和 host (ip) 都会生成 一个 discovery 事件, 如下事件:

时间:  条件
`Service Up`: zabbix 检测到可用的service
`Service Down`: zabbix 无法检测到 service
`Host Up`: 某个IP 上至少有一个 service 是 up 状态
`Host Down`: 所有service 都无响应
`Service Discovered`: 一个service 首次被发现或者在维护
`Service Lost`: service 在 UP 之后又丢失了
`Host Discovered`: 一个host 首次倍发现或者在维护后重新归队
`Host Lost`: 一个 host 在 up 之后又丢失了


### Actions 动作
zabbix 所有 action 都是基于发现事件, 如:
* 发送 通知
* 添加/移除主机
* 启用/禁用主机
* 添加到主机组
* 从组中移除主机
* 主机link模板/unlink模板
* 执行远程命令

