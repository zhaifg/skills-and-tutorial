#有用的Javascript片段
---
## 1. 全选,反选

### 1. js实现

`全选和全不选`
第一个参数为复选框名称，第二个参数为是全选还是全部不选。
```javascript
function allCheck(name,boolValue) {  
    var allvalue = document.getElementsByName(name);   
    for (var i = 0; i < allvalue.length; i++) {        
        if (allvalue[i].type == "checkbox")             
            allvalue[i].checked = boolValue;             
    }  
}  
```

`反选`
 参数为复选框名称

```javascript
function reserveCheck(name){  
    var revalue = document.getElementsByName(name);   
    for(i=0;i<revalue.length;i++){  
        if(revalue[i].checked == true)   
            revalue[i].checked = false;  
        else   
            revalue[i].checked = true;  
    }  
}
```

```html
  <input type="radio" name="all" id="all" onclick="checkAll('test')" />  
    全选  
    <input type="radio" name="all" id="Checkbox1" onclick="uncheckAll('test')" />  
    全不选  
    <input type="radio" name="all" id="Checkbox2" onclick="switchAll('test')" />  
    反选<br /> 
```

### JQuery实现
```html

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">  
<html>  
<head>  
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">  
<meta http-equiv="pragma" content="no-cache">  
<meta http-equiv="cache-control" content="no-cache">  
<meta http-equiv="expires" content="0">  
<script type="text/javascript" src="./res/js/jquery-1.8.2.js">  
</script>  
<title>JQuery实现checkbox全选，反选，全不选</title>  
<script type="text/javascript">  
  
      
    //复选框选择  
    function checkboxOnclick(){  
        if($("[name='test'][checked]").length>1){  
            $("input[name='test']").each(function(){  
                $(this).attr("checked",false);  
            });    
        }else{  
            $("input[name='test']").each(function(){  
                $(this).attr("checked",true);  
            });    
        }  
    }  
      
    //获取选中复选框的值，一般在批量删除时需要使用  
    function getCheckBoxValues(){  
        var idsStr="";  
        $("input[name='test']").each(function(){  
            if($(this).attr("checked") == "checked"){  
                if($(this).val()!=""){  
                    idsStr+=$(this).val()+",";  
                }  
            }  
        });  
        if(idsStr!=""){  
            //进行删除  
            alert(idsStr);  
        }else{  
            alert("请选择需要删除的记录!");  
        }  
          
    }  
</script>  
</head>  
<body>  
      
    <input name="test" value="" type="checkbox" onclick="checkboxOnclick()" /> 复选框 <br />  
    <input name="test" value="1" type="checkbox" /> 1 <br />  
    <input name="test" value="2" type="checkbox" /> 2 <br />  
    <input name="test" value="3" type="checkbox" /> 3 <br />  
    <input name="test" value="4" type="checkbox" /> 4 <br />  
    <input name="test" value="5" type="checkbox" /> 5 <br />  
    <input name="test" value="6" type="checkbox" /> 6 <br />  
    <input type="button" value="获取选中复选框的值集合" onclick="getCheckBoxValues()">  
</body>  
</html>  
```
