# unicode python

Python unicode处理的原则:
1. 尽早的解码到unicode
2. 各个部分使用unicode
3. 尽量晚进行编码为utf8

```python
def  to_unicode_or_bust(
        obj, encoding="utf8"
    ):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj
```
