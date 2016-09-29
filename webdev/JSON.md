# JSON教程

---

## JSON的介绍

>JSON 文件的文件类型是 ".json"
JSON 文本的 MIME 类型是 "application/json"

***什么是 JSON ？***

JSON 指的是 JavaScript 对象表示法（JavaScript Object Notation）

- JSON 是轻量级的文本数据交换格式
- JSON 独立于语言 *
- JSON 具有自我描述性，更易理解

> JSON 使用 JavaScript 语法来描述数据对象，但是 JSON 仍然独立于语言和平台。JSON 解析器和 JSON 库支持许多不同的编程语言。


**JSON - 转换为 JavaScript 对象**
JSON 文本格式在语法上与创建 JavaScript 对象的代码相同。
由于这种相似性，无需解析器，JavaScript 程序能够使用内建的 `eval()` 函数，用 JSON 数据来生成原生的 JavaScript 对象。


##　JSON和XML的区别

###　类似 XML
* JSON 是纯文本
* JSON 具有“自我描述性”（人类可读）
* JSON 具有层级结构（值中存在值）
* JSON 可通过 JavaScript 进行解析
*　JSON 数据可使用 AJAX 进行传输

###　相比 XML 的不同之处
- 没有结束标签
- 更短
- 读写的速度更快
- 能够使用内建的 JavaScript eval() 方法进行解析
- 使用数组
- 不使用保留字

### 为什么使用 JSON？
对于 AJAX 应用程序来说，JSON 比 XML 更快更易使用：
### 使用 XML
- 读取 XML 文档
- 使用 XML DOM 来循环遍历文档
- 读取值并存储在变量中
### 使用 JSON
- 读取 JSON 字符串
- 用 eval() 处理 JSON 字符串


## JSON的语法格式

JSON语法是Javascript 语法的子集

### JSON语法规则
JSON语法是JavaScript对象表示法语法的子集
- 数据在`名称/值`对中
- 数据由逗号分隔
- 花括号保存对象
- 方括号保存数组

### JSON 名称/值对

```
"firstname": "John"
```


### JSON值

- 数字(整数或浮点数)
- 字符串(在双引号中)
- 逻辑值(true或者false)
- 数组(方括号中)
- 对象(在花括号中)
- null

###JSON对象
对象可以包含多个`名称/值对`:
```
{"firstname":"John", "Lastname":"Doe"}
```

### JSON数组
JSON数组的在方括号中书写:
数组可包含多个对象:
```
{
    "employees":[
        {"firstname":"John", "Lastname":"Doe"},
        {"firstname":"Anna", "Lastname":"Smith"},
        {"firstname":"Peter", "Lastname":"Jones"},

    ]
}

```

## JSON使用JavaScript语法
JSON使用javascript语法,是javascript的子集,无需额外的软件就能处理Javascr的JSON.
```
var employees =     "employees":[
        {"firstname":"John", "Lastname":"Doe"},
        {"firstname":"Anna", "Lastname":"Smith"},
        {"firstname":"Peter", "Lastname":"Jones"},

    ];


# 用js语法
employees[0].Lastname
employees[0].Lastname="Jobs";
```

## 把 JSON 文本转换为 JavaScript 对象

JSON最常见的用法之一，是从 web 服务器上读取JSON数据(作为文件或作为HttpRequest),
将 JSON 数据转换为 JavaScript 对象，然后在网页中使用该数据.
为了更简单地为您讲解，我们使用字符串作为输入进行演示（而不是文件）。

### JSON 实例 - 来自字符串的对象

创建包含 JSON 语法的 JavaScript 字符串：
```
var txt = '{ "employees" : [' +
'{ "firstName":"Bill" , "lastName":"Gates" },' +
'{ "firstName":"George" , "lastName":"Bush" },' +
'{ "firstName":"Thomas" , "lastName":"Carter" } ]}';
```

由于 JSON 语法是 JavaScript 语法的子集，JavaScript 函数 `eval()` 可用于将 JSON 文本转换为 JavaScript 对象。

`eval()` 函数使用的是 JavaScript 编译器，可解析 JSON 文本，然后生成 JavaScript 对象。必须把文本包围在括号中，这样才能避免语法错误：

`var obj = eval ("(" + txt + ")");`

### 在网页中使用 JavaScript 对象：
例子
```
<html>
<body>
<h2>通过 JSON 字符串来创建对象</h3>
<p>
First Name: <span id="fname"></span><br /> 
Last Name: <span id="lname"></span><br /> 
</p> 
<script type="text/javascript">
var txt = '{"employees":[' +
'{"firstName":"Bill","lastName":"Gates" },' +
'{"firstName":"George","lastName":"Bush" },' +
'{"firstName":"Thomas","lastName":"Carter" }]}';

var obj = eval ("(" + txt + ")");

document.getElementById("fname").innerHTML=obj.employees[1].firstName 
document.getElementById("lname").innerHTML=obj.employees[1].lastName 
</script>
</body>
</html>

##
通过 JSON 字符串来创建对象

First Name: George
Last Name: Bush
```

## JQuery处理JSON

### `jQuery.getJSON(url, [data], [callback])`
通过 HTTP GET 请求载入 JSON 数据。
在 jQuery 1.2中，您可以通过使用JSONP形式的回调函数来加载其他网域的JSON数据，如 `"myurl?callback=?"`。jQuery 将自动替换 ? 为正确的函数名，以执行回调函数。 注意：此行以后的代码将在这个回调函数执行前执行。
参数
`url,[data],[callback]String,Map,FunctionV1.0`

`url`:发送请求地址。
`data`:待发送 Key/value 参数。
`callback`:载入成功时回调函数。

### `jQuery.parseJSON(json)`

接受一个JSON字符串，返回解析后的对象。传入一个畸形的JSON字符串会抛出一个异常。比如下面的都是畸形的JSON字符串：
```
{test: 1} （ test 没有包围双引号）
{'test': 1} （使用了单引号而不是双引号）
```
另外，如果你什么都不传入，或者一个空字符串、null或undefined，parseJSON都会返回 null 。


描述:
解析一个JSON字符串
jQuery 代码:
```
var obj = jQuery.parseJSON('{"name":"John"}');
alert( obj.name === "John" );
```

## Python处理JSON

###　使用json模块
`import json`

- `json.dumps()` : 把一个Python对象编码转换成Json字符串
- `json.loads()` : 把Json格式的字符串解码转化成Python对象

```
import json
s = json.loads('{"name":"test", "type":{"name":"seq","paramter":["1","2"]}}')
print s.keys()
d1 = json.dumps(s, sort_keys=True)

```
