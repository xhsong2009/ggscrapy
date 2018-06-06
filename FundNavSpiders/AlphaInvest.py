# Department : 保障部
# Author : 钱斌
# Create_date : 2018-05-08

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
import re


class AlphaInvestSpider(GGFundNavSpider):
    name = 'FundNav_AlphaInvest'
    sitename = '宁波阿尔法投资'
    channel = '投资顾问'

    fps = [{
        'url': 'http://www.nb-alpha.cn/a/jijinchanpin/jijinjingzhi/list_38_1.html',
        'pg': 1
    }]

    def parse_fund(self, response):
        if response.status != '404':
            href_list = response.css('div.news a::attr(href)').extract()
            for href in href_list:
                self.ips.append({
                    'url': urljoin(get_base_url(response), href),
                    'ref': response.url,
                })

            next_pg = response.meta['pg'] + 1
            self.fps.append({
                'url': re.sub('list_38_\d+', 'list_38_' + str(next_pg), response.url),
                'ref': response.url,
                'pg': next_pg
            })

    def parse_item(self, response):
        rows = response.css('div.content tr')[1:]
        fund_name = response.css('div.article_title h2::text').extract_first().replace('净值', '')
        if '嘉得新三板一号' not in fund_name:
            for r in rows:
                row = [_.strip() for _ in r.css('td ::text').extract() if _.strip()]

                date = row[0].strip().replace('.', '-')
                nav = row[1].strip()

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['fund_name'] = fund_name
                item['channel'] = self.channel
                item['url'] = response.url
                item['nav'] = float(nav) if nav else None
                item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d') if date else None
                yield item
