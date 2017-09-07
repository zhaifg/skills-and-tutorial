# Python实现的命令交互工具
---

## 安装


## 快速开始


## 介绍
支持emacs或者vi的键绑定


### hello world

1. 类似 input或者raw_input的实现
```
from __future__ import unicode_literals
from prompt_toolkit import prompt

text = prompt('Give me some input: ')
print('You said: %s' % text)
```

### 语法高亮
使用Pygments包实现
:class:`~prompt_toolkit.layout.lexers.PygmentsLexer`. 或者继承:class:`~prompt_toolkit.layout.lexers.Lexer` 

```
from pygments.lexers import HtmlLexer
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.layout.lexers import PygmentsLexer

text = prompt('Enter HTML', lexer=PygmentsLexer(HtmlLexer))
print('You said: %s' % text)
```

### 颜色
颜色定义在 class:`~prompt_toolkit.styles.Style` 默认的情况下,默认使用样式出自`prompt_toolkit.shortcuts.prompt`. 定制样式的简单方法通过`~prompt_toolkit.styles.style_from_dict`
```
from pygments.lexers import HtmlLexer
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.token import Token
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.layout.lexers import PygmentsLexer

our_style = style_from_dict({
    Token.Comment:   '#888888 bold',
    Token.Keyword:   '#ff88ff bold',
})

text = prompt('Enter HTML: ', lexer=PygmentsLexer(HtmlLexer),
              style=our_style)
```

#### 使用 Pygments 风格
`prompt_toolkit.styles.style_from_pygments`

Suppose we'd like to use a Pygments style, for instance pygments.styles.tango.TangoStyle, that is possible like this:

Creating a custom style could be done like this:

```
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.styles import style_from_pygments
from prompt_toolkit.layout.lexers import PygmentsLexer

from pygments.styles.tango import TangoStyle
from pygments.token import Token
from pygments.lexers import HtmlLexer

our_style = style_from_pygments(TangoStyle, {
    Token.Comment:   '#888888 bold',
    Token.Keyword:   '#ff88ff bold',
})

text = prompt('Enter HTML: ', lexer=PygmentsLexer(HtmlLexer),
              style=our_style)

```

#### prompt自身的颜色
prompt 自身的颜色可以通过 `get_prompt_tokens()`函数取得. 这个函数可以得到一个
`~prompt_toolkit.interface.CommandLineInterface` 这个类的实例可以返回一个(Token, text) 元组, 每一个Token 可以单独设置样式

```
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token


example_style = style_from_dict({
    # User input.
    Token:          '#ff0066',

    # Prompt.
    Token.Username: '#884444',
    Token.At:       '#00aa00',
    Token.Colon:    '#00aa00',
    Token.Pound:    '#00aa00',
    Token.Host:     '#000088 bg:#aaaaff',
    Token.Path:     '#884444 underline',
})

def get_prompt_tokens(cli):
    return [
        (Token.Username, 'john'),
        (Token.At,       '@'),
        (Token.Host,     'localhost'),
        (Token.Colon,    ':'),
        (Token.Path,     '/user/john'),
        (Token.Pound,    '# '),
    ]

text = prompt(get_prompt_tokens=get_prompt_tokens, style=example_style)
```
默认情况下，颜色从256色调色板中取出。
如果你想拥有24bit的真彩色，这可以通过在提示函数中添加t`rue_color = True`选项来实现。
```
text = prompt(get_prompt_tokens=get_prompt_tokens, style=example_style,
              true_color=True)
```

#### 打印的字符的颜色, 输出的颜色

:func:`~prompt_toolkit.shortcuts.print_tokens` function
```
from prompt_toolkit.shortcuts import print_tokens
from prompt_toolkit.styles import style_from_dict
from pygments.token import Token

# Create a stylesheet.
style = style_from_dict({
    Token.Hello: '#ff0066',
    Token.World: '#44ff44 italic',
})

# Make a list of (Token, text) tuples.
tokens = [
    (Token.Hello, 'Hello '),
    (Token.World, 'World'),
    (Token, '\n'),
]

# Print the result.
print_tokens(tokens, style=style)
```

### 自动完成
自动完成可以在 prompt 里增加一个'completer'. 它是 class:`~prompt_toolkit.completion.Completer`  抽象基类的一个实例.
WordCompleter是一个实现该接口的完成器的示例
```
from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter

html_completer = WordCompleter(['<html>', '<body>', '<head>', '<title>'])
text = prompt('Enter HTML: ', completer=html_completer)
print('You said: %s' % text)
```

> `WordCompleter` is a simple completer that completes the last word before the cursor with any of the given words.

#### 自定义一个自动完成
```
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion

class MyCustomCompleter(Completer):
    def get_completions(self, document, complete_event):
        yield Completion('completion', start_position=0)

text = prompt('> ', completer=MyCustomCompleter())
```

继承 class:`~prompt_toolkit.completion.Completer` 必须实现一个 带有生成器的方法 `~prompt_toolkit.completion.Completer.get_completions`, 这个方法需要 class:`~prompt_toolkit.document.Document` 的参数, 以及yield返回一个 class:`~prompt_toolkit.completion.Completion`
