# Python Click工具
---
Click 是类似于argparse, optparse 的命令行工具, 基于optparse的二次封装

Why click? 


Quickstart

## 基础的名词概念
click.command 在最简单的情况下，只需使用这个装饰器装饰一个函数就可以将它变成一个可调用的脚本
`click.command()`: 这个装饰器, 编程一个cmd
```
import click
@click.command
```

`click.echo()`:代替为python的print函数, 兼容python2和python3



嵌套命令
使用Group, group()类似command()的一个装饰器, 他创建一个Group的对象,使用add_command()附件到Group对象的自命令

简单的实例
```
@click.group()
def cli():
    pass

@cli.command()
def initdb():
    click.echo('Initialized the database')

@cli.command()
def dropdb():
    click.echo('Dropped the database')

cli.add_command(initdb)
cli.add_command(dropdb)

if __name__ == "__main__":
    cli()
```

## 整合Setuptools 
为什么要整合到Setuptools?

## 参数
Click支持两种不同参数方式: `options` 和 `arguments`. 通常情况下使用这两种方式, 可能会存在混乱, 这里对这些差异进行叙述. 
* 通过名称可能可以看出`option`是选项, 是可选的, 可以不进行赋值
* `argument`是必选的, 定义变量后必须赋值
* 使用arguments, 最好在一下情况下, 去除自命令, 文件或urls输入, 其他的推荐使用option


options 和 arguments 的区别
options能做, arguments不能做的
* 没有输入时自动提示
* 作为标志使用时, 使用boolean或者其他
* options可以通过环境变量取得
* options 在帮助页面中完整记录，arguments不是

arguments 可以接受任意数量的参数。
options 只能接受固定数量的参数（默认为1）。


参数的类型
str / click.STRING:
int / click.INT
float / click.FLOAT:
bool / click.BOOL:
click.UUID:
class click.File(mode='r', encoding=None, errors='strict', lazy=None, atomic=False)
class click.Path(exists=False, file_okay=True, dir_okay=True, writable=False, readable=True, resolve_path=False)
class click.Choice(choices)
class click.IntRange(min=None, max=None, clamp=False)

参数名称
?

自定义类型
