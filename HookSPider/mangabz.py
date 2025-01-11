import scrapy


class MangabzSpider(scrapy.Spider):
    name = 'mangabz'
    allowed_domains = ['https://www.mangabz.com/']
    start_urls = ['http://https://www.mangabz.com//']

    def parse(self, response):
        pass
