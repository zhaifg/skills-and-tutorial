# requests
---

```py

>>> r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
>>> r.status_code
200
>>> r.headers['content-type']
'application/json; charset=utf8'
>>> r.encoding
'utf-8'
>>> r.text
u'{"type":"User"...'
>>> r.json()
```

## 功能特性

* Keep-Alive & 连接池
* 国际化域名和 URL
* 带持久 Cookie 的会话
* 浏览器式的 SSL 认证
* 自动内容解码
* 基本/摘要式的身份认证
* 优雅的 key/value Cookie
* 自动解压
* Unicode 响应体
* HTTP(S) 代理支持
* 文件分块上传
* 流下载
* 连接超时
* 分块请求
* 支持 .netrc
