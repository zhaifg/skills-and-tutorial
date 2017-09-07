# Werkzeug 的手册
---



## Werkzeug 的使用

### DebuggedApplication
`werkzeug.debug.DebuugedApplication` 实现了杀手级别的调试器.

```
from werkzeug.debug import DebuggedApplication
from myapp import app
app = DebuggedApplication(app, evalex=True)
```

可以与django和tornado结合

tornado 自定义请求类
```
import tornado.web
from werkzeug.debug import DebuggedApplication

class Handler(tornado.web.RequestHandler):
    def initialize(self, debug):
        if debug:
            self.write_error = self.write_debugger_error

    def write_debugger_error(self, status_code, **kwargs):
        assert isinstance(self.application, DebuggedApplication)

        html = self.application.render_exception()
        self.write(html.encode('utf-8', 'replace'))
```

如果是开启了Debug模式, 则使用DebugApplication 的 render_exception方法生成HTML. 基于Handler 创建一个使用GET就会报错的BadHandler:
```
class BadHandler(Handler):
    def get(self):
        raise Exception('This is a test')
        self.write('You will never see this text.')
```
