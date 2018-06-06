# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-18

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy import FormRequest
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin


class PuShiTouZiInvestSpider(GGFundNavSpider):
    name = 'FundNav_PuShiTouZiInvest'
    sitename = '朴石投资'
    channel = '投资顾问'
    allowed_domains = ['www.postone.com.cn']

    username = '403073939@qq.com'
    password = '123456'
    fps = [{'url': 'http://www.postone.com.cn/info.asp?base_id=2'}]

    def start_requests(self):
        yield FormRequest(url='http://www.postone.com.cn/user_login.asp',
                          formdata={'name': '403073939@qq.com', 'pass': '123456'},
                          callback=self.parse_fund)

    def parse_fund(self, response):
        fund_urls = response.xpath("//div[@class='menu']/dl/dt//@href").extract()
        for fund_url in fund_urls:
            self.ips.append({
                'url': 'http://www.postone.com.cn/' + fund_url + '&page=1',
                'ref': response.url,
                'pg': 1
            })

    def parse_item(self, response):
        rows = response.xpath("//div[@class='list2']/ul//li")
        if len(rows) > 1:
            for row in rows[1:]:
                fund_name = row.xpath(".//span[@class='title']//text()").extract_first()
                statistic_date = row.xpath(".//span[@class='title4']//text()").extract_first()
                nav = row.xpath("./span[@class='title3'][2]//text()").extract_first()
                added_nav = row.xpath("./span[@class='title2']//text()").extract_first()
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav)
                item['added_nav'] = float(added_nav)
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item

        next_url = response.xpath('//a[text()="下一页"]/@href').extract_first()
        if next_url and next_url != 'javascript:void(0);':
            # pg = response.meta['pg']
            # next_pg = pg + 1
            # self.ips.append({
            #     'url': response.url.replace('page=' + str(pg), 'page=' + str(next_pg)),
            #     'ref': response.url,
            #     'pg': next_pg,
            # })
            self.ips.append({
                'url': urljoin(get_base_url(response), next_url),
                'ref': response.url
            })
