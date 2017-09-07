#Flask使用教程
---

## Flask基础

### Flask 路由
Flask的路由可以使用装饰`route`

`变量规则`
要给 URL 添加变量部分，你可以把这些特殊的字段标记为` <variable_name>` ， 这个部分将会作为命名参数传递到你的函数。规则可以用 `<converter:variable_name>` 指定一个可选的转换器。这里有一些不错的例子:
```python
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id
```

`转换器有下面几种`：

`string`: 接受任何没有斜杠"/"的文本, 默认.
`int`  接受整数
`float`   同 int ，但是接受浮点数
`path`  和默认的相似，但也接受斜线
`uuid`: 只接受uuid字符串
`any`: 可以指定多种路径, 但是需要传入参数
  `@app.route('/<any(a,b):page_name>/')`

如果不希望定制路径, 还是通过传递参数的方式,如/people/?name=a等. 
可以通过`request.args.get('name')`来获得.

__唯一 URL / 重定向行为__
Flask 的 URL 规则基于 Werkzeug 的路由模块。这个模块背后的思想是基于 Apache 以及更早的 HTTP 服务器主张的先例，保证优雅且唯一的 URL。

以这两个规则为例:
```
@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'
```
虽然它们看起来着实相似，但它们结尾斜线的使用在 URL 定义 中不同。 第一种情况中，指向 projects 的规范 URL 尾端有一个斜线。这种感觉很像在文件系统中的文件夹。访问一个结尾不带斜线的 URL 会被 Flask 重定向到带斜线的规范 URL 去。

然而，`第二种情况的 URL 结尾不带斜线，类似 UNIX-like` 系统下的文件的路径名。访问结尾带斜线的 URL 会产生一个` 404 “Not Found” `错误。

这个行为使得在遗忘尾斜线时，允许关联的 URL 接任工作，与 Apache 和其它的服务器的行为并无二异。此外，也保证了 URL 的唯一，有助于避免搜索引擎索引同一个页面两次。

### 构造URL
Flask可以构造URL,可以使用`url_for()` 来指定函数构造URL, 它接受函数名作为url_for()的第一个参数, 也可以对应的URL规则变量部分的命名参数.
```python
>>> from flask import Flask, url_for
>>> app = Flask(__name__)
>>> @app.route('/')
... def index(): pass
...
>>> @app.route('/login')
... def login(): pass
...
>>> @app.route('/user/<username>')
... def profile(username): pass
...
>>> with app.test_request_context():
...  print url_for('index')
...  print url_for('login')
...  print url_for('login', next='/')
...  print url_for('profile', username='John Doe')
...
/
/login
/login?next=/
/user/John%20Doe

```


url_for()函数最简单的用法是以视图函数名（或者`app.add_url_route()`定义路由时使用的端点名）作为参数，返回对应的URL。例如，在当前版本的hello.py程序中调用`url_for('index')`得到的结果是`/`。调用`url_for('index', _exter-nal=True)`返回的则是绝对地址，在这个示例中是`http://local-host:5000/`。

例如，`url_for('user', name='john', _external=True)`的返回结果是`http://localhost:5000/user/john`。

### redirect 跳转
redirect(location);
redirect(location, code=301) 

### 自定义URL转换器
Reddit通过在URL中用一个加号(+)隔开各个社区名字,方便同时查看多个社区的帖子(http://redit.com/r/flask+lisp).
我们来自定义一个转换器来实现这个功能, 它还可以设置所使用的分隔符, 不一定用"+"
```python
import urllib
from flask import Flask 
from werkzeug.routing import BaseConverter

app = Flask(__name__)

class ListConverter(BaseConverter):
    def __init__(self, url_map, separator="+"):
        super(ListConverter, self).__init__(url_map)
        self.separator = urllib.unique(separator)

    def to_python(self, value):
        return value.split(self.separator)

    def to_url(self, values):
        return self.separator.join(BaseConverter.to_url(value) for value in values)

app.url_map.converters['list'] = ListConverter

@app.route('/list1/<list:page_name>/')
def index():
    return 'Separator: {} {}'.format('+', page_name)

@app.route("/list2/<list(separator=u'|'):page_names>/")
def list2(page_names):
    return 'Separator: {} {}'.format('|', page_names)
    

if __name__=='__main__':
    app.run(debug=True)
```

### Cookies
通过cookies属性来访问Cookies, 用响应对象的set_cookie方法来设置Cookies. 请求对象的cookies属性是一个内容为客户端提交的所有Cookies的字典.

1.读取cookie
```python
from  flask import request

@app.route('/')
def index():
    username = request.cookie.get('username')
```

2. 存储cookies

```
from flask import make_response

@app.route("")
def index():
    resp = make_response(render_template(...))
    resp.set_cookie('username', 'the username'
    return resp

```



### 会话
除请求对象之外, 还有一个session对象.它允许在不同的请求间存储特定用户的信息. 他是在Cookies的基础上实现的, 并且对Cookies进行密钥签名. 这就意味着用户可以查看你的Cookie内容,但是不能修改它,除非用户知道签名的密钥.

要使用会话, 需要设置一个密钥.

```python
from  flask import Flask, session, redirect, url_for, escape, request
app = Flask(__name__)
@app.route("/")
def index():
    if 'username' in session:
        return 'Login'
    return 'You are not login'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''
# 当使用request.form去取POST的提交时, 最好使用request.form.get('username', None), 当username没有值时指定默认值,如果不指定会返回http 的400错误.
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
```

### Flask的上下文
1.程序上下文: 
2.请求上下文

|变量名| 上下文| 说明|
|:---|----|-----------|
|current_app|程序上下文|当前激活程序实例|
|g|程序上下文|处理请求时做临时存储对象,每次请求都会设置这个变量|
|request|请求上下文|请求对象,封装了客户端发出的HTTP请求中的内容|
|session|请求上下文|用户会话,用于存储请求之间需要'记住'的值的词典|

Flask在分发请求之前激活(或者推送)程序和请求上下文, 请求处理完成后再将其删除.程序上下文被推送后, 就可以在线程中使用`current_app`和`g`变量. 类似地, 请求上下文在被推送后,就可以使用`session`,`request`变量.
。如果使用这些变量时我们没有激活程序上下文或请求上下文，就会导致错误。

```
>>> from hello import app
>>> from flask import current_app
>>> current_app.nameTraceback (most recent call last):...RuntimeError: working outside of application context
>>>
>>> app_ctx = app.app_context() 
>>> app_ctx.push()
>>> current_app.name'hello'
>>> app_ctx.pop()
```

### 请求钩子
在处理请求之前或者之后执行代码.

1. `before_first_request`: 注册一个函数, 在处理第一个请求之前执行.
2. `before_request`: 注册一个函数, 在每次请求之前执行
3. `after_request`:  注册一个函数, 如果没有未处理的异常抛出, 在每次请求执行后运行.
4. `teardown_request`: 注册一个函数, 即使有未处理的异常抛出, 也在每次请求后执行.

在请求钩子函数和视图函数之间共享数据一般使用上下文全局变量g。例如，`before_request`处理程序可以从数据库中加载已登录用户，并将其保存到`g.user`中。随后调用视图函数时，视图函数再使用`g.user`获取用户。

### 如何使用g
g是一个被LocalProxy包装的对象, 而且还需要借助before_request使用:
```
@before_request
def set_g():
    g.user = 
```

### 访问请求数据
对于Web应用,与客户端发送给服务器的数据交互至关重要. 在Flask中由全局的request对象来提供这些信息. 

#### 环境局部变量
Flask中的某些对象是全局对象,但却不是通常的那种. 这些对象实际上是特定环境的局部对象代理.

想象一下处理线程的环境. 一个请求传入, Web服务器决定生成一个新的线程(或者别的什么, 只要这个底层的对象可以胜任并发系统,而不仅仅是线程). 当Flask开始它内部的请求处理时, 它认定当前线程是活动的环境, 并绑定当前的应用和WSGI环境到那个环境上(线程). 它的实现很巧妙, 能保证一个应用调用另一个应用时不会出现问题.

所以, 这对你来说意味着什么?除非你要做类似单元测试的东西, 否则你基本上可以全无视它.你会发现依赖于一段请求对象的代码, 因没有请求对象无法正常运行. 解决的方案是,自行创建一个请求对象并且绑定到环境中. 单元测试的最简单的解决方案是: 用`test_request_context()`环境管理器. 结合with声明, 绑定一个测试请求, 这样你才能与之交互.如:
```python
from  flask import request

with app.test_request_context("/hello", methods=['POST']):
    assert request.path == '/hello'
    assert rquest.method == 'POST'
```
另一种可能是: 传递整个WSGI环境给`request_context()`方法:
```python
from flask import request
with app.request_context(environ):
    assert request.method == "POST"
```


### flash 
请求完成后，有时需要让用户知道状态发生了变化。这里可以使用确认消息、警告或者错误提醒。一个典型例子是，用户提交了有一项错误的登录表单后，服务器发回的响应重新渲染了登录表单，并在表单上面显示一个消息，提示用户用户名或密码错误。
使用flash 来完成这种效果

### url的跳转, 404错误处理, abort

### flask logger
#### 错误邮件
```
ADMINS = ['yourname@example.com']
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler('127.0.0.1',
                               'server-error@example.com',
                               ADMINS, 'YourApplication Failed')
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
```


#### 记录到文件
即便你收到了邮件，你可能还是想记录警告。当调试问题的时候，收集更多的信息是个好主意。请注意 Flask 核心系统本身不会发出任何警告，所以在古怪的事情发生时发出警告是你的责任。

在日志系统的方框外提供了一些处理程序，但它们对记录基本错误并不是都有用。最让人感兴趣的可能是下面的几个:

`FileHandler` - 在文件系统上记录日志
`RotatingFileHandler` - 在文件系统上记录日志， 并且当消息达到一定数目时，会滚动记录
`NTEventLogHandler` - 记录到 Windows 系统中的系统事件日志。如果你在 Windows 上做开发，这就是你想要用的。
`SysLogHandler` - 发送日志到 Unix 的系统日志
```
if not app.debug:
    import logging
    from themodule import TheHandlerYouWant
    file_handler = TheHandlerYouWant(...)
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)
```

```
from flask import Flask
import logging

app = Flask(__name__)


@app.route('/')
def root():
    app.logger.info('info log')
    app.logger.warning('warning log')
    return 'hello'

if __name__ == '__main__':
    app.debug = True
    handler = logging.FileHandler('flask.log')
    app.logger.addHandler(handler)
    app.run(
```

## flask 的管理的配置
### 直接硬编码
app.config['DEBUG'] = True

app.config 是flask.config.Config类的一个实例, 继承自dict.
app.config支持多种更新配置方式. 假设现在有个叫做settings.py 的配置文件, 其中的内容如下:
A=1

* 1.通过配置文件加载
  `app.config.from_object('settings')`: 通过字符串的模块名字
  # 或者通过引入模块的方式. 直接引入模块对象
  `importsettings`
  `app.config.from_object(settings)`
* 2.通过文件名字加载. 直接传入文件名字, 但是不限于只用于.py后缀的文件名
  `app.config.form_pyfile('settings', silent=True)`: 默认当配置文件不存在时,会抛出异常, 使用silent=True时候只返回False, 不抛出异常.

* 3.通过加载环境变量的方式. 这种方式依然支持silent参数, 获得路径后其实还是使用from_pyfile的.
```
export YOUR_SETTINGS='settings.py'
app.config.from_envvar('SETTINGS')
```

### 响应的错误处理
```python
@app.errorhandler(404)
def not_found(error):
    return rend_template('error.html'), 404
#可以改成如下显示的调用make_respone的方式:
@app.errorhandler(404)
def not_found():
    resp = make_respone(render_template('error.html', 404))
    return resp
```
第二种方法灵活,可以添加一些额外的工作,如cookie, header等

## 即插视图
Flask 的这种视图类型有两种.
### 标准视图
需要继承flask.views.View, 必须实现dispatch_request, 看一个例子(app_view.py)
```python
from flask import Flask, request, rend_template
from flask.views import View

app = Flask(__name__, template_folder='../../template')

class BaseView(View):
    def get_template_name(self):
        raise NotImplementedError()

    def render_template(self, context):
        return rend_template(self.get_template_name(), **context)

    def dispatch_request(self):
        if request.method != 'GET':
            return 'UNSUPPORTED!'
        context = {'users' : self.get_user()}
        return self.render_template(context)

class UserView(BaseView):
    def get_template_name(self):
        return 'chapater3/section1/users.html'

    def get_users(self):
        return [{
            'username': 'fake',
            'avatar': 'http://lorempixel.com/100/100/nature/'
        }]

app.add_url_rule('/users', view_func=UserView.as_view('userview'))
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
```

### 基于调用调度方法的视图
flask.views.MethodView对于每个HTTP方法会执行不同的函数, 这对HTTP的REST ful很有帮助.
```python
from flask import Flask, jsonify
from flask.views import MethodView

class UserAPI(MethodView):
    def get(self):
        return jsonify({
            'username': 'fake',
            'avatar': 'http://lorempixel.com/100/100/nature/'
            })

    def post(self):
        return 'UNSOPPORTED!'

app.add_url_rule('/user', view_func=UserAPI.as_view('userview'))
if __name__ == '__main__':
    app.run()
```

通过装饰器as_view的返回值来实现对于视图的装饰功能, 常用于权限检查,登录验证等:
```
def  user_required(f):
    def decorator(*args, **kwargs):
        if not g.user:
            abort(401)
        return f(*args, **kwargs)
    return decorator

view = user_required(UserAPI.as_view('users'))
app.add_url_rule('/users/', **kwargs)
```

## flask 的signals

### 常用函数

## flask手动处理提交表单
### 处理get的从url中的querystring
```
request.args.get('a')
```
### form 提交
```
#POST
request.form['username'] # 处理PUT和POST提交
```
### json
```
var obj = {
    "username": "aaaa",
    "password": "111111"
}
$.ajax({
    data: JSON.stringify(obj)
    })

$.ajax({
        url: "/host/quickImport",
        data: JSON.stringify(obj),
        type: 'POST',
        contentType: "application/json",
        success: function(data){  
                  },
                  error: function(error){
                    console.log(error)
                  }
                });
```

## Flask 扩展

### 1.使用Flask-Script支持命令行选项

```python
from  flask.ext.script import Manager
manager = Manager(app)


if __name__ == '__main__':
    manager.run()
```

`python manager.py ....`



### 2. 使用Flask-Bootstrap集成 Twitter Bootstrap

`{% extends "bootstrap/base.html" %}` 使用继承bootstrap的

基本模板:
```html
{% extends "bootstrap/base.html" %}
{% block title %} {% endblock %}
{% block content %} {% endblock %}
```


Bootstrap所需的文件在styles和scripts块中声明。如果程序需要向已经有内容的块中添加新内容，必须使用Jinja2提供的super()函数。例如，如果要在衍生模板中添加新的JavaScript文件，需要这么定义scripts块：
```
{% block scripts %}
{{ super() }}
<script type="text/javascript" src="my-script.js"></script>
{% endblock %}
```



### 3.使用Flask-Moment本地化日期和时间

处理多时区时, 把时间传给客户端, 在客户端的浏览器来来处理时间, 所以可以使用`moment.js`.

导入`moment.js`库

```
{% block scripts %}
{{ super() }}
{{ moment.include_moment() }}
{% endblock %}
```

__在模板中处理使用moment.js__

```
{{ moment(current_time).format('LLL') }}
{{ moment(current_time).fromNow(refresh=True) }}
```

`format('LLL')`根据客户端电脑中的时区和区域设置渲染日期和时间。参数决定了渲染的方式，'L'到'LLLL'分别对应不同的复杂度。format()函数还可接受自定义的格式说明符。

第二行中的fromNow()渲染相对时间戳，而且会随着时间的推移自动刷新显示的时间。这个时间戳最开始显示为“a few sec-onds ago”，但指定refresh参数后，其内容会随着时间的推移而更新。如果一直待在这个页面，几分钟后，会看到显示的文本变成“a minute ago”“2 minutes ago”等。


### 4. Web 表单处理 Flask-wtf

避免跨站请求伪造保护, 设置密钥.

使用Flask-WTF时，每个Web表单都由一个继承自Form的类表示。这个类定义表单中的一组字段，每个字段都用对象表示。字段对象可附属一个或多个验证函数。验证函数用来验证用户提交的输入值是否符合要求。

```python
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField # 导入字段类, 可以继承扩展这些字段
from wtforms.validators import Required # 导入验证的函数
class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')
```

常用的表单
1. StringfField
2. TextAreaField
3. PasswordField
4. HiddenField
5. DateField
6. DateTimeField
7. IntegerField
8. DecimalField
9. BooleanField
10. RadioField
11. SelectField
12. SelectMultipleField
13. FileField
14. SubmitField
15. FormField :把表单作为字段嵌入另一个表单
16. FileList: 一组指定类型字段

__验证函数__
|验证函数| 说明|
|---|---|
|Email|验证邮件地址|
|EqualTo|比较两个字段的值,常用于两次输入密码比较|
|IPAddress|验证IPv4|
|Length|验证字符串的长度|
|NumberRange|数值范围|
|optional|无输入值时跳过其他验证函数|
|Rquired|非空验证|
|Regexp|正则表达式验证|
|URL|URL验证|
|AnyOf|确保输入值在可选列表里|
|NoneOf|确保输入值,不在可选列表里|


__自定义验证__:
自定义验证通过,在Form里创建验证函数来验证,验证不通过触发一个异常. 验证函数的定义格式为:
`validate_`attr(self, field) attr是在Form里已定义字段的名称,确保名称一样. 如下面验证`useranem`的字段, 

```python
def user(Form):
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
```
#### 使用Flask-Bootstrap渲染wtf
```
{% import "bootstrap/wtf.html" as wtf %}{{ wtf.quick_form(form) }}
```


#### 视图中处理Form
```python
@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name)
```

`form.validate_on_submit()`: 当POST提交的内容,提交后,Form验证通过后提交, `form.validate_on_submit()`返回True


### mulixcheckbox
http://stackoverflow.com/questions/19564080/how-to-pre-populate-checkboxes-with-flask-wtforms

https://gist.github.com/doobeh/4668212

### 手动处理form


#### 实例

* 1.ddd
```python
from wtforms import StringField, TextField, BooleanField, SelectField, \
    SubmitField, IntegerField, SelectMultipleField, HiddenField, FileField
from wtforms.validators import Required, Length, Email, Regexp, IPAddress, NumberRange, \
    URL

from ..models import Tomcat
import os
from flask import current_app

from ..exceptions import ValidationError


class TomcatForm(Form):
    app_name = StringField('tomcat Name', validators=[
                           Required(), Length(1, 20)])

    http_port = IntegerField('http_port', validators=[
                             Required(), NumberRange(min=8000, max=9000)])
    ajp_port = IntegerField('ajp_port', validators=[
                            Required(), NumberRange(min=7000, max=7999)])
    # 下拉框的选择, 通过在__init__ 初始化 select的列表
    host = SelectField('Host', coerce=int)
    # 多选框, 通过在__init__ 初始化 多选框
    aaa = SelectMultipleField('Aaa', coerce=int)

    # 密码验证,以及密码
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])

    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(TomcatForm, self).__init__(*args, **kwargs)
        # 初始化select的列表
        self.host.choices = [(host.id, host.hostname)
                             for host in Host.query.order_by(Host.hostname).all()]
        self.aaa.choices = [
            (tomcat.id, tomcat.app_name) for tomcat in Tomcat.query.order_by(Tomcat.app_name).all()
        ]

    def validate_http_port(self, field):
        if Tomcat.query.filter_by(host_id=self.host.data).filter_by(_httpport=field.data).first():
            raise ValidationError(
                'The http port %s already used!' % field.data)


    def validate_ajp_port(self, field):
        if Tomcat.query.filter_by(host_id=self.host.data).filter_by(_ajpport=field.data).first():
            raise ValidationError('The ajp port %s already used!' % field.data)
      

    def validate_app_name(self, field):
        if os.path.exists(current_app.config['TOMCAT_APPDIR'] + "/tomcat_" + field.data):
            raise ValidationError(
                "The Tomcat is exist at the /usr/local/%s" % field.data)

```



* 2.上传文件
``` python
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename

class PhotoForm(Form):
    photo = FileField('Your photo')


@app.route('/upload/', methods=('GET', 'POST'))
def upload():
    form = PhotoForm()
    if form.validate_on_submit():
        filename = secure_filename(form.photo.data.filename)
        form.photo.data.save('uploads/' + filename)
    else:
        filename = None
    return render_template('upload.html', form=form, filename=filename)
```


限制类型的上传

```python

from flask_uploads import UploadSet, IMAGES
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired

images = UploadSet('images', IMAGES)

class UploadForm(Form):
    upload = FileField('image', validators=[
        FileRequired(),
        FileAllowed(images, 'Images only!')
    ])
```

同一种另一种方式实现
```python
class UploadForm(Form):
    upload = FileField('image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])

```

#### FormField
[文档](https://wtforms.readthedocs.io/en/latest/fields.html)

```
class TelephoneForm(Form):
    country_code = IntegerField('Country Code', [validators.required()])
    area_code    = IntegerField('Area Code/Exchange', [validators.required()])
    number       = StringField('Number')

class ContactForm(Form):
    first_name   = StringField()
    last_name    = StringField()
    mobile_phone = FormField(TelephoneForm)
    office_phone = FormField(TelephoneForm)
```
#### FormList
```
authors = FieldList(StringField('Name', [validators.DataRequired()]))
```
```
class IMForm(Form):
    protocol = SelectField(choices=[('aim', 'AIM'), ('msn', 'MSN')])
    username = StringField()

class ContactForm(Form):
    first_name  = StringField()
    last_name   = StringField()
    im_accounts = FieldList(FormField(IMForm))
```

### Flask-Bootstrap
#### 设置bootstrap的cdn或者本地资源
```
nano flask_bootstrap/__init__.py
def lwrap(cdn, primary=static):
    return ConditionalCDN('BOOTSTRAP_SERVE_LOCAL', primary, cdn)

bootstrap = lwrap(WebCDN('//cdn.bootcss.com/bootstrap/%s/' % BOOTSTRAP_VERSION), local)
jquery = lwrap(WebCDN('//cdn.bootcss.com/jquery/%s/' % JQUERY_VERSION), local)
html5shiv = lwrap(WebCDN('//cdn.bootcss.com/html5shiv/%s/' % HTML5SHIV_VERSION))
respondjs = lwrap(WebCDN('//cdn.bootcss.com/respond.js/%s/' % RESPONDJS_VERSION))


# 关闭CDN使用本地的静态文件
# app.config.setdefault('BOOTSTRAP_SERVE_LOCAL', False)
app.config.setdefault('BOOTSTRAP_SERVE_LOCAL', True)
```

#### csrf
```
# init_app
from flask_wtf.csrf import CsrfProtect
csrf = CsrfProtect()
csrf.init_app(app)
```
`@csrf.exempt` 排除

页面处理
```
<meta name="csrf-token" content="{{ csrf_token() }}">
    <script type="text/javascript">
    var csrftoken = $('meta[name=csrf-token]').attr('content')

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    })
    </script
```

### 数据层ORM:Flask-SQLAlchemy

使用Flask-SQLAlchemy 作为ORM的屏蔽后端的db的不同.

使用方式:
```python
from flask.ext.sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

```

mysql的设置方式`mysql://username:password@server/db`

```
postgresql://scott:tiger@localhost/mydatabase
oracle://scott:tiger@127.0.0.1:1521/sidname
```



#### 定义模型:

* 1.普通字段
```python

class Role(db.Model):
    __tablename__ = 'roles' # 数据库中表面
    id = db.Column(db.Integer, primary_key=True) # 字段名:id, 字段类型 Integer, 主键

    name = db.Column(db.String(64), unique=True) # 字段名:name, 字段类型 String, 唯一存在
    default = db.Column(db.Boolean, default=False, index=True) # 字段名:default, 字段类型 Boolean, 建立索引
    permissions = db.Column(db.Integer)

```

|字段|说明|
|:---|----|
|Integer| an integer|
|String (size) |  a string with a maximum length|
|Text  |  some longer unicode text|
|DateTime   | date and time expressed as Python datetime object.|
|Float  | stores floating point values|
|Boolean |stores a boolean value|
|PickleType|  stores a pickled Python object|
|LargeBinary |stores large arbitrary binary data|



* 2.简单多表关系
一对多时, 在多的一端, 加一个外键
```python 
from datetime import datetime

# person 1: n address

class Person(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(12))
    address = db.relationship(
                    "Address", # 在少的一方添加一个引用,访问使用persion.address 
                    backref = 'person', # 这个添加的是本Model的表名称
                    lazy = 'dynamic' # 动态获取
                            )

class Adress(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(12))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id')) # 多的一方添加外键.  address.person


# 官方
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category',
        backref=db.backref('posts', lazy='dynamic'))
# relationship 使用 backref绑定与Category的关系,在Category的属性为posts, 动态的查询.

    def __init__(self, title, body, category, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category

    def __repr__(self):
        return '<Post %r>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name

```


- 创建一些实例
```
>>> py = Category('Python')
>>> p = Post('Hello Python!', 'Python is pretty cool', py)
>>> db.session.add(py)
>>> db.session.add(p)
```

- 我们定义了posts相关的动态关系, 所以可以这么查询:
```
>>> py.posts
<sqlalchemy.orm.dynamic.AppenderBaseQuery object at 0x1027d37d0>

>>> py.posts.all()
[<Post 'Hello Python!'>]
```

### 枚举字段
```python
import enum
#class MyEnum(enum.ENUM):
#    one='one'
#    two='two'
#    three = 'three'
UserRole = ['add', 'delete']
class Tmod(db.Module):
    types = db.Column(db.ENUM(*UserRole), default='add')

```

* db的一些操作
初始化环境,以及删除
```
>>> from yourapplication import db
>>> db.create_all()
>>> db.drop_all()
```


## flask-sqlalchmey的crud
```
>>> from yourapp import User
>>> me = User('admin', 'admin@example.com')
>>> db.session.add(me)
>>> db.session.commit()

>>> me.id
1

>>> db.session.delete(me)
>>> db.session.commit()
>>> 


>>> peter = User.query.filter_by(username='peter').first()
>>> peter.id
1
>>> peter.email
u'peter@example.org'


>>> missing = User.query.filter_by(username='missing').first()
>>> missing is None
True

>>> User.query.filter(User.email.endswith('@example.com')).all()
[<User u'admin'>, <User u'guest'>]


>>> User.query.order_by(User.username)
[<User u'admin'>, <User u'guest'>, <User u'peter'>]


>>> User.query.get(1)
<User u'admin'>


```


## 多数据库的绑定

```python
SQLALCHEMY_DATABASE_URI = 'postgres://localhost/main'
SQLALCHEMY_BINDS = {
    'users':        'mysqldb://localhost/users',
    'appmeta':      'sqlite:////path/to/appmeta.db'
}
```

```
>>> db.create_all()
>>> db.create_all(bind=['users'])
>>> db.create_all(bind='appmeta')
>>> db.drop_all(bind=None)
```

```python
class User(db.Model):
    __bind_key__ = 'users' # 指定数据库
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
```
or
```python
user_favorites = db.Table('user_favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('message_id', db.Integer, db.ForeignKey('message.id')),
    info={'bind_key': 'users'}
)
```


## Flask-sqlchmey的models的使用继承的方式

```python
class BaseApp(db.Model):
    """
http://blog.csdn.net/wenxuansoft/article/details/50243155
http://www.sdg32.com/posts/sqlalchemy-mixin-event
http://docs.sqlalchemy.org/en/rel_0_9/orm/extensions/declarative/mixins.html
    """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(64), unique=True)
    app_dir = db.Column(db.String(128))
    app_cmd_start = db.Column(db.String(64))
    app_cmd_stop = db.Column(db.String(64))
    app_comments = db.Column(db.Text())

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def cmd_shutdown(self):
        pass

    def cmd_start(self):
        pass

    def status(self):
        pass

class Tomcat(BaseApp):
    __tablename__ = 'tomcat'

    _shutdownport = db.Column(db.Integer)
    _httpport = db.Column(db.Integer)
    _ajpport = db.Column(db.Integer)
    _sslport = db.Column(db.Integer)
    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'))

    def __init__(self, *args, **kwargs):
        super(Tomcat, self).__init__(*args, **kwargs)
        self.app_dir = current_app.config[
            'TOMCAT_APPDIR'] + "/tomcat_" + self.app_name
        stport = db.session.query(db.func.max(Tomcat._shutdownport)).scalar()
        if stport is None:
            self._shutdownport = 4004
        else:
            self._shutdownport = stport + 1
        sslport = db.session.query(db.func.max(Tomcat._sslport)).scalar()
        if sslport is None:
            self._sslport = 5121
        else:
            self._sslport = sslport + 1

        tomcatbase = current_app.config['TOMCATINITPAGE']

        # sh.copy(tomcatbase, toTomcatName)
        shutil.copytree(tomcatbase, self.app_dir)

    def setJvm(self, **kwargs):
        pass

    def setPorts(self):
        setTomcatPort(self.app_dir + "/conf/server.xml", self._shutdownport,
                      self._httpport, self._ajpport,
                      self._sslport)

    @property
    def http_port(self):
        return self._httpport

    @http_port.setter
    def http_port(self, http_port):
        #....
        self._httpport = http_port

    @property
    def ajp_port(self):
        return self._ajpport

    @ajp_port.setter
    def ajp_port(self, ajpport):
        #.....
        self._ajpport = ajpport

    @property
    def shutdown_port(self):
        return self._shutdownport

    @shutdown_port.setter
    def shutdown_port(self, shutdown_port):
        #...
        self._shutdownport = shutdown_port

    @property
    def ssl_port(self):
        return self._sslport

    @ssl_port.setter
    def ssl_port(self, ssl_port):
        #...
        self._sslport = ssl_port

    def __repr__(self):
        return '<Tomcat %r>' % self.app_name


class Nginx(BaseApp):
    __tablename__ = 'nginx'
    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'))
    vhost = db.relationship('Vhost', backref='nginx', lazy='dynamic')

    def __repr__(self):
        return '<Nginx %r>' % self.app_name
```


### Flask-SQLAlchemy的分页
使用flask-sqlalchemy 的paginate()分页

请求得到页数
```python
page = request.args.get('page',1, type=int)

pagination = Post.query.order_by(Post.timestamps.desc()).paginate(
                page,
                per_page = current_app['POST_PER_PAGE'],
                error_out = False)

posts = pagination.items
return render_template('index.html', form=form, posts=posts, pagniation=pagination)
```
为了显示某页中的记录，要把`all()`换成`Flask-SQLAlchemy`提供的`paginate()`方法。`页数`是`paginate()`方法的第一个参数，也是唯一必需的参数。可选参数per_page用来指定每页显示的记录数量；如果没有指定，则默认显示20个记录。另一个可选参数
paginate()方法的返回值是一个`Pagination类对象`, 这个类在Flask-SQLAlchemy中定义. 这个对象包含很多属性, 用于在模板中生成分页链接, 因此将其对象参数传入了模板, 分页对象的属性简介如下:

`items`: 当前页面中的记录
`query`: 分页的源查询
`page`: 当前页数
`prev_num`: 上一页的页数
`next_num`: 下一页的页数
`has_next`: 如果有下一页, 返回True
`has_prev`: 如果有上一页, 返回True
`pages`: 查询到的总页数
`per_page`: 每页显示的记录数量
`total`: 查询返回的记录总数

在Flask-SQLAlchemy对象上可以调用的方法
```
iter_pages(
            left_edge=2,
            left_current=2,
            right_current=5,
            right_edge=2
            ): 
```
一个迭代器,返回一个在分页导航中显示的页数列表. 这个列表的最左边显示left_edge页,当前页的昨天显示left_current页, 当前页的右边right_current页,最右边显示right_edge页. 例如,在一个100页的列表中,当前为第50页,使用默认配置, 这个方法返回一下页数:
             1,2,None,48,49,50,51,52,53,54,55,None,99,100

`perv()`: 上一页对象
`next()`: 下一页对象




## Flask-wtf Flask-
