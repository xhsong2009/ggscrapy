# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
import re


class DaYeTrustSpider(GGFundNoticeSpider):
    name = 'FundNotice_DaYeTrust'
    sitename = '大业信托'
    entry = 'http://www.dytrustee.com/'

    lps = [
        {
            'url': 'http://www.dytrustee.com/Information.aspx',
            'ref': 'http://www.dytrustee.com/',
            'ext': {'flag': 0}
        }
    ]

    def parse_list(self, response):
        if response.meta['ext']['flag'] == 1:
            pg = response.meta['pg']
            self.ips.append({
                'url': response.url + '&page=' + str(pg),
                'ref': response.url
            })
        else:
            urls = response.xpath("//ul[@class='fix']/li/a")
            for url in urls[2:]:
                href = url.xpath('./@href').extract_first()
                type = url.xpath('./text()').extract_first()
                self.lps.append({
                    'url': urljoin(get_base_url(response), href),
                    'ref': response.url,
                    'pg': 1,
                    'ext': {'flag': 1, 'type': type}
                })

    def parse_item(self, response):
        datas = response.xpath("//div[@class='news_list fix']/ul/li")
        for notice in datas:
            href = notice.xpath('./a/@href').extract_first()
            url = urljoin(get_base_url(response), href)
            title = notice.xpath('./a/text()').extract_first()
            publish_time = notice.xpath('./small/text()').extract_first()

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        next_url = response.xpath('//div[@id="AspNetPager1"]/div[1]/a[contains(text(),"下一页")]/@href').extract_first()
        if next_url is not None:
            self.ips.append({
                'url': urljoin(get_base_url(response), next_url),
                'ref': response.url
            })


