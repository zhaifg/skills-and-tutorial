# jQuery 的各个插件的应用
---

## jquery-validate 验证

```
   <div class="form-group">
       <label class="control-label col-sm-2" for="username">姓名</label>
       <div class="col-sm-7">
           <input class="form-control" id="username" name="username" placeholder="用户名" type="text">
       </div>
   </div>

   var form = $('#add_user_form');
                form.validate({
                    errorElement: 'span', //错误信息的容器
                    errorClass: 'text-danger',
                    //验证规则
                    rules: {
                        username: {
                            required: true,
                        },
                        login_name: {
                            required: true,
                            login_name: true
                        },
                        email: {
                            required: true,
                            eamil: true,
                        },
                        weixin: {
                            required: true,
                        },
                        mobile: {
                            required: true,
                            phone: true
                        },
                    },
                     //错误提示信息
                    messages: {
                        username: "组名不能为空",
                        login_name: "不能为空, 或者只能有数字和字母和下划线组成",
                        email: "格式不正确",
                        weixin: "填写微信账号",
                        mobile: "电话不能为空"
                    }
                });
```

### 常用规则
```
required    Boolean  若为true，则字段必填
minlength   Number   字段最小长度
maxlength   Number   字段最大长度
min   Number  最小值
max   Number  最大值
email    Boolean  若为true，则字段必须符合email格式
url   Boolean   若为true，则字段必须符合url格式
date     Boolean  若为true，则字段必须符合日期格式
number   Boolean   若为true，则字段必须是数字，可含小数点
digits    Boolean   若为true，则字段必须是数字，不能有小数点
equalTo Selector如'#element'   此字段和某个输入的值相等，常用于输入确定密码

```

### 常用方法
```
valid() //判断表单输入是否正确
var form = $( "#myform" );
form.validate();
form.valid()

rules() //添加或删除规则

$( "#myinput" ).rules( "add", {
      required: true,
      minlength: 2,
      messages: {
        required: "Required input"
      }
});

$( "#myinput" ).rules( "remove", "min max" );


addMethod() //扩展自定义校验
$.validator.addMethod("phone",function(value, element, param){  
    if(/^1\d{10}$/.test(value)){
         return true;
    }
});
    
            
```

## jquery 把form改变成object的json

### 方法一
```

$.fn.serializeObject = function(){
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
}


```


### 方法二
```

var data = {};
$("form").serializeArray().map(function(x){
    if (data[x.name] !== undefined) {
        if (!data[x.name].push) {
            data[x.name] = [data[x.name]];
        }
        data[x.name].push(x.value || '');
    } else {
        data[x.name] = x.value || '';
    }
});
```

### 实例
```
<!DOCTYPE html>
<html lang="en-US">
    <head>
        <meta charset="utf-8">
        <style type="text/css">
            .group{margin: 10px 0; clear: both; display: flex;}
            .left{float: left; width: 120px; text-align: right;}
            .right{float: right; flex: 1;}
            .size{margin: 5px 0;}
            input[type='number']{width: 80px;}
            .show{width: 400px; height: 400px; overflow: auto;}
            input[type='button']{height: 40px;}
            div{margin-bottom: 10px;}
        </style>
    </head>
    <body>
        <form onSubmit="return false;">
         <div class="group">
          <div class="left">radio：</div>
                <div class="right">
                    <label for="radio-0"><input value="是" type="radio" name="radio" id="radio-0" />是</label>
                    <label for="radio-1"><input value="否" type="radio" name="radio" id="radio-1" />否 </label>
                </div>
            </div>
            <div class="group">
          <div class="left">checkbox：</div>
                <div class="right">
                    <label for="checkbox-0"><input value="0" type="checkbox" name="checkbox" id="checkbox-0" />0 </label>
                    <label for="checkbox-1"><input value="1" type="checkbox" name="checkbox" id="checkbox-1" />1 </label>
                </div>
            </div>
            <div class="group">
             <div class="left">input：</div>
             <div class="right">
               <input type="text" name="input1" placeholder="正常" />
               <input type="text" name="input2" value="已禁用" disabled />
             </div>
            </div>
            <div class="group">
             <div class="left">textarea：</div>
             <div class="right">
              <textarea name="textarea"></textarea>
             </div>
            </div>
            <div class="group">
             <div class="left">select：</div>
             <div class="right">
              <select name="select" style="width: 100px;">
               <option value="1">value=1</option>
               <option value="2">value=2</option>
              </select>
             </div>
            </div>
            <div><input type="button" id="fun1" value="转换1" /> <input id="fun2" type="button" value="转换2" /></div>
            <div style="color: red;">注意：disabled的input没有显示出来</div>
            <div>结果1：</div><div id="result1"></div>
            <div>结果2：</div><div id="result2"></div>
        </form>
        <script src="http://asset.jdk5.com/js/lib/jquery.js"></script>
        <script src="http://asset.jdk5.com/js/lib/json.js"></script>
        <script type="text/javascript">
         $(function (){
          $.fn.serializeObject = function(){
        var o = {};
        var a = this.serializeArray();
        $.each(a, function() {
            if (o[this.name] !== undefined) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return o;
    }
    $("#fun1").click(function (){
        var data = {};
     $("form").serializeArray().map(function(x){
      if (data[x.name] !== undefined) {
                if (!data[x.name].push) {
                    data[x.name] = [data[x.name]];
                }
                data[x.name].push(x.value || '');
            } else {
                data[x.name] = x.value || '';
            }
     });
     $("#result1").html(JSON.stringify(data));
       });
       $("#fun2").click(function (){
        var data = $("form").serializeObject();
        $("#result2").html(JSON.stringify(data));
       });
         });
        </script>
    </body>
</html>


```
