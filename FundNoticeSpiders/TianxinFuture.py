# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class TianxinFutureSpider(GGFundNoticeSpider):
    name = 'FundNotice_TianxinFuture'
    sitename = '北京天鑫财富'
    entry = 'http://www.tianxinfortune.com/'

    ips = [{
        'url': 'http://www.tianxinfortune.com/info/1/',
    }]

    def parse_item(self, response):
        rows = response.xpath('//div[@class="newsbox-little"]/ul/li')
        for row in rows:
            url = row.xpath('./a/@href').extract_first()
            url = urljoin(get_base_url(response), url)

            title = row.xpath('./a/@title').extract_first().strip().replace('\t', '').replace('\r', '').replace('\n', '')

            publish_time = row.xpath('./span/text()').extract_first().strip().replace('\t', '').replace('\r', '').replace('\n', '')
            publish_time = '20'+str(publish_time)
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time

            yield item
