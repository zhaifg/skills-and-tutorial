# fabric的使用
---

## 介绍
fabric是一个利用ssh的命令集合,用于部署或者系统管理的python应用.

特点:
1. 可以使用任意的python函数来执行bash命令
2. A library of subroutines (built on top of a lower-level library) to make executing shell commands over SSH easy and Pythonic.

fabric的程序一般包括:
> 1. env: 环境变量的定义, 定义服务器的帐号密码,角色,以及变量等
> 2. task: 定义的程序执行的任务列表, 一般是一个python函数
> 3. fab执行: 使用fab命令来执行任务计划.



## 安装
```shell
yum -y install python-devel libxml2-devel libxml++-devel
pip install fabric

```

## fabric简单应用
```python

from fabric.api import run

def host_type():
    run('uname -s')
```

`fab -H localhost, linuxbox, host_type`


`vim fabfile1.py 默认名字`


```python
#!/usr/bin/python
from fabric.api import run

def host_os():
    run('uname -s')


fab -H root@IP host_os  or fab -H user@ip host_os -f f1.py


def hello():
    print("Hello world!")

def hello(name="world"):
    print("Hello %s!" % name)
```

```
$ fab hello:name=Jeff
  Hello Jeff!
 
  Done.
```

## Task的定义
### task中的带参数
```python
def hello(name="world"):
    print('Hello %s' %name)
```
**传入参数的方式**:
`fab hello:name=Jeff -f fab1.py` 

- Local: local表示在本机执行
```python
    from fabric.api import local
    
    def prepare_deploy():
        local("./manage.py test my_app")
        local("git add -p && git commit")
        local("git push")
```
or:
```python
   from fabric.api import local

   def test():
       local("./manage.py test my_app")
   
   def commit():
       local("git add -p && git commit")
   
   def push():
       local("git push")
   
   def prepare_deploy():
       test()
       commit()
       push()
```


## 处理失败的情况
`Faiture`: Failure handling
```python    
from __future__ import with_statement
from fabric.api import local, settings, abort
from fabric.contrib.console import confirm

def test():
    with settings(warn_only=True):
        result = local('./manage.py test my_app', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")    
```

## 配置env, hosts

### `env`： 
`user`: 

`password`: 

`warn_only`: a Boolean setting determining whether Fabric exits when detecting errors on the remote end. See Execution model for more on this behavior.

env下的其他变量：
abort_exception：

`env.hosts = ['host1','host2']`


`Hosts`:
username@hostname:port   以最后一个@分割用户名和IP

`Roles`: 定义角色和指定变量
```python
env.roledefs['webservers'] = ['www1', 'www2', 'www3']

env.roledefs = {
    'web' : ['www1', 'www2', 'www3'],
    'dns' : ['ns1', 'ns2']
}

env.roledefs = {

        'web' : {
        'hosts':['www1', 'www2', 'www3'],
        'foo' : 'bar'
        },
        'dns' : {
        'hosts' : ['ns1', 'ns2'],
        'foo' : 'baz'

        }
    }

env.hosts.extend(['host1', 'host2'])
```

### 代码中设置hosts
```
def set_hosts():
    env.hosts=['host1', 'host2']
```



## 指定某些主机执行
  1. `fab mytask:hosts="host1,host2"`
  2. 构造函数方式：
```
     @hosts('host1', 'host2')
     def mytast():
        pass

     my_hosts = ('host1','host2')
     @hosts(my_hosts)
     def mytask():
         pass
```

### hosts的执行顺序：
1. fab 命令指定的hosts，会重置所有设置
2. 构造指定时(@hosts),会覆盖掉env设置的。
3. 全局指定主机列表（env.hosts = ['host1']），会覆盖掉命令行指定主机。？
4. 全局指定（--hosts=host1）会初始化env变量。


###联合主机列表：
```python
from fabric.api import env, hosts, roles, run

env.roledefs = {'role1': ['b', 'c']}

@hosts('a', 'b')
@roles('role1')
def mytask():
    run('ls /var/www')
```
执行的主机为a,b,c.两个坐并集处理。

### 排除主机：
1. fab  -R myrole -x host2,host5 mytask
2. fab mytask:roles=myrole,exclude_hosts="host2,host5"
      
##Combining exclusions
Host exclusion lists, like host lists themselves, are not merged together across the different “levels” they can be declared in. For example, a global -x option will not affect a per-task host list set with a decorator or keyword argument, nor will per-task exclude_hosts keyword arguments affect a global -H list.

There is one minor exception to this rule, namely that CLI-level keyword arguments (mytask:exclude_hosts=x,y) will be taken into account when examining host lists set via @hosts or @roles. Thus a task function decorated with @hosts('host1', 'host2') executed as fab taskname:exclude_hosts=host2 will only run on host1.

As with the host list merging, this functionality is currently limited (partly to keep the implementation simple) and may be expanded in future releases.
 



##　错误处理：
    

##并发处理
fab -f fabfile.py -H host1,host2 -P -z 5  

@parallel
@parallel(pool_size=3)


##顺序执行
@serial


##fab命令



## 参考
[fabric文档]!(http://docs.fabfile.org/en/1.11/index.html)
[fabric中文文档]!(http://fabric-chs.readthedocs.io/zh_CN/)
