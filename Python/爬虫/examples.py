#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-16 15:12:11
# @Author  : Zhaifg (zhaifengguo@foxmail.com)
# @Link    : http://htop.me
# @Version : $Id$

import os
import urllib
import urllib2
import urlparse
import coookielib


def download(url, num_retries=3):
    print "Downing:", url
    try:
        html = urllib2.urlopen(url).read()
    except　urllib2.URLError as e:
        print "Down error: ", e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return downlaod(url, num_retries - 1)
        return html

# 设置用户代理


def download(url, user_agent='wsap', num_retries=3):
    print "Downing:", url
    headers = {
        'User-agent': user_agent,
    }
    request = urllib2.Request(url, headers=headers)
    try:
        html = urllib2.urlopen(request).read()
    except　urllib2.URLError as e:
        print "Down error: ", e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return downlaod(url, num_retries - 1)
        return html


# 爬取网站地图

# urlparse : 相对路径和绝对路径

# 解析robots.txt 文件robotparser
# can_fetch

# 使用代理
proxy = 'ip'
opener = urllib2.build_opener()
proxy_params = {urlparse.urlparse(url).scheme: proxy}
opener.add_handler(urllib2.ProxyHandler(proxy_params))
respone = opener.open(request)


def download(url, user_agent='wswp', proxy=None, num_retries=3):
    print "Downloading....", url

    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)

    opener = urllib2.build_opener()

    if proxy:
        proxy_params = proxy_params = {urlparse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        html = opener.open(request).read()
    except　urllib2.URLError as e:
        print "Down error: ", e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return downlaod(url, num_retries - 1)
    return html

# 现在限速
# 增加两次下载之间的延时


class Throttle:
    '''
    增加同一站点上的两个下载之间的延时.
    '''

    def __init__(self, delay):
        self.delay = delay
        self.domains = {}

    def wait(self, url):
        domain = urlparse.urlparse(url).netloc
        last_accessedd = self.domains.get('domain')

        if self.delay > 0 and last_accessedd is not None:
            sleep_secs = self.delay - \
                (datetime.datetime.now() - last_accessedd).secends
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.datetime.now()

# 避免爬虫陷阱

# 添加回调函数

# 添加缓存


class Downloader(object):
    def __init__(self, delay=5, user_agent='wswp', proxies=None,
                 num_retries=2, cache=None):
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.cache = cache

    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                pass
            else:
                if self.num_retries > 0 and \
                        500 <= result['code'] < 600:
                    result = None
        if result is None:
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-agent': self.user_agent}
            result = self.downlaod(url, headers, proxy, self.num_retries)
            if self.cache:
                self.cache[url] = result
        return result['html']

    def download(self, url, headers, proxy, num_retries, data=None):
        return {
            'html': html,
            'code': code
        }

# 基于磁盘的缓存, 文件名限制, 目录的/的限制


# 登录

LOGIN_URL = ''
LOGIN_EMAIL = ''
PASSEWORD = ''
data = {
    'email': LOGIN_EMAIL,
    'password': PASSEWORD
}

encoded_data = urllib.urlencode(data)
request = urllib2.Request(LOGIN_URL, encoded_data)
response = urllib2.urlopen(request)
response.geturl()

cj = cookielib.CookeJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
request = urllib2.Request(LOGIN_URL, encoded_data)
response = opener.open(request)


def load_ff_sessions(session_filename):
    cj = cookielib.CookieJar()
    if os.path.exists(session_filename):
        json_data = json.loads(open(session_filename, 'rb').read())
        for window in json_data.get('windows', []):
            for cookie in window.get('cookies', []):
                c = cookielib.Coookie(0,
                    cookie.get('name', ''),
                    cookie.get('value', ''), None, False,
                    cookie.get('host'), '',
                    cookie.get('host', '').startswith('.'),
                    cookie.get('host', '').startswith('.'),
                    cookie.get('path', ''), False, False,
                    str(int(time.time()) + 3600 * 24 * 7),
                    False, None, None, {}
                    )
                cj.set_cookie(c)
        else:
            print "Session file name does not exist:", session_filename
        return cj


# 从浏览器加载cookie
session_filename = ''
cj = load_ff_sessions(session_filename)
processor = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(processor)
url = 'htttp://......'
html = opener.open(url).read()

# memchanize



