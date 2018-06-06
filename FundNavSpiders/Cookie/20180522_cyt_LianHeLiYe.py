# Department : 保障部
# Author : 陈雅婷
# Create_date : 2018-05-22

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class LianHeLiYeSpider(GGFundNavSpider):
    name = 'FundNav_LianHeLiYe'
    sitename = '深圳前海联合利业投资'
    channel = '投顾净值'
    allowed_domains = ['www.qhlhly.com']
    start_urls = ['http://www.qhlhly.com/product.aspx?key=1']

    username = '350402197902120017'
    password = 'ZYYXSM123'
    cookies = 'Hm_lvt_32deacaddae51078587f3f5c35c88f1d=1527065297; ASP.NET_SessionId=oauzy12nr3c3rxxmo0mn4lcn; Hm_lpvt_32deacaddae51078587f3f5c35c88f1d=1527065841'

    ips = [{'url': 'http://www.qhlhly.com/product.aspx?key=1'}]

    def parse_item(self, response):
        name_info = response.xpath('//div[@class="wapper clearfix overhide"]/dl[@class="subleft"]/dd/a/text()').extract()
        nav_area = response.xpath('//div[@id="page01s01"]/div[contains(@class,"box_b")]/div')
        for name, nav_detail in zip(name_info, nav_area):
            fund_name = name
            nav_info = nav_detail.xpath('div[contains(@id,"area")]')
            for n in nav_info:
                nav_rows = n.xpath('table/tbody/tr')
                for row in nav_rows[1:]:
                    nav_info_detail = row.xpath('td/text()').extract()
                    statistic_date = nav_info_detail[1]
                    nav = nav_info_detail[2]

                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['fund_name'] = fund_name
                    item['statistic_date'] = datetime.strptime(statistic_date, '%Y/%m/%d') if statistic_date else None
                    item['nav'] = float(nav) if nav else None
                    yield item
