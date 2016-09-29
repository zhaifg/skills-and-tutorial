#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-01-01 10:10:32
# @Author  : Zhaifg (zhaifengguo@foxmail.com)
# @Link    : http://htop.me
# @Version : $Id$

import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadingName)-10s) %(message)s')

def daemon():
    logging.debug('Starting')
    time.sleep(2)
    logging.debug('Exiting')

d = threading.Thread(name='daemon', target=daemon)
d.setDaemon(True)

def non_daemon():
    logging.debug('Starting')
    logging.debug('Exiting')

t = threading.Thread(name='non-daemon', target=non_daemon)
d.start()
t.start()


