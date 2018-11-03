# Spider 类
---
## Spider

Spider类定义了如何爬取某个(或某些)网站。包括了爬取的动作(例如:是否跟进链接)以及如何从网页的内容中提取结构化数据(爬取item)。 换句话说，Spider就是您定义爬取的动作及分析某个网页(或者是有些网页)的地方。

对spider来说，爬取的循环类似下文:

1. 以初始的URL初始化`Request`，并设置回调函数。 当该`request`下载完毕并返回时，将生成 `response`，并作为参数传给该回调函数。

spider中初始的request是通过调用 `start_requests()` 来获取的。 `start_requests()` 读取 `start_urls` 中的URL， 并以 `parse` 为回调函数生成 `Request` 。

2. 在回调函数内分析返回的(网页)内容，返回 Item 对象或者 Request 或者一个包括二者的可迭代容器。 返回的Request对象之后会经过Scrapy处理，下载相应的内容，并调用设置的callback函数(函数可相同)。

3. 在回调函数内，您可以使用 选择器(Selectors) (您也可以使用BeautifulSoup, lxml 或者您想用的任何解析器) 来分析网页内容，并根据分析的数据生成item。

4. 最后，由spider返回的item将被存到数据库(由某些 Item Pipeline 处理)或使用 Feed exports 存入到文件中。

### scrapy.Spider
`class scrapy.spider.Spider`:

爬虫的基类, 提供基本的函数, start_requests(), parse() 等.

类变量: 
`name`: 爬虫标示符, scrapy 根据这个 查找爬虫. 全局唯一
`allowed_domains`:  可选的的列表, 允许爬虫爬取的 域名
`start_urls`:  list of urls, 爬虫开始url 列表
`custom_settings`: 字典形式的配置文件, 覆盖工程中的配置

`crawler`: 该属性由初始化类之后由from_crawler()类方法设置，并链接到此蜘蛛实例绑定到的Crawler对象。
`settings`:
`logger`:
`from_crawler(crawler, *args, **kwargs)`: 这是Scrapy用来创建蜘蛛的类方法。


方法:
`start_requests()`:
此方法必须返回一个可追溯的第一个请求爬网为这个蜘蛛。当蜘蛛打开刮刀时，它被Scrapy称为。 Scrapy只将其称为一次，因此可以安全地将start_requests()作为生成器实现。

默认实现为start_urls中的每个url生成Request（url，dont_filter = True）。
如果要更改用于开始抓取域的请求，则这是要覆盖的方法。例如，如果您需要首先使用POST请求登录，则可以执行以下操作：
```py
class MySpider(scrapy.Spider):
    name = 'myspider'

    def start_requests(self):
        return [scrapy.FormRequest("http://www.example.com/login",
                                   formdata={'user': 'john', 'pass': 'secret'},
                                   callback=self.logged_in)]

    def logged_in(self, response):
        # here you would extract links to follow and return Requests for
        # each of them, with another callback
        pass
```

`parse(response)`
当response没有指定回调函数时，该方法是Scrapy处理下载的response的默认方法。

parse 负责处理response并返回处理的数据以及(/或)跟进的URL。 Spider 对其他的Request的回调函数也有相同的要求。

该方法及其他的Request回调函数必须返回一个包含 Request 及(或) Item 的可迭代的对象。

参数: response (Response) – 用于分析的response
`log(message[, component])`
使用 scrapy.log.msg() 方法记录(log)message。 log中自动带上该spider的 name 属性。 更多数据请参见

`closed(reason)`
当spider关闭时，该函数被调用。 该方法提供了一个替代调用signals.connect()来监听 spider_closed 信号的快捷方式。

```py
import scrapy


class MySpider(scrapy.Spider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = [
        'http://www.example.com/1.html',
        'http://www.example.com/2.html',
        'http://www.example.com/3.html',
    ]

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
```

Return multiple Requests and items from a single callback:

```py
import scrapy

class MySpider(scrapy.Spider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = [
        'http://www.example.com/1.html',
        'http://www.example.com/2.html',
        'http://www.example.com/3.html',
    ]

    def parse(self, response):
        for h3 in response.xpath('//h3').extract():
            yield {"title": h3}

        for url in response.xpath('//a/@href').extract():
            yield scrapy.Request(url, callback=self.parse)
```

Instead of start_urls you can use start_requests() directly; to give data more structure you can use Items:

```py
import scrapy
from myproject.items import MyItem

class MySpider(scrapy.Spider):
    name = 'example.com'
    allowed_domains = ['example.com']

    def start_requests(self):
        yield scrapy.Request('http://www.example.com/1.html', self.parse)
        yield scrapy.Request('http://www.example.com/2.html', self.parse)
        yield scrapy.Request('http://www.example.com/3.html', self.parse)

    def parse(self, response):
        for h3 in response.xpath('//h3').extract():
            yield MyItem(title=h3)

        for url in response.xpath('//a/@href').extract():
            yield scrapy.Request(url, callback=self.parse)
```

## Spider 参数
`scrapy  crawl myspider -a  category=electronics`

```py
import scrapy
class MySpider(scrapy.Spider):
    name = 'myspider'

    def __init__(self, category=None, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://www.example.com/categories/%s' % category]
```
or
```py

import scrapy

class MySpider(scrapy.Spider):
    name = 'myspider'

    def start_requests(self):
        yield scrapy.Request('http://www.example.com/categories/%s' % self.category)
```

## CrawlSpider

### 属性
* rules:
  * `class scrapy.spiders.Rule(link_extractor, callback=None, cb_kwargs=None, follow=None, process_links=None, process_request=None)`
  * link_extractor
  * callback
  * cb_kwargs
  * follow
  * process_links
  * process_request
* parse_start_url

```py
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MySpider(CrawlSpider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    )

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        item = scrapy.Item()
        item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
        item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
        item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
        return item
```

## XMLFeedSpider

## CSVFeedSpider

## SitemapSpider
