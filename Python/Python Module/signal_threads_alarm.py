#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-01-01 08:25:08
# @Author  : Zhaifg (zhaifengguo@foxmail.com)
# @Link    : http://htop.me
# @Version : $Id$

import signal
import time
import threading

def signal_handler(num, stack):
    print time.ctime(), "Alarm in", threading.currentThread().name

signal.signal(signal.SIGALRM, signal_handler)

def use_alarm():
    t_name = threading.currentThread().name
    print time.ctime(), 'Setting alarm in', t_name
    signal.alarm(1)
    print time.ctime(), 'Sleeping in', t_name
    time.sleep(3)
    print time.ctime(), 'Done with sleep in', t_name

# start a thread that will not receive the signal

alarm_thread = thread.Thread(target=use_alarm, name='alarm_thread')

alarm_thread.start()
time.sleep(0.1)

# Wait for the thread to see the signal (not going to happen!)
alarm_thread.join()

print time.ctime(), 'Exiting normally'


