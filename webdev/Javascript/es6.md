# es6
---

let命令
用于声明变量, 只能在代码块里生效, 作用域.
```
{
let a = 10;
var b = 11;
}
a //
b //
# for循环中使用let做计数器
for(let i= 0; i< 10; i++)
{

}
```
暂时性死区
```
var tmp = 123;

if (true) {
  tmp = 'abc'; // ReferenceError
  let tmp;
}
```

`不允许重复声明`

```
// 报错
function () {
  let a = 10;
  var a = 1;
}

// 报错
function () {
  let a = 10;
  let a = 1;
}
```
### 块级作用域
```
function f1() {
  let n = 5;
  if (true) {
    let n = 10;
  }
  console.log(n); // 5
}
```

* let 的作用域
* 严格模式 es6 默认开启

## const命令
只读常量, 作用域与let相同, 声明后立即赋值.
```
const pi = 3.14;
pi = 8; // 出错, 不能改
```

* const 声明的常量, 不能改.
* const 有块作用域
* 声明的时候必须赋值


## 字符串扩展

```javascript
{
  // es6
  console.log('a', '\u0061')
  console.log('a', '\u20BB7') // u20BB7 超过了 oxffff 乱码

  console.log('s', '\u{20BB7}') // unicode 表示方法
}

{
  //es5
  let s='等等'
  console.log('length', )
  console.log('0', s.charAt(0))
  console.log('1', s.charAt(1))
  console.log('Code at 0', s.charCodeAt(0))
  console.log('Code at 1', s.charCodeAt(1))

  // s1.codePointAt(0).toString(16) //  es 6 取码值, 之后转换成16进制

}

{
  String.fromCharCode('0x20bb7') ; //es5 
  string.fromCodePoint('0x2bb7') //es6 从码值打印为
}

{
  let str ="\u{20bb7}abc";
  for(let i=0; i < str.length; i++){
    console.log('es5', 'str[i'); //前两个 乱码
  }
  //es6 处理
  for(let code of str){
    console.log('es6', code)
  }
}


{
  let str = "string";
  str.includes("c"); //包含
  str.startsWith('str') // 起始
  str.endsWith('g') // 结束

}

{
  let str = 'abc';
  console.log(str.repeat(2)) // 重复几次 abcabc

}

// 模板字符串
{
  let name="list", info = "hello World";

  let m = `i am ${name} , ${info}`; // 定义模板 使用 `` 包含 ${}
}

{
  console.log('1'.padStart(2, '0')); // 补白 输出01
  console.log('1'.padEnd(2, '0')); // 补白 输出10

  string.raw`` // \n等 进行转义

}
```



### 数值的扩展

```js

{
  console.log(0b1111) //0b开始的 二进制
  // 0o 八进制
  //0x 16进制
}

{
  // Number.isFinite  //是不是有尽
   Number.isFinite(15);
    Number.isFinite(NaN);
    Number.isNaN(0)
}


{
  Number.isInteger(15) // 判断是不是数字
  Number.MAX_SAFE_INTEGER
  Number.MIN_SAFE_INTEGER
  Number.isSafeInteger(10)

  Math.trac(4.1) // 整数和小数分离
  Math.sign(-5) // 判断是整数, 负数, 还是整数
}

```



### 数组扩展
```js

let arr = Array.of(3,4,7,9,11) // 把一组变量转换成数组

Array.from() // 转换数组
[].fill() //
```
## global对象
es5的顶层对象, windows

