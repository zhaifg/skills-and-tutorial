# javascript操作Dom常用API总结
---

## 基本概念

### Node 类型
DOM1级定义了一个Node 接口, 该接口由DOM中的所有节点类型实现. 这个 NODE 接口在JS中是作为Node类型实现的. 在IE9 以下 版本无法访问到这个类型, js中所有节点都是继承自Node类型, 都共享着相同的 基本属性和方法.

Node 有一个属性nodeType 表示 Node 的类型, 他是个整数, 其数值分别表示相应的 Node 类型, 具有如下:

`Node.ELEMENT_NODE`:1
`Node.ATTRIBUTE_NODE`:2
`Node.TEXT_NODE`:3
`Node.CDATA_SECTION_NODE`:4
`Node.ENTITY_REFERENCE_NODE`:5
`Node.ENTITY_NODE`:6
`Node.PROCESSING_INSTRUCTION_NODE`:7
`Node.COMMENT_NODE`:8
`Node.DOCUMENT_NODE`:9
`Node.DOCUMENT_TYPE_NODE`:10
`Node.DOCUMENT_FRAGMENT_NODE`:11
`Node.NOTATION_NODE`:12

假设我们要判断一个Node是不是元素, 我可以这样判断
```
if(someNode.NodeType == 1){
    console.log("Node is  a element")
}
```

Node的类型中, 最常用的是 element, text, attribute, comment, document, document_fragment这几种类型

### Element 例行
提供了对元素标签名, 子节点和特性访问, 我们常用于HTML元素比如 DIV, span, a 等标签就是element的一种, Element 几种特性:
1. nodeType 为 1
2. nodeName 为元素的标签名, tagName也是返回标签名
3. nodeValue 为 null
4. parentNode 可能是Document或 Element
5. 子节点可能是Element, text, Comment, Processing_instruction, CDATASection或者EntiyReference


### Text类型
表示文本节点, 它包含是纯文本内容,不包含html代码, 但可以包含转义后的html 代码 
1. nodeType 为 3
2. nodeName 为 #Text
3. nodeValue 为 文本内容
4. parentNode 是一个Element
5. 没有子节点

### Attr 类型
元素特性, 相当于的元素的 attributes属性中节点, 
1. nodeType 2
2. nodeName 是特性的名称
3. nodeValue是特性的值
4. parentNode 为null

### Comment 类型
文档中注释
1. nodeType 8
2. nodeName 为 #comment
3. nodeValue 为 注释的内容
4. parentNode 可能是Document 或者Element
5. 没有子节点

### Document
表示文档, 在浏览器中, Document对象是HTMLDocument 的一个实例, 表示整个页面, 同时他也是window 对象的一个属性, 
1. nodeType 9
2. nodeName 为 #document
3. nodeVaule 为 null
4. parentNode 为 null
5. 子节点可能是 DocumentType 或者 Element

### DocumentFragment
是所有节点唯一一个没有对应标记的类型, 它表示一种轻量级的文档, 可能是当做一个临时的仓库用来保存可能会添加到文档中的节点,
1. nodeType 为 11
2. nodeName #document-fragment
3. nodeValue 为 null
4. parentNode 为 null


> html 中节点并不只是包括元素节点, 它包括文本节点, 注释节点等


## 节点创建API
### createElement
createELement 通过传入一个指定的标签名创建一个元素, 如果传入的标签名是一个未知的, 则会创建一个自定义的标签

```js
var div = document.createElement("div");
```

使用createElemnt 创建出来的元素, 并不属于文档, 需要使用appendChild 或者insertBefore等方法将其添加到HTML 文档中.

### createTextNode
```js
var textNode = document.createTextNode("xxxsdfasdf");
```
createTextNode接收一个参数，这个参数就是文本节点中的文本，和createElement一样，创建后的文本节点也只是独立的一个节点，同样需要appendChild将其添加到HTML文档树中

### cloneNode
cloneNode是用来返回调用方法的节点的一个副本，它接收一个bool参数，用来表示是否复制子元素，使用如下：

```js
var parent = document.getElementById("parentElement"); 
var parent2 = parent.cloneNode(true);// 传入true
parent2.id = "parent2";
```

这段代码通过cloneNode复制了一份parent元素，其中cloneNode的参数为true，表示parent的子节点也被复制，如果传入false，则表示只复制了parent节点。
```html
<div id="parent">
    I am parent element
    </br>
    <span>I am child element</span>
</div>
<button id="btnCopy">copy</button>
<script type="text/javascript">
    var parent = document.getElementById('parent');
    document.getElementById("btnCopy").onclik = function(){
        var parent2 = parent.cloneNode(true);
        parent2.id = 'parent2';
        document.body.appendChild(parent2);
    }
</script>

```

这段代码很简单，主要是绑定button事件，事件内容是复制了一个parent，修改其id，然后添加到文档中。
这里有几点要注意：
1. 和createElement一样，cloneNode创建的节点只是游离有html文档外的节点，要调用appendChild方法才能添加到文档树中
2. 如果复制的元素有id，则其副本同样会包含该id，由于id具有唯一性，所以在复制节点后必须要修改其id
3. 调用接收的bool参数最好传入，如果不传入该参数，不同浏览器对其默认值的处理可能不同

除此之外，我们还有一个需要注意的点：
如果被复制的节点绑定了事件，则副本也会跟着绑定该事件吗？这里要分情况讨论：
1. 如果是通过addEventListener或者比如onclick进行绑定事件，则副本节点不会绑定该事件
2. 如果是内联方式绑定比如

```
<div onclick="showParent()"></div>
```
这样的话，副本节点同样会触发事件。


### createDocumentFragment

createDocumentFragment方法用来创建一个DocumentFragment。在前面我们说到DocumentFragment表示一种轻量级的文档，它的作用主要是存储临时的节点用来准备添加到文档中。
createDocumentFragment方法主要是用于添加大量节点到文档中时会使用到。假设要循环一组数据，然后创建多个节点添加到文档中，比如示例
```
<ul id="list"></ul>
<input type="button" value="添加多项" id="btnAdd" />

document.getElementById("btnAdd").onclick = function(){
    var list = document.getElementById("list");
    for(var i = 0;i < 100; i++){
        var li = document.createElement("li");
        li.textContent = i;
        list.appendChild(li);
    }
}
```
这段代码将按钮绑定了一个事件，这个事件创建了100个li节点，然后依次将其添加HTML文档中。这样做有一个缺点：每次一创建一个新的元素，然后添加到文档树中，这个过程会造成浏览器的回流。所谓回流简单说就是指元素大小和位置会被重新计算，如果添加的元素太多，会造成性能问题。这个时候，就是使用createDocumentFragment了。
DocumentFragment不是文档树的一部分，它是保存在内存中的，所以不会造成回流问题。我们修改上面的代码如下：

```js
document.getElementById("btnAdd").onclick = function(){
    var list = document.getElementById("list"); 
    var fragment = document.createDocumentFragment();

    for(var i = 0;i < 100; i++){
      var li = document.createElement("li");
        li.textContent = i;
        fragment.appendChild(li);
    }

    list.appendChild(fragment);
}
```

优化后的代码主要是创建了一个fragment，每次生成的li节点先添加到fragment，最后一次性添加到list，大家可以看示例

### 创建型API总结

创建型api主要包括createElement，createTextNode，cloneNode和createDocumentFragment四个方法，需要注意下面几点：
（1）它们创建的节点只是一个孤立的节点，要通过appendChild添加到文档中
（2）cloneNode要注意如果被复制的节点是否包含子节点以及事件绑定等问题
（3）使用createDocumentFragment来解决添加大量节点时的性能问题


### 页面修改型API
appendChild，insertBefore，removeChild，replaceChild

#### appendChild
`parent.appendChild(child);`
appendChild这个方法很简单，但是还有有一点需要注意：如果被添加的节点是一个页面中存在的节点，则执行后这个节点将会添加到指定位置，其原本所在的位置将移除该节点，也就是说不会同时存在两个该节点在页面上，相当于把这个节点移动到另一个地方
```
<div id="child">
    要被添加的节点
</div>
<br/>
<br/>
<br/>
<div id="parent">
    要移动的位置
</div>      
<input id="btnMove" type="button" value="移动节点" />

document.getElementById("btnMove").onclick = function(){
    var child = document.getElementById("child");
    document.getElementById("parent").appendChild(child);
}
```

这段代码主要是获取页面上的child节点，然后添加到指定位置，可以看到原本的child节点被移动到parent中了。
这里还有一个要注意的点：如果child绑定了事件，被移动时，它依然绑定着该事件。

#### insertBefore

insertBefore用来添加一个节点到一个参照节点之前，用法如下：

`parentNode.insertBefore(newNode,refNode);`
`parentNode` 表示新节点被添加后的父节点
`newNode` 表示要添加的节点
`refNode` 表示参照节点，新节点会添加到这个节点之前
我们来看这个例子

```html
<div id="parent">
    父节点
    <div id="child">                
        子元素
    </div>
</div>
<input type="button" id="insertNode" value="插入节点" />
<script type="text/javascript">
var parent = document.getElementById("parent");
var child = document.getElementById("child");
document.getElementById("insertNode").onclick = function(){
    var newNode = document.createElement("div");
    newNode.textContent = "新节点"
    parent.insertBefore(newNode,child);
}
</script>
```
这段代码创建了一个新节点，然后添加到child节点之前。
和appendChild一样，如果插入的节点是页面上的节点，则会移动该节点到指定位置，并且保留其绑定的事件。

关于第二个参数参照节点还有几个注意的地方：
1. refNode是必传的，如果不传该参数会报错
2. 如果refNode是undefined或null，则insertBefore会将节点添加到子元素的末尾

#### removeChild

removeChild顾名思义，就是删除指定的子节点并返回，用法如下：

`var deletedChild = parent.removeChild(node);`
deletedChild 指向被删除节点的引用，它等于node，被删除的节点仍然存在于内存中，可以对其进行下一步操作。

>如果被删除的节点不是其子节点，则程序将会报错。我们可以通过下面的方式来确保可以删除：

```js
if(node.parentNode){
    node.parentNode.removeChild(node);
}
```
通过节点自己获取节点的父节点，然后将自身删除。

#### replaceChild

replaceChild用于使用一个节点替换另一个节点，用法如下

`parent.replaceChild(newChild,oldChild);`

`newChild` 是替换的节点，可以是新的节点，也可以是页面上的节点，如果是页面上的节点，则其将被转移到新的位置

`oldChild` 是被替换的节点

### 页面修改型API总结

页面修改型api主要是这四个接口，要注意几个特点：
1. 不管是新增还是替换节点，如果新增或替换的节点是原本存在页面上的，则其原来位置的节点将被移除，也就是说同一个节点不能存在于页面的多个位置
2. 节点本身绑定的事件会不会消失，会一直保留着。

### 节点查询型API
节点查询型API也是非常常用的api，下面我们分别说明一下每一个api的使用。

#### document.getElementById

这个接口很简单，根据元素id返回元素，返回值是Element类型，如果不存在该元素，则返回null。
使用这个接口有几点要注意：
1. 元素的Id是大小写敏感的，一定要写对元素的id
2. HTML文档中可能存在多个id相同的元素，则返回第一个元素
3. 只从文档中进行搜索元素，如果创建了一个元素并指定id，但并没有添加到文档中，则这个元素是不会被查找到的

#### document.getElementsByTagName

这个接口根据元素标签名获取元素，返回一个即时的HTMLCollection类型，什么是即时的HTMLCollection类型呢？我们来看看这个示例
```html
<div>div1</div>
<div>div2</div>
        
<input type="button" value="显示数量" id="btnShowCount"/>
<input type="button" value="新增div" id="btnAddDiv"/> 
<script type="text/javascript">

    var divList = document.getElementsByTagName("div");
    document.getElementById("btnAddDiv").onclick = function(){
        var div = document.createElement("div");
        div.textContent ="div" + (divList.length+1);
        document.body.appendChild(div);
    }
        
    document.getElementById("btnShowCount").onclick = function(){
            alert(divList.length);
    }
</script>
```
这段代码中有两个按钮，一个按钮是显示HTMLCollection元素的个数，另一个按钮可以新增一个div标签到文档中。前面提到HTMLCollcetion元素是即时的表示该集合是随时变化的，也就是是文档中有几个div，它会随时进行变化，当我们新增一个div后，再访问HTMLCollection时，就会包含这个新增的div。
使用document.getElementsByTagName这个方法有几点要注意：
1. 如果要对HTMLCollection集合进行循环操作，最好将其长度缓存起来，因为每次循环都会去计算长度，暂时缓存起来可以提高效率
2. 如果没有存在指定的标签，该接口返回的不是null，而是一个空的HTMLCollection
3. “*”表示所有标签


#### document.getElementsByName

getElementsByName 主要是通过指定的name属性来获取元素，它返回一个即时的NodeList对象。
使用这个接口主要要注意几点：
1. 返回对象是一个即时的NodeList，它是随时变化的
2. 在HTML元素中，并不是所有元素都有name属性，比如div是没有name属性的，但是如果强制设置div的name属性，它也是可以被查找到的
3. 在IE中，如果id设置成某个值，然后传入getElementsByName的参数值和id值一样，则这个元素是会被找到的，所以最好不好设置同样的值给id和name

#### document.getElementsByClassName

这个API是根据元素的class返回一个即时的HTMLCollection，用法如下

`var elements = document.getElementsByClassName(names);`

这个接口有下面几点要注意：
1. 返回结果是一个即时的HTMLCollection，会随时根据文档结构变化
2. IE9以下浏览器不支持
3. 如果要获取2个以上classname，可传入多个classname，每个用空格相隔，例如
```js

var elements = document.getElementsByClassName("test1 test2");
```

#### document.querySelector 和document.querySelectorAll
这两个api 很相似, 通过css 选择器来查找元素, 注意选择器要符合css选择的规则

首先来介绍一下 document.querySector 返回第一个匹配的元素, 如果配有匹配, 则返回null

```html
<div>
    <div>
        <span class="test">第三级的span</span>  
    </div>
</div>
<div class="test">          
    同级的第二个div
</div>
<input type="button" id="btnGet" value="获取test元素" />
<script type="text/javascript">
    document.getElementById("btnGet").addEventListener("click",function(){
    var element = document.querySelector(".test");
    alert(element.textContent);
})
</script>

```
这个例子很简单，就是两个class都包含“test”的元素，一个在文档树的前面，但是它在第三级，另一个在文档树的后面，但它在第一级，通过querySelector获取元素时，它通过深度优先搜索，拿到文档树前面的第三级的元素。

document.querySelectorAll的不同之处在于它返回的是所有匹配的元素，而且可以匹配多个选择符，我们来看看下面这个例子

```html
<div class="test">
    class为test
</div>
<div id="test">
    id为test
</div>
<input id="btnShow" type="button" value="显示内容" />
<script type="text/javascript">
    document.getElementById("btnShow").addEventListener("click",function(){
    var elements = document.querySelectorAll("#test,.test");    
    for(var i = 0,length = elements.length;i<length;i++){
        alert(elements[i].textContent);
    }   
})
</script>

```

这段代码通过querySelectorAll，使用id选择器和class选择器选择了两个元素，并依次输出其内容。要注意两点：
1. querySelectorAll也是通过深度优先搜索，搜索的元素顺序和选择器的顺序无关
2. 返回的是一个非即时的NodeList，也就是说结果不会随着文档树的变化而变化

兼容性问题：querySelector和querySelectorAll在ie8以下的浏览器不支持。


### 节点关系型api

在html文档中的每个节点之间的关系都可以看成是家谱关系，包含父子关系，兄弟关系等等，下面我们依次来看看每一种关系。

#### 父关系型api

`parentNode` : 每个节点都有一个parentNode属性，它表示元素的父节点。Element的父节点可能是Element，Document或DocumentFragment。
`parentElement` ：返回元素的父元素节点，与parentNode的区别在于，其父节点必须是一个Element，如果不是，则返回null

#### 兄弟关系型api

previousSibling：节点的前一个节点，如果该节点是第一个节点，则为null。注意有可能拿到的节点是文本节点或注释节点，与预期的不符，要进行处理一下。
previousElementSibling：返回前一个元素节点，前一个节点必须是Element，注意IE9以下浏览器不支持。

`nextSibling` ：节点的后一个节点，如果该节点是最后一个节点，则为null。注意有可能拿到的节点是文本节点，与预期的不符，要进行处理一下。 

`nextElementSibling`： 返回后一个元素节点，后一个节点必须是Element，注意IE9以下浏览器不支持。

#### 子关系型api

`childNodes` ：返回一个即时的NodeList，表示元素的子节点列表，子节点可能会包含文本节点，注释节点等。
`children` ：一个即时的HTMLCollection，子节点都是Element，IE9以下浏览器不支持。
`firstNode` ：第一个子节点
`lastNode` ：最后一个子节点
`hasChildNodes` 方法：可以用来判断是否包含子节点


### 元素属性型api
#### setAttribute
根据名称和值修改元素的特性
`element.setAttribute(name, value)`

其中name是特性名，value是特性值。如果元素不包含该特性，则会创建该特性并赋值。
如果元素本身包含指定的特性名为属性，则可以世界访问属性进行赋值，比如下面两条代码是等价的：
```js
element.setAttribute("id", "test");
element.id = "test";
```

#### getAttribute

getAttribute返回指定的特性名相应的特性值，如果不存在，则返回null或空字符串。用法如下：
```
var value = element.getAttribute("id");
```

### 元素样式型api

#### window.getComputedStyle
用来获取应用到元素后的样式, 假设某个元素并未设置高度而是通过其内容将其高度撑开, 这时要获取它的高度就要用到getComputeStyle.
`var style = window.getComputeStyle(element[, paseudoElt])`

element是要获取的元素，pseudoElt指定一个伪元素进行匹配。
返回的style是一个CSSStyleDeclaration对象。
通过style可以访问到元素计算后的样式

#### getBoundingClientRect

getBoundingClientRect用来返回元素的大小以及相对于浏览器可视窗口的位置，用法如下
```js
var clientRect = element.getBoundingClientRect();
clientRect是一个DOMRect对象，包含left，top，right，bottom，
```
它是相对于可视窗口的距离，滚动位置发生改变时，它们的值是会发生变化的。除了IE9以下浏览器，还包含元素的height和width等数据，具体可查看链接

http://luopq.com/2015/11/30/javascript-dom/
