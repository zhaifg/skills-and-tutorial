#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-11-19 20:21:11
# @Author  : Zhaifg (zhaifengguo@foxmail.com)
# @Link    : http://htop.me
# @Version : $Id$

import os
from werkzeug.wrappers import Request, Response

import tornado.web
from werkzeug.debug import DebuggedApplication

@Request.application
def application(request):
    return Response('Hello World')


class Handler(tornado.web.RequestHandler):
    def initialize(self, debug):
        if debug:
            self.write_error = self.write_debugger_error

    def write_debugger_error(self, status_code, **kwargs):
        assert isinstance(self.application, DebuggedApplication)

        html = self.application.render_exception()
        self.write(html.encode('utf-8', 'replace'))

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 4000, application)
