# flask-sqlalchemy 数据关系
---

##　一对多(one-to-many)关系
最常见的关系, 您可以使用字符串来指代还没有创建的类(例如如果Person定一个到Article的关系,而Article在Person后面才会声明.)

关系使用`relationship()`函数表示.然而外键必须使用类`sqlalchemy.schema.ForeignKey`单独声明:

```python
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    addresses = db.relationship('Address', backrf='person', lazy='dynamic')

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    person_id =db.Column(db.Integer, db.ForeignKey('person.id'))

```

`db.relationship()`做了什么?这个函数返回一个可以做许多事情的新的属性.在本案例中,我们让他指向`Address`类并加载了多个地址.他如何知道会返回不止一个地址呢?因为sqlalchemy从您的声明中猜测了一个游泳的默认值.如果您想要一对一的关系,可以把`ueselist=False`传给`relationship()`.

外键指定`db.relationship('Address', backrf='person', lazy='dynamic')` 这个也可以放在Address里.


那么 `backref`和`lazy`意味着什么?`backref`是一个在`Address`类声明新的属性的简单方法.您可以使用`my_address.person`来获取该地址(address)的人.lazy决定了SLQAlchemy什么时候从数据库中加载数据:
>1. `select`(默认值)就是说Sqlalchemy会使用一个标准的select语句必要时一次加载数据,调用多对多对象时,进行查询.
2. `joined` 告诉Sqlalchemy使用JOIN语句作为父级在同一查询中来加载关系,即查询对象的时候把所关联的多对多对象一次查出来.
3. `subquery` 类似`joined`,但是SQLAlchemy会使用子查询.
4. `dynamic`在有多条数据的时候特别有用.不是直接加载这些数据,Sqlalchemy会返回一个查询对象,在加载数据前您可以过滤(提取)他们.

如何反向引用(backrf)定义惰性(lazy)状态? 使用backrf()函数:
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    address = db.relationship('Address',
                backrf=db.backrf('person', lazy='joined'), lazy='dynamic')

```


###  当两个Model之间有多个外键关联时,需要在relationship中指定forign_keys的关联字段.如下:
当Person有多个地址,公司地址,家庭住址时:

```
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    person_id =db.Column(db.Integer, db.ForeignKey('person.id'))
    company_user_id = db.Column(db.Integer(), db.Foreignkey('person.id'))

    # 明确多个外键的关系
    person = db.relationship("Person", foreign_keys=[person_id])
    company_user = db.relationship("Person", foreign_keys=[company_user_id])

```

## 多对多关系(many-to-many)

如果想要多对多关系,需要定义一个关系的辅助表.对于辅助表,强烈建议不要使用模型,而是采用一个实际的表.

```python
tags = db.Table('tags',
        db.Column('tag_id', db.Integer, db.Foreignkey('tag.id')),
        db.Column('page_id', db.Integer, db.ForeignKey('page.id'))
        )

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tags = db.relationship('Tag', secondary=tags, 
                    backrf=db.backrf('pages', lazy='dynamic'))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
```

这里配置Page.tags加载后作为标签的列表,因为我们并不希望每页出现太多标签,而每个tag的页面列表(Tag.pages)是一个动态的反向引用.正如上面提到的，这意味着您会得到一个可以发起 select 的查询对象。

### 多对多的自引用关系
在Flasky的项目中, 出现关注者和被关注者都是User, 在关联表中,两侧应用过的是同一张表.


在关注中,管理的左侧是用户实体, 可以称之为为'关注者'; 关系的右侧也是用户实体, 但这些是"被关注者". 从概念上来看, 自引用关系和普通引用没有什么区别, 只是不容易理解.下图是自引用的关系数据库图解, 表示用户之间的关注:
如下图
![](../images/user_followers.png)

本例的关联表是follows, 其中每一行都表示一个用户关注了另一个用户.图中左边表示一对多关系把用户和follows表中的一组记录联系起来, 用户是关注者. 图中右边表示的一对多关系把用户和follows表中的一组记录联系起来, 用户是被关注者.

把关联表换成可以访问的模型:
```python
class  Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeginKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeginKey('users.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.ntcnow)    


class User(UserMixin, db.Model):
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')

```
followed和followers关系都定义单独的一对多关系. 注意, 为了消除外键间的歧义, 定义关系时必须使用可选参数`foregin_key`指定外键. 而且`,db.backref()`参数并不是指定这个关系的应用关系,而是回引Follow模型.

回引(backref)中lazy参数指定是`joined`. 这个lazy模式可以实现立即从连接查询中加载相关对象. 例如某个用户关注了100个用户, 调用user.followed.all()后会返回一个列表, 其中包含了100 个Follow实例, 么个实例的follower和followed回引属性都指向相应的用户. 设定lazy为joined可以在一次查询中查询完, 如果lazy 为默认的select的话, 首次访问follwer和followed属性才会加载获取全部被关注的用户时需要增加100次额外的数据库的查询.

这两个关系中，User一侧设定的lazy参数作用不一样。lazy参数都在“一”这一侧设定，返回的结果是“多”这一侧中的记录。上述代码使用的是dynamic，因此关系属性不会直接返回记录，而是返回查询对象，所以在执行查询之前还可以添加额外的过滤器。

`cascade`参数配置在父对象上执行的操作对相关对象的影响. 比如, 层叠选项可以设定为: 将用户添加到数据库会话后, 要自动把所有关系的对象都添加到会话中. 层叠选项的默认值满足大多数需求, 但对于这个多对多关系来说却不合用. 删除对象时, 默认的层叠行为是把对象连接的所有相关对象的外键设置为空值. 但在关联表中, 删除记录后正确的行为应该是把指向该对象的记录的实体删除, 因为这样能有效销毁连接. 这就是层叠选项值为`delete-orphan`的作用.

> cascade参数的值是有一组逗号分割的层叠选项, 这看起来可能让人有点困惑, 但是all表示出了delete-orphan之外的所有层叠选项.设置为 all, delete-orphan的意思就是启用所有默认的层叠选项,而且还要删除孤儿记录.

## 当的使用的Model上有多个外键时, 
当的使用的Model上有多个外键时, sqlalchemy要指定哪个表的哪个键作为主键.否则会报
`AmbiguousForeignKeysError: Could not determine join condition between parent/child tables on relationship`

```

class Group(db.Model):
    __tablename__ = "group"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship(
        "User",
        backref='group',
        lazy='dynamic',
        foreign_keys="User.group_id"
        
    )
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    create_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    remark = db.Column(db.String(512))
    create_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    is_enable = db.Column(db.Boolean, default=True)
    is_del = db.Column(db.Boolean, default=False)


class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    
    login_name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), unique=True)
    QQ = db.Column(db.String(12))
    weixin = db.Column(db.String(64))
    
    password_hash = db.Column(db.String(256))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    avatar = db.Column(db.String(32))
    is_del = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    create_user = db.relationship(
        'Group',
        backref='user',
        lazy='dynamic',
        foreign_keys="HostGroup.create_user_id" # foreign_keys 如果是多个键的组合键时, 使用"[HostGroup.create_user_id,dddd.id]"
    )

    is_enable = db.Column(db.Boolean, default=True)
    remark = db.Column(db.String(512))

#http://docs.sqlalchemy.org/en/latest/orm/join_conditions.html
```
https://www.keakon.net/2012/12/03/SQLAlchemy%E4%BD%BF%E7%94%A8%E7%BB%8F%E9%AA%8C
