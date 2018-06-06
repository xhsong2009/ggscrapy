# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class DaBoDiInvestNoticeSpider(GGFundNoticeSpider):
    name = 'FundNotice_DaBoDiInvestNotice'
    sitename = '大柏地投资'
    entry = 'http://www.bgclfund.com'

    ips = [{
        'url': 'http://www.bgclfund.com/index.php?c=article&a=type&tid=10&page=1',
    }]

    def parse_item(self, response):
        rows = response.xpath('//ul[@class="hd newslist"]/li')
        for row in rows:
            url = row.xpath('./a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            title = row.xpath('./a/text()').extract_first()
            publish_time = row.xpath('./a/span/text()').re_first(r'(\d+-\d+-\d+)')
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time
            yield item
