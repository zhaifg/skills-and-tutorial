<<<<<<< Updated upstream
# django-rest-framework
---


## 快速入门

### 安装配置


### 1.app下创建 serializers.py 的序列化文件
如
Goods
```py
from goods.models import Goods
from rest_framework import serializers

class GoodsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Goods
        fields = ('xxx', 'xxx') # 要序列化的 models的字段
```

### 2.创建views
```py
from django.shortcuts import render
from goods.models import Goods
from rest_framework import viewsets
from goods.serializers import GoodsSerializers

class GoodViewSet(viewsets.ModelViewSet):
    queryset = Goods.objects.all().order_by('-add_time')
    serializer_class = GoodsSerializers


```

### 3.配置urls， 全局的urls
```py
from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls

from rest_framework import routers
from goods import views

router = routers.DefaultRouter()
router.register('goods', views.GoodViewSet)

urlpatterns = [
    url(r'docs/$', include_docs_urls(title="MxShop")),
    url('^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]

```

### 运行， 并测试
=======
# django-rest-framework
---


## 快速入门


### 使用views的 class views 方式
```py
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SnippetDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


```

在urls 中使用as_view() 方式
到目前为止，我们使用的创建/检索/更新/删除操作将与我们创建的任何支持模型的API视图非常相似

###  使用mixins 模式
使用 view 视图模式的可以自由的组合后台行为
我们来看看我们如何使用mixin类编写视图。这是我们的views.py模块。
```py
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import mixins
from rest_framework import generics

class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

```

基类提供了核心功能，而mixin类提供了 `.list()` 和`.create()` 操作。然后，我们明确地将get和post方法绑定到适当的操作。到目前为止足够简单的东西.

很相似再次，我们使用GenericAPIView类来提供核心功能，并在mixins中添加以提供.retrieve()，.update()和.destroy()操作。

`GenericAPIView`:

`ListModelMixin`:

`CreateModelMixin`:


### 使用 generics 基类视图
使用mixin类，我们重写了这些视图，使用的代码比以前少一些，但我们可以进一步。 REST框架提供了一组已经混合的通用视图，我们可以使用它来修剪我们的views.py模块。

```
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
```


## 认证 和 权限




## 关系 && Hyperlinked APIs

















### 1.app下创建 serializers.py 的序列化文件
如
Goods
```py
from goods.models import Goods
from rest_framework import serializers

class GoodsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Goods
        fields = ('xxx', 'xxx') # 要序列化的 models的字段
```

### 2.创建views
```py
from django.shortcuts import render
from goods.models import Goods
from rest_framework import viewsets
from goods.serializers import GoodsSerializers

class GoodViewSet(viewsets.ModelViewSet):
    queryset = Goods.objects.all().order_by('-add_time')
    serializer_class = GoodsSerializers


```

### 3.配置urls， 全局的urls
```py
from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls

from rest_framework import routers
from goods import views

router = routers.DefaultRouter()
router.register('goods', views.GoodViewSet)

urlpatterns = [
    url(r'docs/$', include_docs_urls(title="MxShop")),
    url('^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]

```
>>>>>>> Stashed changes
