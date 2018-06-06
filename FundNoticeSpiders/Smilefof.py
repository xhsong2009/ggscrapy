# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class SmilefofSpider(GGFundNoticeSpider):
    name = 'FundNotice_Smilefof'
    sitename = '上海拾麦资产'
    entry = 'http://www.smilefof.com'

    lps = [
        {
            'url': 'http://www.smilefof.com/news/cpgg/',
            'ref': 'http://www.smilefof.com/news/'
        }
    ]

    def parse_list(self, response):
        datas = response.xpath('/html/body/div//ul[@class="article"]/li')
        for notice in datas:
            href = notice.xpath('./span[1]/a/@href').extract_first().strip()
            title = notice.xpath('./span[1]/a/text()').extract_first().strip()
            publish_time = notice.xpath('./span[2]/text()').extract_first()

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = self.entry + href
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

