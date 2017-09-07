# 怎么构建一个基于Flask的大型项目
---

如果构建一个大型的Flask项目, 一般的结构为:


程序一般保存在app包中.
config.py 存储配置变量
manage.py 用于启动以及其他程序

1. config.py
```python
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'unix': UnixConfig,

    'default': DevelopmentConfig
}
```
基类Config中包含通用的配置, 子类分别定义专用配置.
为了让配置方式更灵活且安全, 某些配置可以从环境变量中导入.

配置类可以定义init_app()类方法, 七参数是程序实例.在这个方式中,可以执行对当前环境的配置初始化. 基类中Config中
的init_app()方法为空.

config字典中注册了不同的配置环境, 而且设置了一个默认的配置.

### 2. 程序包app
用来存放程序的所有代码, 模板和静态方法.


### 3.使用程序工厂函数
`延迟创建程序实例`: 把创建过程到可显式调用的工厂函数中.这种方法不仅可以给脚本留出配置程序的时间,还能创建多个程序实例,这些实例有时在测试中非常有用.程序的工厂函数在app包的构造文件中定义.

构造文件导入了大多数正在使用的Flask扩展.由于尚未初始化所需的程序实例,所以没有初始化扩展,创建扩展类时没有向构造函数传入参数.create_app()函数就是程序的工厂函数,接受一个参数,程序使用的配置名.配置类在config.py文件中定义, 其中保存的配置可以使用Flaskapp.config配置对象提供的from_object()方法直接导入程序.至于配置对象,则可以通过名字从config字典中选择.程序创建并配置好后, 就能初始化扩展了.在之前创建的扩展对象上调用init_app()可以完成初始化过程.


### 在蓝本中实现程序功能
在单脚本程序中, 程序实例存在于全局作用域中, 路由可以直接使用app.route修饰定义.但现在程序在运行时创建,只有调用create_app()之后才能使用app.route修饰器,这是定义路由就太晚了.和路由一样, 自定义的错误页面处理也面临相同的困难,因为错误页面处理程序使用app.errorhandler修使其定义.

