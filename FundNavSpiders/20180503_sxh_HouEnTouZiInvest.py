# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-02

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy import Request


class HouEnTouZiInvestSpider(GGFundNavSpider):
    name = 'FundNav_HouEnTouZiInvest'
    sitename = '厚恩投资'
    channel = '投资顾问'
    allowed_domains = ['www.hone2015.com']
    userName = '2650174701@qq.com'
    password = '123456'

    fps = [{'url': 'http://www.hone2015.com/index.php/Product_index_navid_2_all_1.html'}]

    def start_requests(self):
        yield Request(
            url='http://www.hone2015.com/index.php/Home/Members_ajaxLogin.html?userName=2650174701%40qq.com&password=123456&autoLogin=1',
            callback=self.parse_fund)

    def parse_fund(self, response):
        fund_urls = response.xpath("//div[@class='col-lg-12 col-md-12 col-sm-12']")
        for url in fund_urls:
            fund_url = url.xpath('.//@href').extract_first()
            fund_name = url.xpath(".//h4[@class='colo_main col-lg-10 col-md-10 col-sm-10']//text()").extract_first()
            self.ips.append({
                'url': 'http://www.hone2015.com' + fund_url.replace('.html', '_type_unit_p_1.html'),
                'ref': response.url,
                'ext': {'fund_name': fund_name},
                'pg': 1
            })


    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = response.xpath(
            "//div[@class='col-lg-12 col-md-12 col-sm-12']/table[@class='table table-striped']/tbody/tr")
        if '暂无信息' not in response.text:
            for row in rows:
                statistic_date = row.xpath("./td[1]//text()").extract_first().strip()
                nav = row.xpath("./td[2]//text()").extract_first().strip()
                added_nav = row.xpath("./td[3]//text()").extract_first().strip()
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav)
                item['added_nav'] = float(added_nav)
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item
            pg = response.meta['pg']
            next_pg = pg + 1
            next_url = response.url.replace('type_unit_p_' + str(pg), 'type_unit_p_' + str(next_pg))
            self.ips.append({
                'url': next_url,
                'ref': response.url,
                'pg': next_pg,
                'ext': {'fund_name': fund_name}
            })
        yield self.request_next()
