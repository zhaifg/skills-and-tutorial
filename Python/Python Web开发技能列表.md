#Python Web开发技能列表清单 以及教程总结
---
## 如果要作为Python Web工程师需要具备的技能:
1. 至少熟悉一种Python Web框架
2. 熟悉Python语法
3. 熟悉数据库,缓存,消息队列等技术的使用场景,使用方法.
4. 日常能够使用Linux或者mac系统工作
5. 对性能调优经验, 能快速定位问题.
6. 对HTML/CSS/Javascript有一定的了解,  有使用经验.


## Python的开发环境
1. Vagrant

2. Docker

## Python 的包管理和虚拟环境
### 使用pip 代替easy_install
pip 的更改代码源 

### virtualenv
```
pip install virtualenv # sudo apt-get install virtualenv

# 创建一个env环境
virtualenv env
source env/bin/activate
deactivate
```

#### virtualenv定制化
实例定制化virutal环境, 同时安装flake8的自定义脚本
`create_env_scritp.py`

```
import subprocess
import virtualenv

virtualenv_path = subprocess.check_out(['which', 'virtualenv']).strip()

EXTRA_TEXT = """
def after_install(options, home_dir):
    subprocess.call(['{}/bin/pip'.format(home_dir), 'install', 'flake8'])
"""
def main():
    text = virtualenv.create_bootstrap_script(EXTRA_TEXT, python_version='2.7)
    print 'Updating %s' % virtualenv_path
    with open(virtualenv_path) as f:
        f.write(text)
if __name__ == "__main__":
    main()
```
增加新功能
#### virtualenvwrapper  重点
用来管理全部的虚拟环境, 能够方便的创建, 删除和copy虚拟环境, 使用单个名利就可以切换不同的虚拟环境. 可以使用tab进行不全虚拟环境, 支持用户粒度的钩子支持.
```
pip install virtualenvwrapper
export WORKON_HOME=~/venv
export /usr/local/bin/virtualenvwrapper.sh
```

### autoenv




### 包管理
1. distribute
2. disutils
3. setuptools: 用来解决disutils的限制的替代品. 好处:
  1. 可以创建Eggs和WHeel格式的包
  2. 自带easy_install, 能够帮助你找到, 下载, 安装,已经更新需要的包
  3. 支持Pypi上传
  4. 支持集成测试
  5. 提供了更多的功能函数和额外特性.
  
### pip 高级用法
- 1.命令自动补全, 对于zsh用户支持非常友好
```
pip completion --zsh >> ~/.zprofile
source ~/.zprofile
```

- 2.普通用户安装软件
`pip install django --user`
`pip show django| grep Location`

- 3.编辑模式
- 4.使用devapi作为缓存代理服务器
```
pip install devpi-server
devpi-server --host=0.0.0.0 --start

pip install -i http://localhost:3141/root/pypi tornado

# 或者配置pip.conf

# web界面
pip install -U devpi-web
```

- 5.PYPI的完全镜像
