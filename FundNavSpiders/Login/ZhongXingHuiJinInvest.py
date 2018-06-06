# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy import FormRequest
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class ZhongXingHuiJinInvestSpider(GGFundNavSpider):
    name = 'FundNav_ZhongXingHuiJinInvest'
    sitename = '中兴汇金投资'
    channel = '投顾净值'
    allowed_domains = ['www.sczxhj.com']

    fps = [
        {
            'url': 'http://www.sczxhj.com/zxhj-1/',
            'ref': 'http://www.sczxhj.com/',
            'ext': {'a': 0}
        }
    ]

    def start_requests(self):
        yield FormRequest(url='http://www.sczxhj.com/index.php?m=content&c=member&a=login',
                          formdata={'username': 'ZYYXSM', 'password': 'ZYYXSM'},
                          )

    def parse_fund(self, response):
        ext = response.meta['ext']
        a = ext['a']
        if a == 1:
            fund_name = response.meta['ext']['fund_name']
            fund_url = response.meta['ext']['fund_url']
            self.ips.append({
                'url': fund_url + '?page=1',
                'ref': response.url,
                'ext': {'fund_name': fund_name, 'fund_url': fund_url}
            })
        else:
            fund_urls = response.xpath('//ul[@class="btn"]/li /a')
            for fund in fund_urls:
                fund_name = fund.xpath('./text()').extract_first()
                url = fund.xpath("./@href").extract_first()
                if url:
                    fund_url = urljoin(get_base_url(response), url)
                    self.fps.append({
                        'url': fund_url,
                        'ref': response.url,
                        'ext': {'a': 1, 'fund_name': fund_name, 'fund_url': fund_url}
                    })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = response.xpath('//div[@class="Details"]/ul/li')
        for row in rows[1:]:
            nav = row.xpath("./div[4]/text()").extract_first()
            nav = "".join(nav.split())
            add_nav = row.xpath("./div[5]/text()").extract_first()
            add_nav = "".join(add_nav.split()).replace("..", ".")
            statistic_date = row.xpath("./div[3]/text()").extract_first()
            statistic_date = "".join(statistic_date.split())
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(add_nav) if add_nav is not None else None
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            yield item

        fund_url = response.meta['ext']['fund_url']
        next_url = response.xpath("//a[contains(@title, '下一页')]/@href").extract_first()
        next_url = fund_url + next_url
        if next_url is not None and next_url != response.url:
            self.ips.append({
                'url': next_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name, 'fund_url': fund_url}
            })
