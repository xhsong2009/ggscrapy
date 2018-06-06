# -*- coding: utf-8 -*-
from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url


class ZiJinTrustSpider(GGFundNavSpider):
    name = 'FundNav_ZiJinTrust'
    sitename = '紫金信托'
    channel = '发行机构'

    fps = [{
        'url': 'https://www.zjtrust.com.cn/cn/page/41.html',
        'ref': 'https://www.zjtrust.com.cn/cn/index.html'
    }]

    def parse_fund(self, response):
        urls = response.xpath('//table[@class="t1"]/tr/td[4]/a/@href').extract()
        for url in urls:
            self.ips.append({
                'url': urljoin(get_base_url(response), url),
                'ref': response.url
            })
        yield self.request_next()

    def parse_item(self, response):
        rows = response.xpath('//table[@class="t1"]/tr')
        for row in rows[1:]:
            fund_name = row.xpath('./td[1]/text()').extract_first()
            if fund_name is None:
                continue
            statistic_date = row.xpath('normalize-space(./td[3]/text())').extract_first()
            nav = row.xpath('normalize-space(./td[2]/text())').extract_first()
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            item['nav'] = float(nav) if nav is not None else None

            yield item

