# -*- coding: utf-8 -*-


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
