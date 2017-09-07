# xml处理

##　xml.etree.ElementTree
> 生成和解析xml文档
>\>python 2.5

已解析的XML文档在内存中由ElementTree和Element对象表示.
用parse() 解析一个完整文档时,会放回一个ElementTree实例.这个树了解输入文档中的所有数据,另外可以原地搜索或操纵树中的节点.

> 基于内存加载全部文档.


`a.xml`
```
<?xml version="1.0" encoding="UTF-8"?>
<framework>
  <processers>
    <processer name="AProcesser" file="lib64/A.so" path="/tmp"/>
    <processer name="BProcesser" file="lib64/B.so" value="fordelete"/>
    <processer name="BProcesser" file="lib64/B.so2222222"/>
    <services>
      <service name="search" prefix="/bin/search?" output_formatter="OutPutFormatter:service_inc">
        <chain sequency="chain1"/>
        <chain sequency="chain2"/>
      </service>
      <service name="update" prefix="/bin/update?">
        <chain sequency="chain3" value="fordelete"/>
      </service>
    </services>
  </processers>
</framework>
```

读取整个xml
```
from xml.etree. import ElementTree

with open('a.xml','rt') as f:
    tree = ElementTree.parse(f)

print tree

```

```
<closed file 'a.xml', mode 'rt' at 0x022ED230>
```

### 遍历解析树



### 解析时监视事件


###　创建一个定制树构造器


###  用元素节点构造文档

### 美观打印xml

### 设置元素属性
