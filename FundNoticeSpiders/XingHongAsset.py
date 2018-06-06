# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
import re


class XingHongAssetSpider(GGFundNoticeSpider):
    name = 'FundNotice_XingHongAsset'
    sitename = '星鸿资产'
    entry = 'http://www.starluckwm.com/'

    ips = [{'url': 'http://www.starluckwm.com/?p=home_xhnews_list&type=board',
            'ref': 'http://www.starluckwm.com/'},
           {'url': 'http://www.starluckwm.com/?p=home_xhnews_list&type=disclosure',
            'ref': 'http://www.starluckwm.com/'}]

    def parse_item(self, response):
        next_url = response.xpath('//*[@id="main-content"]/div[2]//div[@class="page-nbm"]/a[text()="Next > "]/@href').extract_first()
        rows = response.xpath('//*[@id="main-content"]/div[2]/ul/li/h4')
        for row in rows:
            title = row.xpath('./a/text()').extract_first()
            url = row.xpath('./a/@href').extract_first()
            publish_time = row.xpath('./span/text()').extract_first()
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = urljoin(get_base_url(response), url)
            item['title'] = title
            item['publish_time'] = publish_time
            yield item
        if next_url:
            next_url = urljoin(get_base_url(response), next_url)
            self.ips.append({
                'url': next_url,
                'ref': response.url
            })
