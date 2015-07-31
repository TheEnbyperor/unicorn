#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
    pass
#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#

import wikipedia
import re
from cgi import parse_qs, escape

def fact():
    pageTitle = wikipedia.random();
    page = wikipedia.summary(pageTitle, sentences=1);
    if ("is" in page or "was" in page) and page[0] != '<':
        page = re.sub("[\(\[].*?[\)\]]", "", page)
        return page
    else:
        return fact()

def application(environ, start_response):

    if (environ['PATH_INFO'] == "/donate"):
        ctype = 'text/html; charset=utf-8'
        d = parse_qs(environ['QUERY_STRING'])
        amount = str(escape(d.get("amount", [''])[0]))
        response_body = """<html><body><form action="https://www.paypal.com/cgi-bin/webscr" method="post" id="form">
<input type="hidden" name="cmd" value="_xclick">
<input type="hidden" name="business" value="beninjam174@gmail.com">
<input type="hidden" name="lc" value="GB">
<input type="hidden" name="item_name" value="Unicorn">
<input type="hidden" name="amount" value='""" + amount + """.00'>
<input type="hidden" name="currency_code" value="GBP">
<input type="hidden" name="button_subtype" value="services">
<input type="hidden" name="no_note" value="1">
<input type="hidden" name="no_shipping" value="1">
<input type="hidden" name="bn" value="PP-BuyNowBF:btn_buynow_LG.gif:NonHosted">
<img alt="" border="0" src="https://www.paypalobjects.com/en_GB/i/scr/pixel.gif" width="1" height="1">
</form><script>document.getElementById("form").submit()</script></body></html>"""
    else:
        ctype = 'text/plain; charset=utf-8'
        response_body = fact().encode('utf-8')
    status = '200 OK'
    response_headers = [('Content-Type', ctype), ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)
    return response_body

#
# Below for testing only
#
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8051, application)
    # Wait for a single request, serve it and quit.
    httpd.handle_request()
