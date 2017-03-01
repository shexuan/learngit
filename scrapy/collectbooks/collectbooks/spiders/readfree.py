# -*- coding: utf-8 -*-
import scrapy
from collectbooks.items import CollectbooksItem
from scrapy.selector import Selector


class ReadfreeSpider(scrapy.Spider):
    name = "readfree"
    allowed_domains = ["http://readfree.me"]

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        # Cookie:csrftoken=LK77JvW3TPBrr2olsWZkfJWaOPhB2TxgZFCUHXWEBNOtFsONWkSrQmLvdmtBw23g;
        # Hm_lvt_375aa6d601368176e50751c1c6bf0e82=1487928032;
        # Hm_lpvt_375aa6d601368176e50751c1c6bf0e82=1488290001;
        # bd_st=%28%7B%22s%22%3A1488290227723%2C%22r%22%3A%22http%3A//readfree.me/psyche/%3Fpage%3D358%22%7D%29
        'Host': 'readfree.me',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://readfree.me/psyche/?page=358',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }

    def start_requests(self):
        reqs = []
        for i in range(1, 359):
            req = scrapy.Request(
                'http://readfree.me/psyche/?page={}'.format(i), headers=self.headers)
            reqs.append(req)
        return reqs

    def parse(self, response):
        item = CollectbooksItem()
        sel = Selector(response)
        for i in range(1, 21):
            item['TITLE'] = sel.xpath(
                '//*[@id="container"]/ul/li[{}]/div/div[2]/a/text()'.format(i)).extract_first().strip()
            item['AUTHOR'] = sel.xpath(
                '//*[@id="container"]/ul/li[{}]/div/div[2]/div/a/text()'.format(i)).extract_first().strip()
            item['SCORE'] = sel.xpath(
                '//*[@id="container"]/ul/li[1]/div/div[3]/span/span/text()'.format(i)).extract_first().strip()
            yield item
