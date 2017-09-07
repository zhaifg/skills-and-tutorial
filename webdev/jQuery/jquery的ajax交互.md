# jQuery 的ajax交互
---

## $.get

## $.post
### 使用Json提交

```javascript
  function authenticate(userName, password) {
    $.ajax
    ({
        type: "POST",
        //the url where you want to sent the userName and password to
        url: 'username:password@link to the server/update',
        dataType: 'json',
        async: false,
        //json object to sent to the authentication url
        data: '{"userName": "' + userName + '", "password" : "' + password + '"}',
        success: function () {

        alert("Thanks!"); 
        }
    })
}

// 数据应该json化
data: JSON.stringify({ "userName": userName, "password" : password })
data: JSON.stringify(formData)

```


### post 是xml等格式
```
<form action="/" id="searchForm">
  <input type="text" name="s" placeholder="Search...">
  <input type="submit" value="Search">
</form>

<script>
// Attach a submit handler to the form
$( "#searchForm" ).submit(function( event ) {
  // Stop form from submitting normally
  event.preventDefault();
  // Get some values from elements on the page:
  var $form = $( this ),
    term = $form.find( "input[name='s']" ).val(),
    url = $form.attr( "action" );
 
  // Send the data using post
  var posting = $.post( url, { s: term } );
 
  // Put the results in a div
  posting.done(function( data ) {
    var content = $( data ).find( "#content" );
    $( "#result" ).empty().append( content );
  });
});
```



## $.ajax

```
$.ajax(url, {
    data : JSON.stringify(myJSObject),
    contentType : 'application/json',
    type : 'POST',
```

## ajax 序列化
`serialize()` 方法通过序列化表单值，创建 URL 编码文本字符串。
您可以选择一个或多个表单元素（比如 input 及/或 文本框），或者 form 元素本身。

```
$("button").click(function(){
  $("div").text($("form").serialize());
});
```

```
<form>
  <div><input type="text" name="a" value="1" id="a" /></div>
  <div><input type="text" name="b" value="2" id="b" /></div>
  <div><input type="hidden" name="c" value="3" id="c" /></div>
  <div>
    <textarea name="d" rows="8" cols="40">4</textarea>
  </div>
  <div><select name="e">
    <option value="5" selected="selected">5</option>
    <option value="6">6</option>
    <option value="7">7</option>
  </select></div>
  <div>
    <input type="checkbox" name="f" value="8" id="f" />
  </div>
  <div>
    <input type="submit" name="g" value="Submit" id="g" />
  </div>
</form>
```

.serialize() 方法可以操作已选取个别表单元素的 jQuery 对象，比如 <input>, <textarea> 以及 <select>。不过，选择 <form> 标签本身进行序列化一般更容易些：

```
$('form').submit(function() {
  alert($(this).serialize());
  return false;
});
```

```
a=1&b=2&c=3&d=4&e=5
```

## 把序列化的form 转换为json对象

1. var input = $("#inputId").val();
2. var input = $("form.login").serialize();
3. var input = $("form.login").serializeArray();
```
<form class="login">
    <label for="_user_name">username:</label>
    <input type="text" id="_user_name" name="user[name]" value="dev.pus" />
    <label for="_user_pass">password:</label>
    <input type="password" id="_user_pass" name="user[pass]" value="1234" />
    <button type="submit">login</button>
</form>
```

```
var formData = $("form.login").serializeObject();
console.log(formData);

// output
{
    "name": "dev.pus",
    "pass": "1234"
}
```

### 别的方法

#### 
```
var frm = $(document.myform);
 var data = JSON.stringify(frm.serializeArray());
```

#### 2. 定义一个转换函数
```
function getFormData($form){
    var unindexed_array = $form.serializeArray();
    var indexed_array = {};

    $.map(unindexed_array, function(n, i){
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}
//Usage:

var $form = $("#form_data");
var data = getFormData($form);
```
