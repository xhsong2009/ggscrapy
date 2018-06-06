# -*- coding: utf-8 -*-


# Department : 保障部
# Author : 袁龚浩
# Create_date : 2018-05-17


from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class ShangHaiTaiRongAssetSpider(GGFundNavSpider):
    name = 'FundNav_ShangHaiTaiRongAsset'
    sitename = '上海泰荣资产'
    channel = '投资顾问'
    allowed_domains = ['www.tairong-asset.com']

    fps = [{
        'url': 'http://www.tairong-asset.com/html/products/'
    }]

    def parse_fund(self, response):
        funds = response.xpath('//div[@class ="cncontent"]//li//@href').extract()
        fund_names = response.xpath('//div[@class ="cncontent"]//li//span//text()').extract()
        for fund_name, f_url in zip(fund_names, funds):
            self.ips.append({
                'url': f_url,
                'ref': response.url,
                'ext': fund_name
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']
        f_list = response.xpath('//div[@id ="content_jz"]//table//tr')
        for i in f_list[1:]:
            t = i.xpath('td//text()').extract()
            # 判断此行含有数据
            if '-' in ''.join(t):
                statistic_date = t[1]
                nav = t[2]
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['statistic_date'] = datetime.strptime(statistic_date,'%Y-%m-%d')
                item['nav'] = float(nav) if nav is not None else None
                yield item
