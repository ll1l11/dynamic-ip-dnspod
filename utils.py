# -*- coding: utf-8 -*-
try:
    from urllib.parse import urlencode
    from urllib.request import urlopen, Request
except ImportError:
    from urllib import urlencode
    from urllib2 import urlopen, Request


def validate_ip(ip):
    ss = ip.split('.')
    if len(ss) != 4:
        return False
    for x in ss:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True


def request(url, data=None, headers={}):
    if data:
        data = urlencode(data).encode()
    req = Request(url, data, headers)
    return urlopen(req).read().decode()
