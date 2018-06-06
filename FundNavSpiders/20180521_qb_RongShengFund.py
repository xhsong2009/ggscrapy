# Department : 保障部
# Author : 钱斌
# Create_date : 2018-05-21

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class RongShengFundSpider(GGFundNavSpider):
    name = 'FundNav_RongShengFund'
    sitename = '融升基金'
    channel = '投资顾问'

    # 页面无法正常访问，取TRS历史链接
    ips = [{'url': 'http://www.rongshengjijin.com/teamview_1433024.html?name=融升凤舞私募投资基金',
            'ext': '融升凤舞私募投资基金'},
           {'url': 'http://www.rongshengjijin.com/teamview_1778216.html?name=融升多策略私募投资基金',
            'ext': '融升多策略私募投资基金'},
           {'url': 'http://www.rongshengjijin.com/teamview_473621.html?name=融升稳健投资基金',
            'ext': '融升稳健投资基金'},
           {'url': 'http://www.rongshengjijin.com/teamview_713077.html?name=申万汇富威海融升一号集合资产管理计划',
            'ext': '申万汇富威海融升一号集合资产管理计划'}]

    def parse_item(self, response):
        fund_name = response.meta['ext']
        rows = response.xpath('//table[last()]//tr')
        for r in rows[1:]:
            dt = r.xpath('td[1]/text()').re_first('\S+')
            nav = r.xpath('td[2]/text()').re_first('\S+')
            added_nav = r.xpath('td[3]/text()').re_first('\S+')

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['fund_name'] = fund_name
            item['channel'] = self.channel
            item['url'] = response.url
            item['nav'] = float(nav) if nav else None
            item['added_nav'] = float(added_nav) if added_nav else None
            item['statistic_date'] = datetime.strptime(dt, '%Y年%m月%d日') if dt else None
            yield item
