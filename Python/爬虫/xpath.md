# xpath 的教程
---

xpath  路径表达式


节点

选取节点

nodeName : 选取此节点的所有节点
/ : 从根节点选取
// : 从匹配选择的当前节点选择文档中的节点, 而不考虑它们的位置
. : 选取当前节点
.. : 选取当前节点
@ 选取属性

### 实例
```xml
<?xml version="1.0" encoding="ISO-8859-1"?>

<bookstore>

<book>
  <title lang="eng">Harry Potter</title>
  <price>29.99</price>
</book>

<book>
  <title lang="eng">Learning XML</title>
  <price>39.95</price>
</book>

</bookstore>
```

1. `backstore`: 选取bookstore 元素的所有节点
2. `/backstore`  选取根元素 bookstore. 
3. `backstore/book`: 选取 bookstore 的子元素的所有 book 元素
4. //book 选取所有 book 子元素, 而不管他们在文档中的位置
5. `bookstore//book`: 选择属于bookstore 元素的后代的所有 book 元素, 而不管他们位于 bookstore 之下的什么位置
6. `//@lang`: 选取名为 lang 的所有属性

###  谓语
谓语用来查找某个特定的节点或者包含某个指定值的节点
谓语被嵌在方括号中

实例 带有谓语的 路径表达式

`/bookstore/book[1]`:  选取属于 bookstore 子元素的第一个book 元素
`/bookstore/book[last()]`:
`/bookstore/book[last()-1]`:
`/bookstore/book[position() < 3]`
`//title[@lang]`:
`//title[@lang='eng']`
`/bookstore/book[price>34.00]`
`/bookstore/book[price>35.00]/title`

### 选取未知节点

`*`: 匹配任何元素节点
`@*`: 匹配任何属性节点
`node()`: 匹配任何类型节点

`/bookstore/*`: 选取 bookstore 元素的所有子元素
`//*`: 选取文档中所有元素
`//title[@*]`: 选取所有带有属性的title元素

### 选取若干路径
通过在路径表达式中使用 "|" 运算符, 您可以选取若干个路径.

`//bookt/title | //book/price`: 选取book元素的所有的title 和 price 元素
`//title | //price` : 选取文档中的所有的 title 和 price 元素
`/bookstore/book/title | //price` 选取属于 bookstore 元素的 book 元素的所有 title 元素，以及文档中所有的 price 元素。

### XPath 轴
轴可定义相对于当前节点的节点集

`ancestor`: 选取当前节点的所有先辈(父, 祖父等).
`ancestor-or-self`: 选取当前节点的所有先辈节点以及当前节点自身
`attribute`: 选取当前节点的所有属性
`child`: 选取当前节点的所有子元素.
`descendant`: 选取当前节点的所有后代元素(子, 孙等).
`descendant-or-self`: 选取当前节点的所有后代元素(子, 孙) 以及 自己
`following`: 选取文档中当前节点的结束标签之后的所有节点
`namespace`: 选取当前节点的所有命名空间节点
`parent`: 选取当前节点的父节点
`preceding`: 选取文档中当前节点的开始标签之前的所有节点
`preceding-sibling`: 选取当前节点之前的所有同级节点
`self`:


### 位置路径表达式
位置路径可以是绝对的, 也可以是相对的

`/step/step/...`
`step/step`
每一步均根据当前节点集之中的节点来进行计算

**步 Step 包括**

步的语法:
`轴名称::节点测试[谓语]`

`child::book`: 选取所有属于当前节点的子元素的book 节点. 
`attribute::lang`: 选取当前节点的lang 属性
`child::*`: 选取当前节点的所有子元素
`attribute::*` 选取当前节点的所有属性
`child::text()`: 选取当前节点的所有文本子节点
`child::node()`: 选取当前节点的所有子节点
`descendant::book`: 选取当前节点的所有book 后代
`ancerstor::book`: 选取当前节点的所有book 先辈节点
`ancestor-or-sel::book`: 选取当前节点的素有book先辈以及当前节点(如果此节点是book节点)
`child::*/child::price`: 选取当前节点的所有price孙节点


### XPath 运算符

``
