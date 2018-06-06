# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class RuiYuFundSpider(GGFundNoticeSpider):
    name = 'FundNotice_RuiYuFund'
    sitename = '上海睿豫投资'
    entry = 'http://www.ruiyufund.com/news'

    ips = [
        {
            'url': 'http://www.ruiyufund.com/news'
        }
    ]

    def parse_item(self, response):
        rows = response.xpath('//div[@class="list"]/div/a')
        for row in rows:
            url = row.xpath('./@href').extract_first()
            url = urljoin(get_base_url(response), url)
            title = row.xpath('./span[@class="stxt"]/i/text()').extract_first()
            year = row.xpath('./span[@class="time"]/text()').re_first('\d+')
            publish_time = year + '-' + row.xpath('./span[@class="time"]/i/text()').re_first('\d+-\d+')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['title'] = title
            item['url'] = url
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        next_url = response.xpath('//div[@class="pagenum"]/a[contains(text(),">")]/@href').extract_first()
        if next_url:
            self.ips.append({
                'url': urljoin(get_base_url(response), next_url),
                'ref': response.url
            })
