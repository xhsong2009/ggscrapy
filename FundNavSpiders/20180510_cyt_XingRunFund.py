# Department : 保障部
# Author : 陈雅婷
# Create_date : 2018-05-10

from urllib.parse import urljoin
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from datetime import datetime


class XingRunFundSpider(GGFundNavSpider):
    name = 'FundNav_XingRunFund'
    sitename = '深圳星润资产'
    channel = '投资顾问'
    allowed_domains = ['www.xingrunfund.com']
    start_urls = ['http://www.xingrunfund.com/product.asp']

    fps = [{'url': 'http://www.xingrunfund.com/product.asp'}]

    def parse_fund(self, response):
        link_key = response.xpath('//div[@class="proC"]//dd/a/@href').extract()
        for key in link_key:
            fund_link = urljoin('http://www.xingrunfund.com/', key)
            self.ips.append({
                'url': fund_link,
                'ref': response.url
            })

    def parse_item(self, response):
        fund_name = response.xpath('//div[@class="pro_title"]/h1/text()').extract_first()
        nav_rows = response.xpath('//div[@class="pj_table"]//tr')
        for row in nav_rows[1:]:
            nav_info = row.xpath('td/text()').extract()
            statistic_date = nav_info[0].replace('/', '-')
            nav = nav_info[1]

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name.replace('（已结束）', '').replace('（已成立）', '')
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            item['nav'] = float(nav) if nav is not None else None

            yield item
