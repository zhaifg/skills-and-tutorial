# scrapy  命令
---

## 配置设置
1. scrapy.cfg  c:/scrapy/scrapy.cfg
2. /etc/scrapy.cfg  ($XDG_CONFIG_HOME)   ~/.scrapy/cfg
3. scrapy.cfg 项目

## 默认的项目结构
```
scrapy.cfg
myproject/
    __init__.py
    items.py
    middlewares.py
    pipelines.py
    settings.py
    spiders/
        __init__.py
        spider1.py
        spider2.py
```

## scrapy 命令工具
`scrapy startproject myproject [project_dir]`

`scrapy genspider mydomain mydomain.com` 创建新的spider

### 全局命令
1. startproject
2. genspider
3. settings
4. runspider
5. shell
6. fetch
7. view
8. version

### 项目命令
1. crawl
2. check
3. list
4. edit
5. parse
6. bench
