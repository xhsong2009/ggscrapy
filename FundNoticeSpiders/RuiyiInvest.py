# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class RuiyiInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_RuiyiInvest'
    sitename = '睿亿投资'
    entry = 'http://www.ruiyiinvestment.com/'

    ips = [{
        'url': 'http://www.ruiyiinvestment.com/news/index/id/6',
    }]

    def parse_item(self, response):
        rows = response.xpath('//div[@class="right"]/div[@class="list"]')
        for row in rows:
            url = row.xpath('./div[1]/a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            title = row.xpath('./div[1]/a/text()').extract_first().strip().replace('\t', '').replace('\r', '').replace('\n', '')#标题
            publish_time = row.xpath('./div[2]/text()').extract_first().strip().replace('\t', '').replace('\r', '').replace('\n', '')#时间格式
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time
            yield item
