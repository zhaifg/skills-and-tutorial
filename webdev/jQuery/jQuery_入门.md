
## jQuery对象和Dom对象
```angular2html
<p id="imooc"></p>

```
```javascript
var p = document.getElementById('imooc');
p.innerHTML = "dafsfdsaf";
p.style.color = 'red'
```
上面通过原生dom模型获取的对象是dom对象

```javascript
var $p = $("#imooc")
// 对象是jquery对象
```

## jquery对象转dom对象
```html
<div>a</div>
<div>b</div>
<div>c</div>
```
```javascript
var $div = $("div") // jquery 对象
var div = $div[0] // 转化成Dom对象  ==$div.get(0)
div.style.color = 'red'
```

## dom 对象转换成 jquery 对象

如果传递给$(DOM)函数参数是一个DOM对象, jQuery方法会把这个加工成jQuery
对象. 
```html
<div>a</div>
<div>b</div>
<div>c</div>
```

```javascript
var div = document.getElementsByTagName('div');

var $div = $(div)
var $first = $div.first()
$first.css('color', 'red')
```

## jquery的this和 html的this

this, 表示当前的上下文对象是一个html对象, 可以调用html对象所拥有的属性和方法.

$(this), 代表的上下文对象是一个jquery的上下文对象, 可以调用jQuery的方法
和属性值.
