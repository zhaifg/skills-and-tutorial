## 关于移动互联网TCP协议栈优化的一些材料总结

1. http://blog.chunshengster.me/2013/12/optimizing_your_linux_stack_for_maximum_mobile_web_performance.html [翻译，原文见：http://blog.cloudflare.com/optimizing-the-linux-stack-for-mobile-web-per

2. https://docs.google.com/presentation/d/1f2J_HrzMNvVHhsB3f7DKJFPl2N0Q_QR2ZEECWQu6oV8/present#slide=id.p19  google大神关于 high performance browser networking 的简版PPT

3. http://chimera.labs.oreilly.com/books/1230000000545/index.html   high performance browser networking 的在线电子书

4. https://developers.google.com/speed/protocols/tcpm-IW10?csw=1  协议栈优化中IW10 的所有关联文档
5. http://lwn.net/Articles/427104/  LWN中关于TCP initial congestion window 的解释
6. http://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/commit/?id=356f039822b8d802138f7121c80d2a9286976dbd  kernel git中关于 TCP: increase default initial receive window 的文档和代码
7. https://datatracker.ietf.org/doc/rfc6928/?include_text=1 rfc 6928关于 initial congestion window 的文档
8. http://research.csc.ncsu.edu/netsrv/?q=content/iw10  Experimental Evaluation of Increasing TCP Initial Congestion Window to 10 Segments
其他http://static.googleusercontent.com/media/research.google.com/en//pubs/archive/36640.pdf
http://lwn.net/Articles/426883/
http://www.ietf.org/proceedings/10mar/slides/iccrg-4.pdf
http://tools.ietf.org/html/rfc3390
http://tools.ietf.org/html/draft-mathis-tcpm-proportional-rate-reduction-01
http://monolight.cc/2010/12/increasing-tcp-initial-congestion-window/
http://www.cdnplanet.com/blog/tune-tcp-initcwnd-for-optimum-performance/
http://blog.habets.pp.se/2011/10/Optimizing-TCP-slow-start
http://idning.github.io/tcp_ip_increasing_init_cwnd.html
http://itindex.net/detail/46633-tcp-%E4%BC%98%E5%8C%96
http://blog.csdn.net/zhangskd/article/details/7608343
http://blog.csdn.net/zhangskd/article/details/7609465
