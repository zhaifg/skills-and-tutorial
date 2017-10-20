

### 默认参数
在JavaScript中，函数参数的默认值是undefined。然而，在某些情况下设置不同的默认值是有用的。这时默认参数可以提供帮助。

在过去，用于设定默认的一般策略是在函数的主体测试参数值是否为undefined，如果是则赋予一个值。如果在下面的例子中，调用函数时没有实参传递给b，那么它的值就是undefined，于是计算a*b得到、函数返回的是 NaN
```js
b = typeof b !== 'undefined' ?  b : 1; //设置参数的默认值
```

```js
typeof 123; // 'number'
typeof NaN; // 'number'
typeof 'str'; // 'string'
typeof true; // 'boolean'
typeof undefined; // 'undefined'
typeof Math.abs; // 'function'
typeof null; // 'object'
typeof []; // 'object'
typeof {}; // 'object'
```


<script type="text/javascript">
  document.write("I love JavaScript！"); //内容用""括起来，""里的内容直接输出。
</script>


### JavaScript类型转换
typeof: 适合基本类型或者以及function检测, 遇到null失效

`[[class]]`: 通过{}.tostring拿到, 适合内置对象和基本元类, 遇到null和undefined失效(IE678等返回[object Object])

instanceof: 适合自定义对象, 也可以用来检测原生的对象, 在不同iframe和window间检测时失效.


confirm 消息对话框通常用于允许用户做选择的动作，如：“你对吗？”等。弹出对话框(包括一个确定按钮和一个取消按钮)。

语法:

confirm(str);
参数说明:

str：在消息对话框中要显示的文本
返回值: Boolean值
返回值:

当用户点击"确定"按钮时，返回true
当用户点击"取消"按钮时，返回false
注: 通过返回值可以判断用户点击了什么按钮

看下面的代码:

<script type="text/javascript">
    var mymessage=confirm("你喜欢JavaScript吗?");
    if(mymessage==true)
    {   document.write("很好,加油!");   }
    else
    {  document.write("JS功能强大，要学习噢!");   }
</script>



prompt弹出消息对话框,通常用于询问一些需要与用户交互的信息。弹出消息对话框（包含一个确定按钮、取消按钮与一个文本输入框）。

语法:

prompt(str1, str2);
参数说明：

str1: 要显示在消息对话框中的文本，不可修改
str2：文本框中的内容，可以修改
返回值:

1. 点击确定按钮，文本框中的内容将作为函数返回值
2. 点击取消按钮，将返回null
看看下面代码:

var myname=prompt("请输入你的姓名:");
if(myname!=null)
  {   alert("你好"+myname); }
else
  {  alert("你好 my friend.");  }



  open() 方法可以查找一个已经存在或者新建的浏览器窗口。

语法：

window.open([URL], [窗口名称], [参数字符串])
参数说明:

URL：可选参数，在窗口中要显示网页的网址或路径。如果省略这个参数，或者它的值是空字符串，那么窗口就不显示任何文档。
窗口名称：可选参数，被打开窗口的名称。
    1.该名称由字母、数字和下划线字符组成。
    2."_top"、"_blank"、"_selft"具有特殊意义的名称。
       _blank：在新窗口显示目标网页
       _self：在当前窗口显示目标网页
       _top：框架网页中在上部窗口中显示目标网页
    3.相同 name 的窗口只能创建一个，要想创建多个窗口则 name 不能相同。
    4.name 不能包含有空格。
参数字符串：可选参数，设置窗口参数，各参数用逗号隔开。
参数表:



例如:打开http://www.imooc.com网站，大小为300px * 200px，无菜单，无工具栏，无状态栏，有滚动条窗口：

<script type="text/javascript"> window.open('http://www.imooc.com','_blank','width=300,height=200,menubar=no,toolbar=no, status=no,scrollbars=yes')
</script>
注意：运行结果考虑浏览器兼容问题。



HTML文档可以说由节点构成的集合，三种常见的DOM节点:

1. 元素节点：上图中<html>、<body>、<p>等都是元素节点，即标签。

2. 文本节点:向用户展示的内容，如<li>...</li>中的JavaScript、DOM、CSS等文本。

3. 属性节点:元素属性，如<a>标签的链接属性href="http://www.imooc.com"。


学过HTML/CSS样式，都知道，网页由标签将信息组织起来，而标签的id属性值是唯一的，就像是每人有一个身份证号一样，只要通过身份证号就可以找到相对应的人。那么在网页中，我们通过id先找到标签，然后进行操作。

语法:

 document.getElementById(“id”) 

 innerHTML 属性用于获取或替换 HTML 元素的内容。

语法:

Object.innerHTML
注意:

1.Object是获取的元素对象，如通过document.getElementById("ID")获取的元素。

2.注意书写，innerHTML区分大小写。

<!DOCTYPE HTML>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>innerHTML</title>
</head>
<body>
<h2 id="con">javascript</H2>
<p> JavaScript是一种基于对象、事件驱动的简单脚本语言，嵌入在HTML文档中，由浏览器负责解释和执行，在网页上产生动态的显示效果并实现与用户交互功能。</p>
<script type="text/javascript">
  var mychar= document.getElementById("con")          ;
  document.write("原标题:"+mychar.innerHTML+"<br>"); //输出原h2标签内容
  mychar.innerHTML = "Hello World!"
  document.write("修改后的标题:"+mychar.innerHTML); //输出修改后h2标签内容
</script>
</body>
</html>

HTML DOM 允许 JavaScript 改变 HTML 元素的样式。如何改变 HTML 元素的样式呢？

语法:

Object.style.property=new style;
注意:Object是获取的元素对象，如通过document.getElementById("id")获取的元素。

基本属性表（property）:



注意:该表只是一小部分CSS样式属性，其它样式也可以通过该方法设置和修改。

看看下面的代码:

改变 <p> 元素的样式，将颜色改为红色，字号改为20,背景颜色改为蓝：

<p id="pcon">Hello World!</p>
<script>
   var mychar = document.getElementById("pcon");
   mychar.style.color="red";
   mychar.style.fontSize="20";
   mychar.style.backgroundColor ="blue";
</script>

显示和隐藏（display属性）
网页中经常会看到显示和隐藏的效果，可通过display属性来设置。

语法：

Object.style.display = value
注意:Object是获取的元素对象，如通过document.getElementById("id")获取的元素。


className 属性设置或返回元素的class 属性。

语法：

object.className = classname
作用:

1.获取元素的class 属性

2. 为网页内的某个元素指定一个css样式来更改该元素的外观


<!DOCTYPE HTML>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<title>className属性</title>
<style>
    body{ font-size:16px;}
    .one{
        border:1px solid #eee;
        width:230px;
        height:50px;
        background:#ccc;
        color:red;
    }
    .two{
        border:1px solid #ccc;
        width:230px;
        height:50px;
        background:#9CF;
        color:blue;
    }
    </style>
</head>
<body>
    <p id="p1" > JavaScript使网页显示动态效果并实现与用户交互功能。</p>
    <input type="button" value="添加样式" onclick="add()"/>
    <p id="p2" class="one">JavaScript使网页显示动态效果并实现与用户交互功能。</p>
    <input type="button" value="更改外观" onclick="modify()"/>

    <script type="text/javascript">
       function add(){
          var p1 = document.getElementById("p1");
          p1.className="one";
       }
       function modify(){
          var p2 = document.getElementById("p2");
          p2.className="two";
       }
    </script>
</body>
</html>


小伙伴们，请编写"改变颜色"、"改变宽高"、"隐藏内容"、"显示内容"、"取消设置"的函数，点击相应按钮执行相应操作，点击"取消设置"按钮后，提示是否取消设置，如是执行操作，否则不做操作。

<!DOCTYPE HTML>
<html>
<head>
<meta http-equiv="Content-Type" Content="text/html; charset=utf-8" />
<title>javascript</title>
<style type="text/css">
body{font-size:12px;}
#txt{
    height:400px;
    width:600px;
    border:#333 solid 1px;
    padding:5px;}
p{
    line-height:18px;
    text-indent:2em;}
</style>
</head>
<body>
  <h2 id="con">JavaScript课程</H2>
  <div id="txt"> 
     <h5>JavaScript为网页添加动态效果并实现与用户交互的功能。</h5>
        <p>1. JavaScript入门篇，让不懂JS的你，快速了解JS。</p>
        <p>2. JavaScript进阶篇，让你掌握JS的基础语法、函数、数组、事件、内置对象、BOM浏览器、DOM操作。</p>
        <p>3. 学完以上两门基础课后，在深入学习JavaScript的变量作用域、事件、对象、运动、cookie、正则表达式、ajax等课程。</p>
  </div>
  <form>
  <!--当点击相应按钮，执行相应操作，为按钮添加相应事件-->
    <input type="button" value="改变颜色" onclick="chgecolor()" >  
    <input type="button" value="改变宽高" onclick="chagewidth()">
    <input type="button" value="隐藏内容" onclick="chagehide()">
    <input type="button" value="显示内容" onclick="chageshow()">
    <input type="button" value="取消设置" onclick="cancel()">
  </form>
  <script type="text/javascript">
//定义"改变颜色"的函数
function chgecolor()
{
    var mychar = document.getElementById("txt")
    mychar.style.color = 'red';
    mychar.style.backgroundColor='blue';
}

//定义"改变宽高"的函数
function chagewidth()
{
   var mychar = document.getElementById("txt")
   mychar.style.width='200px';
   mychar.style.height='300px';
}

//定义"隐藏内容"的函数
function chagehide()
{
   var mychar = document.getElementById("txt")
   mychar.style.display="none";
}

//定义"显示内容"的函数
function chageshow()
{
    var mychar = document.getElementById("txt")
    mychar.style.display="block"
}

//定义"取消设置"的函数
function cancel()
{
    var mychar = document.getElementById("txt")
    con = confirm("是否取消设置?")
    if(con == true)
    {
       mychar.style.color = '';
       mychar.style.backgroundColor='';  
       mychar.style.display="block"
       mychar.style.width='600px';
       mychar.style.height='400px';
    }
    else
    {
        
    }
}


  </script>
</body>
</html>
