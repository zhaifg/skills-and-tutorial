# Python 性能测试方式
---
## cProfile
python -m cProfile -o profile.out  myscript.py

## pstats查看cProfile的效果

python -c "import pstats; p=pstats.Stats('profile.out');p.sort_stats('time')"

## line_profiler
一个按行计时和记录执行频率的工具, 能非常直观的看到哪一行有性能问题.
`pip install line_profiler`
最常用的是`@profile` 装饰器

`kernprof -l -v myscript.py`


## memory_profiler
监控python代码内存使用量, 使用psutil库来提高memory_profiler的性能. 
`pip install memory_profiler`


## timeit

## Python 代码质量测试


