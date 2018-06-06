# -*- coding: utf-8 -*-


# Department : 保障部
# Author : 袁龚浩
# Create_date : 2018-05-17


from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class ShangHaiTuoQuanInvestSpider(GGFundNavSpider):
    name = 'FundNav_ShangHaiTuoQuanInvest'
    sitename = '上海拓权投资'
    channel = '投资顾问'
    allowed_domains = ['www.cn-fof.com']

    ips = [{
        'url': 'http://www.cn-fof.com/index.php?g=portal&m=NetDisclosure&a=index'
    }]

    def parse_item(self, response):
        f_list = response.xpath('//table//tr')
        for i in f_list:
            if i.xpath('td//text()'):
                t = i.xpath('td//text()').extract()
                fund_name = t[1]
                statistic_date = t[0]
                nav = re.findall('\d+.\d+', t[2])[0]
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['statistic_date'] = datetime.strptime(statistic_date,'%Y-%m-%d')
                item['nav'] = float(nav) if nav is not None else None
                yield item
