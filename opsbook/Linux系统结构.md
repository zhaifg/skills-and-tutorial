cpu: 寄存器, 运算器,控制器
一级缓存,二级缓存,三级缓存是共享的
cpu缓存的造价非常高

N路关联技术:




PAE: 物理地址扩展 physical address extension
32bit + 4位 =64G

cpu>>mem>>disk
   缓存  缓存

通写策略: write-through
回写策略: write-back 数据要丢弃的时候,才写到主存中

pci I/O高速I/O  南桥
pcie 总线  高速IO  在北桥


IO port 65535 任何设备接入主机时,向cpu注册申请连续的一片port

中断控制器

临界区: 有可能产生竞争的地方
DMA:  直接内存访问
