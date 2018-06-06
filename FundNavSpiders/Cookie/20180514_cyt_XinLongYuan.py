# Department : 保障部
# Author : 陈雅婷
# Create_date : 2018-05-14

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin


class XinLongYuanSpider(GGFundNavSpider):
    name = 'FundNav_XinLongYuan'
    sitename = '深圳前海新隆源投资'
    channel = '投资顾问'
    allowed_domains = ['www.sinlongyoon.com']
    start_urls = ['http://www.sinlongyoon.com/prolist.asp']

    username = 'ZYYXSM'
    password = 'ZYYXSM123'
    cookies = 'ASPSESSIONIDCSBTADDB=LFCNCHIACDKHHFCCGPCBOJHP; Users=UserName=ZYYXSM&UserID=13; ASPSESSIONIDCSDQCDDA=ALNLHMJAIAPHCCJDEIKBNPCN; company=wzckeckd=agress'

    fps = [{'url': 'http://www.sinlongyoon.com/prolist.asp'}]

    def parse_fund(self, response):
        fund_list = response.xpath('//div[@class="cplist"]/ul/li/a/@href').extract()
        for key in fund_list:
            fund_url = urljoin('http://www.sinlongyoon.com/', key)
            self.ips.append({
                'url': fund_url,
                'ref': response.url
            })

    def parse_item(self, response):
        fund_info = response.xpath('//div[@class="cpdata"]/table[@class="zsbg"][2]//tr')
        for row in fund_info:
            row_info = row.xpath('td/text()').extract()
            fund_name = row_info[0].strip()
            statistic_date = row_info[1]
            nav_info = row_info[2]
            if nav_info[0: 1] == '.':
                nav = '0' + nav_info
            else:
                nav = nav_info

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d') if statistic_date else None
            item['nav'] = float(nav) if nav else None
            yield item
