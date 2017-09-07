# coding: utf-8

import sys
import socket
import fcntl
import struct
import logging
import urllib2
import re

pattern = re.compile(r'\s+')
url = 'http://192.168.8.103:8080/audit/add/'
socket.setdefaulttimeout(Connect_TimeOut)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    filename=sys.path[0] + 'omsys.log',
    filename='a'
)

if len(sys.argv) < 6:
    logging.error('History not configured in /etc/profile')
    sys.exit()


def get_local_ip(ethname):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        addr = fcntl.ioctl(sock.fileno(), 0x8915, struct.pack('256s', ethname))
        return socket.inet_ntoa(addr[20:24])
    except Exception as e:
        logging.error('get localhost IP address error: %s' % str(e))
        return '127.0.0.1'


def get_cmd(args):
    try:
        # Local Linux 1107 root 2017-07-03 14:30:05 ls
        seps = re.split(pattern, args, 6)
        temp_dict = {
            "run_user": seps[3],
            "client": seps[0],
            "tty": seps[1],
            "run_time": "{0} {1}".format(seps[4], seps[5]),
            'cmd': seps[-1],
            'history_id': seps[2],
            'host_ip': get_local_ip,
            'send_time': datetime.datetime.strftime(datetime.datetime.now(), TIME_FORMAT)
        }
       return json.dumps(temp_dict).encode('utf-8')
    except Exception as e:
        log.error('to_json error %s' % str(e))
        return None



def pull_history(data, url=url):
    if data is None:
        return
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json;charset=utf-8')
    response = urllib2.urlopen(req, json.dumps(data), timeout=1)


def main():
    data = sys.argv[1:]
    if data[0] != '127.0.0.1':
        data.pop(1)
        data.pop(1)

    data_cmd = get_cmd(' '.join(data))
    pull_history(data_cmd)


if __name__ == '__main__':
    main()
