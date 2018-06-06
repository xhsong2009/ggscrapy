# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-23


from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class HuaChuangZhengQuanSecutiesSpider(GGFundNavSpider):
    name = 'FundNav_HuaChuangZhengQuanSecuties'
    sitename = '华创证券'
    channel = '券商资管净值'
    allowed_domains = ['www.hczq.com']
    urername = '13916427906'
    password = 'ZYYXSM123'

    fps = [{'url': 'http://www.hczq.com/hczq/getNavigation.do?type=2'}, ]

    def parse_fund(self, response):
        fund_urls = response.xpath("//a[contains(text(), '净值公布')]//@href").extract()
        for fund_url in fund_urls:
            self.ips.append({
                'url': 'http://www.hczq.com' + fund_url,
                'pg': 1,
                'ref': response.url,
            })
        yield self.request_next()

    def parse_item(self, response):
        rows = response.xpath("//div[@class='col_fr col_w838']//tr")
        if len(rows) > 1:
            for row in rows[1:]:
                fund_name = row.xpath('./td[2]//text()').extract_first().strip()
                statistic_date = row.xpath('./td[3]//text()').extract_first().strip()
                item = GGFundNavItem()
                if '万份收益' not in response.text:

                    nav = row.xpath('./td[4]//text()').extract_first()
                    add_nav = row.xpath('./td[5]//text()').extract_first()
                    if nav:
                        item['nav'] = float(nav.strip()) if nav else None
                        item['added_nav'] = float(add_nav.strip()) if add_nav else None
                else:
                    income_value_per_ten_thousand = row.xpath('./td[4]//text()').extract_first().strip()
                    d7_annualized_return = row.xpath('./td[5]//text()').extract_first().strip().replace('%', '')
                    item['d7_annualized_return'] = float(d7_annualized_return) if d7_annualized_return else None
                    item['income_value_per_ten_thousand'] = float(
                        income_value_per_ten_thousand) if income_value_per_ten_thousand else None
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item

            pg = response.meta['pg']
            next_pg = pg + 1
            next_url = response.url.replace('currentPage=' + str(pg), 'currentPage=' + str(next_pg))
            self.ips.append({
                'url': next_url,
                'ref': response.url,
                'pg': next_pg
            })
