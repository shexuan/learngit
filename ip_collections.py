#!/usr/bin/env python3
# coding: utf-8

from lxml import etree
import requests
import sys
import io


def get_res(url):
    '''return html for xpath.'''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    res = requests.get(url, headers=headers)
    html = etree.HTML(res.content)
    return html


def parse_html(url):
    '''parse html and extract ip.'''
    html = get_res(url)
    ip = html.xpath('//tr[@class]/td[2]/text()')
    return ip


def write_down(url):
    '''write ips into file.'''
    ips = parse_html(url)
    with open('proxy.txt', 'wt') as f:
        for ip in ips:
            f.write(ip+'\n')


url = 'http://www.xicidaili.com/'
write_down(url)
