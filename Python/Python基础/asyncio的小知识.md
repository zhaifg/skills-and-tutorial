# asyncio 的小技巧
---

开启事件循环有两种方法，一种方法就是通过调用`run_until_complete`，另外一种就是调用 `run_forever` `。run_until_complete` 内置 `add_done_callback` ，使用 `run_forever` 的好处是可以通过自己自定义 `add_done_callback`.

## asyncio.gather vs asyncio.wait
https://stackoverflow.com/questions/42231161/asyncio-gather-vs-asyncio-wait
· 