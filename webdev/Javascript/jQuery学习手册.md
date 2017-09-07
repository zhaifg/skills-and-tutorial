# jQuery学习手册
---

jQuery的核心方法`$()`:
```
$(function(){});
# 也可以写成
jQuery(function(){})
```

1. jQuery(): 方法返回一个空 jQuery对象. 在jQuery 1.4之前, 该方法返回一个包含Document节点的对象.
2. jQuery(elements): 是想将一个或多个DOM元素转换为jQuery对象或者集合.
3. jQuery(callback): 该方法等价于jQuery(document).ready(callback);
  主要用来实现绑定在DOM文档载入完成后执行的方法.
4. jQuery(expression,[context]): 该方法接收一个包含jQuery选择器的字符串,  
   在具体执行时, 会使用出入字符串去匹配一个或者多个元素.
5. jQuery(html): 该方法具体执行时, 会根据传入的html标签代码, 动态的创建
   由jQuery对象封装的DOM元素.
6. jQuery(html, props): 该方法具体执行时, 不仅会根据传入的html标签代码, 
  动态的创建由jQuery对象封装的DOM元素, 而且还会设置DOM元素的属性.
7. jQuery(html,[ownerDocument]): 该方法在具体执行时,不仅会根据传入
   的html标签代码,动态的创建由jQuery对象封装的DOM元素, 而且还会指定该DOM元素的所在的文档.

## 延迟加载
```
$(function(){}) 执行多次
== window.onload = function() # 执行一次
```

## jQuery对象和DOM对象的转换
- 1) jQuery对象转换成DOM对象
  jQuery对象时特殊的数组对象,即使只有一个元素, jQuery对象仍然是一个数组.
```
var  $cr = $("#div1"); // 获取jquery对象$cr
var cr = $cr[0]  // 将jquery对象$cr 转换成dom对象.
或者为
var cr = $cr.get(0)
```

- 2) 将dom对象转换成jQuery对象-->$(dom)
```
var cr = document.getElementById('div3')
var $cr = $(cr)
```

## jQuery选择器

### 基本选择器
包括:  
1. id 选择器,根据元素的id选择 : $("#divid")
2. 标签选择器, 根据元素的标签名称选择, $("a")
3. css的样式选择器, 更具应用到DOM的css类进行选择, $(".red")
4. 通配符选择器: select01, select02... $(*), $("#divid, a, .red")

5. 使用选择器组合, 通过使用多个选择器组合, 可以同时更改选中的标签的样式或内容.
  $("#div1, #span2").css('','') 可以设置不同两个元素


### 层次选择器
- 1. 后代选择:
 使用 "form input"的形式选中form中的所有的input元素,
 $(".bgRed div")  类为bgRed元素中的所有div

- 2, 父子选择器: parent->child
  选择parent的直接子节点child. child必须是包含在parent中并且父类是parent元素.
  $(".myList>li"), CSS类为myList元素中的直接子节点的<li>对象

- 3, prev + next: prev和next是连个同级的元素, 选中在prev元素后面的所有元素next元素. $("#hibscus+img")选择id为hibiscus元素后面的所有的img对象. 相邻还可以$("#id_li").next()

- 4, prev ~ sibings, 平级选择器: 选择prev后面的根据sibling过滤的元素, `sibling`是过滤器.   $("#someDiv~[title]") 选择id为someDiv的后面的所有带有title属性的元素



### 过滤选择器
过滤选择器以"冒号"开头, 过滤选择器根据其过滤规则的种类, 

#### 基本过滤选择器
1. :first, 匹配第一个元素; 表格第一行:$("tr:first")
2. :last, 最后一个元素,
3. :not(selector), 去掉所有与给定选择器匹配的元素. 
   查找所有未选中的input元素: $(input:not(checked))
4. :odd, 匹配索引值为奇数的元素,从0开始计算, $("tr:odd")
5. :even, 匹配索引值为偶数的元素
6. :eq(index), 匹配一个给定索引值的元素, index从0开始.
7. :gt(index),
8. :lt(index),
9. :header, 选择所有的h1,h2,h3一类的header标签. 
  给所有的header添加背景$(":header).css("backgroud", "#EEE")
10. animated, 匹配所有的正在执行动画效果的元素
  只有对不在执行动画效果的元素执行一个动画特效
  $("#run").click(function(){
     $("div:not(animated).animate({left: +=20}, 1000)")
  })

#### 内容过滤选择器
1. :contains(text), 匹配包含给定字符文本的元素.
  查找所有包含"John"的div元素 $("div:contains('John')")
2. :empty, 匹配所有不包含子元素或文本的空元素. $("td:empty")
3. :has(selector), 匹配含有选择器所匹配的元素的元素.
  给素有包含p元素的div添加一个text类: $("div:has(p)").addClass('test')
4. :parent, 匹配所有含有子元素或者文本的元素.
  查找所有含有子元素或者文本的td元素:$("td:parent")


#### 可见性过滤选择器
1. :hidden, 所有的不可见的元素: css:display=none, type=hidden, width,height=0, 继承隐藏的
2. :visible, 匹配所有的可见元素

#### 属性过滤选择器
1. [attribute], 匹配包含给定属性的元素; 查找所有含有id的div元素:$("div[id]")
2. [attribute=value], 匹配给定的属性是某个特定值的元素; 查找所有name属性是new
  newsletter的input元素:$("input[name='newsletter']").attr("checked", true);
3. [attribute!=value],匹配给定的属性是不包含某个特定值的元素.
4. [attribute^=value], 匹配给定的属性是以某些值开始的元素
5. [attribute$=value],匹配给定的属性是以某些值结尾的元素
6. [attribute*=value],匹配给定的属性是包含某些值的元素
7. [attributeFilter1][attributeFilter2]..., 复合属性,需要同时满足,如:
  $("input[id][name$='man']")

#### 子元素过滤选择器
根据父元素中的某些过滤规则来选择子元素.

1. :nth-child(index/even/odd/equation): 
  匹配其父元素下的第N个子元素或奇偶元素':eq(index)'只匹配一个元素,而这个将每一个父元素匹配子元素:nth-child从1开始的,而:eq()从0算起.可以使用:
  :th-childe(even), :th-child(odd), :th-child(3n), :th-child(2), :th-child(3n+1); 在每个ul查找第2个li: $("ul li:nth-child(2)")

2. :first-child, 匹配第一个元素, ':first-child'只匹配一个元素,而此选择符将为每个父元素匹配一个子元素
3. :last-child
4. :only-child: 如果某个元素是父元素中 唯一的一个元素, 那么将会匹配.

#### 表单对象属性过滤器
1. :enabled, 匹配所有可用元素,
2. :disabled,
3. checked,匹配所有被选中的元素(复选框,单选框, 不包括select中的option),
  $("input:checked")
4. :selected, 匹配所有选中的option

### 表单选择器

1. :input, 匹配所有的input, textarea, select, button元素,
  查找所有的input元素$(":input")

2. :text,匹配所有的文本框,
3. :password, 匹配所有的密码框
4. :radio,
5. :checkbox
6. :submit
7. :image, 匹配所有的图像域
8. :reset, 所有的重置按钮
9. :button
10. :file, 所有的文件域


### 常见问题
1. $("input") 与$(":input")的区别


## 三 用jQuery来操作DOM

### 3.1 修改元素属性
#### 3.1.1 获取元素属性
$(selector).attr(attribute)   -- 获取与设置
$('img').attr("src")
设置属性
$(selector).attr(attribute, value);

$(selector).removeAttr(),删除属性

### 3.2 修改元素内容
1. text(): 设置或返回所选元素的文本内容
2. html(): 设置或返回所选元素的内容,包括html
3. val(): 设置或返回表单字段的值


### 3.3 动态创建内容
jQuery 动态添加内容, 相当于原生js的CreateElement:
$(html), html为要动态创建的HTML标记, 它会动态的创建一个DOM对象,但是这个DOM对象并没有添加到DOM对象树中,可以使用一下函数来添加:
1. append(), 在备选元素的结尾添加内容.
2. preappend(), 在备选元素的开头添加内容
3. after(), 在备选元素之后添加内容
4. before(), 在被选元素之前插入内容.
```javascript
$("div", {
    text: "this is dd create page",
    click: function(){
        $(this).toggleClass("test")
        },
    }).appendTo("body")
```
### 3.4 动态插入节点
1. append(): 在备选元素的结尾(仍在内部)插入指定内容
2. appendTo():在备选元素的结尾(仍在内部)插入指定内容
3. prepend():在备选元素的开头(仍在内部)插入指定内容
4. prependTo(): 在备选元素的开头(仍在内部)插入指定内容
5. after(): 在被选元素后面插入指定内容
6. before():  在被选元素前面插入指定内容
7. insertAfter(): 把匹配的元素插入到另一个指定的集合后面.
8. insertBefore():把匹配的元素插入到另一个指定的集合前面.

### 3.5 动态删除节点

1. remove()方法:用来删除指定的ＤＯＭ元素, 它会将节点从DOM元素树中删除, 但是会返回一个指向DOM元素的引用, 因此它并不是真正的将jQuery引用到的元素对象删除,而是可以用过这个引用来继续操作元素.

2. empty(): 该方法不会删除节点, 只是情况节点的内容, DOM元素依然保持在DOM树中.


## 四, jQuery的事件与事件对象

### 4.1 jQuery所支持事件和事件类型

1. 简单的事件绑定方法

|方法|  描述|
|----|------|
|bind()|  向匹配元素附加一个或更多事件处理器|
|blur()|  触发、或将函数绑定到指定元素的 blur 事件|
|change()|  触发、或将函数绑定到指定元素的 change 事件|
|click()| 触发、或将函数绑定到指定元素的 click 事件|
|dblclick()|  触发、或将函数绑定到指定元素的 double click 事件|
|delegate()|  向匹配元素的当前或未来的子元素附加一个或多个事件处理器|
|die()| 移除所有通过 live()| 函数添加的事件处理程序。|
|error()| 触发、或将函数绑定到指定元素的 error 事件|
|event.isDefaultPrevented()|  返回 event对象上是否调用了event.preventDefault()||
|event.pageX |相对于文档左边缘的鼠标位置。|
|event.pageY| 相对于文档上边缘的鼠标位置。|
|event.preventDefault()|  阻止事件的默认动作。|
|event.result|  包含由被指定事件触发的事件处理器返回的最后一个值。|
|event.target | 触发该事件的 DOM 元素。|
|event.timeStamp| 该属性返回从 1970 年 1 月 1 日到事件发生时的毫秒数。|
|event.type|  描述事件的类型。|
|event.which| 指示按了哪个键或按钮。|
|focus()| 触发、或将函数绑定到指定元素的 focus 事件|
|keydown()| 触发、或将函数绑定到指定元素的 key down 事件|
|keypress()|  触发、或将函数绑定到指定元素的 key press 事件|
|keyup()| 触发、或将函数绑定到指定元素的 key up 事件|
|live()|  为当前或未来的匹配元素添加一个或多个事件处理器|
|load()|  触发、或将函数绑定到指定元素的 load 事件|
|mousedown()| 触发、或将函数绑定到指定元素的 mouse down 事件|
|mouseenter()|  触发、或将函数绑定到指定元素的 mouse enter 事件|
|mouseleave()|  触发、或将函数绑定到指定元素的 mouse leave 事件|
|mousemove()| 触发、或将函数绑定到指定元素的 mouse move 事件|
|mouseout()|  触发、或将函数绑定到指定元素的 mouse out 事件|
|mouseover()| 触发、或将函数绑定到指定元素的 mouse over 事件|
|mouseup()| 触发、或将函数绑定到指定元素的 mouse up 事件|
|one()| 向匹配元素添加事件处理器。每个元素只能触发一次该处理器。|
|ready()| 文档就绪事件（当 HTML 文档就绪可用时）|
|resize()|  触发、或将函数绑定到指定元素的 resize 事件|
|scroll()|  触发、或将函数绑定到指定元素的 scroll 事件|
|select()|  触发、或将函数绑定到指定元素的 select 事件|
|submit()|  触发、或将函数绑定到指定元素的 submit 事件|
|toggle()|  绑定两个或多个事件处理器函数，当发生轮流的 click 事件时执行。|
|trigger()| 所有匹配元素的指定事件|
|triggerHandler()|  第一个被匹配元素的指定事件|
|unbind()|  从匹配元素移除一个被添加的事件处理器|
|undelegate()|  从匹配元素移除一个被添加的事件处理器，现在或将来|
|unload()|  触发、或将函数绑定到指定元素的 unload 事件|

2. 复合事件
ready(): 当DOM加载完毕后触发事件
hover([fn1,] fn2): 当鼠标移入触发第一个fn1, 移出触发fn2
toggle(fn1, fn2[,fn3...]): 1.10后后废除. 当鼠标单击触发fn1, 再单击触发fn2,....


3. 事件对象的属性

type: 事件类型, 如果使用一个事件处理方法来处理多个事件, 可以使用此属性来获得事件类型.

target: 获取事件触发者DOM对象
data: 事件调用时传入额外参数.

relatedTarget: 对于鼠标事件,标示触发事件时离开或者进入的DOM元素.
currentTarget: 冒泡前当前触发事件的DOM对象, 等于this
pageX/Y: 鼠标事件中, 事件相对于也面对原点的水平/垂直坐标
result: 上一个事件处理方法返回的值.
timeStamp: 事件发生时的时间戳
altKey: Alt被按下, 如果按下返回true
crtlKey: 
metaKey: Ctrl/Command
shiftKey:
keyCode: 对于keyup和keydown事件返回按下的键, 不区分大小写. 对于keypress事件请使用which属性, 因为which属性跨浏览器时依然可靠.

which: 对于键盘事件, 返回触发事件的键的数字编码, 对于鼠标事件, 返回鼠标按键号, 1为左键,2为中建, 3为右键
screenX/Y: 对于鼠标事件, 获取事件相对于屏幕原点的水平和垂直坐标.

4. 事件对象所有用的方法

preventDefault(): 取消可能引起任何语意操作的事件, 比如<a> 标签元素的href链接加载, 表单时间提交以及click引起复选框的状态切换.

isDefaultPrevent(): 是否调用过preventDefault()
stopPropagation(): 取消事件冒泡
isPropagation(): 是否调用过stopPropagation()
stopImmediatePropagation(): 取消执行其他的事件处理方法, 并取消事件冒泡. 如果同一个事件绑定了多个事件处理方法, 在其中一个事件处理方法中调用了此方法后, 将不会继续调用其他的事件处理方法.
isImmediatePropagation(): 


### 4.2 页面初始化
```
$().ready(function)
$(function)
```


### 4.3 绑定事件

`$(selector).bind(event, data, function)`: event: 是事件 比如click等.
可选data参数作为event.data属性值传给事件对象的额外数据对象
function
bind可以同时绑定多个事件:
```
bind({
  click: function(){

    },
    mouseover:function(){},
    ....
  })
```

`$(selector).click(function(){})`

### 4.4 移除绑定事件
`$(selector).unbind(event, function)`


### 4.5 切换事件

`hover`方法: 元素在鼠标悬停与鼠标移除事件中进行切换, 这个方法实际是对mouseenter和mouserleave事件的合并. 用来模仿一种悬停效果.

`toggle`方法, 可以一次调用多个指定的函数, 直到最后一个函数, 接下来重复操作.. 新版本以废弃

`hover([over,]out)`

### 4.6 表单中常见的时间

#### 4.6.1 表单元素焦点的获取和失去
#### 4.6.2文本域高度的动态变化

#### 4.6.3 表单验证


## 五 原始AJAX与jQuery中的AJAX

### 5.1 两个AJAX对比

原始的AJAX编写
```javascript
var client; //定义XMLHttpRequest对象
//button click的回调函数
function sendAjax(){
    if(window.ActiveOXbject){
        client = new ActiveOXbject("Microsoft.XMLHTTP");
    }
    else if(window.XMLHttpRequest){
            client = new XMLHttpRequest();
    }else{
        alert('创建ajax客户端失败');
    }
    if(client){
        //GET请求方法,参数只能放在URL后面, 这种方式受到url长度限制.
        client.open('GET', "data.txt");
        client.send();
        client.onreadystatechange = myCallBack(); //指定回调函数
    }
}

//自定义回调函数
function myCallBack(){
    //如果请求的response正常返回
    if(client.readystatechange == 4){
        if(client.status==200){
            var resp = client.responseText; //返回的值字符串形式
            alert(resp);
        }
        else if(client.status == 404){
            aliert("ddddd");
        }
        else if(client.status == 500){
            alert('xxxxx')
        }
    }
}

```
### 5.2 使用jQuery的AJAX函数进行页面交互.
### jQuery Ajax操作函数

`jQuery.ajax()` 执行异步 HTTP (Ajax) 请求。
`.ajaxComplete()` 当 Ajax 请求完成时注册要调用的处理程序。这是一个 Ajax 事件。
`.ajaxError()`  当 Ajax 请求完成且出现错误时注册要调用的处理程序。这是一个 Ajax 事件。
`.ajaxSend()` 在 Ajax 请求发送之前显示一条消息。
`jQuery.ajaxSetup()`  设置将来的 Ajax 请求的默认值。
`.ajaxStart()`  当首个 Ajax 请求完成开始时注册要调用的处理程序。这是一个 Ajax 事件。
`.ajaxStop()` 当所有 Ajax 请求完成时注册要调用的处理程序。这是一个 Ajax 事件。
`.ajaxSuccess()`  当 Ajax 请求成功完成时显示一条消息。
`jQuery.get()`  使用 HTTP GET 请求从服务器加载数据。
`jQuery.getJSON()`  使用 HTTP GET 请求从服务器加载 JSON 编码数据。
`jQuery.getScript()`  使用 HTTP GET 请求从服务器加载 JavaScript 文件，然后执行该文件。
`.load()` 从服务器加载数据，然后把返回到 HTML 放入匹配元素。
`jQuery.param()`  创建数组或对象的序列化表示，适合在 URL 查询字符串或 Ajax 请求中使用。
`jQuery.post()` 使用 HTTP POST 请求从服务器加载数据。
`.serialize()`  将表单内容序列化为字符串。
`.serializeArray()` 序列化表单元素，返回 JSON 数据结构数据。

#### jQuery.ajax函数
```javascript
$(document).ready(function(){
  $("#b01").click(function(){
  htmlobj=$.ajax({url:"/jquery/test1.txt",async:false});
  $("#myDiv").html(htmlobj.responseText);
  });
});
```


#### jQuery.post
```
var jqXHR = jQuery.post( url [, data ] [, success(data, textStatus, jqXHR) ] [, dataType ] );
```

```javascript
//request with URL,data,success callback
$.post("AJAX_POST_URL",
    {name:"ravi",age:"31"},
    function(data, textStatus, jqXHR)
    {
          //data: Received from server
    });
 
//request with URL,success callback
$.post("AJAX_POST_URL",function(data)
{
    //data: Received from server
});
//request with only URL
$.post("AJAX_POST_URL");

//      =======
// 带有错误处理的
$.post("AJAX_POST_URL",
    {username:"ravi",pass:"124",submit:true},
    function(data, textStatus, jqXHR)
    {
        //data - response from server
    }).fail(function(jqXHR, textStatus, errorThrown) 
    {
        alert(textStatus);
    });
 
//With jqXHR callbacks .done() and .fail()
$.post("AJAX_POST_URL",
    {username:"ravi",pass:"124",submit:true}).done(function(data, textStatus, jqXHR) 
        {
 
        }).fail(function(jqXHR, textStatus, errorThrown) 
    {
        alert(textStatus);
    });



```

* 带有form的post提交
```
<form name="myform" id="myform" action="ajax-post.php">
User: <input type="text" value="Ravishanker" name="user"  /> <br/>
Password: <input type="password" name="password" value="abcdefgh" />
<input type="hidden" name="xyz" value="123" />
<input type="hidden" name="submit" value="true" />
 
</form>
```

```
//var formData = $("#myform").serialize();  //or
var formData = $("#myform").serializeArray();
var URL = $("#myform").attr("action");
$.post(URL,
    formData,
    function(data, textStatus, jqXHR)
    {
       //data: Data from server.    
    }).fail(function(jqXHR, textStatus, errorThrown) 
    {
 
    });
```

```
Use $('form').serializeArray(), which returns an array:

[
  {"name":"foo","value":"1"},
  {"name":"bar","value":"xxx"},
  {"name":"this","value":"hi"}
]
Other option is $('form').serialize(), which returns a string:

"foo=1&bar=xxx&this=hi"
```

#### 实例
* 1. 
```
var  formData = "name=ravi&age=31";  //Name value Pair
    or
var formData = {name:"ravi",age:"31"}; //Array 
 
$.ajax({
    url : "AJAX_POST_URL",
    type: "POST",
    data : formData,
    success: function(data, textStatus, jqXHR)
    {
        //data - response from server
    },
    error: function (jqXHR, textStatus, errorThrown)
    {
 
    }
});
```

formData: can be an array or name value pairs.
success: callback function is called when the AJAX POST is successful
error: callback function is called when the AJAX POST is failed



__定义和用法__
`ajax()` 方法通过 HTTP 请求加载远程数据。
该方法是 jQuery 底层 AJAX 实现。简单易用的高层实现见` $.get`, `$.post` 等。`$.ajax()` 返回其创建的 XMLHttpRequest 对象。大多数情况下你无需直接操作该函数，除非你需要操作不常用的选项，以获得更多的灵活性。
最简单的情况下，`$.ajax()` 可以不带任何参数直接使用。

>注意：所有的选项都可以通过 $.ajaxSetup() 函数来全局设置。

**jQuery.ajax([settings])**
settings: 可选. 用于配置Ajax请求的键值集合. 可以通过`$.ajaxSetup()` 设置任何选项的默认值.

**相关参数**:
`options`
类型：Object
可选。AJAX 请求设置。所有选项都是可选的。

`async`
类型：Boolean
默认值: true。默认设置下，所有请求均为异步请求。如果需要发送同步请求，请将此选项设置为 false。
注意，同步请求将锁住浏览器，用户其它操作必须等待请求完成才可以执行。

`beforeSend(XHR)`
类型：Function
发送请求前可修改 XMLHttpRequest 对象的函数，如添加自定义 HTTP 头。
XMLHttpRequest 对象是唯一的参数。
这是一个 Ajax 事件。如果返回 false 可以取消本次 ajax 请求。

`cache`
类型：Boolean
默认值: true，dataType 为 script 和 jsonp 时默认为 false。设置为 false 将不缓存此页面。
jQuery 1.2 新功能。

`complete(XHR, TS)`
类型：Function
请求完成后回调函数 (请求成功或失败之后均调用)。
参数： XMLHttpRequest 对象和一个描述请求类型的字符串。
这是一个 Ajax 事件。

`contentType`
类型：String
默认值: "application/x-www-form-urlencoded"。发送信息至服务器时内容编码类型。
默认值适合大多数情况。如果你明确地传递了一个 content-type 给 $.ajax() 那么它必定会发送给服务器（即使没有数据要发送）。

`context`
类型：Object
这个对象用于设置 Ajax 相关回调函数的上下文。也就是说，让回调函数内 this 指向这个对象（如果不设定这个参数，那么 this 就指向调用本次 AJAX 请求时传递的 options 参数）。比如指定一个 DOM 元素作为 context 参数，这样就设置了 success 回调函数的上下文为这个 DOM 元素。
就像这样：
```
$.ajax({ url: "test.html", context: document.body, success: function(){
        $(this).addClass("done");
      }});
```

`data`
类型：String
发送到服务器的数据。将自动转换为请求字符串格式。GET 请求中将附加在 URL 后。查看 processData 选项说明以禁止此自动转换。必须为 Key/Value 格式。如果为数组，jQuery 将自动为不同值对应同一个名称。如 {foo:["bar1", "bar2"]} 转换为 '&foo=bar1&foo=bar2'。

`dataFilter`
类型：Function
给 Ajax 返回的原始数据的进行预处理的函数。提供 data 和 type 两个参数：data 是 Ajax 返回的原始数据，type 是调用 jQuery.ajax 时提供的 dataType 参数。函数返回的值将由 jQuery 进一步处理。

`dataType`
类型：String
预期服务器返回的数据类型。如果不指定，jQuery 将自动根据 HTTP 包 MIME 信息来智能判断，比如 XML MIME 类型就被识别为 XML。在 1.4 中，JSON 就会生成一个 JavaScript 对象，而 script 则会执行这个脚本。随后服务器端返回的数据会根据这个值解析后，传递给回调函数。可用值:
- "xml": 返回 XML 文档，可用 jQuery 处理。
- "html": 返回纯文本 HTML 信息；包含的 script 标签会在插入 dom 时执行。
- "script": 返回纯文本 JavaScript 代码。不会自动缓存结果。除非设置了 "cache" 参数。注意：在远程请求时(不在同一个域下)，所有 POST 请求都将转为 GET 请求。（因为将使用 DOM 的 script标签来加载）
- "json": 返回 JSON 数据 。
- "jsonp": JSONP 格式。使用 JSONP 形式调用函数时，如 "myurl?callback=?" jQuery 将自动替换 ? 为正确的函数名，以执行回调函数。
- "text": 返回纯文本字符串

`error`
类型：Function
默认值: 自动判断 (xml 或 html)。请求失败时调用此函数。
有以下三个参数：XMLHttpRequest 对象、错误信息、（可选）捕获的异常对象。
如果发生了错误，错误信息（第二个参数）除了得到 null 之外，还可能是 "timeout", "error", "notmodified" 和 "parsererror"。
这是一个 Ajax 事件。

`global`
类型：Boolean
是否触发全局 AJAX 事件。默认值: true。设置为 false 将不会触发全局 AJAX 事件，如 ajaxStart 或 ajaxStop 可用于控制不同的 Ajax 事件。
`ifModified`
类型：Boolean
仅在服务器数据改变时获取新数据。默认值: false。使用 HTTP 包 Last-Modified 头信息判断。在 jQuery 1.4 中，它也会检查服务器指定的 'etag' 来确定数据没有被修改过。
`jsonp`
类型：String
在一个 jsonp 请求中重写回调函数的名字。这个值用来替代在 "callback=?" 这种 GET 或 POST 请求中 URL 参数里的 "callback" 部分，比如 {jsonp:'onJsonPLoad'} 会导致将 "onJsonPLoad=?" 传给服务器。
`jsonpCallback`
类型：String
为 jsonp 请求指定一个回调函数名。这个值将用来取代 jQuery 自动生成的随机函数名。这主要用来让 jQuery 生成度独特的函数名，这样管理请求更容易，也能方便地提供回调函数和错误处理。你也可以在想让浏览器缓存 GET 请求的时候，指定这个回调函数名。
`password`
类型：String
用于响应 HTTP 访问认证请求的密码
`processData`
类型：Boolean
默认值: true。默认情况下，通过data选项传递进来的数据，如果是一个对象(技术上讲只要不是字符串)，都会处理转化成一个查询字符串，以配合默认内容类型 "application/x-www-form-urlencoded"。如果要发送 DOM 树信息或其它不希望转换的信息，请设置为 false。
`scriptCharset`
类型：String
只有当请求时 dataType 为 "jsonp" 或 "script"，并且 type 是 "GET" 才会用于强制修改 charset。通常只在本地和远程的内容编码不同时使用。
`success`
类型：Function
请求成功后的回调函数。
参数：由服务器返回，并根据 dataType 参数进行处理后的数据；描述状态的字符串。
这是一个 Ajax 事件。
`traditional`
类型：Boolean
如果你想要用传统的方式来序列化数据，那么就设置为 true。请参考工具分类下面的 jQuery.param 方法。
`timeout`
类型：Number
设置请求超时时间（毫秒）。此设置将覆盖全局设置。
`type`
类型：String
默认值: "GET")。请求方式 ("POST" 或 "GET")， 默认为 "GET"。注意：其它 HTTP 请求方法，如 PUT 和 DELETE 也可以使用，但仅部分浏览器支持。
`url`
类型：String
默认值: 当前页地址。发送请求的地址。
`username`
类型：String
用于响应 HTTP 访问认证请求的用户名。
`xhr`
类型：Function
需要返回一个 XMLHttpRequest 对象。默认在 IE 下是 ActiveXObject 而其他情况下是 XMLHttpRequest 。用于重写或者提供一个增强的 XMLHttpRequest 对象。这个参数在 jQuery 1.3 以前不可用。

*回调函数*
如果要处理 $.ajax() 得到的数据，则需要使用回调函数：`beforeSend`、`error`、`dataFilte`r、`success`、`complete`。

`beforeSend`
在发送请求之前调用，并且传入一个 XMLHttpRequest 作为参数。
`error`
在请求出错时调用。传入 XMLHttpRequest 对象，描述错误类型的字符串以及一个异常对象（如果有的话）
`dataFilter`
在请求成功之后调用。传入返回的数据以及 "dataType" 参数的值。并且必须返回新的数据（可能是处理过的）传递给 success 回调函数。
`success`
当请求之后调用。传入返回后的数据，以及包含成功代码的字符串。
`complete`
当请求完成之后调用这个函数，无论成功或失败。传入 XMLHttpRequest 对象，以及一个包含成功或错误代码的字符串。

*数据类型*
$.ajax() 函数依赖服务器提供的信息来处理返回的数据。如果服务器报告说返回的数据是 XML，那么返回的结果就可以用普通的 XML 方法或者 jQuery 的选择器来遍历。如果见得到其他类型，比如 HTML，则数据就以文本形式来对待。
通过 dataType 选项还可以指定其他不同数据处理方式。除了单纯的 XML，还可以指定 html、json、jsonp、script 或者 text。
其中，text 和 xml 类型返回的数据不会经过处理。数据仅仅简单的将 XMLHttpRequest 的 responseText 或 responseHTML 属性传递给 success 回调函数。
注意：我们必须确保网页服务器报告的 MIME 类型与我们选择的 dataType 所匹配。比如说，XML的话，服务器端就必须声明 text/xml 或者 application/xml 来获得一致的结果。
如果指定为 html 类型，任何内嵌的 JavaScript 都会在 HTML 作为一个字符串返回之前执行。类似地，指定 script 类型的话，也会先执行服务器端生成 JavaScript，然后再把脚本作为一个文本数据返回。
如果指定为 json 类型，则会把获取到的数据作为一个 JavaScript 对象来解析，并且把构建好的对象作为结果返回。为了实现这个目的，它首先尝试使用 JSON.parse()。如果浏览器不支持，则使用一个函数来构建。
JSON 数据是一种能很方便通过 JavaScript 解析的结构化数据。如果获取的数据文件存放在远程服务器上（域名不同，也就是跨域获取数据），则需要使用 jsonp 类型。使用这种类型的话，会创建一个查询字符串参数 callback=? ，这个参数会加在请求的 URL 后面。服务器端应当在 JSON 数据前加上回调函数名，以便完成一个有效的 JSONP 请求。如果要指定回调函数的参数名来取代默认的 callback，可以通过设置 $.ajax() 的 jsonp 参数。
注意：JSONP 是 JSON 格式的扩展。它要求一些服务器端的代码来检测并处理查询字符串参数。
如果指定了 script 或者 jsonp 类型，那么当从服务器接收到数据时，实际上是用了 <script> 标签而不是 XMLHttpRequest 对象。这种情况下，$.ajax() 不再返回一个 XMLHttpRequest 对象，并且也不会传递事件处理函数，比如 beforeSend。
发送数据到服务器
默认情况下，Ajax 请求使用 GET 方法。如果要使用 POST 方法，可以设定 type 参数值。这个选项也会影响 data 选项中的内容如何发送到服务器。
data 选项既可以包含一个查询字符串，比如 key1=value1&key2=value2 ，也可以是一个映射，比如 {key1: 'value1', key2: 'value2'} 。如果使用了后者的形式，则数据再发送器会被转换成查询字符串。这个处理过程也可以通过设置 processData 选项为 false 来回避。如果我们希望发送一个 XML 对象给服务器时，这种处理可能并不合适。并且在这种情况下，我们也应当改变 contentType 选项的值，用其他合适的 MIME 类型来取代默认的 application/x-www-form-urlencoded 。

*高级选项*
global 选项用于阻止响应注册的回调函数，比如 .ajaxSend，或者 ajaxError，以及类似的方法。这在有些时候很有用，比如发送的请求非常频繁且简短的时候，就可以在 ajaxSend 里禁用这个。
如果服务器需要 HTTP 认证，可以使用用户名和密码可以通过 username 和 password 选项来设置。
Ajax 请求是限时的，所以错误警告被捕获并处理后，可以用来提升用户体验。请求超时这个参数通常就保留其默认值，要不就通过 jQuery.ajaxSetup 来全局设定，很少为特定的请求重新设置 timeout 选项。
默认情况下，请求总会被发出去，但浏览器有可能从它的缓存中调取数据。要禁止使用缓存的结果，可以设置 cache 参数为 false。如果希望判断数据自从上次请求后没有更改过就报告出错的话，可以设置 ifModified 为 true。
scriptCharset 允许给 <script> 标签的请求设定一个特定的字符集，用于 script 或者 jsonp 类似的数据。当脚本和页面字符集不同时，这特别好用。
Ajax 的第一个字母是 asynchronous 的开头字母，这意味着所有的操作都是并行的，完成的顺序没有前后关系。$.ajax() 的 async 参数总是设置成true，这标志着在请求开始后，其他代码依然能够执行。强烈不建议把这个选项设置成 false，这意味着所有的请求都不再是异步的了，这也会导致浏览器被锁死。
$.ajax 函数返回它创建的 XMLHttpRequest 对象。通常 jQuery 只在内部处理并创建这个对象，但用户也可以通过 xhr 选项来传递一个自己创建的 xhr 对象。返回的对象通常已经被丢弃了，但依然提供一个底层接口来观察和操控请求。比如说，调用对象上的 .abort() 可以在请求完成前挂起请求。



## 6 jQuery中的动画效果

### 6.1 jQuery库所支持的动画方法
#### 6.1.1 基本动画方法

`show()`: 显示隐藏的匹配元素. 这个就是show(speed,[callback])无动画版本. 如果选择的元素是可见的, 这个方法则不会改变任何东西. 无论这个元素是通过hide()方法隐藏, 还是在css设置属性为display:none 隐藏, 都有效.

`show(speed[,callback])`, 以优雅的动画显示所有匹配的元素, 并在显示完成后可选的触发一个回调方法. 可以根据指定的速度动态的改变每个匹配元素的高度,宽度和不透明度. 在jQuery 1.3中 padding和margin也有动画.

`hide()`: 隐藏显示元素.

`hide(speed[,callback])`: 类似show(spedd,[callback])

`toggle()`: 切换元素的可见状态. 如果元素是可见的, 切换为隐藏, 若为隐藏切换为可见.

`toggle(switch)`: 根据switch参数切换元素的可见状态(true: 可见, false:不可见). 如果switch设为true, 则调用show()方法来显示匹配元素,如果为false则调用hide()方法.

`toggle(speed[,callback])`:   

#### 6.1.2 滑动动画方法

`slideDown(speed[,callback])`: 通过高度变化(向下增大)来动态的显示所有匹配元素, 在显示完成后可以出发一个回调方法. 这个动画效果只能调整元素的高度, 可以使匹配的元素以'滑动'的方式显示出来.

`slideUp(speed[,callback])`: 通过高度变化(向上减小)来动态的隐藏所匹配的元素, 隐藏完成后可以选择的触发一个回调方法.

`slideToggle(speed[,callback])`: 通过高度变化来切换所有匹配的元素的可见性, 并在切换完成后可选的触发一个回调方法.

#### 6.1.3 淡入淡出的动画方法
`fadeIn(speed[,callback])` 通过不透明度的变化来实现所匹配的元素的淡入效果, 并在动画完成后可选的执行一个回调方法.

`fadeOut(speed[,callback])` 通过不透明度的变化来.

`fadeTo(speed, opacity[,callback])`  所有匹配元素的不透明度以渐进方式调整到指定的不透明度, 并在动画完成后选择的执行一个回调方法.

### 6.4 自定义动画animate
```
$(selector).animate({params}, speed, callback)
```
params: 必须的, 形成动画的css属性.
speed: 可选,show,fast,毫秒数
callback, 可选,回调方法.
