# Department : 保障部
# Author : 钱斌
# Create_date : 2018-05-18

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class TianQiInvestmentSpider(GGFundNavSpider):
    name = 'FundNav_TianQiInvestment'
    sitename = '天琪投资'
    channel = '投资顾问'

    cookies = 'judge=tq_cookie'
    fps = [{'url': 'http://www.tqtz.com.cn/qixiazijin/qixiajijin/'}]

    def parse_fund(self, response):
        href_list = response.css('div.qxjj_con_1 a::attr(href)').extract()
        fname_list = response.css('div.qxjj_con_1 p.qxjj_title::text').extract()
        for href, fname in zip(href_list, fname_list):
            self.ips.append({
                'url': 'http://www.tqtz.com.cn' + href,
                'ref': response.url,
                'ext': fname
            })

    def parse_item(self, response):
        nav_list = re.findall("asd='(.*)';.*zxc=", response.text, re.DOTALL)[0].split('|')
        date_list = re.findall("zxc='(.*)';.*cpqy=", response.text, re.DOTALL)[0].split('|')

        for dt, nav in zip(date_list, nav_list):
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['fund_name'] = response.meta['ext']
            item['channel'] = self.channel
            item['url'] = response.url
            item['nav'] = float(nav) if nav else None
            item['statistic_date'] = datetime.strptime(dt, '%Y/%m/%d') if dt else None
            yield item
