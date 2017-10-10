# Vue js的教程
---

## 构造器
每个Vue.js应用都是通过构造函数 Vue 创建一个 Vue 的根实例启动的:

```
var vm = new Vue({
    // 选项
    })
```
vm == ViewModel表示变量名表示 Vue 实例.

在实例化Vue时, 需要传入一个 选项对象, 它可以包含数据, 模板, 挂在元素, 方法, 生命周期的钩子等选项.

可以扩展Vue 构造器, 从而用预定义选项创建可复用的组件构造器:
```js
var  MyComponent = Vue.extend({
    // 扩展选项
    })

// 所有 MyComponent 实例都将以预定义的扩展选项被创建.
var myComponentInstance = new MyComponent()
```

尽管可以命令式的创建扩展实例, 不过在多数情况下建议将组件构造器注册为一个自定义元素, 然后声明式的用在模板中.


## 全局API

`Vue.set(target, key, value)`
参数: 
- {object | Array} target
- {string | number} key
- {any} value

返回值: 设置的值
用法:
设置对象属性. 如果对象是响应式的, 确保属性被创建后也是响应式的, 同时触发视图更新. 这个方法主要用于避开Vue不能检测属性被添加的限制.
> 这个对象不能是Vue 实例, 或者 Vue 实例的根数据对象
