Java的标识符
1. 必须以字母,下划线,美元符开头,后面跟任意数目的字母,数字,下划线和美元符,可以包含中文字符,日文字符,不能有空格,不能有Java的关键字和保留字,长度无限制
2. 不能以数字开头

char:
字符型常量有三种表示形式:
1. 直接通过单个字符来指定字符常量,例如'A','9'
2. 通过转义字符表示特殊字符常量,'\n','\t'
3. 直接使用Unicode值来表示字符常量,'\uxxxx'

> char类型使用单引号括起来,而字符串使用双引号.

## 浮点型
默认为double,强制使用float, 5.2f
正无穷大,负无穷大和非数. 所有的正无穷大数值都是相等的,所有负无穷大数值都是相等的,而NaN不与任何数值相等,甚至和NaN都不想等.

## 基本类型的类型转换
### 自动类型转换
char-->int-->long-->float-->double
byte-->short-->int-->long-->float-->double


###强制类型转换
使用()进行转换
int iValue=233;
byte bValute = (byte)iValue;

截取int右边8位

###表达式类型的自动挑升
当一个算术表达式中包含多个基本类型的时,真个算术表达式的数据类型将自动发生提升:
1. 所有byte型, short型和char型将被提升到int型
2. 整个算术表达式的数据类型自动提升到与表达式中最高级操作数同样的类型.

## Java 面向对象

### 内部类
### 泛型

## 常用的类
### Java IO

### 集合

### 字符串

## 反射

## 注解
### 注解分类
按照运行机制的分:
1. 源码注解: 注解只在源码中存在, 编译成.class文件就不存在了.
2. 编译时注解: 注解存在源码和.class文件中. @Override @Deprecated @Suppvisewarnings
3. 运行时注解: 在运行阶段还起作用, 甚至会运行逻辑


来自JDK注解
来自第三方注解
我们自己定义注解

元注解: 给注解的注解

### 自定义注解
#### 语法要求:

```java
@Target({ElementType.METHOD, ElementType.Type}) // 元注解, 注解的作用域列表
@Retention(RetentionPolicy.RUNTIME) //元注解 运行时注解
@Inherited  //元注解 标示型, 可以子注解继承
@Documented  //元注解
public @interface Description{  //定义注解  @interface关键字定义注解
    String desc();  // 成员变量以无参数无异常方式声明.
    String author();
    int age() default 18;  //默认是18, 可以用default设定默认值
}
/*
成员类型是受限的, 合法的类型包括原型类型及String, Class, Annotation, Enumeration.
如果注解只有一个成员时, 则成员名必须取名为value(), 在使用时可以忽略成员名和赋值号(=).

注解类可以没有成员, 没有成员的注解称之为标示注解.
*/
```
#### 使用自定义注解
使用注解的语法:
@<注解名>(<成员名1>=<成员值1>, <成员值1>=<成员值1>....)

```java
@Description(desc="I am eyeColor", author="Mooc boy", age=18)
public String eyeColor(){
    return "red";
}
```

## 注解实战
项目说明:
项目取自一个公司的持久层架构, 用来代替Hibernate的解决方案, 核心代码就是通过注解来实现的.

需求:
