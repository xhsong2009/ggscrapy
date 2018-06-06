# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class ShangHaiYuanKuiAssetSpider(GGFundNoticeSpider):
    name = 'FundNotice_ShangHaiYuanKuiAsset'
    sitename = '上海元葵资产'
    entry = 'http://www.ucanfund.cn/'

    ips = [{
        'url': 'http://www.ucanfund.cn/index.php?m=content&c=index&a=lists&catid=16',
    }]

    def parse_item(self, response):
        rows = response.xpath('//li[@class="clearfix"]/a')
        for row in rows:
            url = row.xpath('./@href').extract_first()
            url = urljoin(get_base_url(response), url)

            title = row.xpath('./div/div[1]/text()').extract_first()

            publish_time = row.xpath('./div/span/text()').extract_first()
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time
            yield item
























