# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class DingLiInvestNoticeSpider(GGFundNoticeSpider):
    name = 'FundNotice_DingLiInvestNotice'
    sitename = '鼎力投资'
    entry = 'http://www.one-up-china.com/'

    ips = [{
        'url': 'http://www.one-up-china.com/index.html',
    }]

    def parse_item(self, response):
        rows = response.xpath('//div[@class="sy_news_cen"]')
        for row in rows:
            url = row.xpath('./a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            title = row.xpath('./a/text()').extract_first()
            publish_time = row.xpath('./text()').re_first(r'(\d+-\d+-\d+)')
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time
            yield item
