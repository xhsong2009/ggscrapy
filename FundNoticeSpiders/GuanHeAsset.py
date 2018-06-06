# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class GuanHeAssetSpider(GGFundNoticeSpider):
    name = 'FundNotice_GuanHeAsset'
    sitename = '浙江观合资产'
    entry = 'http://www.guanheasset.com/website/w/h?mt=2&mc=2799282&cc=2776206'

    lps = [
        {
            'url': 'http://www.guanheasset.com/website/w/h?mt=2&mc=2799282&cc=2776206'
        }
    ]

    def parse_list(self, response):
        rows = response.xpath('//div[@class="simu-site-subnav"]')[1].xpath('./ul/li/a')
        for row in rows:
            url = row.xpath('./@href').extract_first()
            self.ips.append({
                'url': urljoin(get_base_url(response), url),
                'ref': response.url
            })

    def parse_item(self, response):
        rows = response.xpath('//div[@class="simu-site-list"]/ul/a')
        for row in rows:
            url = row.xpath('./@href').extract_first()
            url = urljoin(get_base_url(response), url)
            title = row.xpath('./li/div[1]/text()').extract_first().strip()
            publish_time = row.xpath('./li/div[2]/text()').re_first('\d+-\d+-\d+')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item
