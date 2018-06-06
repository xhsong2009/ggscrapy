# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class YiCunInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_YiCunInvest'
    sitename = '一村投资'
    entry = 'http://www.v-investment.com/news/public'

    lps = [
        {
            'url': 'http://www.v-investment.com/news/public'
        }
    ]

    def parse_list(self, response):
        rows = response.xpath('//div[@class="news-title"]/a')
        for row in rows:
            url = row.xpath('./@href').extract_first()
            self.ips.append({
                'url': urljoin(get_base_url(response), url),
                'ref': response.url
            })

    def parse_item(self, response):
        url = response.url
        title = response.xpath('//div[@class="news-title"]/text()').extract_first()
        publish_time = response.xpath('//span[@class="date"]/text()').re_first('\d+-\d+-\d+')

        item = GGFundNoticeItem()
        item['sitename'] = self.sitename
        item['channel'] = self.channel
        item['url_entry'] = self.entry
        item['title'] = title
        item['url'] = url
        item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
        yield item
