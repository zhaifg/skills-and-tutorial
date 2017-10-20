# Django个人总结
---


```
class Order(models.Model):
    customer = models.ForeignKey(Customer)
    goods = models.ForeignKey(Goods)
    unit_price = models.FloatField()

    nums = models.IntegerField()
    total_price = models.FloatField(editable=False)
    create_datetime = models.DateTimeField(auto_now=True)  # 前端不是显示
    send_date = models.DateField("发货时间") # 发货日期,自由选择

    # clean处理填入对象的属性值的范围,自定义,可以触发一个错误
    def clean(self): 
        if self.unit_price < 0  or self.nums < 0 :
            raise ValidationError(u"单价或数量不能小于零!")
            # self.unit_price = 0
            # self.nums = 0
    
    # save自定义保存对象,重写save方法,注意要执行super,这样才可以存入数据库
    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.nums
        super(Order, self).save(*args, **kwargs)
```

## Django更改models的后操作



### 修改你的模型（在models.py文件中）。
1. 运行python manage.py makemigrations ，为这些修改创建迁移文件
2. 运行python manage.py migrate ，将这些改变更新到数据库中。
3. 将生成和应用迁移文件的命令分成几个命令来执行，是因为你可能需要将迁移文件提交到你的版本控制系统中并跟随你的应用一起变化； 

这样做不仅可以使开发变得更加简单，而且对其他开发者以及上线生产非常有用。

```
python manage.py makemigrations app
python manage.py sqlmigrate app 00x

 python manage.py migrate xxx
```

## 视图

`views.py`

1. 导入相应的http包,models.
2. 修改urls.py映射相应的url.


### `url()`函数
url()函数具有四个参数:两个必须的regex和view, 以及两个可选的kwargs和name.
1. regex: 用来匹配字符串中的模式语法.Django从第一个正则表达式开始,将一次请求的url与每个正则表达式匹配,直到找到匹配的那个为止.
2. `view`: 当Django找到一个匹配的正则表达式时,就会调用view参数指定的视图函数,并将httpRequest对象作为第一个参数,从正则表达式中"捕获"的其他的值作为其他参数,传入到该视图函数中.如果正则表达式使用简单的捕获方式,值将作为位置参数传递;如果使用命名捕获方式,值将作为关键字参数传递.
3. kwargs:任何关键字参数都可以字典形式传递给目标视图.
4. name: 命名的url.这样就可以在Django的其他地方尤其是模版中,通过名称来明确的引导这个url.这个强大的特性可以使你仅仅修改一个文件可以改变全局的URL模式.

实例:
`views`:
```
def datail(request, question_id):
    return HttpReponse("ddd")

def results(requests, question_id):
    return

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

```

`urls`:
```
from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
```

请求`/polls/34/`时,urls提交给views是:
```
detail(request=<HttpRequest object>, question_id='34')
```


##引起一个404错误
```
#polls/views.py
from django.http import Http404
from django.shortcuts import render

from .models import Question
# ...
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
```

### 快捷方式：get_object_or_404()

一种常见的习惯是使用get()并在对象不存在时引发`Http404`。Django为此提供一个快捷方式。 下面是重写后的detail()视图：

`polls/views.py`
```
from django.shortcuts import get_object_or_404, render

from .models import Question
# ...
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
```
`get_object_or_404() `函数将一个Django模型作为它的第一个参数，任意数量的关键字参数作为它的第二个参数，它会将这些关键字参数传递给模型管理器中的get() 函数。如果对象不存在，它就引发一个 Http404异常。

## 移除模板中硬编码的URLs
例如:
```
    <li><a href="/polls/{{ question.id }}/">{{ question.question_text }} </a></li>
```
这种硬编码,紧耦合的方法有一个问题,就是如果我们想在拥有许多模板文件中的项目中修
改URLs,将会变得很麻烦. 然而,因为在`polls.urls`的模块的url()函数中定义了`name`参数,你可以通过{% url %} 模板标签来移除对你URL配置中定义的特定的URL依赖.
```
    <li><a href={% url 'datail' question.id %}>{{ question.question_text }}</a></li>"
```

它的工作原理是在polls.urls模块里查找指定的URL的定义。你可以看到名为‘detail’的URL的准确定义：

```
# the 'name' value as called by the {% url %} template tag
url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
```
如果你想把polls应用中detail视图的URL改成其它样子比如 polls/specifics/12/，就可以不必在该模板（或者多个模板）中修改它，只需要修改 polls/urls.py：

```
# added the word 'specifics'
url(r'^specifics/(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
```
### 带命名空间的URL名字

教程中的这个项目只有一个应用polls。在真实的Django项目中，可能会有五个、十个、二十个或者更多的应用。 Django如何区分它们URL的名字呢？ 例如，polls 应用具有一个detail 视图，相同项目中的博客应用可能也有这样一个视图。当使用模板标签`{% url %}`时，人们该如何做才能使得Django知道为一个URL创建哪个应用的视图？

答案是在你的主URLconf下添加命名空间。 在`mysite/urls`.py文件中，添加命名空间将它修改成：

`mysite/urls.py`
```
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^admin/', include(admin.site.urls)),
]
```
现在将你的模板polls/index.html由：

`polls/templates/polls/index.html`
```
<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
```
修改为指向具有命名空间的详细视图：

`polls/templates/polls/index.html`
```
<li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
```
当你对你写的视图感到满意后，请阅读教程的第4部分来了解简单的表单处理和通用视图。


## QuerySet
一旦你建立好数据模型,Django会自动为你生成一套数据库抽象的API,可以让你创建,检索,更新和删除对象.

模型参考:
```
from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):              # __unicode__ on Python 2
        return self.headline
```

###创建对象

一个模型代表数据库中的一张表，一个模型实例代表这个数据库表中的一条特定记录．
`save()`保存对象.

```
from blog.models import Blog
b = Blog(name="dddd", tagline="Aliedd")
b.save()
```
`save`之前不会访问数据库,save()方法没有返回值.

### 保存对象的改动
```
b5.name='test2'
b5.save()
```

###  保存ForeignKey和ManyToManyField字段
更新ForeignKey字段的方式和保存普通字段的方式相同.只要把一个正确的类型的对象赋值
给该字段就可以.
```
entry = Entry.objects.get(pk=1)
cheese_blog = Blog.objects.get(name="Cheddr Talk")
entry.blog = cheese_blog
entry.save()
```

更新ManyToManyField的方式有一些不同. 需要使用字段的add()方法来增加关联一条记录.
```
joe = Author.objects.create(name="Joe")
entry.authors.add(joe)
```
为了在一条语句中,向ManyToManyField添加多条记录,可以调用`add()`方法时传入多个
参数.

```
john = Author.objects.create(name='John')
paul = Author.objects.create(name='Paul')
ringo = Author.objects.create(name='Ringo')
entry.authors.add(john,paul,ringo)
```
Django 将会在你赋值或添加错误类型的对象时报错。

### 获取对象
通过模型中的`管理器`构造的一个`查询集`,来从你的数据库中获取对象.
`查询集`表示从数据库中取出来的对象的集合.可以含有零个,一个或者多个过滤器.过滤器
根据所给的参数限制查询结构.从SQL的角度,`查询集`和`select`语句等价,过滤器是像`WHERE`和`LIMIT`一样的限制子句.

管理器:`objects`

###　获取所有对象
`all_entries = Entry.objects.all()`, 可以使用管理器`all()`

**使用过滤器获取特定对象**

`all()`
`filter(**kwargs)`: 返回一个新的查询集, 它包含满足查询参数的对象.
`exclude(**kwargs)`: 返回一个新的查询集, 它包含不满足查询参数的对象.

举个例子，要获取年份为2006的所有文章的查询集，可以这样使用filter()方法：

`Entry.objects.filter(pub_date__year=2006)`
利用默认的管理器，它相当于：
`Entry.objects.all().filter(pub_date__year=2006)`

###　链式过滤
```
Entry.objects.filter(
    headline__startswith='What'
    ).exclude(
    pub_date__gete=datetime.date.today()
        ).filter(
            pub_date__gte=datetime(2005,1,30)
            )
```
这个例子最开始获取数据库中所有对象的一个查询集，之后增加一个过滤器，然后又增加一个排除，再之后又是另外一个过滤器。最后的结果仍然是一个查询集，它包含标题以”What“开头、发布日期在2005年1月30日至当天之间的所有记录。

###  过滤后查询集是独立的
每次你筛选一个查询集,得到的都是全新的另一个查询集, 他和之前的查询集之间没有任何
绑定关系.
```
>>> q1 = Entry.objects.filter(headline__startswith="What")
>>> q2 = q1.exclude(pub_date__gte=datetime.date.today())
>>> q3 = q1.filter(pub_date__gte=datetime.date.today())
```
这三个查询集都是独立的。第一个是一个基础的查询集，包含所有标题以“What”开头的记录。第二个查询集是第一个的子集，它增加另外一个限制条件，排除pub_date 为今天和将来的记录。第三个查询集同样是第一个的子集，它增加另外一个限制条件，只选择pub_date 为今天或将来的记录。原始的查询集(q1)不会受到筛选过程的影响。

###查询集是惰性执行的
查询集是惰性执行的－－创建查询集不会带来任何数据库的访问．可以将过滤器保持一整天．直到查询集需要求值时，Django才会真正的运行这个查询．
```
>>> q = Entry.objects.filter(headline__startswith="What")
>>> q = q.filter(pub_date__lte=datetime.date.today())
>>> q = q.exclude(body_text__icontains="food")
>>> print(q)
```
虽然它看上去有三次数据库访问，但事实上只有在最后一行（print(q)）时才访问一次数据库。一般来说，只有在“请求”查询集 的结果时才会到数据库中去获取它们。当你确实需要结果时，查询集 通过访问数据库来求值。 关于求值发生的准确时间，参见何时计算查询集。

###通过get获取一个单一的对象
filter()始终给你一个查询集,即使只有一个对象满足条件--这种情况下,查询集将只包含一个元素.

`get()`: 管理器

`one_entry = Entry.objects.get(pk=1)`
可以对get()使用任何查询表达式,和filter()一样.
> 注意，使用get() 和使用filter() 的切片[0] 有一点区别。如果没有结果满足查询，get() 将引发一个DoesNotExist 异常。这个异常是正在查询的模型类的一个属性 —— 所以在上面的代码中，如果没有主键为1 的Entry 对象，Django 将引发一个Entry.DoesNotExist。

> 类似地，如果有多条记录满足get() 的查询条件，Django 也将报错。这种情况将引发MultipleObjectsReturned，它同样是模型类自身的一个属性。


###其他查询方式
大多数情况下，需要从数据库中查找对象时，你会使用all()、 get()、filter() 和exclude()。 然而，这只是冰山一角；查询集 方法的完整列表，请参见查询集API 参考。

##　限制查询集

可以使用Python 的切片语法来限制查询集记录的数目 。它等同于SQL 的LIMIT 和OFFSET 子句。

例如，下面的语句返回前面5 个对象(LIMIT 5)：

    Entry.objects.all()[:5]

下面这条语句返回第6 至第10 个对象(OFFSET 5 LIMIT 5)：

    >>> Entry.objects.all()[5:10]

**不支持负的索引**（例如Entry.objects.all()[-1]）。

通常，查询集 的切片返回一个新的查询集它不会执行查询。有一个例外，是如
果你使用Python 切片语法中`"step"`参数。例如，下面的语句将返回前10 个对象中每隔2个对象，它将真实执行查询：

    >>> Entry.objects.all()[:10:2]

若要获取一个单一的对象而不是一个列表（例如，SELECT foo FROM bar LIMIT 1），可以简单地使用一个索引而不是切片。例如，下面的语句返回数据库中根据标题排序后的第一条Entry：

    >>> Entry.objects.order_by('headline')[0]

它大体等同于：

    >>> Entry.objects.order_by('headline')[0:1].get()

然而请注意，如果没有对象满足给定的条件，第一条语句将引发`IndexError`而第二条语句将引发`DoesNotExist`。 更多细节参见get()。

###　字段查询

字段查询是指如何指定SQL WHERE 子句的内容。它们通过查询集方法`filter()`、`exclude()` 和 `get()` 的关键字参数指定。

查询的关键字参数的基本形式是`field__lookuptype=value`。（中间是两个下划线）。例如：

    >>> Entry.objects.filter(pub_date__lte='2006-01-01')

翻译成SQL（大体）是：

`SELECT * FROM blog_entry WHERE pub_date <= '2006-01-01';`
这是如何实现的

Python 定义的函数可以接收任意的`键/值`对参数，这些名称和参数可以在运行时求值。
更多信息，参见Python 官方文档中的关键字参数。

查询条件中指定的字段必须是模型字段的名称。但有一个例外，对于`ForeignKey`你可以使用`字段名`加上`_id` 后缀。
在这种情况下，该参数的值应该是外键的原始值。例如：

    >>> Entry.objects.filter(blog_id=4)

如果你传递的是一个不合法的参数，查询函数将引发 `TypeError`。

这些数据库API 支持大约二十多种查询的类型；在字段查询参考 中可以找到完整的参考。为了让你尝尝鲜，下面是一些你可能用到的常见查询：

###exact
`“精确”`匹配。例如：

    >>> Entry.objects.get(headline__exact="Man bites dog")

将生成下面的SQL：

`SELECT ... WHERE headline = 'Man bites dog';`
如果你没有提供查询类型 即如果你的关键字参数不包含双下划线. 默认假定查询类型是exact。

例如，下面的两条语句相等：
```
>>> Blog.objects.get(id__exact=14)  # Explicit form
>>> Blog.objects.get(id=14)         # __exact is implied
```
这是为了方便，因为exact 查询是最常见的情况。

### iexact
`大小写不敏感的匹配`。所以，查询：
```
>>> Blog.objects.get(name__iexact="beatles blog")
```
将匹配标题为"Beatles Blog"、"beatles blog" 甚至"BeAtlES blOG" 的Blog。

### contains
大小写敏感的包含关系测试。例如：

`Entry.objects.get(headline__contains='Lennon')`
大体可以翻译成下面的SQL：
`SELECT ... WHERE headline LIKE '%Lennon%';`
注意，这将匹配'`Today Lennon honored`' 但不能匹配'`today lennon honored`'。

还有一个大小写不敏感的版本，
### `icontains`。
### startswith
### endswith
### istartswith
### iendswith

分别表示以XXX开头和以XXX结尾。当然还有大小写不敏感的版本，叫做istartswith 和 iendswith。
同样，这里只是表面。完整的参考可以在字段查询参考中找到。

[查询的api详细](http://python.usyiyi.cn/django/ref/models/querysets.html#queryset-api)

###　跨关联关系的查询
Django提供一种强大而直观的方式来"处理"查询中的关联关系, 他在后台自动帮你处理`join`.若要跨越关联关系,只需要使用关联的模型字段的名称,并使用双下划线分隔,直至你想要的字段:
```
Entry.objects.filter(blog__name='Beats Blog')
```
> 这种跨越可以任意的深度. 它还可以反向工作.若要引用一个`反向`关系,只要使用该模型的小写的名称.


```
Blog.objects.filter(entry__headline__contains='Lennon')
```
如果在多个关联关系直接过滤而且某个中介模型没有满足过滤条件的值,Django将把他作为一个空的(所有的值为NULL)但是合法的对象.

```
Blog.objects.filter(entry__authors__name='Lemon')
```
（如果有一个相关联的Author 模型），如果Entry 中没有找到对应的author，那么它将当作其没有name，而不会因为没有author 引发一个错误。通常，这就是你想要的。唯一可能让你困惑的是当你使用isnull 的时候。因此：

`Blog.objects.filter(entry__authors__name__isnull=True)`
返回的Blog 对象包括author 的name 为空的对象和entry 的author 为空的对象。如果你不需要后者，你可以这样写：
```
Blog.objects.filter(entry__authors__isnull=False,
        entry__authors__name__isnull=True)
```

###跨越多值的关联关系
当你基于ManyToManyField或方向ForeignKey来过滤一个对象时,有两种不同种类的过滤器.考虑`Blog`和`Entry`关联关系(Blog和Entry是一对多关系).可能想找出标题行中包含`Lennon`且在2008年发布的Entry.或者我们可能想找出这个blog,他包含一个标题行具有`Lennon`的Entry和一个在2008发布的Entry.因为实际上有和单Blog相关联的多个Entry,所以这个两个查询在某些场景下都是有可能并有意义的.

ManyToManyField 有类似的情况。例如，如果Entry 有一个ManyToManyField 叫做 tags，我们可能想找到tag 叫做“music” 和“bands” 的Entry，或者我们想找一个tag 名为“music” 且状态为“public”的Entry。

对于这两种情况，Django 有种一致的方法来处理filter() 调用。一个filter() 调用中的所有参数会同时应用以过滤出满足所有要求的记录。接下来的filter() 调用进一步限制对象集，但是对于多值关系，它们应用到与主模型关联的对象，而不是应用到前一个filter() 调用选择出来的对象。

###　或还是且的问题
这些听起来可能有点混乱，所以希望展示一个例子使它变得更清晰。选择headline 包含Lennon 并且发表时间是2008 的所有blog（同一个entry 满足两个条件），我们的代码是：
```
Blog.objects.filter(entry__headline__contains=''Lennon, entry__pub_date__year=2008)
```
选择headline包含`Lemnon`或者发表时间是2008的所有blog:
```
Blog.objects.filter(entry__headline__contains='Lenmon').filter(entry__pub_date__year=2008)
```
假如只有一个blog 对象同时含有两种entry，其中一种headline 包含“Lennon”和另外一种发表时间是2008，但是发表在2008 的entry 没有包含“Lennon” 的。第一个查询不会返回任何blog，第二个查询将会返回一个blog。

在第二个例子中， 第一个filter 限定查询集中的blog 与headline 包含“Lennon” 的entry 关联。第二个filter 进一步 限定查询集中的blog 关联的entry 的发表时间是2008。第二个filter 过滤出来的entry 与第一个filter 过滤出来的entry 可能相同也可能不同。每个filter 语句过滤的是Blog，而不是Entry。

###　注意

跨越多值关系的filter() 查询的行为，与exclude() 实现的不同。单个exclude() 调用中的条件不必引用同一个记录。

例如，下面的查询排除headline 中包含“Lennon”的Entry和在2008 年发布的Entry：
```
Blog.objects.exclude(
    entry__headline__contains='Lennon',
    entry__pub_date__year=2008,
)
```
然而，这与使用filter() 的行为不同，它不是排除同时满足两个条件的Entry。为了实现这点，即选择的Blog中不包含在2008年发布且healine 中带有“Lennon” 的Entry，你需要编写两个查询：
```
Blog.objects.exclude(
    entry=Entry.objects.filter(
        headline__contains='Lennon',
        pub_date__year=2008,
    ),
)
```

### Filter 可以引用模型的字段

到目前为止给出的示例中，我们构造过将模型字段与常量进行比较的filter。但是，如果你想将模型的一个字段与同一个模型的另外一个字段进行比较该怎么办？

Django 提供`F `表达式 来允许这样的比较。`F()` `返回的实例用作查询内部对模型字段的引用`。这些引用可以`用于查询的filter 中来比较相同模型实例上不同字段之间值的比较`。

例如，为了查找`comments 数目`多于`pingbacks` 的Entry，我们将构造一个`F()` 对象来引用`pingback 数目`，并在查询中使用`该F()` 对象：
```
>>> from django.db.models import F
>>> Entry.objects.filter(n_comments__gt=F('n_pingbacks'))
```
Django 支持对F() 对象使用`加法`、`减法`、`乘法`、`除法`、`取模`以及`幂计算`等算术操作，两个`操作数`可以都是`常数`和其它`F() 对象`。为了查找`comments` 数目比`pingbacks `两倍还要多的Entry，我们将查询修改为：
```
>>> Entry.objects.filter(n_comments__gt=F('n_pingbacks') * 2)
```
New in Django 1.7:
`添加 ** 操作符`。

为了查询rating 比pingback 和comment 数目总和要小的Entry，我们将这样查询：
```
>>> Entry.objects.filter(rating__lt=F('n_comments') + F('n_pingbacks'))
```
你还可以在`F() 对象`中使用双下划线标记来跨越关联关系。带有双下划线的F() 对象将引入任何需要的join 操作以访问关联的对象。例如，如要获取author 的名字与blog 名字相同的Entry，我们可以这样查询：
```
>>> Entry.objects.filter(authors__name=F('blog__name'))
```
对于date 和date/time 字段，你可以给它们加上或减去一个timedelta 对象。下面的例子将返回发布超过3天后被修改的所有Entry：
```
>>> from datetime import timedelta
>>> Entry.objects.filter(mod_date__gt=F('pub_date') + timedelta(days=3))
```
F() 对象支持`.bitand()` 和`.bitor()` 两种位操作，例如：
```
>>> F('somefield').bitand(16)
```

### 查询的快捷方式pk
为了方便,Django提供一个查询的快捷方式pk, 表示'primary key'
在Blog 模型示例中，主键是id 字段，所以下面三条语句是等同的：
```
>>> Blog.objects.get(id__exact=14) # Explicit form
>>> Blog.objects.get(id=14) # __exact is implied
>>> Blog.objects.get(pk=14) # pk implies id__exact
```
pk 的使用不仅限于__exact 查询 —— 任何查询类型都可以与pk 结合来完成一个模型上对主键的查询：
```
# Get blogs entries with id 1, 4 and 7
>>> Blog.objects.filter(pk__in=[1,4,7])

# Get all blog entries with id > 14
>>> Blog.objects.filter(pk__gt=14)
```
pk查询在join 中也可以工作。例如，下面三个语句是等同的：
```
>>> Entry.objects.filter(blog__id__exact=3) # Explicit form
>>> Entry.objects.filter(blog__id=3)        # __exact is implied
>>> Entry.objects.filter(blog__pk=3)        # __pk implies __id__exact
```

### 转义LIKE语句中的百分号和下划线
这意味着语句将很直观，不会显得太抽象。例如，要获取包含一个百分号的所有的Entry，只需要像其它任何字符一样使用百分号：
```
>>> Entry.objects.filter(headline__contains='%')
```
Django 会帮你转义；生成的SQL 看上去会是这样：

`SELECT ... WHERE headline LIKE '%\%%';`
对于下划线是同样的道理。百分号和下划线都会透明地帮你处理。


### 缓存和查询集
每个查询集都包含一个缓存来最小化对数据库的访问。理解它是如何工作的将让你编写最高效的代码。

在一个新创建的查询集中，缓存为空。首次对查询集进行求值,同时发生数据库查询 ,Django 将保存查询的结果到查询集的缓存中并返回明确请求的结果（例如，如果正在迭代查询集，则返回下一个结果）。接下来对该查询集 的求值将重用缓存的结果。

要记住这个缓存行为，如果查询集使用不当，它会坑你的。例如，下面的语句创建两个查询集，对它们求值，然后扔掉它们：
```
>>> print([e.headline for e in Entry.objects.all()])
>>> print([e.pub_date for e in Entry.objects.all()])
```
这意味着相同的`数据库查询将执行两次`，显然倍增了你的数据库负载。同时，还有可能两个结果列表并不包含相同的数据库记录，因为在两次请求期间有可能有Entry被添加进来或删除掉。

为了避免这个问题，只需保存查询集并重新使用它：
```
>>> queryset = Entry.objects.all()
>>> print([p.headline for p in queryset]) # Evaluate the query set.
>>> print([p.pub_date for p in queryset]) # Re-use the cache from the evaluation.
```
### 何时查询集不会被缓存
`查询集不会永远缓存它们的结果`。当`只对查询集的部分进行求值时会检查缓存`， 但是如果这个部分不在缓存中，那么接下来查询返回的记录都将不会被缓存。特别地，这意味着使用`切片或索引来限制查询集将不会填充缓存`。

例如，重复获取查询集对象中一个特定的索引将每次都查询数据库：
```
>>> queryset = Entry.objects.all()
>>> print queryset[5] # Queries the database
>>> print queryset[5] # Queries the database again
```
然而，如果已经对全部查询集求值过，则将检查缓存：
```
>>> queryset = Entry.objects.all()
>>> [entry for entry in queryset] # Queries the database
>>> print queryset[5] # Uses cache
>>> print queryset[5] # Uses cache
```
下面是一些其它例子，它们会使得全部的查询集被求值并填充到缓存中：
```
>>> [entry for entry in queryset]
>>> bool(queryset)
>>> entry in queryset
>>> list(queryset)
```
### 注意

简单地打印查询集不会填充缓存。因为`__repr__()` 调用只返回全部查询集的一个切片。
使用`Q` 对象进行复杂的查询

`filter() `等方法中的关键字参数查询都是一起进行`“AND”` 的。 如果你需要执行更复杂的查询（例如OR 语句），你可以使用`Q 对象`。

### Q 对象 (django.db.models.Q) 
对象用于封装一组关键字参数。这些关键字参数就是上文“字段查询” 中所提及的那些。

例如，下面的Q 对象封装一个LIKE 查询：
```
from django.db.models import Q
Q(question__startswith='What')
```
Q 对象可以使用& 和| 操作符组合起来。当一个操作符在两个Q 对象上使用时，它产生一个新的Q 对象。

例如，下面的语句产生一个Q 对象，表示两个"question__startswith" 查询的“OR” ：

Q`(question__startswith='Who') | Q(question__startswith='What')`
它等同于下面的SQL WHERE 子句：

`WHERE question LIKE 'Who%' OR question LIKE 'What%'`
你可以组合& 和|  操作符以及使用括号进行分组来编写任意复杂的Q 对象。同时，Q 对象可以使用~ 操作符取反，这允许组合正常的查询和取反(NOT) 查询：

`Q(question__startswith='Who') | ~Q(pub_date__year=2005)`
每个接受关键字参数的查询函数（例如filter()、exclude()、get()）都可以传递一个或多个Q 对象作为位置（不带名的）参数。如果一个查询函数有多个Q 对象参数，这些参数的逻辑关系为“AND"。例如：
```
Poll.objects.get(
    Q(question__startswith='Who'),
    Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6))
)
```
... 大体上可以翻译成这个SQL：
```
SELECT * from polls WHERE question LIKE 'Who%'
    AND (pub_date = '2005-05-02' OR pub_date = '2005-05-06')
```

#### 查询函数可以混合使用Q 
对象和关键字参数。所有提供给查询函数的参数（关键字参数或Q 对象）都将"AND”在一起。但是，如果出现Q 对象，它必须位于所有关键字参数的前面。例如：
```
Poll.objects.get(
    Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)),
    question__startswith='Who')
```
... 是一个合法的查询，等同于前面的例子；但是：
```
# INVALID QUERY
Poll.objects.get(
    question__startswith='Who',
    Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)))
```
... 是不合法的。

> 另见
Django 单元测试中的OR 查询示例演示了几种Q 的用法。

### 比较对象¶

为了比较两个模型实例，只需要使用标准的Python 比较操作符，即双等于符号：`==`。在后台，它会比较两个模型主键的值。

利用上面的Entry 示例，下面两个语句是等同的：
```
>>> some_entry == other_entry
>>> some_entry.id == other_entry.id
```
如同模型的主键不叫id，也没有问题。比较将始终使用主键，无论它叫什么。例如，如果模型的主键字段叫做name，下面的两条语句是等同的：
```
>>> some_obj == other_obj
>>> some_obj.name == other_obj.name
```
### 删除对象¶

删除方法，为了方便，就取名为`delete()`。这个方法将立即删除对象且没有返回值。例如：

`e.delete()`
你还可以批量删除对象。每个`查询集 都有一个delete()` 方法，它将删除该查询集中的所有成员。

例如，下面的语句删除pub_date 为2005 的所有Entry 对象：

`Entry.objects.filter(pub_date__year=2005).delete()`
记住，这将尽可能地使用纯SQL 执行，所以这个过程中不需要调用每个对象实例的delete()方法。如果你给模型类提供了一个自定义的delete() 方法并希望确保它被调用，你需要手工删除该模型的实例（例如，迭代查询集并调用每个对象的delete()）而不能使用查询集的批量delete() 方法。
### 注意
当Django 删除一个对象时，它默认使用`SQL ON DELETE CASCADE` 约束 —— 换句话讲，`任何有外键指向要删除对象的对象将一起删除`。例如：
```
b = Blog.objects.get(pk=1)
# This will delete the Blog and all of its Entry objects.
b.delete()
```
这种级联的行为可以通过的`ForeignKey 的on_delete 参数`自定义。

> 注意，delete() 是唯一没有在管理器 上暴露出来的查询集方法。这是一个安全机制来防止你意外地请求Entry.objects.delete()，而删除所有 的条目。

如果你确实想删除所有的对象，你必须明确地请求一个完全的查询集：

`Entry.objects.all().delete()`

### 拷贝模型实例

虽然没有内建的方法用于拷贝模型实例，但还是很容易创建一个新的实例并让它的所有字段都拷贝过来。最简单的方法是，只需要将pk 设置为None。利用我们的Blog 示例：
```
blog = Blog(name='My blog', tagline='Blogging is easy')
blog.save() # blog.pk == 1

blog.pk = None
blog.save() # blog.pk == 2
```
如果你用继承，那么会复杂一些。考虑下面Blog 的子类：
```
class ThemeBlog(Blog):
    theme = models.CharField(max_length=200)

django_blog = ThemeBlog(name='Django', tagline='Django is easy', theme='python')
django_blog.save() # django_blog.pk == 3
```
由于继承的工作方式，你必须设置pk 和 id 都为None：
```
django_blog.pk = None
django_blog.id = None
django_blog.save() # django_blog.pk == 4
```
这个过程不会拷贝关联的对象。如果你想拷贝关联关系，你必须编写一些更多的代码。在我们的例子中，Entry 有一个到Author 的多对多字段：
```
entry = Entry.objects.all()[0] # some previous entry
old_authors = entry.authors.all()
entry.pk = None
entry.save()
entry.authors = old_authors # saves new many2many relations
```
### 一次更新多个对象

有时你想为一个查询集中所有对象的某个字段都设置一个特定的值。这时你可以使用update() 方法。例如：
```
# Update all the headlines with pub_date in 2007.
Entry.objects.filter(pub_date__year=2007).update(headline='Everything is the same')
```
你只可以对非关联字段和ForeignKey 字段使用这个方法。若要更新一个非关联字段，只需提供一个新的常数值。若要更新ForeignKey 字段，需设置新的值为你想指向的新的模型实例。例如：
```
>>> b = Blog.objects.get(pk=1)

# Change every Entry so that it belongs to this Blog.
>>> Entry.objects.all().update(blog=b)
```
update() 方法会立即执行并返回查询匹配的行数（如果有些行已经具有新的值，返回的行数可能和被更新的行数不相等）。更新查询集 唯一的限制是它只能访问一个数据库表，也就是模型的主表。你可以根据关联的字段过滤，但是你只能更新模型主表中的列。例如：
```
>>> b = Blog.objects.get(pk=1)

# Update all the headlines belonging to this Blog.
>>> Entry.objects.select_related().filter(blog=b).update(headline='Everything is the same')
```
要注意update() 方法会直接转换成一个SQL 语句。它是一个批量的直接更新操作。它不会运行模型的save() 方法，或者发出pre_save 或 post_save信号（调用save()方法产生）或者查看auto_now 字段选项。如果你想保存查询集中的每个条目并确保每个实例的save() 方法都被调用，你不需要使用任何特殊的函数来处理。只需要迭代它们并调用save()：
```
for item in my_queryset:
    item.save()
```
对update 的调用也可以使用F 表达式 来根据模型中的一个字段更新另外一个字段。这对于在当前值的基础上加上一个值特别有用。例如，增加Blog 中每个Entry 的pingback 个数：
```
>>> Entry.objects.all().update(n_pingbacks=F('n_pingbacks') + 1)
```
然而，与filter 和exclude 子句中的F() 对象不同，在update 中你不可以使用F() 对象引入join —— 你只可以引用正在更新的模型的字段。如果你尝试使用F() 对象引入一个join，将引发一个FieldError：
```
# THIS WILL RAISE A FieldError
>>> Entry.objects.update(headline=F('blog__name'))
```

###关联的对象

当你在一个模型中定义一个关联关系时（例如，ForeignKey、 OneToOneField 或ManyToManyField），该模型的实例将带有一个方便的API 来访问关联的对象。

利用本页顶部的模型，一个Entry 对象e 可以通过blog 属性e.blog 获取关联的Blog 对象。

（在幕后，这个功能是通过Python 的描述器实现的。这应该不会对你有什么真正的影响，但是这里我们指出它以满足你的好奇）。

Django 还会创建API 用于访问关联关系的另一头 —从关联的模型访问定义关联关系的模型。例如，Blog 对象b 可以通过entry_set 属性 b.entry_set.all()访问与它关联的所有Entry 对象。

这一节中的所有示例都将使用本页顶部定义的Blog、 Author 和Entry 模型。

### 一对多关系

#### 前向查询¶
如果一个模型具有ForeignKey，那么该模型的实例将可以通过属性访问关联的（外部）对象。

例如：
```
>>> e = Entry.objects.get(id=2)
>>> e.blog # Returns the related Blog object.
```
你可以通过外键属性获取和设置。和你预期的一样，对外键的修改不会保存到数据库中直至你调用save()。例如：
```
>>> e = Entry.objects.get(id=2)
>>> e.blog = some_blog
>>> e.save()
```
如果ForeignKey 字段有null=True 设置（即它允许NULL 值），你可以分配None 来删除对应的关联性。例如：
```
>>> e = Entry.objects.get(id=2)
>>> e.blog = None
>>> e.save() # "UPDATE blog_entry SET blog_id = NULL ...;"
```
一对多关联关系的前向访问在第一次访问关联的对象时被缓存。以后对同一个对象的外键的访问都使用缓存。例如：
```
>>> e = Entry.objects.get(id=2)
>>> print(e.blog)  # Hits the database to retrieve the associated Blog.
>>> print(e.blog)  # Doesn't hit the database; uses cached version.
```
注意select_related() 查询集方法递归地预填充所有的一对多关系到缓存中。例如：
```
>>> e = Entry.objects.select_related().get(id=2)
>>> print(e.blog)  # Doesn't hit the database; uses cached version.
>>> print(e.blog)  # Doesn't hit the database; uses cached version.
```
### 反向查询
如果模型有一个ForeignKey，那么该ForeignKey 所指的模型实例可以通过一个管理器返回前一个模型的所有实例。默认情况下，这个`管理器`的名字为`foo_set`，其中`foo` 是`源模型的小写名称`。该管理器返回的查询集可以用上一节提到的方式进行过滤和操作。

例如：
```
>>> b = Blog.objects.get(id=1)
>>> b.entry_set.all() # Returns all Entry objects related to Blog.
```
```
# b.entry_set is a Manager that returns QuerySets.
>>> b.entry_set.filter(headline__contains='Lennon')
>>> b.entry_set.count()
```
你可以在ForeignKey 定义时设置related_name 参数来覆盖foo_set 的名称。例如，如果Entry 模型改成blog = ForeignKey(Blog, related_name='entries')，那么上面的示例代码应该改成这样：
```
>>> b = Blog.objects.get(id=1)
>>> b.entries.all() # Returns all Entry objects related to Blog.

# b.entries is a Manager that returns QuerySets.
>>> b.entries.filter(headline__contains='Lennon')
>>> b.entries.count()
```

#### 使用自定义的反向管理器¶
New in Django 1.7.
默认情况下，用于反向关联关系的`RelatedManager` 是该模型默认管理器 的子类。如果你想为一个查询指定一个不同的管理器，你可以使用下面的语法：
```
from django.db import models

class Entry(models.Model):
    #...
    objects = models.Manager()  # Default Manager
    entries = EntryManager()    # Custom Manager

b = Blog.objects.get(id=1)
b.entry_set(manager='entries').all()
```
如果EntryManager 在它的get_queryset() 方法中使用默认的过滤，那么该过滤将适用于all() 调用。

当然，指定一个自定义的管理器还可以让你调用自定义的方法：

`b.entry_set(manager='entries').is_published()`

### 处理关联对象的其它方法¶
除了在上面”获取对象“一节中定义的查询集 方法之外，ForeignKey 管理器 还有其它方法用于处理关联的对象集合。下面是每个方法的大概，完整的细节可以在关联对象参考 中找到。

`add(obj1, obj2, ...)`
添加一指定的模型对象到关联的对象集中。

`create(**kwargs)`
创建一个新的对象，将它保存并放在关联的对象集中。返回新创建的对象。

`remove(obj1, obj2, ...)`
从关联的对象集中删除指定的模型对象。

`clear()`
从关联的对象集中删除所有的对象。
若要一次性给关联的对象集赋值，只需要给它赋值一个可迭代的对象。这个可迭代的对象可以包含对象的实例，或者一个主键值的列表。例如：
```
b = Blog.objects.get(id=1)
b.entry_set = [e1, e2]
```
在这个例子中，e1 和e2 可以是Entry 实例，也可以是主键的整数值。

如果有clear() 方法，那么在将可迭代对象中的成员添加到集合中之前，将从entry_set 中删除所有已经存在的对象。如果没有clear() 方法，那么将直接添加可迭代对象中的成员而不会删除所有已存在的对象。

这一节中提到的每个”反向“操作都会立即对数据库产生作用。每个添加、创建和删除操作都会立即并自动保存到数据库中。

### 多对多关系¶

多对多关系的两端都会自动获得访问另一端的API。这些API 的工作方式与上面提到的“方向”一对多关系一样。

唯一的区别在于属性的名称：定义 ManyToManyField 的模型使用该字段的属性名称，而“反向”模型使用源模型的小写名称加上'_set' （和一对多关系一样）。

一个例子可以让它更好理解：
```
e = Entry.objects.get(id=3)
e.authors.all() # Returns all Author objects for this Entry.
e.authors.count()
e.authors.filter(name__contains='John')

a = Author.objects.get(id=5)
a.entry_set.all() # Returns all Entry objects for this Author.
```
类似ForeignKey，ManyToManyField 可以指定related_name。在上面的例子中，如果Entry 中的ManyToManyField 指定related_name='entries'，那么Author 实例将使用 entries 属性而不是entry_set。

### 一对一关系¶

一对一关系与多对一关系非常相似。如果你在模型中定义一个OneToOneField，该模型的实例将可以通过该模型的一个简单属性访问关联的模型。

例如：
```
class EntryDetail(models.Model):
    entry = models.OneToOneField(Entry)
    details = models.TextField()

ed = EntryDetail.objects.get(id=2)
ed.entry # Returns the related Entry object.
```
在“反向”查询中有所不同。一对一关系中的关联模型同样具有一个管理器对象，但是该管理器表示一个单一的对象而不是对象的集合：
```
e = Entry.objects.get(id=2)
e.entrydetail # returns the related EntryDetail object
```
如果没有对象赋值给这个关联关系，Django 将引发一个DoesNotExist 异常。

实例可以赋值给反向的关联关系，方法和正向的关联关系一样：

`e.entrydetail = ed`

### 反向的关联关系是如何实现的？¶

其它对象关系映射要求你在关联关系的两端都要定义。Django 的开发人员相信这是对DRY（不要重复你自己的代码）原则的违背，所以Django 只要求你在一端定义关联关系。

但是这怎么可能，因为一个模型类不知道哪个模型类与它关联直到其它模型类被加载？

答案在app registry 中。当Django 启动时，它导入INSTALLED_APPS 中列出的每个应用，然后导入每个应用中的models 模块。每创建一个新的模型时，Django 添加反向的关系到所有关联的模型。如果关联的模型还没有导入，Django 将保存关联关系的记录并在最终关联的模型导入时添加这些关联关系。

由于这个原因，你使用的所有模型都定义在INSTALLED_APPS 列出的应用中就显得特别重要。否则，反向的关联关系将不能正确工作。

### 通过关联的对象进行查询¶

在关联对象字段上的查询与正常字段的查询遵循同样的规则。当你指定查询需要匹配的一个值时，你可以使用一个对象实例或者对象的主键的值。

例如，如果你有一个id=5 的Blog 对象b，下面的三个查询将是完全一样的：
```
Entry.objects.filter(blog=b) # Query using object instance
Entry.objects.filter(blog=b.id) # Query using id from instance
Entry.objects.filter(blog=5) # Query using id directly
```

### 回归到原始的 SQL¶

如果你发现需要编写的SQL 查询对于Django 的数据库映射机制太复杂，你可以回归到手工编写SQL。Django 对于编写原始的SQL 查询有多个选项；参见执行原始的SQL 查询。

最后，值得注意的是Django 的数据库层只是数据库的一个接口。你可以利用其它工具、编程语言或数据库框架来访问数据库；对于数据库，Django 没有什么特别的地方




