# Serializers


## 序列化

序列化 允许把复杂的数据 如queryset 或者model 实例转换成 python
的数据结构, 然后可以简单的转换为 Json xml 等形式.
序列化的语法 类似于 Form 和 ModelForm

### 定义序列化

```
from datetime import datetime

class Comment(object):
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()

comment = Comment(email='leila@example.com', content='foo bar')
```




```py

from rest_framework import serializers

class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```

# 类似于Form 通过 serializers.Field 自定义 Field
# 获取数据
```
serializer = CommentSerializer(**args)
serializer.data
```
#JSON 格式化
```
from rest_framework.renders import JSONRender
json = JSONRender().render(serializer.data)
```
# 反序列化 对象
```
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
stream = BytesIO(json)
data = JSONParser().parse(stream)
```

**验证 serialzier 对象**
```
serializer = CommentSerializer(data=data)
serializer.is_valid()
# True
serializer.validated_data
```

**新建,更新,保存 一个实例** 
```
class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

    def  create(self, validaate_data):
        return Commnet(**valiadated_data)
        # or return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        
        #        instance.save() serializer.save()
        return instance

# serializer.save(owner=request.user)

    # 可以定义save 方法
    def save(self):
        pass

```

#### **serializer 的验证**
```
serializer.is_valid()
# False
serializer.errors
# # {'email': [u'Enter a valid e-mail address.'], 'created': [u'This field is required.']} 
```
每一个 key 都是 字段名称, values 是 一个列表.
 non_field_errors键也可能存在,并将列出任何验证错误。non_field_errors键的名称可以自定义使用NON_FIELD_ERRORS_KEY REST框架设置。

**validate 不通过是 可以 raise 一个异常**
```python
serializer.is_validate(raise_exception=True)

```
会触发一个 serializers.ValidationError 异常, 这个会自动处理 请求 为400

**字段的验证**
自定义字段的验证方式类似于 form 的field 使用`.validate_<filed_name>`. 使用`.clean_<field_name>` 来定义验证方式.

```py
from rest_framework import serializers

class BlogPostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField()

    def validate_title(self, value):
        """
        Check that the blog post is about Django.
        """
        if 'django' not in value.lower():
            raise serializers.ValidationError("Blog post is not about Django")
        return value
```

**实例级别的验证**
可以使用`.validate()` 方法验证 实例的所有字段的, 这个方法只有只接受一个保存了所有字段值的字典作为参数, 可以触发 `ValidationError`, 但是仅仅返回验证的 字段
```py
from rest_framework import serializers

class EventSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=100)
    start = serializers.DateTimeField()
    finish = serializers.DateTimeField()

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data['start'] > data['finish']:
            raise serializers.ValidationError("finish must occur after start")
        return data
```

**声明serilizer 时, 指定自定义验证**

```py
def  multiple_of_ten(value):
if value % 10 != 0:
    raise serializers.ValidationError('Not a multiple of ten')

class GameRecord(serializer.Serializer):
    socore = serilizer.IntegerField(validators=[multiple_of_ten])

```


Serilizer 类也支持重用的 验证器, 使用方式是在类中的子类Meta中
```py
class EventSerializer(serilizer.Serializer):
    name = serializers.CharField()
    room_number = serializers.IntegerField(choices=[101, 102, 103, 201])
    date = serializers.DateField()

    class Meta:
        validators = UniqueTogetherValidator(
            queryset = Event.object.all(),
            fields = ['room_number', 'date']
            )
```



### 部分更新
默认情况下, serializer 必须传递所有的必须字段, 否则serializer 验证不通过, 但是可以使用 partial 参数来更新
```py

serializer = CommentSerializer(commment,  data={'content': u'foo bar'}, partial=True)
```


### 处理嵌套对象

前面的例子很好处理对象,只有简单的数据类型,但有时我们也需要能够代表更复杂的对象,对象的一些属性的可能不是简单的数据类型,如字符串、日期或整数。

Serializer类本身是一个类型是一个Field,并且可以用来代表的关系,一个对象类型是嵌套在另一个。

```py

class UserSerilizer(serilzer.Serializer):
    email = serializers.EmailField()
    username = serialziers.CharField(max_length=100)

class CommentSerializer(serializer.Serilizser):
    user = UserSerializer()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

```

如果一个嵌套对象是可选, 可以接受None 值, 这是 可以使用 嵌套 字段上required=False, `user = UserSerializer(required=False) `

```
class CommentSerializer(serializers.Serializer):
    user = UserSerializer(required=False)  # May be an anonymous user.
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```

类似的如果一个嵌套可以使用列表来表示所有的对象, 这时 可以在字段上 使用many=True.

```
class CommentSerializer(serializers.Serializer):
    user = UserSerializer(required=False)
    edits = EditItemSerializer(many=True)  # A nested list of 'edit' items.
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```

### 处理嵌套对象的写
处理嵌套的对象写操作时, 验证出现错误, errors 信息也是嵌套的.
```py
serializer = CommentSerializer(data={'user': {'email': 'foobar', 'username': 'doe'}, 'content': 'baz'})
serializer.is_valid()
# False
serializer.errors
# {'user': {'email': [u'Enter a valid e-mail address.']}, 'created': [u'This field is required.']}
```

类似的, `.validated_data()` 也可以处理嵌套对象.

#### 使用 `.create()` 方法处理 嵌套对象
如果支持写嵌套对象时, 我们使用 `create()` 和 `update()` 处理多个嵌套的对象.
```py
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'email', 'profile')

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user
```

####  使用`.update()` 方法处理 嵌套对象
更新的时候需要仔细的思考怎么更新嵌套对象的之间的关系. 比如 relationship 是 None, 或者没有提供 值, 会发生如下情况:
1. 对象之间关系设置为 NULL, models
2. 删除相关的实例
3. 忽略了数据和离开的实例。
4. 触发一个验证错误?

```py

def update(self, instance, validated_data):
    profile_data = validated_data.pop('profile')

    profile = instance.profile

    instance.username = validated_data.get('username', instance.username)
    instance.email = validated_data.get('email', instance.email)
    instance.save()

    profile.is_premium_member = profile_data.get('is_premium_member', profile.is_premium_member)

    profile.has_support_contract = profile_data.get(
            'has_support_contract',
            profile.has_support_contract
         )

    profile.save()

    return instance

```

因为嵌套的创建和更新的行为是不确定的, 而且可能需要复杂的的相关模型之间的依赖关系,  DRF 3.1 以后需要明确的书写关系. 没人的情况下 ModelSerializer 的 `.create()` 与 `.update()` 方法不支持嵌套的关系.

可能是第三方包,提供自动支持某些自动可写的嵌套表示可能会在3.1版本发布。

#### 使用 模型的 manger 类处理保存相关实例
另一种保存多个相关实例序列化器是编写自定义模型管理员处理创建正确的实例的类。

假如, 如uguowomen希望确保 User 实例和Profile 实例 总是一起创建, 我们写一个定制的 manager 类. 如下:

```py
class  UserManager(models.Manager):
    ...


    def create(self, username, email, is_premium_member=False, has_support_contract=False):
        user = User(username=username, email=email)
        user.save()
        profile =  Profile(
            user=user,
            is_premium_member=is_premium_member,
            has_support_contract=has_support_contract
        )

        profile.save()
        return user
```

此 mananger 类现在更很好地封装了用户实例总是创建和配置实例在同一时间.
我们序列化类可以重写这个 create()方法
```py
def create(self, validated_data):
    return User.objects.create(
        username=validated_data['username'],
        email=validated_data['email']
        is_premium_member=validated_data['profile']['is_premium_member']
        has_support_contract=validated_data['profile']['has_support_contract']
    )

```

### 处理多个对象

Serializer 类也可以 处理多个存放在list中对象.

#### 序列化多个对象
序列化 queryset  或者 list 等的多个对象, 可以在实例化过程中传入 `many=True` 标志.
```py

queryset = Book.ojects.all()
serialzier = BookSerializer(many=True)
serilizer.data
```

#### 反序列化多个对象
反序列化多个对象的默认行为是支持多个对象创建,但不支持多个对象的更新. 

有关如何支持的更多信息或定制这两种情况下,参见下面ListSerializer文档

### 额外的上下文
有些情况下,你需要提供额外的上下文的序列化器除了被序列化的对象外。一个常见的情况是,如果您正在使用一个序列化器,包括超链接关系,这需要序列化器可以访问当前请求,让它能够正确地生成完全限定url。

您可以提供任意附加上下文通过context参数实例化时序列化器。例如:
```py
serilizser = AccountSerializer(account, context={'request':request})
seriaizer.data
```

## ModelSerializer
通常你需要序列化器类紧密地映射到Django模型定义。ModelSerializer类提供了一个快捷方式,可以自动创建一个 Serializer 类字段,字段对应模型。


ModelSerializer类是一样的一个常规的Serializer 类,除了:
* 它会自动为你生成一组字段,根据模型。
* 它会自动生成序列化器的验证器,如unique_together验证器。
* 它包括简单的默认实现.create()和.update()。


```py
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'account_name', 'users', 'created')
```

任何外键等的关系模型将映射到PrimaryKeyRelatedField。

反向关系并不包含在默认情况下,除非显式地包含在文档中指定序列化器关系。

### 检查ModelSerializer

```py
>>> from myapp.serializers import AccountSerializer
>>> serializer = AccountSerializer()
>>> print(repr(serializer))
AccountSerializer():
    id = IntegerField(label='ID', read_only=True)
    name = CharField(allow_blank=True, max_length=100, required=False)
    owner = PrimaryKeyRelatedField(queryset=User.objects.all())

```

### 指定包括哪些字段

* fields
* exclude
* depth: 指定嵌套的深度

#### 明确的指定字段

```
class AccountSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    groups = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = Account
```

### 指定只读字段
您可能希望指定多个字段为只读。而不是显式地添加每个字段与read_only = True属性,你可以使用快捷键元选项,read_only_fields。

```py
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'account_name', 'users', 'created')
        read_only_fields = ('account_name',)

```

模型字段editable= False设置,默认和AutoField字段将被设置为只读,并且不需要添加到read_only_fields选项。
> 有特殊情况的,一个只读字段unique_together约束模型级别的一部分。在这种情况下所需的字段序列化器类为了验证约束,但也应该不是由用户可编辑。正确的方式来处理这是显式地指定字段序列化器,提供read_only = True和默认=…关键字参数
> 这方面的一个例子是一个只读与当前身份验证的用户是unique_together与另一个标识符。在这种情况下,你将宣布用户字段一样:
> `user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())`


### 额外的关键字参数
还有一个快捷方式允许您指定任意额外关键字参数字段,使用extra_kwargs选项。read_only_fields而言,这意味着您不需要显式地声明上的字段序列化器。
```py

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
```


### 关系领域
当序列化模型实例,有许多不同的方式你可以选择代表的关系。的默认表示ModelSerializer是使用主键相关的实例。

包括替代表示序列化使用超链接,序列化完整的嵌套表示,或用一个自定义序列化的表示。详情参见文档的序列化器关系。

### 自定义字段映射
