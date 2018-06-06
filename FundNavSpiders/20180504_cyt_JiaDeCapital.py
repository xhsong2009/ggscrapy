# Department : 保障部
# Author : 陈雅婷
# Create_date : 2018-05-04

from urllib.parse import urljoin
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from datetime import datetime


class JiaDeCapitalSpider(GGFundNavSpider):
    name = 'FundNav_JiaDeCapital'
    sitename = '嘉得资产'
    channel = '投顾净值'

    fps = [{'url': 'http://www.zj-jd.cn/touzizheguanxi/jijinjingzhi'}]

    def parse_fund(self, response):
        link_key = response.xpath('//div[@class="news-zx"]/ul/li/a/@href').extract()
        for key in link_key:
            fund_link = urljoin('http://www.zj-jd.cn/', key)
            self.ips.append({
                'url': fund_link,
                'ref': response.url
            })

    def parse_item(self, response):
        fund_info = response.xpath('//div[@class="title"]/h1/text()').extract_first()
        nav_rows = response.xpath('//div[@class="content"]/table/tbody/tr')
        title = response.xpath('//div[@class="content"]//table/tbody/tr/td[2]/text()').extract_first()
        if '净值' in title:
            for row in nav_rows[1:]:
                nav_info = row.xpath('td/text()').extract()
                fund_name = fund_info.replace('净值', '')
                statistic_date = nav_info[0].replace('.', '-').strip()
                nav = nav_info[1]
                added_nav = nav_info[1]

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                if fund_name == '嘉得趋势策略二号基金':
                    item['nav'] = float(nav) if nav is not None else None
                else:
                    item['added_nav'] = float(added_nav) if added_nav is not None else None
                yield item
