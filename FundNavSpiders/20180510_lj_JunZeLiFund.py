# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 李婧
# Create_date : 2018-05-10

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin


class JunZeLinFundSpider(GGFundNavSpider):
    name = 'FundNav_JunZeLinFund'
    sitename = '深圳君泽利投资发展企业'
    channel = '投资顾问'
    allowed_domains = ['www.jzlfund.com']

    fps = [{'url': 'http://www.jzlfund.com/Products.asp'}]

    def parse_fund(self, response):
        self.ips.append({'url': 'http://www.jzlfund.com/'})
        href_list = response.xpath('//div[@class="left_menu"]//@href').extract()
        fund_names = response.xpath('//div[@class="left_menu"]/a//text()').extract()
        for url, name in zip(href_list, fund_names):
            ips_url = urljoin('http://www.jzlfund.com/', url)
            fund_name = name
            self.ips.append({
                'url': ips_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        if 'ID' in response.url:
            rows = response.xpath('//div[@id="faq_content_1"]/div/table//tr')
            fund_name = response.meta['ext']['fund_name']
            for row in rows[1:]:
                fund_date = row.xpath('.//td[2]//text()').extract_first()
                fund_nav = row.xpath('.//td[3]//text()').extract_first()
                added_nav = row.xpath('.//td[4]//text()').extract_first()
                if '%' not in added_nav:
                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['fund_name'] = fund_name
                    item['statistic_date'] = datetime.strptime(fund_date, '%Y-%m-%d')
                    item['nav'] = float(fund_nav)
                    item['added_nav'] = float(added_nav)
                    yield item
        else:
            rows = response.xpath('//div[@class="iproducts_tbe"][@id="iproducts_0"]//tr')
            for row in rows[1:]:
                fund_name = row.xpath('./td[1]//text()').extract_first().strip()
                fund_nav = row.xpath('./td[2]//text()').extract_first().strip()
                fund_date = row.xpath('.//td[5]//text()').extract_first().strip()
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['statistic_date'] = datetime.strptime(fund_date, '%Y-%m-%d')
                item['nav'] = float(fund_nav)
                yield item
        yield self.request_next()
