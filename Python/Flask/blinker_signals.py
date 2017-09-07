from blinker import signal

# 创建信号
started = signal('test-started')

def each(round):
    print "Round {}!".format(round)


def round_two(round):
    print "Only {}.".format(round)


def round_three(round):
    print "Three {}.".format(round)

#信号连接
started.connect(each)
started.connect(round_two, sender=2)
# started.connect(round_three, sender=3)

# 发送信号
for round in range(1, 4):
    started.send(round)
