# django-rest-framework
---


## 快速入门

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