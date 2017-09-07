# Elasticsearch 的文档
---

##  安装

...

## 术语

* 索引(名词): index indices/indexes
* 索引(动词): 
* 倒排索引: 关系型数据库通过增加一个 索引 比如一个 B树（B-tree）索引 到指定的列上，以便提升数据检索速度。Elasticsearch 和 Lucene 使用了一个叫做 倒排索引 的结构来达到相同的目的
* 默认: 


## 简单操作


### 创建索引

### 搜索

`GET /index_name/type/_search`

```
{
  "query": {
    "match": {
        "url"
    }
  }
}
```
### DSL

### filter DSL

#### term 过滤
主要用于精确匹配哪些值, 比如数字, 日期, 布尔值, not_analyzed 的字符串(未经分析的文本数据类型)
```
{
    "term": {
        "age": 25
    }

}

# hostname 字段完全匹配成 saaap.wangpos.com

{ 
  "query": { 
    "term": { 
      "hostname": "saaap.wangpos.com" 
    } 
  } 
}
```

#### terms
terms 与 term 相似, 但是terms 允许指定多个匹配条件. 如果某个字段指定了多个值, 那么文档需要一起去匹配

```json
{
    "terms": {
        "tag": ["search", "full_text", "nosql"]
    }
}

# 完整的例子，所有http的状态是 302 、304 的， 由于ES中状态是数字类型的字段，所有这里我们可以直接这么写

{
    "query":{
        "terms":{
            "status": [200, 304]
        }
    }
}
```

#### range 过滤
range 过滤允许我们指定范围内查找一批数据:

`gt` :: 大于
`gte`:: 大于等于
`lt` :: 小于
`lte`:: 小于等于

```json
{
    "range":{
        "age":{
            "gte":20,
            "lt": 30
        }
    }
}

// 请求页面耗时大于1秒的数据，upstream_response_time 是 nginx 日志中的耗时，ES中是数字类型。

{ 
  "query": { 
    "range": { 
      "upstream_response_time": { 
        "gt": 1 
      } 
    } 
  } 
}

```

#### exists 和 missing
exists 和 missing 过滤可以用于查找文档中是否包含指定字段或者某个字段, 类似于SQL语句中的 is_null
```json
{
    "exists": {
        "field": "title"
    }
}
```

> 这两个过滤只是针对已经查出一批数据来，但是想区分出某个字段是否存在的时候使用


#### bool 过滤
bool 过滤可以用来合并多个过滤条件查询结果的布尔值, 它包含以下操作符:

* must : 多个查询条件的完全匹配, 相当于 and
* must_not: 多个查询条件的相反匹配, 相当于not
* should: 至少有一个查询条件匹配, 相当于 or

这些参数可以分别继承一个过滤条件或者一个过滤条件的组

```json
{
    "bool": {
        "must": {
            "term": {
                "folder": "inbox"
            }
        },
        "must_not": {
            "term": {
                "tag": "spam"
            }
        }
        "should": [
            {"term":{
                "sharred": true
                }},
            {
                "term": {
                    "unread": "true"
                }
            }
        ]
    }

}
```

### Query DSL

#### match_all 
可以查询到所有文档, 是没有查询条件下的默认语句

```json
{
    "match_all": {}
}
```

#### match 查询
match 查询是一个标准查询, 不管你需要全文查询还是精确查询基本上都要用到它
如果使用 match 查询一个全文字段, 它会在真正查询之前用分析器 match 一下查询字符:

```json
{
    "match": {
        "tweet": "About Search"
    }
}
```

如果用 match 下指定了一个确切值,  在遇到数字, 日期, 布尔值或者not_analyzed 的字符串时, 它将为你搜索你给定的值.

```json
{ "match": { "age":    26           }} 
{ "match": { "date":   "2014-09-01" }} 
{ "match": { "public": true         }} 
{ "match": { "tag":    "full_text"  }}
```

> 做精确匹配搜索时, 你最好使用过滤语句, 因为过滤语句可以缓存数据

match 查询只能就指定某个确切字段某个确切的值进行搜索, 而你要做的就是为它指定正确的字段名以避免语法错误.

#### multi_match 
multi_match 查询允许你做 match 查询的基础上同时搜索多个字段, 在多个字段中同时查一个:

```json
{ 
    "multi_match": { 
        "query":    "full text search", 
        "fields":   [ "title", "body" ] 
    } 
}
```

#### bool 查询

bool 查询 与 bool 过滤相似, 用于合并多个查询子句. 不同的是, bool 过滤可以直接给出是否匹配成功, 而bool 查询要计算每一个查询子句的_score(相关性分值)_

* must:: 查询指定文档一定要被包含。
* must_not:: 查询指定文档一定不要被包含。
* should:: 查询指定文档，有则可以为文档相关性加分。

以下查询将会找到title 字段中包含 "how to make millions", 并且 "tag" 字段 没有被标记为 spam. 如果表示为"starred" 或者发布日期为2014年以前, 那么这些匹配的文档将比同类网站等级高.

```json
{
    "bool": {
        "must": {
            "match": {
                "title": "how to make millions"
            }
        },
        "must_not": {
            "match": {
                "tag": "spam"
            }
        },
        "should": [
            {
                "match": {
                    "tag": "starred"
                },
                "range": {
                    "date": {
                        "gte": "2014-01-01"
                    }
                }
            }
        ]
    }
}
```

>如果bool 查询下没有must子句，那至少应该有一个should子句。但是 如果有must子句，那么没有should子句也可以进行查询

#### wildcards 查询
使用标准的 shell 通配符查询
以下是包含 W1F 7HW和W2F 8HW的文档:
```json
{
    "query": {
        "wildcards": {
            "postcode": "W?F*HW"
        }
    }
}
```

#### regexp 查询

假设只想匹配w开头, 紧跟数字的邮政编码. 使用regexp:

```json

{
    "query": {
        "regexp": {
            "postcode": "w[0-9].+"
        }
    }
}
```


#### prefix 查询
以什么字符开头的，可以更简单地用 prefix，如下面的例子：
```
{ 
  "query": { 
    "prefix": { 
      "hostname": "wxopen" 
    } 
  } 
}
```

#### 短语匹配(Phrase Matching)
当你需要寻找邻近的几个单词时，你会使用match_phrase查询：
```
GET /my_index/my_type/_search
{
    "query": {
        "match_phrase": {
            "title": "quick brown fox"
        }
    }
}
```
和match查询类似，match_phrase查询首先解析查询字符串来产生一个词条列表。然后会搜索所有的词条，
但只保留含有了所有搜索词条的文档，并且词条的位置要邻接。一个针对短语quick fox的查询不会匹配
我们的任何文档，因为没有文档含有邻接在一起的quick和box词条。
match_phrase查询也可以写成类型为phrase的match查询：
```
"match": {
    "title": {
        "query": "quick brown fox",
        "type":  "phrase"
    }
}
```
