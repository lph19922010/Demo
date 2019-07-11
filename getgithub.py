#!usr/bin/env python3
# _*_ coding:utf-8 _*_

import scapy

class shiyanlourepositoritySpider(scrapy.Spider):
    name = 'shiyanlou_repositority'
    
    @property
    def start_urls(self):
        url_list = ['https://github.com/shiyanlou?tab=repositories']
        return url_list

    def parse(self, response):
        for course  in response.css('div.user-repositories-list'):
            yield {
                "name":course.css('h3 a::text').extract().strip()
                "update_time":course.css('div.mt-2 relative-time::attr(datetime)').extract().strip()
                    }

