## 基本语法和变量

var a = 1 + 3

var a, b
var a;
a = 1;

a // undefined

> 严格地说，var a = 1 与 a = 1，这两条语句的效果不完全一样，主要体现在delete命令无法删除前者。不过，绝大多数情况下，这种差异是可以忽略的。
> 

## 标识符
- 大小写敏感
- 第一个字符可以是任意Unicode字母,以及美元符号,下划线
- 第二个字符以后后米娜,除了Unicode字母,$,\_,还可以用数字0\-9_

下面这些都是合法的标识符。
```
arg0
_tmp
$elem
π
```
下面这些则是不合法的标识符。
```
1a  // 第一个字符不能是数字
23  // 同上
***  // 标识符不能包含星号
a+b  // 标识符不能包含加号
-d  // 标识符不能包含减号或连词线
中文是合法的标识符，可以用作变量名。
```
var 临时变量 = 1;


>如果只是声明变量而没有赋值，则该变量的值是undefined。undefined是一个JavaScript关键字，表示“无定义”。


> JavaScript有一些保留字，不能用作标识符：arguments、break、case、catch、class、const、continue、debugger、default、delete、do、else、enum、eval、export、extends、false、finally、for、function、if、implements、import、in、instanceof、interface、let、new、null、package、private、protected、public、return、static、super、switch、this、throw、true、try、typeof、var、void、while、with、yield。

另外，还有三个词虽然不是保留字，但是因为具有特别含义，也不应该用作标识符：Infinity、NaN、undefined。

`变量提升`  
JavaScript引擎的工作方式是，先解析代码，获取所有被声明的变量，然后再一行一行地运行。这造成的结果，就是所有的变量的声明语句，都会被提升到代码的头部，这就叫做变量提升


##  代码区块


　　　　{　var a = 1;　}
　
## if结构

```
if (expression)
    statement

```


>> 注意，if后面的表达式，不要混淆“赋值表达式”（=）与“严格相等运算符”（===）或“相等运算符”（==）。因为，“赋值表达式”不具有比较作用。

`if ...else`

```
if (m === 0) {
  // ...
} else if (m === 1) {
  // ...
} else if (m === 2) {
  // ...
} else {
  // ...
}
```


## switch结构

```
switch (fruit)
{
    case "banana":
    // ...
    break;
    case "apple":
    //...
    break;
    default :
    //...
}
```
>注意的是，每个case代码块内部的break语句不能少，否则会接下去执行下一个case代码块，而不是跳出switch结构。

> switch语句后面的表达式与case语句后面的表示式，在比较运行结果时，采用的是严格相等运算符（===），而不是相等运算符（==），这意味着比较时不会发生类型转换
>

```
var x = 1;

switch (x) {
  case true:
    console.log('x发生类型转换');
  default:
    console.log('x没有发生类型转换');
}
// x没有发生类型转换
```
上面代码中，由于变量x没有发生类型转换，所以不会执行case true的情况。这表明，switch语句内部采用的是“严格相等运算符”，详细解释请参考《运算符》一节。

## 循环语句

### while循环

```
while (expression)
    statement
```
while语句的循环条件是一个表达式(express), 必须放在圆括号. 

```
var  i=0;
while (i < 100)
{
    console.log('i is:' + i)
    i ++ ;
}
```
代码循环100次,直到i等于100为止

##for 循环
```
for (initialize; test; increment)
    statement

for(initialize; test; increment)
{

}
```
- 初始化表达式:  确定循环的初始值, 只在循环开始时执行一次.
- 测试表达式: 
- 递增表达式: 完成后续操作,然后返回上一步, 再一次检测循环条件.

```
var x = 3;
for(var i = 0; i < x; i++)
{
    console.log(i)
}
```
> 每次循环结束后，i增大1
> 

### do...while循环
do while 和while循环的区别就是先运行一次循环体,然后判断条件

```
do
    statement
while(expression)
```

### break continue


## label
javascript语言, 语句的前面有标签, 相当于定位符, 用于跳转到程序的任意位置.
```
label:
    statement
```

```
top: 
   for (var i = 0; i<3; i++)
   {
     for(var j= 0; j< 3; j++)
     {
        if (i===1 && j===1)  break top

        console.log(i+j)
     }
   }
```


代码为一个双重循环区块，break命令后面加上了top标签（注意，top不用加引号），满足条件时，直接跳出双层循环。如果break语句后面不使用标签，则只能跳出内层循环，进入下一次的外层循环。

continue语句也可以与标签配合使用。
```
top:
  for (var i = 0; i < 3; i++){
    for (var j = 0; j < 3; j++){
      if (i === 1 && j === 1) continue top;
      console.log('i=' + i + ', j=' + j);
  }
}
// i=0, j=0
// i=0, j=1
// i=0, j=2
// i=1, j=0
// i=2, j=0
// i=2, j=1
// i=2, j=2
```
上面代码中，continue命令后面有一个标签名，满足条件时，会跳过当前循环，直接进入下一轮外层循环。如果continue语句后面不使用标签，则只能进入下一轮的内层循环。

##  数据类型

`数值（number）`：整数和小数（比如1和3.14）
`字符串（string）`：字符组成的文本（比如"Hello World"）
`布尔值（boolean）`：true（真）和false（假）两个特定值
`undefined`：表示“未定义”或不存在，即此处目前没有任何值
`null`：表示空缺，即此处应该有一个值，但目前为空
`对象（object）`：各种值组成的集合


数值、字符串、布尔值称为`原始类型`（primitive type）的值，即它们是最基本的数据类型，不能再细分了。而将对象称为`合成类型`（complex type）的值，因为一个对象往往是多个原始类型的值的合成，可以看作是一个存放各种值的容器。至于`undefined`和`null`，一般将它们看成两个特殊值。


对象可以分成三个子类型

- 狭义的对象 (object)
- 数组对象 array
- 函数 function

数据类型。undefined和null两个特殊值和布尔类型Boolean比较简单，将在本节介绍，其他类型将各自有单独的一节。

## typeof运算

javascript 有三种方法,可以确定一个值到底是什么来类型

- typeof 运算符
- instanceof 运算符
- Object.prototype.toString 方法


### 原始类型
```
typeof 123 // number
typeof '123' // string
typeof false //boolean
```

### 函数
```
function f() {}
typeof f // function
```

### undefined
```
typeof undefined
//undefined

typeof null
//object
```

利用这一点，typeof可以用来检查一个没有声明的变量，而不报错。
```
v
// ReferenceError: v is not defined

typeof v
// "undefined"
```
实际编程中，这个特点通常用在判断语句。
```
// 错误的写法
if (v) {
  // ...
}
// ReferenceError: v is not defined

// 正确的写法
if (typeof v === "undefined") {
  // ...
}
```

### 其他

除此以外,其他情况都返回object

```
typeof window //oject
typeof {}
typeof []
typeof null

```

从上面代码可以看到，空数组（[]）的类型也是object，这表示在JavaScript内部，数组本质上只是一种特殊的对象。另外，null的类型也是object，这是由于历史原因造成的，为了兼容以前的代码，后来就没法修改了，并不是说null就属于对象，本质上null是一个类似于undefined的特殊值。

既然typeof对数组（array）和对象（object）的显示结果都是object，那么怎么区分它们呢？instanceof运算符可以做到。
```
var o = {};
var a = [];

o instanceof Array // false
a instanceof Array // true
```
instanceof运算符的详细解释，请见《面向对象编程》一章

#  null和undefined
null与undefined都可以表示'没有',含义非常相似.将一个变量赋值为undefined或null.
老实说,语法效果几乎没有区别.

```
var a = undefined
或
var a = null;
```
上面代码中, a变量分别被赋值为undefined和null,这两种写法的效果几乎等价.

if语句中,他们都会被自动转换为false,相等运算符(==)甚至直接报告两者相等.
```
if (!undefined)
{
   console.log('undefined is false')
}

// undefined is false

if (!null) {
  console.log('null is false');
}
// null is false

undefined == null
// true
```

### 用法和含义
null表示:
- 作为函数的参数, 表示该函数的参数是一个没有任何内容的对象.
- 作为对象原型链的终点.

undefined 表示不存在值,就是此处目前不存在任何值.
1. 变量被声明了, 但是没有赋值时,就等于undefined
2. 调用函数时, 应该提供的参数没有提供, 该参数等于undefined
3. 对象没有赋值的属性,该属性的值为undefined.
4. 函数没有返回值时,默认返回undefined.

```
var i ;
i  //undefined

function f(x)(console.log(x))
f() //undefined

var o = new Object()
o.p //undefined

var x = f();
x // undefined
```

## 布尔值
下列运算符返回布尔值
1. 两元逻辑运算符: &&(AND), ||(OR)
2. 前置逻辑运算符: !(Not)
3. 相等运算符: ===, !==, ==,!=
4. 比较运算符: >, >=, <, <=

视为false:
1. undefined
2. null
3. false
4. 0
5. NaN
6. ""

```
if ('') {
  console.log(true);
}
// 没有任何输出

```
>需要特别注意的是，空数组（[]）和空对象（{}）对应的布尔值，都是true


## 数据类型转换

### 强制转换
主要是Number,string和boolean三个构造函数,手动将各种类型的值, 转换成数字,字符串或者布尔值.

__Number函数__: 强制转换成数值.

- 1. 原是类型值的转换规则
1. 数值: 转换后还是原来的值
2. 字符串: 如果可以被解析为数值,则转换为相应的数值, 否则得到NaN.空字符串为0.
3. 布尔值: true转成1, false或者0
4. undefined: 转成NaN
5. null: 转成0

```
Number("324") // 324

Number("324abc") // NaN

Number("") // 0

Number(false) // 0

Number(undefined) // NaN

Number(null) // 0
```
Number函数将字符串转为数值，要比parseInt函数严格很多。基本上，只要有一个字符无法转成数值，整个字符串就会被转为NaN

```
parseInt('011') // 9
parseInt('42 cats') // 42
parseInt('0xcafebabe') // 3405691582

Number('011') // 11
Number('42 cats') // NaN
Number('0xcafebabe') // 3405691582

```
上面代码比较了Number函数和parsetInt函数, 区别主要在于parsetInt逐个解析字符,而
Number函数整体转换字符串的类型. 另外,Number会忽略八进制的前导0, 而parsetInt不会

Number函数会自动过滤一个字符串前导和后缀的空格。

    Number('\t\v\r12.34\n ')

- 2. 对象的转换规则
1. 先调用对象自身的valueOf方法, 如果该方法返回原始类型的值(数值,字符串和布尔值)
   ,则直接对该值使用Number方法, 不再进行后续步骤.
2. 如果valueOf方法返回符合类型的值,再调用对象的toString方法,如果toString方法返
   回原始类型的值,则对该值使用Number方法,不再进行后续步骤.
3. 如果toString方法返回的是符合类型的值,则报错.

```
Number({a:1})
//NaN
```
上面等于
```
if (typeof {a:1}.valueOf() == 'object')
{
    Number({a:1}.toString());
}
else
{
    Number({a:1}.valueOf())
}
```
上面代码的valueOf方法返回对象本身（{a:1}），所以对toString方法的返回值“[object Object]”使用Number方法，得到NaN。

如果toString方法返回的不是原始类型的值，结果就会报错。
```
var obj = {
    valueOf: function () {
            console.log("valueOf");
            return {};
    },
    toString: function () {
            console.log("toString");
            return {}; 
    }
};

Number(obj)
// TypeError: Cannot convert object to primitive value
```
上面代码的valueOf和toString方法，返回的都是对象，所以转成数值时会报错。

从上面的例子可以看出，valueOf和toString方法，都是可以自定义的。
```
Number({valueOf:function (){return 2;}})
// 2

Number({toString:function(){return 3;}})
// 3

Number({valueOf:function (){return 2;},toString:function(){return 3;}})
// 2
```
上面代码对三个对象使用Number方法。第一个对象返回valueOf方法的值，第二个对象返回toString方法的值，第三个对象表示valueOf方法先于toString方法执行。

- 2.String函数-强制转换成字符串
使用String函数,可以将任意类型的值转换成字符串.规则如下:

(1) 原始类型值的转化规则
1. 数值: 转换相应的字符串
2. 字符串: 转换后还是原来的值
3. 布尔值: true转换为'true', false转换为'false'
4. undefined: 转换"undefined"
5. null:转换'null'

```
String(123)  //"123"
String("abc")  //"abc"
String(true)  //"true"
String(undefined) // "undefined"
String(null) // "null"
```

(2) 对象的转换规则
如果将要对象转为字符串,则是采用一下步骤.

1. 先调用toString方法, 如果toString方法返回的是原始类型的值,则对该值直接使用
   String方法,不再进行一下步骤.
2. 如果toString方法放回的是符合类型的值,再调用valueOf方法,如果valueOf方法返回的
   是原始类型的值,则对该值使用String方法,不再进行以下步骤.
3. 如果valueOf方法返回的是复合类型的值,则报错.

String方法的这种过程正好与Number方法相反。
```
String({a:1})
// "[object Object]"
```
上面代码相当于下面这样。
```
String({a:1}.toString())
// "[object Object]"
```

如果toString方法和valueOf方法，返回的都不是原始类型的值，则String方法报错。
```
var obj = {
    valueOf: function () {
            console.log("valueOf");
            return {}; 
    },
    toString: function () {
            console.log("toString");
            return {}; 
    }
};

String(obj)
// TypeError: Cannot convert object to primitive value
```
下面是一个自定义toString方法的例子。
```
String({toString:function(){return 3;}})
// "3"

String({valueOf:function (){return 2;}})
// "[object Object]"

String({valueOf:function (){return 2;},toString:function(){return 3;}})
// "3"
```
上面代码对三个对象使用String方法。第一个对象返回toString方法的值（数值3），然后对其使用String方法，得到字符串“3”；第二个对象返回的还是toString方法的值
("[object Object]")，这次直接就是字符串；第三个对象表示toString方法先于valueOf
方法执行。

### Boolean函数：强制转换成布尔值
使用Boolean函数，可以将任意类型的变量转为布尔值。

- （1）原始类型值的转换方法

以下六个值的转化结果为false，其他的值全部为true。

> undefined
null
-0
+0
NaN
''（空字符串）

```
Boolean(undefined) // false
Boolean(null) // false

Boolean(0) // false

Boolean(NaN) // false

Boolean('') // false
```
- （2）对象的转换规则

所有对象的布尔值都是true，甚至连false对应的布尔对象也是true。
```
Boolean(new Boolean(false))
// true
```
请注意，空对象{}和空数组[]也会被转成true。
```
Boolean([]) // true

Boolean({}) // true
```

###自动转换
下面情况会自动转换:
1. 不同类型的数据进行相互运算.
2. 对非布尔类型的数据求布尔值
3. 对非数值类型的数据使用一元运算符(即"+"和"-").

#### 自动转换为布尔值
。

因此除了以下六个值，其他都是自动转为true：

> undefined
null
-0
+0
NaN
''（空字符串）
```
if (!undefined && !null && !0 && !NaN && !''){
    console.log('true');
}
// true
```

#### 自动转换为字符串
当JavaScript遇到预期为字符串的地方，就会将非字符串的数据自动转为字符串，转换规则与“强制转换为字符串”相同。

字符串的自动转换，主要发生在加法运算时。当一个值为字符串，另一个值为非字符串，则后者转为字符串。
```
'5' + 1 // '51'
'5' + true // "5true"
'5' + false // "5false"
'5' + {} // "5[object Object]"
'5' + [] // "5"
'5' + function (){} // "5function (){}"
'5' + undefined // "5undefined"
'5' + null // "5null"
```

#### 自动转换为数值
当JavaScript遇到预期为数值的地方，就会将参数值自动转换为数值，转换规则与“强制转换为数值”相同。

除了加法运算符有可能把运算子转为字符串，其他运算符都会把两侧的运算子自动转成数值

```
'5' - '2' // 3
'5' * '2' // 10
true - 1  // 0
false - 1 // -1
'1' - 1   // 0
'5'*[]    // 0
false/'5' // 0
'abc'-1   // NaN
```

> 上面都是二元算术运算符的例子，JavaScript的两个一元算术运算符——正号和负号——也会把运算子自动转为数值

```
+'abc' // NaN
-'abc' // NaN
+true // 1
-false // 0
```

###加法运算符的类型转化
加法运算符（+）需要特别讨论，因为它可以完成两种运算（加法和字符连接），所以不仅涉及到数据类型的转换，还涉及到确定运算类型。

####　三种情况
加法运算符(+)需要特别讨论.

* (1) 运算子之中存在字符串
两个运算子之中,只要有一个是字符串,则另一个不管是什么类型,都会被自动转换为字符串,然后执行字符串连接元算. 

* (2) 两个运算子都为数值或布尔值
这种情况下,执行加法元算,布尔值转为数值(true为1,false为0)
```
true + 5 //6
true + true //2
```

* (3)运算子之中存在对象
运算子之中存在对象(或者准确的说,存在非原始类型的值),则先调用该对象的valueOf方法
.如果返回结果为原是类型的值,则运用上面两条规则;否则继续调用该对象的toString方法
,对其返回值运用上面两条规则.
```
1+[1,2]
//"11,2"
```
上面的代码运行的顺序是，先调用[1,2].valueOf(), 结果还是数组[1,2]本身,则继续调用
[1,2].toString(),结果字符串"1,2",所以最终结果为字符串"11,2".
```
1+{a:1}
//"1[object, object]"
```
对象{a:1}的valueOf方法,返回的就是这个对象的本身,因此接着对它调用toString方法.
({a:1}).toString()默认返回的字符串"[object Object]",所以最终结果就是字符串
"1[object Object]"有趣的是,如果更换上面代码的运算自序,就会得到不同的值.
```
{a:1} + 1
// 1
```

原来此时，JavaScript引擎不将{a:1}视为对象，而是视为一个代码块，这个代码块没有返回值，所以被忽略。因此上面的代码，实际上等同于 {a:1};+1 ，所以最终结果就是1。为了避免这种情况，需要对{a:1}加上括号。
```
({a:1})+1
"[object Object]1"
```
将{a:1}放置在括号之中，由于JavaScript引擎预期括号之中是一个值，所以不把它当作代码块处理，而是当作对象处理，所以最终结果为“[object Object]1”。
```
1 + {valueOf:function(){return 2;}}
// 3
```
上面代码的valueOf方法返回数值2，所以最终结果为3。
```
1 + {valueOf:function(){return {};}}
// "1[object Object]"
```
上面代码的valueOf方法返回一个空对象，则继续调用toString方法，所以最终结果是“1[object Object]”。
```
1 + {valueOf:function(){return {};}, toString:function(){return 2;}}
// 3
```
上面代码的toString方法返回数值2（不是字符串），则最终结果就是数值3。
```
1 + {valueOf:function(){return {};}, toString:function(){return {};}}
// TypeError: Cannot convert object to primitive value
```
上面代码的toString方法返回一个空对象，JavaScript就会报错，表示无法获得原始类型的值。

### 四个特殊表达式

**(1) 空数组 +　空数组**
```
[] + []
```
首先，对空数组调用valueOf方法，返回的是数组本身；因此再对空数组调用toString方法，生成空字符串；所以，最终结果就是空字符串。

**(2) 空数组　+ 空对象**

    []+{}

这等同于空字符串与字符串“[object Object]”相加。因此，结果就是“[object Object]”。

**（3）空对象 + 空数组**

{} + []
// 0
JavaScript引擎将空对象视为一个空的代码块，加以忽略。因此，整个表达式就变成“+ []”，等于对空数组求正值，因此结果就是0。转化过程如下：

+ []
// Number([])
// Number([].toString())
// Number("")
// 0
如果JavaScript不把前面的空对象视为代码块，则结果为字符串“[object Object]”。

({}) + []
// "[object Object]"

**（4）空对象 + 空对象**

{} + {}
// NaN
JavaScript同样将第一个空对象视为一个空代码块，整个表达式就变成“+ {}”。这时，后一个空对象的ValueOf方法得到本身，再调用toSting方法，得到字符串“[object Object]”，然后再将这个字符串转成数值，得到NaN。所以，最后的结果就是NaN。转化过程如下：

+ {}
// Number({})
// Number({}.toString())
// Number("[object Object]")
如果，第一个空对象不被JavaScript视为空代码块，就会得到“[object Object][object Object]”的结果。

({}) + {}
// "[object Object][object Object]"

({} + {})
// "[object Object][object Object]"  

console.log({} + {})
// "[object Object][object Object]"

var a = {} + {};
a
// "[object Object][object Object]"
需要指出的是，对于第三和第四种情况，Node.js的运行结果不同于浏览器环境。

{} + {}
// "[object Object][object Object]"

{} + []
// "[object Object]"
可以看到，Node.js没有把第一个空对象视为代码块。原因是Node.js的命令行环境，内部执行机制大概是下面的样子：

eval.call(this,"(function(){return {} + {}}).call(this)")
Node.js把命令行输入都放在eval中执行，所以不会把起首的大括号理解为空代码块加以忽略


## 数组

定义:
```javascript
var arr = [1,2,3,4]
var arr = []
arr[0]=1
arr[1]=2

var colors = new Array(3);
var names = new Array("Grep", "Tom");

var arr = [
{a:1},
[1,2,3],
function(){return true}]
```

数组的本质
本质上，数组属于一种特殊的对象。typeof运算符会返回数组的类型是object。

typeof [1, 2, 3] // "object"

length

length属性是可写的。如果人为设置一个小于当前成员个数的值，该数组的成员会自动减少到length设置的值
```
var arr = [ 'a', 'b', 'c' ];
arr.length // 3

arr.length = 2;
arr // ["a", "b"]
```

`in运算符`
检查某个键名是否存在的运算符in，适用于对象，也适用于数组。

```
2 in [ 'a', 'b', 'c' ] // true
'2' in [ 'a', 'b', 'c' ] // true
```


`for…in循环和数组的遍历`
for...in循环不仅可以遍历对象，也可以遍历数组，毕竟数组只是一种特殊对象。
```
var a = [1, 2, 3];

for (var i in a) {
  console.log(a[i]);
}
// 1
// 2
// 3
```

`delete命令不影响length属性。`
```
var a = [1, 2, 3];
delete a[1];
delete a[2];
a.length // 3
```

### 栈方式:
LIFO
```
var colors = new Array()
var  count  = colors.push("red", "green")
alert(count) //2 被推入2个

var item = colors.pop();

```

FIFO
```
var colors = new Array()
var  count  = colors.push("red", "green")
alert(count) //2 被推入2个

var item = colors.shift(); //去的第一项
color.unshift("red", "green") // 在数组的前端添加
```

### 重新排序
`reverse()` 和 `sort()`

`conact()`连接数组
`slice()`切片
`splice()`:
  1. 删除: 可以删除任意数量的项. 只需要指定2个参数: 要删除的第一项的位置和要删除的项数.
  2. 插入: 可以向指定插入任意数量的项, 只需要提供3个参数: 起始位置,0(要删除的项数)和要插入的项;`splice(2,0,"red","green")`
  3. 替换: 可以向指定位置插入任意数量的项, 且同时删除任意数量的项, 只需要指定3个参数:起始位置,要删除的书和插入的任一数量的项.
```
var colors = ["red", "green", "blue"];
var colors2 = colors.concat("yellow", ["black", "brown"])

colors.slice(1)
colors.slice(1, 4)

```

### 位置方法
indexOf()
lastIndexOf()

### 迭代方法
`every()`: 对数组中的每一项运行给定函数, 如果该函数对每一项都返回true, 则返回true
`filter()`: 对数组中的每一项运行给定函数, 返回该函数返回true的项组成的数组.
`forEach()`: 对数组中的每一项运行给定函数. 这个函数没有返回值.
`map()`: 对数组中的每一项运行给定函数, 返回每次函数调用的结果组成的数组.
`some()`:对数组中的每一项运行给定函数, 如果该函数对任一项返回true, 则返回true.

```javascript
var  numbers  = [1,2,3,4,5,4,3,2,1];
var  everyResult = numbers.every(function(item, index, array){
      return (item > 2);
  })

  alert(everyResult) // false

var  someResult = numbers.some(function(item, index, array){
      return (item > 2);
  })
  alert(someResult); //true
```


### 缩小方法
`reduce()`
`reduceRight()`

## Object 类型
Object作为构造函数使用时，可以接受一个参数。如果该参数是一个对象，则直接返回这个对象；如果是一个原始类型的值，则返回该值对应的包装对象。

var o = new Object();
var o = {
  'p': 'ssss',
}
var 0 = Object.create(null)

检查所有属性
Object.keys(o)

object.property: 

Object的属性:
1.



## 函数
#### 函数的属性

1. name, f.name
2. length: 参数的个数
3. toString: 函数源码


函数的默认值
```javascript
function f(a){
  // a = a||1
  (a !== undefined && a !== null) ? a = a : a = 1;
  return a
}
```
### arguments对象
#### （1）定义

由于JavaScript允许函数有不定数目的参数，所以我们需要一种机制，可以在函数体内部读取所有参数。这就是arguments对象的由来。

arguments对象包含了函数运行时的所有参数，arguments[0]就是第一个参数，arguments[1]就是第二个参数，以此类推。这个对象只有在函数体内部，才可以使用。
```javascript
var f = function(one) {
  console.log(arguments[0]);
  console.log(arguments[1]);
  console.log(arguments[2]);
}

f(1, 2, 3)
// 1
// 2
// 3
```

arguments对象除了可以读取参数，还可以为参数赋值（严格模式不允许这种用法）。

    var f = function(a, b) {
      arguments[0] = 3;
      arguments[1] = 2;
      return a + b;
    }

    f(1, 1)
    // 5

可以通过arguments对象的length属性，判断函数调用时到底带几个参数。
```javascript
function f() {
  return arguments.length;
}

f(1, 2, 3) // 3
f(1) // 1
f() // 0
```

#### （2）与数组的关系

需要注意的是，虽然arguments很像数组，但它是一个对象。数组专有的方法（比如slice和forEach），不能在arguments对象上直接使用。

但是，可以通过apply方法，把arguments作为参数传进去，这样就可以让arguments使用数组方法了。
```
// 用于apply方法
myfunction.apply(obj, arguments).

// 使用与另一个数组合并
Array.prototype.concat.apply([1,2,3], arguments)
```
要让arguments对象使用数组方法，真正的解决方法是将arguments转为真正的数组。下面是两种常用的转换方法：slice方法和逐一填入新数组。
```
var args = Array.prototype.slice.call(arguments);

// or

var args = [];
for (var i = 0; i < arguments.length; i++) {
  args.push(arguments[i]);
}
```
#### （3）callee属性
arguments对象带有一个callee属性，返回它所对应的原函数。
```
var f = function(one) {
  console.log(arguments.callee === f);
}

f() // true
```
可以通过arguments.callee，达到调用函数自身的目的。这个属性在严格模式里面是禁用的，因此不建议使用。

### 立即调用的函数表达式（IIFE）
在Javascript中，一对圆括号()是一种运算符，跟在函数名之后，表示调用该函数。比如，print()就表示调用print函数。

有时，我们需要在定义函数之后，立即调用该函数。这时，你不能在函数的定义之后加上圆括号，这会产生语法错误。
```
function(){ /* code */ }();
// SyntaxError: Unexpected token (
产生这个错误的原因是，function这个关键字即可以当作语句，也可以当作表达式。

// 语句
function f() {}

// 表达式
var f = function f() {}
```
为了避免解析上的歧义，JavaScript引擎规定，如果function关键字出现在行首，一律解释成语句。因此，JavaScript引擎看到行首是function关键字之后，认为这一段都是函数的定义，不应该以圆括号结尾，所以就报错了。

解决方法就是不要让function出现在行首，让引擎将其理解成一个表达式。最简单的处理，就是将其放在一个圆括号里面。
```
(function(){ /* code */ }());
// 或者
(function(){ /* code */ })();
```
上面两种写法都是以圆括号开头，引擎就会认为后面跟的是一个表示式，而不是函数定义语句，所以就避免了错误。这就叫做“立即调用的函数表达式”（Immediately-Invoked Function Expression），简称IIFE。

注意，上面两种写法最后的分号都是必须的。如果省略分号，遇到连着两个IIFE，可能就会报错。
```
// 报错
(function(){ /* code */ }())
(function(){ /* code */ }())
```
上面代码的两行之间没有分号，JavaScript会将它们连在一起解释，将第二行解释为第一行的参数。

推而广之，任何让解释器以表达式来处理函数定义的方法，都能产生同样的效果，比如下面三种写法。
```
var i = function(){ return 10; }();
true && function(){ /* code */ }();
0, function(){ /* code */ }();
```
甚至像下面这样写，也是可以的。
```
!function(){ /* code */ }();
~function(){ /* code */ }();
-function(){ /* code */ }();
+function(){ /* code */ }();
```
new关键字也能达到这个效果。
```
new function(){ /* code */ }

new function(){ /* code */ }()
// 只有传递参数时，才需要最后那个圆括号
通常情况下，只对匿名函数使用这种“立即执行的函数表达式”。它的目的有两个：一是不必为函数命名，避免了污染全局变量；二是IIFE内部形成了一个单独的作用域，可以封装一些外部无法读取的私有变量。

// 写法一
var tmp = newData;
processData(tmp);
storeData(tmp);

// 写法二
(function (){
  var tmp = newData;
  processData(tmp);
  storeData(tmp);
}());
```
上面代码中，写法二比写法一更好，因为完全避免了污染全局变量。

## 标准对象
### Date

### Regex
JavaScript有两种方式创建一个正则表达式：

第一种方式是直接通过/正则表达式/写出来，第二种方式是通过new RegExp('正则表达式')创建一个RegExp对象。

```
var re1 = /ABC\-001/;
var re2 = new ReExp('ABC\-001');

var re ='^\d{3}-\d{3,8}$/'
re.test('010-12345') // true

```
RegExp对象的test()方法用于测试给定的字符串是否符合条件

#### 切分字符串

用正则表达式切分字符串比用固定的字符更灵活，请看正常的切分代码：

`'a b   c'.split(' '); // ['a', 'b', '', '', 'c']`
嗯，无法识别连续的空格，用正则表达式试试：

`'a b   c'.split(/\s+/); // ['a', 'b', 'c']`
无论多少个空格都可以正常分割。加入,试试：

`'a,b, c  d'.split(/[\s\,]+/); // ['a', 'b', 'c', 'd']`
再加入;试试：

`'a,b;; c  d'.split(/[\s\,\;]+/); // ['a', 'b', 'c', 'd']`
如果用户输入了一组标签，下次记得用正则表达式来把不规范的输入转化成正确的数组。

#### 分组

除了简单地判断是否匹配之外，正则表达式还有提取子串的强大功能。用()表示的就是要提取的分组（Group）。比如：

`^(\d{3})-(\d{3,8})$`分别定义了两个组，可以直接从匹配的字符串中提取出区号和本地号码：
```
var re = /^(\d{3})-(\d{3,8})$/;
re.exec('010-12345'); // ['010-12345', '010', '12345']
re.exec('010 12345'); // null
```
如果正则表达式中定义了组，就可以在RegExp对象上用exec()方法提取出子串来。

exec()方法在匹配成功后，会返回一个Array，第一个元素是正则表达式匹配到的整个字符串，后面的字符串表示匹配成功的子串。

exec()方法在匹配失败时返回null。

提取子串非常有用。来看一个更凶残的例子：
```
var re = /^(0[0-9]|1[0-9]|2[0-3]|[0-9])\:(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|[0-9])\:(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|[0-9])$/;
re.exec('19:05:30'); // ['19:05:30', '19', '05', '30']
```
这个正则表达式可以直接识别合法的时间。但是有些时候，用正则表达式也无法做到完全验证，比如识别日期：
```
var re = /^(0[1-9]|1[0-2]|[0-9])-(0[1-9]|1[0-9]|2[0-9]|3[0-1]|[0-9])$/;
```
对于'2-30'，'4-31'这样的非法日期，用正则还是识别不了，或者说写出来非常困难，这时就需要程序配合识别了。

#### 贪婪匹配

需要特别指出的是，正则匹配默认是贪婪匹配，也就是匹配尽可能多的字符。举例如下，匹配出数字后面的0：
```
var re = /^(\d+)(0*)$/;
re.exec('102300'); // ['102300', '102300', '']
```
由于\d+采用贪婪匹配，直接把后面的0全部匹配了，结果0*只能匹配空字符串了。

必须让\d+采用非贪婪匹配（也就是尽可能少匹配），才能把后面的0匹配出来，加个?就可以让\d+采用非贪婪匹配：
```
var re = /^(\d+?)(0*)$/;
re.exec('102300'); // ['102300', '1023', '00']
```
#### 全局搜索

JavaScript的正则表达式还有几个特殊的标志，最常用的是g，表示全局匹配：
```
var r1 = /test/g;
// 等价于:
var r2 = new RegExp('test', 'g');
```
全局匹配可以多次执行exec()方法来搜索一个匹配的字符串。当我们指定g标志后，每次运行exec()，正则表达式本身会更新lastIndex属性，表示上次匹配到的最后索引：
```
var s = 'JavaScript, VBScript, JScript and ECMAScript';
var re=/[a-zA-Z]+Script/g;

// 使用全局匹配:
re.exec(s); // ['JavaScript']
re.lastIndex; // 10

re.exec(s); // ['VBScript']
re.lastIndex; // 20

re.exec(s); // ['JScript']
re.lastIndex; // 29

re.exec(s); // ['ECMAScript']
re.lastIndex; // 44

re.exec(s); // null，直到结束仍没有匹配到
```

>全局匹配类似搜索，因此不能使用/^...$/，那样只会最多匹配一次。

正则表达式还可以指定i标志，表示忽略大小写，m标志，表示执行多行匹配。

### JSON
```javascript
JSON.parse(string)//--> json;
JSON.stringify(json)// --> string
```

## 错误处理

### Error对象
JavaScript原生提供Error对象, 所有抛出的错误都是这个对象的实例.

```
var err = new Error('出错了')
```
当代码解析或运行时发生错误，JavaScript引擎就会自动产生并抛出一个Error对象的实例，然后整个程序就中断在发生错误的地方。

根据语言标准，Error对象的实例必须有message属性，表示出错时的提示信息，其他属性则没有提及。大多数JavaScript引擎，对Error实例还提供name和stack属性，分别表示错误的名称和错误的堆栈，但它们是非标准的，不是每种实现都有。
> message: 错误提示信息
> name: 错误名称(非标准属性)
> statck: 错误的堆栈(非标准属性)

利用name和message这个两个属性, 可以对发生什么错误有一个大概的了解
```
if(error.name){
  console.log(error.name +":" + error.message)
}
```

`stack` 属性用来查看错误发生时的堆栈
```javascript
function  throwit(){
  throw new Error('')
}

funciton catchit(){
    try {
      throwit();

    }catch(e) {
      console.log(e.stack)
    }
}
catchit()
// Error
//    at throwit (~/examples/throwcatch.js:9:11)
//    at catchit (~/examples/throwcatch.js:3:9)
//    at repl:1:5
```

### Javascript的原生错误类型

1. SyntaxError: 是解析代码是语法错误
2. ReferenceError: 引用一个不存在的变量时发生错误.将一个值分配给无法分配的对象, 比如对函数的运行结果或者this赋值.
3. RangeError: 当一个值超出有效范围时发生的错误.如，一是数组长度为负数，二是Number对象的方法参数超出范围，以及函数堆栈超过最大值。
4. URIError: 是URI相关的参数不正确时抛出的错误, 主要涉及`encodeURI()`,`decodeURI()`,`encodeURIComponet()`,`decodeURIComponent()`, `escape()`和`uncescape()`.
5. TypeError: 变量或参数不是预期的类型时发生的错误.比如，对字符串、布尔值、数值等原始类型的值使用new命令，就会抛出这种错误，因为new命令的参数应该是一个构造函数。
6. EvalError: eval函数没有被正确的执行时, 会抛出`EvalError`.

### 自定义错误
```javascript
function UserError(message){
    this.message = message || '默认信息'
    this.name = 'UserError'
}

UserError.prototype = new Error()
UserError.prototype.constructor = UserError;
```
上面代码自定义一个错误对象UserError，让它继承Error对象。然后，就可以生成这种自定义的错误了。
```
new UserError("这是自定义的错误")
```

### throw语句
throw语句的作用是中断程序执行，抛出一个意外或错误。它接受一个表达式作为参数，可以抛出各种值。

```
// 抛出一个字符串
throw "Error！";

// 抛出一个数值
throw 42;

// 抛出一个布尔值
throw true;

// 抛出一个对象
throw {toString: function() { return "Error!"; } };
```
throw可以接受各种值作为参数. Javascript引擎一旦遇到throw,就会停止执行后面的语句, 并将throw语句的参数值, 返回给用户.

throw抛出自定义的错误
```javascript

function UserError(message) {
  this.message = message || "默认信息";
  this.name = "UserError";
}

UserError.prototype.toString = function (){
  return this.name + ': "' + this.message + '"';
}

throw new UserError("出错了！");
```

可以通过自定义一个`assert`函数，规范化throw抛出的信息。

```
function assert(expression, message) {
  if (!expression)
    throw {name: 'Assertion Exception', message: message};
}
```
上面代码定义了一个assert函数，它接受一个表达式和一个字符串作为参数。一旦表达式不为真，就抛出指定的字符串。它的用法如下。
```
assert(typeof myVar != 'undefined', 'myVar is undefined!');
```
console对象的assert方法，与上面函数的工作机制一模一样，所以可以直接使用。
```
console.assert(typeof myVar != 'undefined', 'myVar is undefined!');
```

### try..catcah 结构
```javascript
try {
  throw new Error('出错了!');
} catch (e) {
  console.log(e.name + ": " + e.message);
  console.log(e.stack);
}
// Error: 出错了!
//   at <anonymous>:3:9
//   ...
```
上面代码中, try代码中抛出一个错误(上例用的是throw语句), javascript殷勤就立即把代码的执行,转到catch代码快中.

```javascript
function throwIt(exception) {
  try {
    throw exception;
  } catch (e) {
    console.log('Caught: '+ e);
  }
}

throwIt(3);
// Caught: 3
throwIt('hello');
// Caught: hello
throwIt(new Error('An error happened'));
// Caught: Error: An error happened
```
上面代码中，throw语句先后抛出数值、字符串和错误对象。

catch代码块捕获错误之后，程序不会中断，会按照正常流程继续执行下去。
```
try {
  throw "出错了";
} catch (e) {
  console.log(111);
}
console.log(222);
// 111
// 222
```

上面代码中，try代码块抛出的错误，被catch代码块捕获后，程序会继续向下执行。

catch代码块之中，还可以再抛出错误，甚至使用嵌套的try...catch结构。
```
var n = 100;

try {
  throw n;
} catch (e) {
  if (e <= 50) {
    // ...
  } else {
    throw e;
  }
}
```
上面代码中，catch代码之中又抛出了一个错误。

为了捕捉不同类型的错误，catch代码块之中可以加入判断语句。

```javascript
try {
  foo.bar();
} catach(e){
  if(e instanceof  EvalError){
    console.log(e.name +":"+e.message)
  }else if(e instanceof RangeError){
    console.log(e.name + ": " + e.message);
  }
  //...
}

```
上面代码中，catch捕获错误之后，会判断错误类型（EvalError还是RangeError），进行不同的处理。

try...catch结构是JavaScript语言受到Java语言影响的一个明显的例子。这种结构多多少少是对结构化编程原则一种破坏，处理不当就会变成类似goto语句的效果，应该谨慎使用。

### finally代码块
try...catch结构允许在最后添加一个finally代码块，表示不管是否出现错误，都必需在最后运行的语句。
```
function cleansUp() {
  try {
    throw new Error('出错了……');
    console.log('此行不会执行');
  } finally {
    console.log('完成清理工作');
  }
}

cleansUp()
// 完成清理工作
// Error: 出错了……
```
上面代码中，由于没有catch语句块，所以错误没有捕获。执行finally代码块以后，程序就中断在错误抛出的地方。
```
function idle(x) {
  try {
    console.log(x);
    return 'result';
  } finally {
    console.log("FINALLY");
  }
}

idle('hello')
// hello
// FINALLY
// "result"
```
上面代码说明，即使有return语句在前，finally代码块依然会得到执行，且在其执行完毕后，才会显示return语句的值。

下面的例子说明，return语句的执行是排在finally代码之前，只是等finally代码执行完毕后才返回。
```
var count = 0;
function countUp() {
  try {
    return count;
  } finally {
    count++;
  }
}

countUp()
// 0
count
// 1
```
上面代码说明，return语句的count的值，是在finally代码块运行之前，就获取完成了。

下面是finally代码块用法的典型场景。
```
openFile();

try {
  writeFile(Data);
} catch(e) {
  handleError(e);
} finally {
  closeFile();
}
```
上面代码首先打开一个文件，然后在try代码块中写入文件，如果没有发生错误，则运行finally代码块关闭文件；一旦发生错误，则先使用catch代码块处理错误，再使用finally代码块关闭文件。

下面的例子充分反应了`try...catch...finally`这三者之间的执行顺序。
```
function f() {
  try {
    console.log(0);
    throw "bug";
  } catch(e) {
    console.log(1);
    return true; // 这句原本会延迟到finally代码块结束再执行
    console.log(2); // 不会运行
  } finally {
    console.log(3);
    return false; // 这句会覆盖掉前面那句return
    console.log(4); // 不会运行
  }

  console.log(5); // 不会运行
}

var result = f();
// 0
// 1
// 3

result
// false
```
上面代码中，catch代码块结束执行之前，会先执行finally代码块。从catch转入finally的标志，不仅有return语句，还有throw语句。
```
function f() {
  try {
    throw '出错了！';
  } catch(e) {
    console.log('捕捉到内部错误');
    throw e; // 这句原本会等到finally结束再执行
  } finally {
    return false; // 直接返回
  }
}

try {
  f();
} catch(e) {
  // 此处不会执行
  console.log('caught outer "bogus"');
}

//  捕捉到内部错误
```
上面代码中，进入catch代码块之后，一遇到throw语句，就会去执行finally代码块，其中有return false语句，因此就直接返回了，不再会回去执行catch代码块剩下的部分了。


### 属性描述对象
Javascript提供了一个内部数据结构, 用来描述一个对象的属性的行为, 控制它的行为,这被称为`属性描述对象(attributes object)`. 每个属性都有自己的描述对象, 保存该属性的一些元信息.

属性描述的对象的实例

```javascript
{
  value: 123,
  writable: false,
  enumerable: true,
  configurable: false,
  get: undefined,
  set: undefined
}
```

#### 属性描述对象提供6个元属性
- 1) value
`value` 存放该属性的的属性值, 默认为`undefined`

- 2) writable
`writable` 存放了一个布尔值, 表示属性值(value)是否可变, 默认为`true`

- 3) enumerable
`enumerable`存放一个布尔值, 表示该属性是否可以美剧, 默认为 true. 如果设置为`false`, 会使的某些操作(比如 for .. in 循环, Object.keys())跳过该属性.

- 4) configurable
`configurable` 存放一个布尔值, 可以表示"可配置性", 默认为true. 如果设置为false, 将阻止某些操作改写此属性, 比如, 无法删除该属性, 也不得改变该属性的属性描述对象(value 属性除外). 也就是说, `configurable` 属性控制力属性描述对象的可写性.

- 5) get
get存放一个函数，表示该属性的取值函数（getter），默认为undefined。

- 6) set
set存放一个函数，表示该属性的存值函数（setter），默认为undefined。

#### 2. Object.getOwnPropertyDescriptor()
可以读出对象自身的属性的描述对象.
```javascript
Object.getOwnPropertyDescriptor(o,'p')
Object {value: "a", writable: true, enumerable: true, configurable: true}
```


####  Object.defineProperty()，Object.defineProperties()

Object.defineProperty方法允许通过定义属性描述对象，来定义或修改一个属性，然后返回修改后的对象。它的格式如下。

`Object.defineProperty(object, propertyName, attributesObject)`
上面代码中，Object.defineProperty方法接受三个参数，第一个是属性所在的对象，第二个是属性名（它应该是一个字符串），第三个是属性的描述对象。比如，新建一个o对象，并定义它的p属性，写法如下。
```
var o = Object.defineProperty({}, 'p', {
  value: 123,
  writable: false,
  enumerable: true,
  configurable: false
});

o.p
// 123

o.p = 246;
o.p
// 123
// 因为writable为false，所以无法改变该属性的值
```
如果属性已经存在，`Object.defineProperty`方法相当于更新该属性的属性描述对象。

需要注意的是，`Object.defineProperty`方法和后面的`Object.defineProperties`方法，都有性能损耗，会拖慢执行速度，不宜大量使用。

如果一次性定义或修改多个属性，可以使用Object.defineProperties方法。
```
var o = Object.defineProperties({}, {
  p1: { value: 123, enumerable: true },
  p2: { value: 'abc', enumerable: true },
  p3: { get: function () { return this.p1 + this.p2 },
    enumerable:true,
    configurable:true
  }
});

o.p1 // 123
o.p2 // "abc"
o.p3 // "123abc"
```
上面代码中的p3属性，定义了取值函数get。这时需要注意的是，一旦定义了取值函数get（或存值函数set），就不能将writable设为true，或者同时定义value属性，会报错。
```
var o = {};

Object.defineProperty(o, 'p', {
  value: 123,
  get: function() { return 456; }
});
// TypeError: Invalid property.
// A property cannot both have accessors and be writable or have a value,
```
上面代码同时定义了get属性和value属性，结果就报错。

`Object.defineProperty()`和`Object.defineProperties()`的第三个参数，是一个属性对象。它的writable、configurable、enumerable这三个属性的默认值都为false。
```
var obj = {};
Object.defineProperty(obj, 'foo', { configurable: true });
Object.getOwnPropertyDescriptor(obj, 'foo')
// {
//   value: undefined,
//   writable: false,
//   enumerable: false,
//   configurable: true
// }
```
上面代码中，定义obj对象的foo属性时，只定义了可配置性configurable为true。结果，其他元属性都是默认值。

writable属性为false，表示对应的属性的值将不得改写。
```
var o = {};

Object.defineProperty(o, 'p', {
  value: "bar"
});

o.p // bar

o.p = 'foobar';
o.p // bar

Object.defineProperty(o, 'p', {
  value: 'foobar',
});
// TypeError: Cannot redefine property: p
```
上面代码由于writable属性默认为false，导致无法对p属性重新赋值，但是不会报错（严格模式下会报错）。不过，如果再一次使用Object.defineProperty方法对value属性赋值，就会报错。

configurable属性为false，将无法删除该属性，也无法修改attributes对象（value属性除外）。
```
var o = {};

Object.defineProperty(o, 'p', {
  value: 'bar',
});

delete o.p
o.p // "bar"
```
上面代码中，由于configurable属性默认为false，导致无法删除某个属性。

enumerable属性为false，表示对应的属性不会出现在for...in循环和Object.keys方法中。
```
var o = {
  p1: 10,
  p2: 13,
};

Object.defineProperty(o, 'p3', {
  value: 3,
});

for (var i in o) {
  console.log(i, o[i]);
}
// p1 10
// p2 13
```
上面代码中，p3属性是用Object.defineProperty方法定义的，由于enumerable属性默认为false，所以不出现在for...in循环中。

#### Object.getOwnPropertyNames()
Object.getOwnPropertyNames方法返回直接定义在某个对象上面的全部属性的名称，而不管该属性是否可枚举。
```
var o = Object.defineProperties({}, {
  p1: { value: 1, enumerable: true },
  p2: { value: 2, enumerable: false }
});

Object.getOwnPropertyNames(o)
// ["p1", "p2"]
```
一般来说，系统原生的属性（即非用户自定义的属性）都是不可枚举的。
```
// 比如，数组实例自带length属性是不可枚举的
Object.keys([]) // []
Object.getOwnPropertyNames([]) // [ 'length' ]

// Object.prototype对象的自带属性也都是不可枚举的
Object.keys(Object.prototype) // []
Object.getOwnPropertyNames(Object.prototype)
// ['hasOwnProperty',
//  'valueOf',
//  'constructor',
//  'toLocaleString',
//  'isPrototypeOf',
//  'propertyIsEnumerable',
//  'toString']
```
上面代码可以看到，数组的实例对象（[]）没有可枚举属性，不可枚举属性有length；Object.prototype对象也没有可枚举属性，但是有不少不可枚举属性。

#### Object.prototype.propertyIsEnumerable()
对象实例的propertyIsEnumerable方法用来判断一个属性是否可枚举。
```
var o = {};
o.p = 123;

o.propertyIsEnumerable('p') // true
o.propertyIsEnumerable('toString') // false
```
上面代码中，用户自定义的p属性是可枚举的，而继承自原型对象的toString属性是不可枚举的。

#### 存取器（accessor）
除了直接定义以外，属性还可以用存取器（accessor）定义。其中，存值函数称为setter，使用set命令；取值函数称为getter，使用get命令。

存取器提供的是虚拟属性，即该属性的值不是实际存在的，而是每次读取时计算生成的。利用这个功能，可以实现许多高级特性，比如每个属性禁止赋值。
```
var o = {
  get p() {
    return 'getter';
  },
  set p(value) {
    console.log('setter: ' + value);
  }
};
```
上面代码中，o对象内部的get和set命令，分别定义了p属性的取值函数和存值函数。定义了这两个函数之后，对p属性取值时，取值函数会自动调用；对p属性赋值时，存值函数会自动调用。
```
o.p // "getter"
o.p = 123 // "setter: 123"
```
注意，取值函数Getter不能接受参数，存值函数Setter只能接受一个参数（即属性的值）。另外，对象也不能有与取值函数同名的属性。比如，上面的对象o设置了取值函数p以后，就不能再另外定义一个p属性。

存取器往往用于，属性的值需要依赖对象内部数据的场合。
```
var o ={
  $n : 5,
  get next() { return this.$n++ },
  set next(n) {
    if (n >= this.$n) this.$n = n;
    else throw '新的值必须大于当前值';
  }
};

o.next // 5

o.next = 10;
o.next // 10
```
上面代码中，next属性的存值函数和取值函数，都依赖于对内部属性$n的操作。

存取器也可以通过Object.defineProperty定义。
```
var d = new Date();

Object.defineProperty(d, 'month', {
  get: function () {
    return d.getMonth();
  },
  set: function (v) {
    d.setMonth(v);
  }
});
```
上面代码为Date的实例对象d，定义了一个可读写的month属性。

存取器也可以使用Object.create方法定义。
```
var o = Object.create(Object.prototype, {
  foo: {
    get: function () {
      return 'getter';
    },
    set: function (value) {
      console.log('setter: '+value);
    }
  }
});
```
如果使用上面这种写法，属性foo必须定义一个属性描述对象。该对象的get和set属性，分别是foo的取值函数和存值函数。

利用存取器，可以实现数据对象与DOM对象的双向绑定。
```
Object.defineProperty(user, 'name', {
  get: function () {
    return document.getElementById('foo').value;
  },
  set: function (newValue) {
    document.getElementById('foo').value = newValue;
  },
  configurable: true
});
```
上面代码使用存取函数，将DOM对象foo与数据对象user的name属性，实现了绑定。两者之中只要有一个对象发生变化，就能在另一个对象上实时反映出来。

## 面向对象


### 构造函数

```
var Vehicle = function(p){
  this.price = p;
};
```
Vehicle就构造函数, 它提供模板, 用来生成对象实例. 为了与区别普通函数, 构造函数名字的第一个字母通常大写.

> 1. 函数内部使用了this关键字, 代表了要生成的对象实例.
> 2. 生成对象的时候, 必须使用new命令. 调用Vehicle函数.

### new命令
```
var v = new Vehicle()
v.price
```

> 在调用构造函数, 如果忘记使用new命令, 结果函数里的变量是成了全局变量, 可以是用严格模式"user strict"

由于在严格模式中，函数内部的this不能指向全局对象，默认等于undefined，导致不加new调用会报错（JavaScript不允许对undefined添加属性）。

另一个解决办法，是在构造函数内部判断是否使用new命令，如果发现没有使用，则直接返回一个实例对象。
```
function Fubar(foo, bar){
  if (!(this instanceof Fubar)) {
    return new Fubar(foo, bar);
  }

  this._foo = foo;
  this._bar = bar;
}

Fubar(1, 2)._foo // 1
(new Fubar(1, 2))._foo // 1
```

### new命令的原理
使用new命令时，它后面的函数调用就不是正常的调用，而是依次执行下面的步骤。
>1. 创建一个空对象，作为将要返回的对象实例
2. 将这个空对象的原型，指向构造函数的prototype属性
3. 将这个空对象赋值给函数内部的this关键字
4. 开始执行构造函数内部的代码

也就是说，构造函数内部，this指的是一个新生成的空对象，所有针对this的操作，都会发生在这个空对象上。构造函数之所以叫“构造函数”，就是说这个函数的目的，就是操作一个空对象（即this对象），将其“构造”为需要的样子。

如果构造函数内部有return语句，而且return后面跟着一个对象，new命令会返回return语句指定的对象；否则，就会不管return语句，返回this对象。
[摘自](http://javascript.ruanyifeng.com/oop/basic.html)

### prototype 对象

#### 构造函数的缺点
JavaScript通过构造函数生成新对象，因此构造函数可以视为对象的模板。实例对象的属性和方法，可以定义在构造函数内部。
```
function Cat (name, color) {
  this.name = name;
  this.color = color;
}

var cat1 = new Cat('大毛', '白色');

cat1.name // '大毛'
cat1.color // '白色'
```
上面代码的Cat函数是一个构造函数，函数内部定义了name属性和color属性，所有实例对象都会生成这两个属性。但是，这样做是对系统资源的浪费，因为同一个构造函数的对象实例之间，无法共享属性。
```
function Cat(name, color) {
  this.name = name;
  this.color = color;
  this.meow = function () {
    console.log('mew, mew, mew...');
  };
}

var cat1 = new Cat('大毛', '白色');
var cat2 = new Cat('二毛', '黑色');

cat1.meow === cat2.meow
// false
```
上面代码中，cat1和cat2是同一个构造函数的实例。但是，它们的meow方法是不一样的，就是说每新建一个实例，就会新建一个meow方法。这既没有必要，又浪费系统资源，因为所有meow方法都是同样的行为，完全应该共享。

#### prototype属性的作用
Javascript的每一个对象都继承另一对象, 后者称为"原型"(prototype)对象, 只有null 除外, 它没有自己的原型对象.

原型对象上的所有属性和方法, 都能被派生对象共享.
通过构造函数生成实例对象时, 会自动为实例对象分配原型对象. 每一个构造函数都有一个prototype属性. 这个属性就是实例对象的原型对象.
```javascript
function Animal(name){
  this.name = name
}
Animal.prototype.color = 'white'
var cat1 = new Animal("damao")
var cat2 = new Animal("ermao")

cat1.color // 'white'
cat2.color // 'white'

```

总结一下，原型对象的作用，就是定义所有实例对象共享的属性和方法。这也是它被称为原型对象的含义，而实例对象可以视作从原型对象衍生出来的子对象。
```
Animal.prototype.walk = function () {
  console.log(this.name + ' is walking');
};
```
上面代码中，Animal.protype对象上面定义了一个walk方法，这个方法将可以在所有Animal实例对象上面调用。

由于JavaScript的所有对象都有构造函数，而所有构造函数都有prototype属性（其实是所有函数都有prototype属性），所以所有对象都有自己的原型对象。

#### 原型链
对象的属性和方法, 有可能定义在自身,也有可能定义在它的原型对象. 由于原型本身也是对象, 又有自己的原型,所以形成一个原型链(prototype chain).

如果一层层的上溯, 所有对象的原型都可以上溯到`Object.prototype`, 即 `Object`构造函数的`prototype`属性指向的那个对象. 那么, `Object.prototype`对象有没有他的原型呢, 可以有的, 就是没有任何属性和方法的null对象, 而null没有自己的原型.

“原型链”的作用是，读取对象的某个属性时，JavaScript引擎先寻找对象本身的属性，如果找不到，就到它的原型去找，如果还是找不到，就到原型的原型去找。如果直到最顶层的Object.prototype还是找不到，则返回undefined。

如果对象自身和它的原型，都定义了一个同名属性，那么优先读取对象自身的属性，这叫做“覆盖”（overiding）。

需要注意的是，一级级向上，在原型链寻找某个属性，对性能是有影响的。所寻找的属性在越上层的原型对象，对性能的影响越大。如果寻找某个不存在的属性，将会遍历整个原型链。

#### constructor属性
`prototype`对象有一个`constructor`属性, 默认指向`prototype`对象所在的构造函数.
```
function P(){}
P.prototype.constructor === P  //true
```

>constructor属性的作用，是分辨原型对象到底属于哪个构造函数。

#### instanceof运算符
instanceof运算符的左边是实例对象，右边是构造函数。它的运算实质是检查右边构建函数的原型对象，是否在左边对象的原型链上。因此，下面两种写法是等价的
```
v instanceof Vehicle
// 等同于
Vehicle.prototype.isPrototypeOf(v)
```

>注意，instanceof运算符只能用于对象，不适用原始类型的值。


`Object.getPrototypeOf`方法返回一个对象的原型。这是获取原型对象的标准方法。
```
// 空对象的原型是Object.prototype
Object.getPrototypeOf({}) === Object.prototype
// true

// 函数的原型是Function.prototype
function f() {}
Object.getPrototypeOf(f) === Function.prototype
// true

// f 为 F 的实例对象，则 f 的原型是 F.prototype
var f = new F();
Object.getPrototypeOf(f) === F.prototype
// true
```

`Object.setPrototypeOf`方法可以为现有对象设置原型，返回一个新对象。

`Object.setPrototypeOf`方法接受两个参数，第一个是现有对象，第二个是原型对象

`Object.create`方法用于从原型对象生成新的实例对象，可以替代new命令。

它接受一个对象作为参数，返回一个新对象，后者完全继承前者的属性，即原有对象成为新对象的原型。

`Object.prototype.isPrototypeOf()`:
对象实例的isPrototypeOf方法，用来判断一个对象是否是另一个对象的原型。

`Object.prototype.__proto__`:
`__proto__`属性（前后各两个下划线）可以改写某个对象的原型对象。

#### 给类添加方法
```javascript
function Animal(name){
  this.name = name
}

# 添加方法speak方法
Animal.prototype.speak = function(line){
  console.log('miaomiao')
}

# 添加属性
Animal.prototype.teeth = 'small'

```

####  覆盖继承的属性
### this关键字



## 事件

### preventDefault:
 取消事件的默认动作
`event.preventDefault()`: 该方法将通知Web浏览器不要执行与事件关联的默认动作(如果存在这样的动作). 例如, 在type 属性 "submit", 在事件传播的任意阶段可以调用任意的时间句柄, 通过调用该方法, 可以阻止提交表单. 注意, 如果Event 对象的 cancelable 属性是 false, 那么就没有默认动作, 或者不能阻止默认动作. 无论那种情况, 调用该方法都没有作用.

```javascript
// 防止链接打开 URL：
$("a").click(function(event){
  event.preventDefault();
});
```



### stopPropagation: 
不再派发事件.  终止事件在传播过程的捕获, 目标处理或者起泡阶段进一步传播. 调用该方法后, 该节点上处理该事件的处理程序将被调用, 事件不再被派发到其他节点上.
`event.stopPropagation()`:
该方法将停止事件的传播, 阻止它被分派到其他Document节点上. 在此事件传播的任何阶段都可以调用它. 注意, 虽然该方法不能阻止同一个Document节点上其他事件句柄被调用, 但是它可以阻止把事件分派到其他节点.


