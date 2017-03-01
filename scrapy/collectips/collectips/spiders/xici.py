# -*- coding: utf-8 -*-
import scrapy
from collectips.items import CollectipsItem
from scrapy.selector import Selector


class XiciSpider(scrapy.Spider):
    name = "xici"
    allowed_domains = ["http://www.xicidaili.com"]

    # headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #            'Accept-Encoding': 'gzip, deflate, sdch',
    #            'Accept-Language': 'zh-CN,zh;q=0.8',
    #            'Cache-Control': 'max-age=0',
    #            'Connection': 'keep-alive',
    #            'Host': 'www.xicidaili.com',
    #            'Referer': 'https://www.google.com/',
    #            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

    def start_requests(self):
        reqs = []
        for i in range(1, 21):
            req = scrapy.Request(
                'http://www.xicidaili.com/nn/{}'.format(i))
            reqs.append(req)

        return reqs

    def parse(self, response):
        item = CollectipsItem()
        sel = Selector(response)
        for i in range(2, 102):
            item['IP'] = sel.xpath(
                '//*[@id="ip_list"]/tr[{}]/td[2]/text()'.format(i)).extract_first()
            item['PORT'] = sel.xpath(
                '//*[@id="ip_list"]/tr[{}]/td[3]/text()'.format(i)).extract_first()
            item['DNS_POSITION'] = sel.xpath(
                '//*[@id="ip_list"]/tr[{}]/td[4]/a/text()'.format(i)).extract_first()
            item['TYPE'] = sel.xpath(
                '//*[@id="ip_list"]/tr[{}]/td[6]/text()'.format(i)).extract_first()
            item['SPEED'] = sel.xpath(
                '//*[@id="ip_list"]/tr[{}]/td[7]/div/@title'.format(i)).extract_first()
            item['LAST_CHECK_TIME'] = sel.xpath(
                '//*[@id="ip_list"]/tr[{}]/td[10]/text()'.format(i)).extract_first()
            yield item
