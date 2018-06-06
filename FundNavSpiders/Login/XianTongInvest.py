# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy import FormRequest
from scrapy.utils.response import get_base_url
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class XianTongInvestSpider(GGFundNavSpider):
    name = 'FundNav_XianTongInvest'
    sitename = '仙童投资'
    channel = '投资顾问'

    username = '15838569960'
    password = '19890226'

    fps = [
        {
            'url': 'http://www.fairchildfund.com/goods/info/viewinfo?goodsid=4&id=25'
        }
    ]

    def start_requests(self):
        yield FormRequest(url='http://www.fairchildfund.com/member/user/login',
                          formdata={
                              'account': self.username,
                              'password': self.password,
                              'returnurl': 'http://www.fairchildfund.com/'
                          },
                          meta={'handle_httpstatus_list': [302]})

    def parse_fund(self, response):
        rows = response.xpath('//ul[@id="cp"]/li/a[contains(@href,"viewinfo")]')
        for row in rows:
            url = row.xpath('./@href').extract_first()
            url = urljoin(get_base_url(response), url)
            goods_id = row.xpath('./@href').re_first('goodsid=([\d]+)')
            fund_id = row.xpath('./@href').re_first('&id=([\d]+)')
            self.ips.append({
                'url': url,
                'ref': response.url,
                'ext': {'goods_id': goods_id, 'fund_id': fund_id}
            })

    def parse_item(self, response):
        rows = response.xpath('//div[@class="product_mon clearfix mmm"]/div/table/tr')[1:]
        for row in rows:
            fund_name = row.xpath('./td[1]/text()').extract_first()
            statistic_date = row.xpath('./td[2]/text()').re_first('\d+-\d+-\d+')
            nav = row.xpath('./td[3]/text()').re_first('[0-9.]+')
            added_nav = row.xpath('./td[4]/text()').re_first('[0-9.]+')
            if nav:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav)
                item['added_nav'] = float(added_nav)
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item

        next_url = response.xpath('//div[@id="pages"]/a[last()]/@href').extract_first()
        if 'javascript' not in next_url:
            self.ips.append({
                'url': urljoin(get_base_url(response), next_url),
                'ref': response.url
            })
