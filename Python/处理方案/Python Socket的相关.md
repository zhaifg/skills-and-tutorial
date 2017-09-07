# Python Socket 相关
--- 

Python 提供了两个基本的socket模块.
1. Socket, 他提供了标准的BSD Sockets API
2. SocketServer, 提供了服务器中心类, 可以简化网络服务器开发

## socket模块下的属性

### 协议族
- `socket.AF_UNIX`: 
- `socket.AF_INET`:
- `socket.AF_INET6`:

### 套接类型
- `socket.SOCK_STREAM` : TCP
- `socket.SOCK_DGRAM`: UDP
- `socket.SOCK_RAW`
- `socket.SOCK_RDM`
- `socket.SOCK_SEQPACKET`

## socket 模块的函数
- `socket.getaddrinfo(host, port[, family[, socktype[, proto[, flags]]]])`

```
socket.getaddrinfo("example.org", 80, 0, 0, socket.IPPROTO_TCP)
[(10, 1, 6, '', ('2606:2800:220:1:248:1893:25c8:1946', 80, 0, 0)),
 (2, 1, 6, '', ('93.184.216.34', 80))]
```

- `socket.getfqdn([name])`: 
- `socket.gethostbyname(hostname)`
- `socket.gethostname()`
- `socket.gethostbyaddr(ip_address)`
- 
- `socket.getnameinfo(sockaddr, flags)`: socketaddr=(host,port) flags
- `socket.getprotobyname(protocolname)`: 通过协议名称获取相应的协议号, 如icmp=1, tcp=6
- `socket.getservbyname(servicename[, protocolname])`: 通过服务名获取端口信息, protocolname:udp, tcp
- `socket.getservbyport(port[, protocolname])`

- `socket.socket([family[, type[, proto]]])`: 
使用给定的协议族,套接类型,协议号,新建一个新socket对象. 
协议族默认是 AF_INET, AF_INET6(ipv6), AF_UNIX, unix的套接字
套接类型:
  SOCKET_STREAM: tcp
  SOCKET_SGRAM: udp
  等

- `socket.socketpair([family[, type[, proto]]])`: 
使用给定的地址族、套接字类型和协议号，构建一对连接的套接字对象。
- `socket.fromfd(fd, family, type[, proto])`:
  复制文件的描述符fd(通过文件对象的 fileno()方法)和并使用fd创建一个socket对象. fd应该指向一个socket 对象,但不会检查. 如果fd无效, 则后面 对象会失败.
  这个很少使用


- `socket.ntohl(x)`:把32位正整数从网络序转换成主机字节序。. 主机字节序和网路网络字节序之间的转换
- `socket.ntohs(x)`:把16位正整数从网络序转换成主机字节序。

- `socket.htonl(x)`: 把32位正整数从主机字节序转换成网络序。
- `socket.htons(x)`:把16位正整数从主机字节序转换成网络序。

- `socket.inet_aton(ip_string)`: 转换IPV4地址字符串（192.168.10.8）成为32位打包的二进制格式（长度为4个字节的二进制字符串），它不支持IPV6。inet_pton()支持IPV4/IPV6地址格式。
- `socket.inet_ntoa(packed_ip)`:转换32位打包的IPV4地址为IP地址的标准点号分隔字符串表示。
- `socket.inet_pton(address_family, ip_string)`: 转换IP地址字符串为打包二进制格式。地址家族为AF_INET和AF_INET6，它们分别表示IPV4和IPV6。
- `socket.inet_ntop(address_family, packed_ip)`: 转换一个打包IP地址为标准字符串表达式，例如：“5aef:2b::8”或“127.0.0.1”。


- `socket.getdefaulttimeout()`
- `socket.setdefaulttimeout(timeout)`


## Socket Objects:

- `socket.accept()`: 
 用于server端, 接受一个连接.sock 必须已经bind和设置listen, 返回(conn, address),
 conn是一个新的socket 对象用于接受和发送消息, address是bind在sock(client端)的地址

- `socket.bind(address)`:  
把address 绑定到socket上, 
- `socket.close()`: 

- `socket.connect(address)`:
用户客户端, 用于连接某个socket server

- `socket.connect_ex(address)`: 
- `socket.fileno()`: 返回 socket 的 fd, 小整数. 使用select.select是比较有用.
windows 与unix 不同

- `socket.getpeername()`: 
返回套接字连接的远程地址。这是找出一个远端IPv4/IPv6套接字的端口号是有用的,. 不是所有操作系统都支持
- `socket.getsockname()`:
- `socket.getsockopt(level, optname[, buflen])`:
返回相应socket操作的值, man getsockopt. 一般是SO_*等,

- `socket.ioctl(control, option)`:
用于windows 平台.

- `socket.listen(backlog)`:
最大的连接数

- `socket.makefile([mode[, bufsize]])`:
返回与套接字关联的文件对象.. 文件对象不明确时，关闭Socket（）方法被调用，但只有删除其引用的socket 对象，使socket将不从其他地方引用封闭.
必须是阻塞的

- `socket.recv(bufsize[, flags])`:
sock 接收数据

- `socket.recvfrom(bufsize[, flags])`:
从socket接收数据. 返回的数据是一个(string, address)元组, string是数据, address是发送端的数据, udp.

- `socket.recvfrom_into(buffer[, nbytes[, flags]])`:
从套接字接收数据，写入缓冲区，而不是创建一个新的字符串。
返回值是一元组（nbytes，address），nbytes是接收的字节和地址发送数据的套接字的地址数。

- `socket.recv_into(buffer[, nbytes[, flags]])`:

- `socket.send(string[, flags])`:
- `socket.sendall(string[, flags])`:
- `socket.sendto(string, address)`:


- `socket.setblocking(flag)`: 
设置是否是阻塞. flag=1阻塞, flag=0 非阻塞
- `socket.settimeout(value)`
- `socket.gettimeout()`

- `socket.setsockopt(level, optname, value)`:
设置一些tcp的属性值.
如:
修改套接字发送和接收的缓冲区大小:
```
    sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
    sock.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_SNDBUF,
        SEND_BUF_SIZE
    )

    sock.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_RCVBUF,
        RECV_BUF_SIZE
    )
```


重用套接字地址
如果在某个端口运行一个Python套接字服务器, 连接一次之后便终止, 就不能再使用这个端口了, 如果再次连接时提示
Address already used

解决办法 开启重用 SO_REUSEADDR
`sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)`

`socket.shutdown(how)`

## 编程实例
### 1. 简单的c/s
```python
# Echo server program
import socket

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr
while 1:
    data = conn.recv(1024)
    if not data: break
    conn.sendall(data)
conn.close()
```

```python
# Echo client program
import socket

HOST = 'daring.cwi.nl'    # The remote host
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall('Hello, world')
data = s.recv(1024)
s.close()
print 'Received', repr(data)
```



### socket 的服务端和client端的通信

C/S的通信图(tcp)
![通信图](img/sokcet_comu.png)

udp图
![通信图](img/sokcet_comu_udp.png)


### udp实例
```python
#服务器端
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket

BUF_SIZE = 1024  #设置缓冲区大小
server_addr = ('127.0.0.1', 8888)  #IP和端口构成表示地址
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #生成新的套接字对象
server.bind(server_addr)  #套接字绑定IP和端口
while True :
    print "waitting for data"
    data, client_addr = server.recvfrom(BUF_SIZE)  #从客户端接收数据
    print 'Connected by', client_addr, ' Receive Data : ', data
    server.sendto(data, client_addr)  #发送数据给客户端
server.close()
```

```python
#客户端
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import struct

BUF_SIZE = 1024  #设置缓冲区
server_addr = ('127.0.0.1', 8888)  #IP和端口构成表示地址
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #生成新的套接字对象

while True :
    data = raw_input('Please Input data > ')
    client.sendto(data, server_addr)  #向服务器发送数据
    data, addr = client.recvfrom(BUF_SIZE)  #从服务器接收数据
    print "Data : ", data
client.close()
```





Python的socket网络编程, 在实现高性能的多用户时, 可以使用多线程
或者多进程方式, 属于同步I/O. 或者通过I/O的复用的方式进行, 比如使用select模式和epoll, 异步I/O.

## SocketServer
+------------+
| BaseServer |
+------------+
      |
      v
+-----------+        +------------------+
| TCPServer |------->| UnixStreamServer |
+-----------+        +------------------+
      |
      v
+-----------+        +--------------------+
| UDPServer |------->| UnixDatagramServer |
+-----------+        +--------------------+

SocketServer模块是用于简化编写网络编程的模块.有四个基础的server类

- `class SocketServer.TCPServer(server_address, RequestHandlerClass, bind_and_activate=True)`: 使用tcp协议完成的SocketServer. 如果 bind_and_activate = True, 自动尝试server_bind和server_active. 其他的参数传递给BaseServer.

- `class SocketServer.UDPServer(server_address, RequestHandlerClass, bind_and_activate=True)`

- `class SocketServer.UnixStreamServer(server_address, RequestHandlerClass, bind_and_activate=True)`
- `class SocketServer.UnixDatagramServer(server_address, RequestHandlerClass, bind_and_activate=True)`: 继承自UDPServer

以上这个四个Class处理请求时同步, 每个请求必须完成才能处理下一个请求. 可以使用`ForkingMixIn`(多进程)和`ThreadMixIn`(多线程)来处理,使之成为异步处理.

一般的步骤为:
1. 先创建一个`BaseRequestHandler`的子类, 重写handle()方法, 这个方法是处理请求的.
2. 实例化一个Server类对象, 通过这个server对象的address和上面的定义Handler类(可以创建一Server类子类, 且继承ForkingMixIn或ThreadMixIn, 来实现异步效果).
3. 调用Server类对象的`handle_request` 或者`serve_forever()`方法, 来处理更多请求
4. 使用`server_close()`关闭对象.
> 如果使用ThreadMixIn时, 必须明确的设置thread的Daemon, 避免提前主程序提前退出.

### Server Objects
`class SocketServer.BaseServer(server_address, RequestHandlerClass)`

方法
- fileno()
- handle_request()
- serve_forever(poll_interval=0.5)
- shutdown()
- server_close()
属性
- address_family
- RequestHandlerClass
- server_address
- socket
- allow_reuse_address
- request_queue_size
- socket_type
- timeout

其他的可以重写的方法:
- finish_request(): 
- get_request()()()
- handle_error()()
- handle_timeout()
- process_request(request, client_address)
- server_activate()
- server_bind()
- verify_request(request, client_address)

### Request Handler Objects
class SocketServer.BaseRequestHandler
方法:
setup(): Called before the handle() method to perform any initialization actions required. The default implementation does nothing.

handle(): 
finish()

### 实例
####  1. 
```python
import SocketServer

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
```


```python
class MyTCPHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        self.wfile.write(self.data.upper())
```

client
```python
import socket
import sys

HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(data + "\n")

    # Receive data from the server and shut down
    received = sock.recv(1024)
finally:
    sock.close()

print "Sent:     {}".format(data)
print "Received: {}".format(received)
```


#### UDP
```python
import SocketServer

class MyUDPHandler(SocketServer.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print "{} wrote:".format(self.client_address[0])
        print data
        socket.sendto(data.upper(), self.client_address)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()
```

client
```python
import socket
import sys

HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().
sock.sendto(data + "\n", (HOST, PORT))
received = sock.recv(1024)

print "Sent:     {}".format(data)
print "Received: {}".format(received)
```
#### 多线程
```python
import socket
import threading
import SocketServer

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        response = "{}: {}".format(cur_thread.name, data)
        self.request.sendall(response)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        print "Received: {}".format(response)
    finally:
        sock.close()

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 0

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print "Server loop running in thread:", server_thread.name

    client(ip, port, "Hello World 1")
    client(ip, port, "Hello World 2")
    client(ip, port, "Hello World 3")

    server.shutdown()
    server.server_close()

```

#### 多进程
```python
import os
import socket
import threading
import SocketServer

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 0
BUF_SIZE = 1024
ECHO_MSG = 'Hello Echo Server'

class ForkingClient(object):

    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.connect((ip, port))

    def run(self):
        current_process_id = os.getpid()
        print "PID %s Sending echo message to the server : '%s'"%(current_process_id, ECHO_MSG)

        send_data_length = self.sock.send(ECHO_MSG)

        print "Send: %d Characters, so far ..." %send_data_length

        response = self.sock.recv(BUF_SIZE)
        print "PID %s recevid: %s" %(current_process_id, response)

    def shutdown(self):
        self.sock.close()


class ForkingServerRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(BUF_SIZE)
        current_process_pid = os.getpid()
        response = "%s: %s" %(current_process_pid, data)
        print "Server sending response [current_process_pid: data] = [%s]"%response
        self.request.send(response)
        return

class ForkingServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
    pass

def main():
    server = ForkingServer((SERVER_HOST, SERVER_PORT), ForkingServerRequestHandler)
    ip, port = server.server_address

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()
    print "Server loop running PID: %s"%os.getpid()

    client1 = ForkingClient(ip, port)
    client1.run()

    client2 = ForkingClient(ip, port)
    client2.run()

    server.shutdown()
    client1.shutdown()
    client2.shutdown()
    server.socket.close()


if __name__ == '__main__':
    main()
```

## 网络多路复用--select
关于的IO模型, 都会牵扯到同步,异步,阻塞,非阻塞.
相关IO模型的概念, 可以参考一下文件

[也谈IO模型](http://www.importnew.com/22019.html)
[简明网络I/O模型---同步异步阻塞非阻塞之惑](http://www.jianshu.com/p/55eb83d60ab1)

Python 在多路复用模型中, 比较常用的有select模型和poll模型,这两个都是系统接口, 由操作系统提供. Python进行了高层封装.

### select 原理
网络通信被Unix系统抽象为文件的读写, 通常一个设备, 由设备驱动程序提供, 驱动可以知道自身的数据是否可用. 支持阻塞操作的设备驱动通常会实现一组自身的等待队列, 例如读/写等待队列用于支持上层(用户层)所需的block或者no_block操作. 设备的文件的资源如果可以使用(可读或者可写)则会通知进程, 反之会让进程睡眠, 等到数据到来的时候, 再唤醒进程.

这些设备的文件描述符放在一个数组中, 然后select调用的时候遍历这个数组,  如果对于的文件描述符可读则会返回文件描述符. 当遍历结束之后, 如果仍然没有一个可用设备描述符,  select让用户进程睡眠,  直到等待资源可用的时候唤醒进程, 遍历之前那个监视数组. 每次遍历都是线性的.

`select.select（rlist, wlist, xlist[, timeout]）` 传递三个参数，一个为输入而观察的文件对象列表，一个为输出而观察的文件对象列表和一个观察错误异常的文件列表。第四个是一个可选参数，表示超时秒数。其返回3个tuple，每个tuple都是一个准备好的对象列表，它和前边的参数是一样的顺序。下面，主要结合代码，简单说说select的使用

### 实例

1. server
```python
import select
import socket
import Queue
 
#create a socket
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setblocking(False)

#set option reused
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR  , 1)
 
server_address= ('192.168.1.102',10001)
server.bind(server_address)
 
server.listen(10)
 
#sockets from which we except to read
inputs = [server]
 
#sockets from which we expect to write
outputs = []
 
#Outgoing message queues (socket:Queue)
message_queues = {}
 
#A optional parameter for select is TIMEOUT
timeout = 20
 
while inputs:
    print "waiting for next event"
    readable , writable , exceptional = select.select(inputs, outputs, inputs, timeout)
 
    # When timeout reached , select return three empty lists
    if not (readable or writable or exceptional) :
        print "Time out ! "
        break;    
    for s in readable :
        if s is server:
            # A "readable" socket is ready to accept a connection
            connection, client_address = s.accept()
            print "    connection from ", client_address
            connection.setblocking(0)
            inputs.append(connection)
            message_queues[connection] = Queue.Queue()
        else:
            data = s.recv(1024)
            if data :
                print " received " , data , "from ",s.getpeername()
                message_queues[s].put(data)
                # Add output channel for response    
                if s not in outputs:
                    outputs.append(s)
            else:
                #Interpret empty result as closed connection
                print "  closing", client_address
                if s in outputs :
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                #remove message queue 
                del message_queues[s]
    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except Queue.Empty:
            print " " , s.getpeername() , 'queue empty'
            outputs.remove(s)
        else:
            print " sending " , next_msg , " to ", s.getpeername()
            s.send(next_msg)
     
    for s in exceptional:
        print " exception condition on ", s.getpeername()
        #stop listening for input on the connection
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        #Remove message queue
        del message_queues[s]
```

- 2. ChatServer 实例
```python

import select
import socket
import sys 
import signal
import cPickle
import struct
import argparse

SERVER_HOST = '127.0.0.1'
CHAT_SERVER_NAME = 'server'

def send(channel, *args):
    buffer = cPickle.dumps(args)
    value = socket.htonl(len(buffer))
    size = struct.pack("L", value)
    channel.send(size)
    channel.send(buffer)

def receive(channel):
    size = struct.calcsize("L")
    size = channel.recv(size)
    try:
        size = socket.ntohl(struct.unpack("L", size)[0])
    except struct.error, e:
        return ''
    buf = ""
    while len(buf) < size:
        buf += channel.recv(size - len(buf))
    return cPickle.loads(buf)[0]


class ChatServer(object):

    def __init__(self, port, backlog=5):
        self.clinets = 0  # client计数
        self.clientmap = {} # 存放client客户端的
        self.outputs = []  # 
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((SERVER_HOST, port))
        print "Server listening to port: %s ..."%port
        self.server.listen(backlog)
        signal.signal(signal.SIGINT, self.sighandler)

    def sighandler(self, signum, frame):
        # 处理新号的函数
        print  "Shutting down server ..."
        for output in self.outputs:
            output.close()
        self.server.close()

    def get_client_name(self, client):
        info = self.clientmap[client]
        host, name = info[0][0], info[1]
        return "@".join((name, host))

    def run(self):
        inputs = [self.server, sys.stdin]
        self.outpus = []
        running = True
        while running:
            try:
                readable, writeable, exceptional = select.select(inputs, self.outputs, [])
            except select.error, e:
                break

            for sock in readable:
                if sock == self.server:
                    clinet, address = self.server.accept()
                    print "ChatServer: got connect %d from %s"%(clinet.fileno(), address)
                    print "Client: %s"%clinet

                    cname = receive(clinet).split('NAME: ')[1]
                    self.clinets += 1
                    send(clinet, 'CLINET: '+str(address[0]))
                    inputs.append(clinet)
                    self.clientmap[clinet] = (address, cname)

                    msg = "\n(Connected: New clinet (%d) from %s" %(self.clinets, self.get_client_name(clinet))

                    for output in self.outputs:
                        send(output, msg)

                    self.outputs.append(clinet)

                elif sock == sys.stdin:
                    junk = sys.stdin.readline()
                    running = False
                else:
                    try:
                        data = receive(sock)
                        if data:
                            msg = "\n#[ " + self.get_client_name(sock) +"]>>" + data
                            for output in self.outputs:
                                if output != sock:
                                    send(output, msg)
                        else:
                            print "Chat Server: %d hung up"%sock.fileno()
                            self.clinets -= 1
                            sock.close()
                            inputs.remove(sock)
                            msg = "\n(Now hung up: Clinet from %s)"%self.get_client_name(sock)

                            # out 可以单独循环发送
                            for output in self.outputs:
                                send(output, msg)
                    except socket.error, e:
                        input.remove(sock)
                        self.outputs.remove(sock)
        self.server.close()

class ChatClient(object):
    def __init__(self, name, port, host=SERVER_HOST):
        self.name = name
        self.connected = False
        self.host = host
        self.port = port
        self.prompt = '[' + '@'.join((name, socket.gethostname().split('.')[0])) + ']>'

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, self.port))
            print "Now connected to chat server @ port %d"%self.port

            self.connected = True
            send(self.sock, 'NAME: ' + self.name)
            data = receive(self.sock)
            addr = data.split('CLINET: ')[1]
            self.prompt = '\n[' + '@'.join((self.name, addr)) + ']>'
        except socket.error, e:
            print "Failed to connected to chat sever @ port %d"%self.port
            sys.exit(1)


    def run(self):

        while self.connected:
            try:
                sys.stdout.write(self.prompt)
                sys.stdout.flush()
                readable, writeable, exceptional = select.select([0, self.sock], [], [])
                for sock in readable:
                    if sock == 0:
                        data = sys.stdin.readline().strip()
                        if data:
                            send(self.sock, data)
                    elif sock ==  self.sock:
                        data = receive(self.sock)
                        if not data:
                            print "Client shutting down."
                            self.connected = False
                            break
                        else:
                            sys.stdout.write(data + '\n')
                            sys.stdout.flush()
            except KeyboardInterrupt:
                print "CLient interrupted ..."
                self.sock.close()
                break


if __name__ == '__main__':
    parse = argparse.ArgumentParser(description="Socket Server Example with select")
    parse.add_argument('--name', action="store", dest="name", required = True)
    parse.add_argument('--port', action='store', dest="port", type=int, required=True)
    give_args = parse.parse_args()
    port = give_args.port
    name = give_args.name

    if name == CHAT_SERVER_NAME:
        server = ChatServer(port)
        server.run()
    else:
        client = ChatClient(name=name, port=port)
        client.run()


```
http://xiaorui.cc/2014/11/13/python%E4%B8%8B%E7%AE%80%E5%8D%95%E5%AE%9E%E7%8E%B0select%E5%92%8Cepoll%E7%9A%84socket%E7%BD%91%E7%BB%9C%E7%BC%96%E7%A8%8B/

### epoll

```python

import socket
import select

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
response  = b'HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 1996 01:01:01 GMT\r\n'
response += b'Content-Type: text/plain\r\nContent-Length: 13\r\n\r\n'
response += b'Hello, world!'
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('0.0.0.0', 8080))
serversocket.listen(1)
serversocket.setblocking(0)

epoll = select.epoll()
epoll.register(serversocket.fileno(), select.EPOLLIN)
try:
   connections = {}; requests = {}; responses = {}
   while True:
      events = epoll.poll(1)
      for fileno, event in events:
         if fileno == serversocket.fileno():
            connection, address = serversocket.accept()
            connection.setblocking(0)
            epoll.register(connection.fileno(), select.EPOLLIN)
            connections[connection.fileno()] = connection
            requests[connection.fileno()] = b''
            responses[connection.fileno()] = response
         elif event & select.EPOLLIN:
            requests[fileno] += connections[fileno].recv(1024)
            if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
               epoll.modify(fileno, select.EPOLLOUT)
               connections[fileno].setsockopt(socket.IPPROTO_TCP, socket.TCP_CORK, 1)
               print('-'*40 + '\n' + requests[fileno].decode()[:-2])
         elif event & select.EPOLLOUT:
            byteswritten = connections[fileno].send(responses[fileno])
            responses[fileno] = responses[fileno][byteswritten:]
            if len(responses[fileno]) == 0:
               connections[fileno].setsockopt(socket.IPPROTO_TCP, socket.TCP_CORK, 0)
               epoll.modify(fileno, 0)
               connections[fileno].shutdown(socket.SHUT_RDWR)
         elif event & select.EPOLLHUP:
            epoll.unregister(fileno)
            connections[fileno].close()
            del connections[fileno]
finally:
   epoll.unregister(serversocket.fileno())

```

### 2. 


[http://scotdoyle.com/python-epoll-howto.html](http://scotdoyle.com/python-epoll-howto.html)
[Epoll 模型简介](http://www.jianshu.com/p/0fb633010296)

## 序列化数据

## 第三方库 diesel


https://docs.python.org/2/library/socketserver.html#module-SocketServer
