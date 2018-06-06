# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin


class HaoenInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_HaoenInvest'
    sitename = '昊恩投资'
    entry = 'http://www.hetz.com.cn'

    ips = [
        {
            'url': 'http://www.hetz.com.cn/news.asp',
            'ref': 'http://www.hetz.com.cn/index.asp',
            'pg': 0
        }
    ]

    def parse_item(self, response):
        datas = response.xpath('//td[@align="left"]/table[1]/tr')
        for notice in datas:
            href = notice.xpath('./td[2]/a/@href').extract_first()
            url = urljoin(get_base_url(response), href)
            title = notice.xpath('./td[2]/a/text()').extract_first()
            publish_time = notice.xpath('./td[3]/text()').extract_first()

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        next_url = response.xpath('//td[@align="left"]/table[2]/tr/td/a[contains(text(), "下一页")]/@href').extract_first()
        if next_url is not None and next_url != '':
            url = response.url + next_url
            self.ips.append({'url': url, 'ref': response.url})


