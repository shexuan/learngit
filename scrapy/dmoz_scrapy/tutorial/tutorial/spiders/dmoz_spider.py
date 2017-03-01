import scrapy
import scrapy.selector


class DmozSpider(scrapy.Spider):
    name = 'dmoz'
    allowed_domains = ['dmoz.org']
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    # def parse(self,response):
    #     filename=response.url.split('/')[-2]+'.html'
    #     with open(filename,'wb') as f:
    #         f.write(response.body)

    def parse(self, response):
        for sel in response.xpath('//ul/li'):
            item=DmozItem()
            item['title'] = sel.xpath('a/text()').extract()
            link['link'] = sel.xpath('a/@href').extract()
            desc['desc'] = sel.xpath('text()').extract()
            yield item
           
