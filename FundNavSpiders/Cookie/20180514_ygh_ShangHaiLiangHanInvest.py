# -*- coding: utf-8 -*-

# Department : 保障部
# Author : 袁龚浩
# Create_date : 2018-05-14


from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class ShangHaiLiangHanInvestSpider(GGFundNavSpider):
    name = 'FundNav_ShangHaiLiangHanInvest'
    sitename = '上海量函投资'
    channel = '投资顾问'
    allowed_domains = ['www.quantfn.com']
    username = '13916427906'
    password = 'ZYYXSM123'
    cookies = '__guid=261440907.29537647574523732.1526266146264.8103; PHPSESSID=lpba7s83ql092em2mh1s3vbio5; DedeUserID=64; DedeUserID__ckMd5=efba1073e76861b3; DedeLoginTime=1526266247; DedeLoginTime__ckMd5=9ee68a34d0e0b1b6; cookie=tongyi; monitor_count=16'

    fps = [{
        'url': 'http://www.quantfn.com/plus/list.php?tid=7'
    }]

    def parse_fund(self, response):
        funds = response.xpath('//table//td[@rowspan]//a[@class ="yuyue"]//@href').extract()
        fund_names = response.xpath('//table//td[@rowspan and @class = "pro_name"]//text()').extract()
        for fund_name, f_url in zip(fund_names, funds):
            self.ips.append({
                'url': 'http://www.quantfn.com/' + f_url,
                'ref': response.url,
                'ext': fund_name
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']
        fund = response.xpath('//div[@id ="c1"]//tbody//tr')
        for i in fund[1:]:
            t = i.xpath('td//text()').extract()
            statistic_date = ''.join(t[0].split())
            nav = ''.join(t[1].split())
            added_nav = ''.join(t[2].split())
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
