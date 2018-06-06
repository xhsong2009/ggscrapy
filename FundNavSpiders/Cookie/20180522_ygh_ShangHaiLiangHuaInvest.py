# -*- coding: utf-8 -*-


# Department : 保障部
# Author : 袁龚浩
# Create_date : 2018-05-22


from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re
import json


class ShangHaiLiangHuaInvestSpider(GGFundNavSpider):
    name = 'FundNav_ShangHaiLiangHuaInvest'
    sitename = '上海量化投资'
    channel = '投资顾问'
    allowed_domains = ['www.qfund.com']
    cookies = '__guid=46425889.3259545501557033500.1526895215504.0994; JSESSIONID=6A21E1488A7C01F48D0F9F7A582BA246; lianghua=%7B%22userName%22%20%3A%20%22139****7906%22%2C%20%22email%22%20%3A%20%22yuangh%40go-goal.com%22%2C%22aniuUid%22%20%3A%20%22svb3zkjjtmzmowvil3n2zlr4umdaqt09%22%2C%22userNickName%22%20%3A%20%22139****7906%22%7D; monitor_count=10'
    password = '13916427906'

    ips = [{
        'url': 'http://www.qfund.com/productionList.do'
    }]

    def parse_item(self, response):
        js_text = response.xpath('//script//text()').extract()[2].split(';')[0]
        funds_js = re.findall('\'{.*?}\'', js_text, re.DOTALL)[0].replace('\'{', '{').replace('}\'', '}')
        funds_name = response.xpath('//ul//li//a/span[1]//text()').extract()
        funds_code = response.xpath('//ul//li//a/span[2]//text()').extract()
        for fund_name, fund_code in zip(funds_name, funds_code):
            fs_list = json.loads(funds_js)[fund_code]['weekNetWorth']
            for f in fs_list:
                statistic_date = f['addTime']
                nav = f['netWorth']
                added_nav = f['totalWorth']
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['statistic_date'] = datetime.strptime(statistic_date,
                                                           '%Y-%m-%d')
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav'] = float(added_nav) if nav is not None else None
                yield item
