#!usr/bin/env python3
# _*_ coding:utf-8 _*_

import scrapy
from datetime import datetime

class ShiyanlourepositoritySpider(scrapy.Spider):
    name = 'shiyanlou_repositority'
    
    def start_requests(self):
        url_list = ['https://github.com/shiyanlou?tab=repositories',
                    'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wN1QwODowNjo1MyswODowMM4FkpKN&tab=repositories',
                    'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNS0wMS0zMVQyMDoyMDowMiswODowMM4BzHi1&tab=repositories',
                    'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0xMi0wNFQwMDoxNzo1MyswODowMM4BpCnu&tab=repositories',
                    'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0wOS0xNlQxMDowNjowMyswODowMM4Bb3Ud&tab=repositories']
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        '''
        for i in response.css('li.col-12'):
            yield {
                'name': i.css('h3 a::text').extract_first().strip(),
                'time': datetime.strptime(i.css('relative-time::attr(datetime)'
                        ).extract_first(), '%Y-%m-%dT%H:%M:%SZ')
            }
        '''
        for repositority in response.css('li.col-12'):
            yield{
                "name":repositority.css('h3 a::text').extract_first().strip(),
                "update_time":repositority.css('div.f6.text-gray.mt-2 relative-time::attr(datetime)').extract_first()
                    }
        
