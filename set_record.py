# -*- coding: utf-8 -*-
import logging
import re
from datetime import datetime


import config
from utils import validate_ip, request, urlencode
from dnspod_api import DNSPodClient

logging.basicConfig(filename='push-ip.log', level=logging.DEBUG)
logging.info('\n\n ******* push ip exec start at: %s *******', datetime.now())


def read_config():
    conf = {}
    for key in dir(config):
        if key.isupper():
            conf[key] = getattr(config, key)
    return conf


def get_httpdns_ip(domain):
    params = {'dn': domain}
    url = 'http://119.29.29.29/d?{}'.format(urlencode(params))
    body = request(url)
    if body:
        ip = str(body).split(';')[0]
        logging.info("%s 's ip is: %s by HTTP DNS", domain, ip)
        return ip


def get_record(client):
    """获取现在domain对应record的(id, ip)"""
    data = client.record_list()
    if data.get('status', {}).get('code') != '1':
        logging.error(data)
        return
    records = data.get('records')
    if not records:
        return
    record = records[0]
    return record['id'], record['value']


def get_new_ip():
    """获取要设置的IP"""
    with open('ip.txt') as f:
        for line in f:
            return line.strip()


def is_same(domain, ip):
    """判断domain对应的ip是否和ip相同"""
    httpdns_ip = get_httpdns_ip(domain)
    return httpdns_ip == ip


def check_token_format(token):
    m = re.match('\d+,\w+$', token)
    return m is not None


def set_ip():
    conf = read_config()
    assert check_token_format(conf['TOKEN'])
    client = DNSPodClient(
        conf['TOKEN'],
        conf['USER_AGENT'],
        conf['DOMAIN'],
        conf['SUB_DOMAIN']
    )
    domain = '{0}.{1}'.format(client.sub_domain, client.domain)
    new_ip = get_new_ip()
    logging.info('new_ip: %s', new_ip)

    if not validate_ip(new_ip):
        logging.error('new_ip: %s format error', new_ip)
        assert False

    if is_same(domain, new_ip):
        logging.info('IP和原来IP相同 %s %s', domain, new_ip)
        return

    record = get_record(client)
    if not record:
        # 情况1: sub_domain不存在, 则创建
        logging.info('no record, create: %s', new_ip)
        result = client.record_create(new_ip)
        logging.info('record create: %s', result)
        return

    record_id, record_ip = record
    logging.info('record_id: %s, record_ip: %s', record_id, record_ip)
    if record_ip != new_ip:
        # 情况2: 域名IP和ip.txt内容不一样, 则修改
        logging.info('record_ip: %s new_ip: %s, modify', record_ip, new_ip)
        result = client.record_modify(record_id, new_ip)
        logging.info('record modify: %s', result)
    else:
        logging.info('new_ip and record_ip is same: %s', record_ip)


if __name__ == '__main__':
    set_ip()
