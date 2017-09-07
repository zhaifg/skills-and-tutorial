#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-12-31 21:40:45
# @Author  : Zhaifg (zhaifengguo@foxmail.com)
# @Link    : http://htop.me
# @Version : $Id$

import signal
import threading
import os
import time

def signal_handler(num, stack):
    print "Received signal  %d in %s" % (num, threading.currentThread().name)

signal.signal(signal.SIGUSR1, signal_handler)


def wait_for_signal():
    print "Waiting for signal in", threading.currentThread().name
    signal.pause()
    print "Done waiting"

receiver = threading.Thread(target=wait_for_signal, name='receiver')
receiver.start()
time.sleep(0.1)

def send_signal():
    print "Sending signal in", threading.currentThread().name()
    os.kill(os.gitpid(), signal.SIGUSR1)

sender = threading.Thread(target=send_signal, name="sender")
sender.start()
sender.join()

print "Waiting for", receiver.name
signal.alarm(2)
receiver.join()

