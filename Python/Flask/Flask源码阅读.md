# Flask源码阅读
---

Flask的包结构解析

```
.
├── app.py  # 主类里面有Flask等
├── blueprints.py
├── _compat.py  # 设置了py2与py3的兼容性
├── config.py
├── ctx.py
├── debughelpers.py
├── ext
│   └── __init__.py
├── exthook.py
├── globals.py
├── helpers.py
├── __init__.py
├── json.py
├── logging.py
├── module.py
├── sessions.py
├── signals.py
├── templating.py
├── testing.py
├── testsuite
│   ├── appctx.py
│   ├── basic.py
│   ├── blueprints.py
│   ├── config.py
│   ├── deprecations.py
│   ├── examples.py
│   ├── ext.py
│   ├── helpers.py
│   ├── __init__.py
│   ├── regression.py
│   ├── reqctx.py
│   ├── signals.py
│   ├── static
│   │   └── index.html
│   ├── subclassing.py
│   ├── templates
│   │   ├── context_template.html
│   │   ├── escaping_template.html
│   │   ├── _macro.html
│   │   ├── mail.txt
│   │   ├── nested
│   │   ├── simple_template.html
│   │   ├── template_filter.html
│   │   └── template_test.html
│   ├── templating.py
│   ├── test_apps
│   │   ├── blueprintapp
│   │   ├── config_module_app.py
│   │   ├── config_package_app
│   │   ├── flask_broken
│   │   ├── flaskext
│   │   ├── flask_newext_package
│   │   ├── flask_newext_simple.py
│   │   ├── importerror.py
│   │   ├── lib
│   │   ├── main_app.py
│   │   ├── moduleapp
│   │   ├── path
│   │   └── subdomaintestmodule
│   ├── testing.py
│   └── views.py
├── views.py
└── wrappers.py

```


`helpers.py`:
`_PackageBoundObject`: 处理jinjia2模板的
