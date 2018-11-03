# go 入门
---

path:
gopath:
   是编译后二进制的存放目的地和import 包时搜索路径(其实也是你的工作目录, 可以在src下创建你自己的go源文件, 然后工作), 可以创建 bin, pkg, src
   不要把gopath设置成go 的安装路径

goroot: 就是go的安装路径


go build: 用于编译源码文件, 代码包, 依赖包
go run: 编译并运行
go get

关键字: 25个
标示符:
package
import 别名
`_`, `.`

25个关键字：
break, default, func, interface, select, case,  defer go map struct
chan else goto package switch const fallthrough if range type continue for import return var

内置预声明：
常量： true false iota nil
类型： int int8 int16 int32 int64
       uint uint8 uint16 uint32 uint64 uinptr
       float32 float64 complex128 complex64
       bool byte  rune string error
函数： make  len cap new append copy close delete complex real imag panic 
      recover


### 声明：

var： 变量声明
const： 常量声明
type： 类型声明
func： 函数声明 

函数声明包括一个名字，一个参数列表（由函数调用者提供的变量）， 一个可选的返回值列表， 以及函数体， 如果函数不返回任何内容，返回列表可以省略。

### 变量
var name type = expriession  
类型和表达式可以省略一个，不能都省略
* 如果省略类型， 他的类型由初始化表达式决定
* 如果省略表达式， 起初是对应类型的零值
  * 数字 0
  * bool false
  * 字符串： ""
  * 接口和引用类型（slice， 指针，map， 通道， 函数） 是nil

#### 短变量声明
在函数中， 一个称作短变量声明的可选形式可以用来声明和初始化局部变量。 它使用
name ：= expresssion 的形式， name 的类型由expression的类型决定

### 指针
变量是存储值的地方
指针的值是变量的地址。 一个指针指示值所保存的位置。 不是所有的值都有地址， 但是所有的变量都有。 只用指针， 可以在无须知道变量名的情况下，间接读取或者更新变量的值。

如果一个变量声明为var x int， 表达式 &x（x的地址） 获取一个指向整型变量的指针， 它的类型是整型指针（*int）。 如果值叫做p， 我们说p指向x， 或者p包含x的地址。
p指向的变量写成*p。 表达式*p获取的变量的值， 一个整型类型， 因为*p代表一个变量， 所以它可以出现在赋值操作符左边， 用于更新变量的值
```go
x := 1
p := &x // p 是整型指针， 指向x
fmt.Println（*p） // 1
*p = 2 //x =2
fmt.Println（x） // 2
```




数值类型:
整型: 有无符号, 
float32/64
complex64/128
byte:
rune:
uint
int
uintptr

字符串类型,布尔类型

## 循环
for initialization； condition; post {
    
}

for condition {
    
}
### range 循环

```go
func  main() {
    s, sep :="", ""

    for _, arg := range os.Args[1:]{ // 一般序号类似Python enumerate
        s += sep + arg
        sep = " "
    }
}

```
range 产生一对值： 索引和这个索引出元素的值
