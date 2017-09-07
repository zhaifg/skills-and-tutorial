# tornado tcp 的编程
---

使用tornado 的 tcpserver 进行 c/s 开发时, 定义tcp server 的通常有两种方式
###  直接继承tcpserver.TCPServer 类, 使用IOStream 进行处理
直接继承tcpserver.TCPServer 类, 使用IOStream 进行处理, 自定义的 TCPServer 类中,  实现 `handle_stream(self, stream, address)` 的方法
如:
```py

class EchoServer(TCPServer):
    def __init__(self, io_loop=None, **kwargs):
        super(EchoServer, self).__init__(io_loop=io_loop, **kwargs)

    def handle_stream(self, stream, address):
        # 处理stream
        Connection(stream=stream, address=address)

class  Connection(object): # 定义一个专门处理连接的类
    clients = set()
    def __init__(self, stream, address):
        Connection.clients.add(self)
        self._stream = stream
        self._address = address
        self._stream.set_close_callback(self._con_close)

    def read_request(self):
        self._stream.read_until('\n', self._handle)

    def _handle(self, data):
        pass

    def _con_close(self):
        Connection.client.remove(self)
        #

```

### 自定义实现 TcpServer

```
class TcpServer(object):
    def __init__(self, address, build_class, **build_kwargs):
        self._address = address
        self._build_class = build_class
        self._build_kwargs = build_kwargs

    def _accept_handler(self, sock, fd, events):
        while True:
            try:
                获得conn
                connection, address = sock.accept()
            except socket.error, e:
                return

            #通过conn解析
            self._handle_connect(connection)

    def _handle_connect(self, sock):
        #这里的conn主要是我们来解析数据的protocol
        conn = self._build_class(sock, **self._build_kwargs)
        self.on_connect(conn)

        close_callback = functools.partial(self.on_close, conn)
        #设置一个conn关闭时执行的回调函数
        conn.set_close_callback(close_callback)

    def startFactory(self):
        pass

    def start(self, backlog=0):
        #创建socket
        socks = build_listener(self._address, backlog=backlog)

        io_loop = ioloop.IOLoop.instance()
        for sock in socks:
            #接受数据的handler
            callback = functools.partial(self._accept_handler, sock)
            #为ioloop添加handler，callback
            io_loop.add_handler(sock.fileno(), callback, WRITE_EVENT | READ_EVENT | ERROR_EVENT)
        #在ioloop开启后，添加一个回调函数
        ioloop.IOLoop.current().add_callback(self.startFactory)

    #接受buff的函数，继承tcpserver的时候可以重写。
    def handle_stream(self, conn, buff):
        logger.debug('handle_stream')

    def stopFactory(self):
        pass

    def on_close(self, conn):
        logger.debug('on_close')

    def on_connect(self, conn):

        logger.debug('on_connect: %s' % repr(conn.getaddress()))

        handle_receive = functools.partial(self.handle_stream, conn)
        conn.read_util_close(handle_receive)
```