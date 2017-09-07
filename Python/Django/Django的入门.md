# Django的入门教程[基于1.8]
---
## Model

### 一个Models的多个字段外键指向同一个用户
```
creator = models.ForeignKey(Users, null=True, related_name='creator')
assignee = models.ForeignKey(Users, null=True, related_name='assignee')
# 多对多也类似
```
### admin
adminModel
```
list_display
search_fileds
list_filter
date_hierarchy
ordering
fields
filter_horizontal
raw_id_fields


```

### Django的Model的Manager

```python
# models.py

class BookManager(models.Manager):
    def title_count(self, keywords):
        return self.filter(title__icontains=keywords).count()
        # self指向BookManager本身

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeginKey(Publisher)
    publication_date = models.DateField()
    num_pages = models.IntegerField(blank=True, null=True)
    objects = BookManager() #

    def __str__(self):
        reutrn self.title


>>> Book.objects.title_count('django')
```

修改初始manager 的 QuerySets
```
class  DahlBookManager(models.Manager):
    def  get_queryset(self):
        super(DahlBookManager, self).get_queryset().filter(
            author='dahl')

class Book(models.Model):
    ...
    dahl_objects = DahlBookManager()
```

Model 的方法
自动定义方法
```
class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()

    def  baby_boomer_status(self):
        import datetime
        if self.birth_date < datetime.date(1945,  8, 1):
            return 'Pre-boomer'
        elif self.birth_date < datetime.date(1965, 1,1):
            return 'Baby boomer'
        else:
            return 'Post-boomer'
    
    def _get_full_name(self):
        return ''


```
继承方法
save()
delete

使用raw sql
Manager.raw()
`Manager.raw(raw_query, params=None, translations=None`: 返回`django.db.models.query.RawQuerySet`

Person.objects.raw('SELECT id, first_name, last_name, birth_date FROM
myapp_person')

>>> Person.objects.raw('''SELECT first AS first_name,
... last AS last_name,
... bd AS birth_date,
... pk AS id,
... FROM some_other_table''')

>>> name_map = {'first': 'first_name', 'last': 'last_name', 'bd':
'birth_date', 'pk': 'id'}
>>> Person.objects.raw('SELECT * FROM some_other_table',
translations=name_map)


Adding extra Manager methods

## xadmin 配置
### xadmin

类的图标
model_icon 
ordering 排序
readonly_field = ['字段']  # 设置为只读(后台)
execlude = ['field']  设置为编辑时,隐藏
execlude 和readonly_field的字段是冲突的

relfield_style = 'fk_ajax' # 设置外键的加载方式


自定义列表返回数据, 同一个model注册两个管理器

在models中,
新建一个继承Model, 只需写Meta信息就可以
Meta:
   proxy = True # 不会生成表, 但具有Model的功能

然后新建一个ModelAdmin之后进行注册,
在ModelAdmin中
定义 queryset()
```
def  queryset():
    qs = super(xxxx, self).queryset()
    qs = qs.filter(xxxx)
    return qs
```

#### xadmin 的其他功能
list_editor = ['degree', 'desc'] # field 在列表页的 那些字段可以修改, 可以是 Model里第一的函数
get_zj_num.description = '章节数'

增加, 自定义html

refresh_times = [3, 5] 定时刷新的时间
在ModelAdmin 重新定义save_models的方法


#### xadmin的插件开发
pip install DjangoUeditor
settings, INSTALL_APP
添加url
使用 UEditorField()

在xadmin/plugin/新建uedtior
在`__init__.py` 添加 ueditor
在 adminx中添加 style_fields = {'detail': 'ueditor'}



## Django rest framework

```
pip install djangorestframework
pip install markdown       # Markdown support for the browsable API.
pip install django-filter


INSTALLED_APPS = (
    ...
    'rest_framework',
)

urlpatterns = [
    ...
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

```

## Django 扩展的 User

```py
# models
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=16, verbose_name=u"昵称", default=u'用户名称')
    gender = models.CharField(choices=(('male', u'男'), ('female', u'女')), default=u'female', max_length=6,
                              verbose_name=u"性别")
    weixin = models.CharField(max_length=100, default=u"", verbose_name=u"微信")
    mobile = models.CharField(max_length=11, verbose_name=u'手机', null=True)
    image = models.ImageField(upload_to='image/%Y/%m', default=u"image/default.png", max_length=100, verbose_name=u"头像")


##  settings 指定 User
AUTH_USER_MODEL = 'users.UserProfile'
```

## Django 1.11 MySQL SQL_MODE
`(mysql.W002) MySQL Strict Mode is not set for database connection 'default'`

```
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }

    # or
    'OPTIONS': {
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    },
```


## Form

### ModelForm
https://stackoverflow.com/questions/2216974/django-modelform-for-many-to-many-fields
