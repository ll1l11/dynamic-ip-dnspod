# -*- coding: utf-8 -*-
import logging
from datetime import datetime
import requests

import config
from dnspod_api import DNSPodClient

logging.basicConfig(filename='ip.log', level=logging.DEBUG)
logging.debug('this is debug info %s', datetime.now())

def read_config():
    conf = {}
    for key in dir(config):
        if key.isupper():
            conf[key] = getattr(config, key)
    return conf


def get_httpdns_ip(domain):
    url = 'http://119.29.29.29/d'
    params = {'dn': domain}
    r = requests.get(url, params=params)
    body = r.text
    if body:
        ip = body.split(';')[0]
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
    return  record['id'], record['value']


def get_new_ip():
    """获取要设置的IP"""
    with open('ip.txt') as f:
        return f.read()


def is_same(domain, ip):
    """判断domain对应的ip是否和ip相同"""
    httpdns_ip = get_httpdns_ip(domain)
    return httpdns_ip == ip


def set_ip():
    conf = read_config()
    client = DNSPodClient(
        conf['TOKEN'],
        conf['USER_AGENT'],
        conf['DOMAIN'],
        conf['SUB_DOMAIN']
    )
    domain = '{0}.{1}'.format(client.sub_domain, client.domain)
    new_ip = get_new_ip()
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
    if record_ip != new_ip:
        # 情况2: 域名IP和ip.txt内容不一样, 则修改
        logging.info('record_ip: %s new_ip: %s, modify', record_ip, new_ip)
        result = client.record_modify(record_id, new_ip)
        logging.info('record modify: %s', result)
    else:
        logging.info('new_ip and record_ip is same: %s', record_ip)


if __name__ == '__main__':
    set_ip()
