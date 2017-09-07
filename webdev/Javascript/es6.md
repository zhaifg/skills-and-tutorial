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

## const命令
只读常量, 作用域与let相同, 声明后立即赋值.

## global对象
es5的顶层对象, windows

