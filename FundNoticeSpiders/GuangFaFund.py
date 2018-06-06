# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
import re


class GuangfaFundSpider(GGFundNoticeSpider):
    name = 'FundNotice_GuangfaFund'
    sitename = '广发基金'
    entry = 'http://www.gffunds.com.cn'

    lps = [
        {
            'url': 'http://www.gffunds.com.cn/zhlc/147/xxgg/149/index.htm',
            'ref': 'http://www.gffunds.com.cn',
            'pg': 0
        }
    ]

    def parse_list(self, response):
        funds = response.xpath('//td[@class="TDbgcolor5"]/table/tbody/tr[4]/td/table/tbody/tr/td[2]/a')
        for fund in funds:
            url = fund.xpath('./@href').extract_first()
            title = fund.xpath('./text()').extract_first()
            publish_time = re.findall('[P0|t]+(\d{8})', url)[0]
            if 'pdf' not in url:
                self.ips.append({
                    'url': urljoin(get_base_url(response), url),
                    'ref': response.url,
                })
            else:
                item = GGFundNoticeItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url_entry'] = self.entry
                item['url'] = url
                item['title'] = title
                item['publish_time'] = datetime.strptime(publish_time, '%Y%m%d')
                yield item
        tp = response.css('script').re_first(r'[1-9]\d+')
        pg = response.meta['pg']
        next_pg = int(pg) + 1
        if next_pg < int(tp):
            next_url = urljoin(get_base_url(response), 'index_' + str(next_pg) + '.htm')
            self.lps.append({
                'url': next_url,
                'ref': response.url,
                'pg': next_pg,
            })

    def parse_item(self, response):
        if '.pdf' not in response.url:
            title = re.search('<h2>(.*?)</h2>', response.text).group(1)
            publish_time = re.search('\d+-\d+-\d+', response.text).group(0)
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = response.url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item




