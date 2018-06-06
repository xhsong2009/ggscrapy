# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
import re


class XinShengTrustSpider(GGFundNoticeSpider):
    name = 'FundNotice_XinShengTrust'
    sitename = '长城新盛信托'
    entry = 'http://www.gwxstrust.com/'

    ips = [
        {
            'url': 'http://www.gwxstrust.com/cn/page.jsp?id=23&pageIndex=1',
            'ref': 'http://www.gwxstrust.com/',
            'pg': 1
        }
    ]

    def parse_item(self, response):
        datas = response.xpath('//div[@class="lh-160p"]/div[@class="m-b-10"]')
        for notice in datas[1:]:
            href = notice.xpath('./div[1]/a/@href').extract_first()
            url = urljoin(get_base_url(response), href)
            title = notice.xpath('./div[1]/a/text()').extract_first()
            publish_time = notice.xpath('./div[2]/text()').extract_first()

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        next_url = response.xpath('//div[@class="pager"]/table/tr/td[3]/image/@onclick').re_first('\d+')
        if next_url is not None:
            self.ips.append({
                'url': 'http://www.gwxstrust.com/cn/page.jsp?id=23&pageIndex=' + next_url,
                'ref': response.url
            })


