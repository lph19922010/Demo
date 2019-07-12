#!usr/bin/env python3
# _*_ coding:utf-8 _*_

import scrapy

class ShiyanlourepositoritySpider(scrapy.Spider):
    name = 'shiyanlou_repositority'
    
    def start_requests(self):
        url = 'https://github.com/shiyanlou\?tab\=repositories'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for repositority in response.css('div#user-repositories-list'):
            yield {
                "name":repositority.css('h3 a::text').extract().strip(),
                "update_time":repositority.css('div.f6.text-gray.mt-2 relative-time::attr(datetime)').extract().strip()
                    }

