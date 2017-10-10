# jstree 插件的使用
---



需要的文件
```html
<script src="https://magicbox.bkclouds.cc/static_api/v3/assets/js/jquery-1.10.2.min.js"></script>
<script src="https://magicbox.bkclouds.cc/static_api/v3/assets/jstree-3.1.1/dist/jstree.min.js"></script>
```


使用方法

1、HTML中直接导入数据： 节点配置可以添加json字符串到data-jstree属性；
```html
<div id="html">
    <ul>
        <li data-jstree='{ "opened" : true }'>Root node
            <ul>
                <li>Child node 1
                    <ul>
                        <li>Child node a</li>
                        <li>Child node b</li>
                    </ul>
                </li>
            </ul>
        </li>
    </ul>
</div>
$('#html').jstree();
```



2、通过JavaScript代码导入数据：
```html
<!-- 建立一个div容器 -->
<div id="frmt"></div>
// 节点状态：open-打开 selected-选中 disabled-禁用
$('#frmt').jstree({
    'core' : {
        'data' : [{
                "text" : "Root node",
                "state" : { "opened" : true },
                "children" : [
                        {"text" : "Child node 1","state" : { "selected" : true },"icon" : "jstree-file"},
                        { "text" : "Child node 2", "state" : { "disabled" : true } }
                    ]
                }]
            }
});
```
3、通过外部文件导入数据：
```html
<!-- 建立一个div容器 -->
<div id="ajax"></div>
$('#ajax').jstree({
    'core' : {
        'data' : {
            "url" : "https://magicbox.bkclouds.cc/static_api/v3/assets/jstree-3.1.1/demo/basic/root.json",
            "dataType" : "json" 
        }
    }
});
```

### 配置参数

`core`: 
类型 Object, 
核心对象，可以传入数列表的数据以及设置其他基本配置参数
- 'data' 可以是数值、对象或方法，树列表的数据
- 'animation' 数值，默认运动时间200(s)
- 'themes' 对象，设置数列表的样式如{'variant' : 'large'}
- 'multiple' 布尔值，是否支持多选

### 事件回调

```js
$('#evts').jstree({
    'core' : {
        'multiple' : false,
        'data' : [
            { "text" : "Root node", "children" : [
                    { "text" : "Child node 1", "id" : 1 },
                    { "text" : "Child node 2" }
            ]}
        ]
      }
    }).on("changed.jstree", function (e, data) {
        if(data.selected.length) {
            alert('The selected node is: ' + data.instance.get_node(data.selected[0]).text);
        }
    });
```

`change.jstree`: 用户选择树节点时触发此回调函数

`close_node.jstree`   关闭节点时触发此回调函数    参照示例代码
`open_node.jstree`    打开节点时触发此回调函数    参照示例代码
`ready.jstree `   树数据初始化完成时触发此回调函数


### 配置css
1, 在html上更改
```
    <li data-jstree='{ "opened" : true, "icon":"fa fa-arrow-circle-down"}'></li>
```

2, js上
添加`"icon":"fa fa-arrow-circle-down"}` 属性

### 单/双击事件 

这种方式可能失效

```
 .bind('click.jstree', function(event) {               
        var eventNodeName = event.target.nodeName;               
            if (eventNodeName == 'INS') {                   
                return;               
            } else if (eventNodeName == 'A') {                   
                var $subject = $(event.target).parent();                   
                if ($subject.find('ul').length > 0) {            
                } else { 
                  //选择的id值
                   alert($(event.target).parents('li').attr('id'));                   
                }               
            }           
    })
//双击  确定jstree.js中已经添加双击事件
    .bind('dblclick.jstree',function(event){
      
    });
});
```

```
//tree change时事件  
$('#treeview1').on("changed.jstree", function (e, data) {  
    console.log("The selected nodes are:");  
    console.log(data.node.id);               //选择的node id  
    console.log(data.node.text);            //选择的node text  
  
    form_data.ay = data.node.text;  
    form_data.ay_id = data.node.id;  
  
});  
```


## 插件

### contextmenu

```js
"contextmenu":{         
    "items": function($node) {
        var tree = $("#tree").jstree(true);
        return {
            "Create": {
                "separator_before": false,
                "separator_after": false,
                "label": "Create",
                "action": function (obj) { 
                    $node = tree.create_node($node);
                    tree.edit($node);
                }
            },
            "Rename": {
                "separator_before": false,
                "separator_after": false,
                "label": "Rename",
                "action": function (obj) { 
                    tree.edit($node);
                }
            },                         
            "Remove": {
                "separator_before": false,
                "separator_after": false,
                "label": "Remove",
                "action": function (obj) { 
                    tree.delete_node($node);
                }
            }
        };
    }
}

```

https://www.jstree.com/

