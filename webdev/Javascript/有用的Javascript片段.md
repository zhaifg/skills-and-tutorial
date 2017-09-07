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


###  使用jQuery 去的checkbox的选中元素
```
$("input[name='chockbname']:checkbox:checked").each()
```
(全选、反选、获得所有选中的checkbox)[http://www.cnblogs.com/0201zcr/p/4704468.html]
(jquery的checkbox,radio,select等方法总结)[http://www.haorooms.com/post/checkandselect]


## jQuery 处理表单中的radio, select和option
### radio
```html
<input type="radio" name="radio" id="radio1" value="1" />1    
<input type="radio" name="radio" id="radio2" value="2" />2    
<input type="radio" name="radio" id="radio3" value="3" />3    
<input type="radio" name="radio" id="radio4" value="4" />4  
```

```javascript
$("input[type='radio'][name='radio']:checked").length == 0 //"没有任何单选框被选中" : "已经有选中";    

$('input[type="radio"][name="radio"]:checked').val(); // 获取一组radio被选中项的值    

$("input[type='radio'][name='radio'][value='2']").attr("checked", "checked");// 设置value = 2的一项为选中    

$("#radio2").attr("checked", "checked"); // 设置id=radio2的一项为选中  

$("input[type='radio'][name='radio']").get(1).checked = true; // 设置index = 1，即第二项为当前选中    

var isChecked = $("#radio2").attr("checked");// id=radio2的一项处于选中状态则isChecked = true, 否则isChecked = false;   

var isChecked = $("input[type='radio'][name='radio'][value='2']").attr("checked");// value=2的一项处于选中状态则isChecked = true, 否则isChecked = false; 
```

### checkbox
```html
<input type="checkbox" name="checkbox" id="checkAll" />全选/取消全选    
<input type="checkbox" name="checkbox" id="checkbox_id1" value="1" />1    
<input type="checkbox" name="checkbox" id="checkbox_id2" value="2" />2    
<input type="checkbox" name="checkbox" id="checkbox_id3" value="3" />3    
<input type="checkbox" name="checkbox" id="checkbox_id4" value="4" />4    
<input type="checkbox" name="checkbox" id="checkbox_id5" value="5" />5
```


```javascript
var val = $("#checkbox_id1").val();// 获取指定id的复选框的值    
var isSelected = $("#checkbox_id3").attr("checked"); // 判断id=checkbox_id3的那个复选框是否处于选中状态，选中则isSelected=true;否则isSelected=false;  

$("#checkbox_id3").attr("checked", true);// or    
$("#checkbox_id3").attr("checked", 'checked');// 将id=checkbox_id3的那个复选框选中，即打勾    

$("#checkbox_id3").attr("checked", false);// or    
$("#checkbox_id3").attr("checked", '');// 将id=checkbox_id3的那个复选框不选中，即不打勾    

$("input[name=checkbox][value=3]").attr("checked", 'checked');// 将name=checkbox, value=3 的那个复选框选中，即打勾    

$("input[name=checkbox][value=3]").attr("checked", '');// 将name=checkbox, value=3 的那个复选框不选中，即不打勾    

$("input[type=checkbox][name=checkbox]").get(2).checked = true;// 设置index = 2，即第三项为选中状态    

$("input[type=checkbox]:checked").each(function(){ //由于复选框一般选中的是多个,所以可以循环输出选中的值    
    alert($(this).val());    
});    
// 全选/取消全选    
$(function() {    
    $("#checkAll").click(function(){    
            if($(this).attr("checked") == true){// 全选    
                $("input[type=checkbox][name=checkbox]").each(function(){    
                        $(this).attr("checked", true);    
                    });    
            } else {// 取消全选    
                $("input[type=checkbox][name=checkbox]").each(function(){    
                    $(this).attr("checked", false);    
                });    
            }    
        });    
});
```

### select

```html
<select name="select" id="select_id" style="width: 100px;">    
    <option value="1">11</option>    
    <option value="2">22</option>    
    <option value="3">33</option>    
    <option value="4">44</option>    
    <option value="5">55</option>    
    <option value="6">66</option>    
</select>  
```

```javascript

/**  
 * jQuery获取select的各种值  
 */    
jQuery("#select_id").change(function(){                         // 1.为Select添加事件，当选择其中一项时触发     
    //code...    
});    

var checkValue = jQuery("#select_id").val();                    // 2.获取Select选中项的Value   

var checkText = jQuery("#select_id :selected").text();          // 3.获取Select选中项的Text     

var checkIndex = jQuery("#select_id").attr("selectedIndex");    // 4.获取Select选中项的索引值,或者：jQuery("#select_id").get(0).selectedIndex;   

var maxIndex = jQuery("#select_id :last").attr("index");        // 5.获取Select最大的索引值,或者：jQuery("#select_id :last").get(0).index;    


/**  
 * jQuery设置Select的选中项  
 */    
jQuery("#select_id").get(0).selectedIndex = 1;                  // 1.设置Select索引值为1的项选中    
jQuery("#select_id").val(4);                                    // 2.设置Select的Value值为4的项选中    
/**  
 * jQuery添加/删除Select的Option项  
 */    
jQuery("#select_id").append("<option value='新增'>新增option</option>");    // 1.为Select追加一个Option(下拉项)     
jQuery("#select_id").prepend("<option value='请选择'>请选择</option>");   // 2.为Select插入一个Option(第一个位置)    
jQuery("#select_id").get(0).remove(1);                                      // 3.删除Select中索引值为1的Option(第二个)    
jQuery("#select_id :last").remove();                                        // 4.删除Select中索引值最大Option(最后一个)     
jQuery("#select_id [value='3']").remove();                                  // 5.删除Select中Value='3'的Option     
jQuery("#select_id").empty();                                               // 6.清空下拉列表    
```
