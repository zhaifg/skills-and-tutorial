# C
---
## C语言的类型
基本类型: int, float, short, double
枚举类: 
指针, 数组, 结构体, 函数, union
char 1byte -128 127 0-255
unsigned char 
signed char
int
unsigned int
short
unsigned short 
long
unsigned long

float 4b 
double 8b
long double 10byte

函数 void--> void exit(int status) or int rannd(void)
指针函数
void *malloc(size_t size)

extern
x=y 左值与右值
左值: 

`#define LENTH 10`
const 关键字
auto  
register 
static
extern

## 操作符
sizeof()
&
*
?:
### 操作符优先级
()[]->.++ -- 左先
+ - ! ~ ++ -- (type)* & sizeof 右优先
* / %  左
+ - 左
<< >> 左
<<= >>= 左
== != 左
& 左
^ 左
| 左
&& 左
|| 左
?: 右
= += -= /= %= >>= <<= &= ^= |= 右
, 左

## 循环
for
while
until
switch
break
contiune
goto
goto lable;
..
.
lable: statement
```c
#include <stdio.h>
 
int main () {

   /* local variable definition */
   int a = 10;

   /* do loop execution */
   LOOP:do {
   
      if( a == 15) {
         /* skip the iteration */
         a = a + 1;
         goto LOOP;
      }
        
      printf("value of a: %d\n", a);
      a++;
     
   }while( a < 20 );
 
   return 0;
}
/*
value of a: 10
value of a: 11
value of a: 12
value of a: 13
value of a: 14
value of a: 16
value of a: 17
value of a: 18
value of a: 19
*/
```
## 符号常量
`#define 名字 替换文本`
```
#include <stdio.h>

#define LOWER 0
#define UPPER 0
#define STEP 20
```

## 字符输入
## 函数

```
return_type function_name( parameter list ) {
   body of the function
}
```
值引用, 地址引用

## 指针
int a = 10;
int *p ;
p = &a;
*p 值
p 为值的地址的值

## 定义字符串:
1. char name[] = {'a','b'};
2. char *name = "dafdfdasf"; 
