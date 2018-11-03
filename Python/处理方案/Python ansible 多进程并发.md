# Ansible 的并发实现
---
通过阅读Ansible 源码，Ansible 通过使用 Process 的来提高性能， 这样可以绕开GIL的局限， 提高cpu多核的利用。

## ansible 多进程设计方式
TaskQueueManager, WorkerProcess， TaskExecutor， ResultExcutor, 
1. 继承Process的 `WorkerProcess`
ansible 扩展了 Process 的类

2. TaskQueueManager:
实现了类似于进程池的功能, 对进程队列进行管理, 一个具有共享数据结构/队列的管理器对象,用于协调所有流程之间的工作.

通过Queue就进行传递
