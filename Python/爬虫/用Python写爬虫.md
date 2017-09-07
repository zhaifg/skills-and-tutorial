# 用Python写爬虫--阅读
---
## 爬虫简介
1. 了解竞争对手价格
2. 价格对比

爬虫合法性

robots.txt
sitemap: 网站提供的Sitemap 文件 （即网 站 地图） 可以帮助爬虫定位网 站 最新的
内 容 ， 而 无须爬 取每 一 个网页。 

网站估算:
利用搜索引擎, 估算
识别网站的技术: builtwith 包
```
pip install buildwith
import builtwith
builtwith.parse('http://www.baidu.com')
```

分析网页:
查看源代码
firebug
chrome 开发者工具

正则表达式
beautifulsoup
lxml


find('ul', attrs={'class': 'country'})
lxml
