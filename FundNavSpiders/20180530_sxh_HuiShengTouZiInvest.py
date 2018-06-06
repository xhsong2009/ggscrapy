# -*- coding: utf-8 -*-
# Department：保障部
# Author：宋孝虎
# Create_Date：2018-05-30

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class HuiShengTouZiInvestSpider(GGFundNavSpider):
    name = 'FundNav_HuiShengTouZiInvest'
    sitename = '汇升投资'
    channel = '投顾净值'
    allowed_domains = ['www.hhhstz.com']

    def start_requests(self):
        urls = ['http://www.hhhstz.com/Home/Index/productDetail/action_name/product/id/5.html&name=汇升睿进二号',
                'http://www.hhhstz.com/Home/Index/productDetail/action_name/product/id/7.html&name=大朴汇升定增一号',
                'http://www.hhhstz.com/Home/Index/productDetail/action_name/product/id/17.html&name=汇升融创一号',
                'http://www.hhhstz.com/Home/Index/productDetail/action_name/product/id/15.html&name=大朴汇升定增二号',
                'http://www.hhhstz.com/Home/Index/productDetail/action_name/product/id/28.html&name=汇升稳进多策略四号',
                'http://www.hhhstz.com/Home/Index/productDetail/action_name/product/id/1.html&name=睿进一号',
                'http://www.hhhstz.com/Home/Index/productDetail/action_name/product/id/24.html&name=稳进七号',
                'http://www.hhhstz.com/Home/Index/productDetail/action_name/product/id/10.html&name=汇升多策略',
                'http://www.hhhstz.com/Home/Index/productDetail/action_name/product/id/25.html&name=创盈一号',
                'http://www.hhhstz.com/Home/Index/productDetail/action_name/product/id/3.html&name=富安达汇升稳进一号',
                'http://www.hhhstz.com/Home/Index/productDetail/action_name/product/id/16.html&name=汇升稳进二号',
                'http://www.hhhstz.com/Home/Index/productDetail/action_name/product/id/21.html&name=稳进五号',
                'http://www.hhhstz.com/Home/Index/productDetail/action_name/product/id/30.html&name=汇升稳进多策略三号',
                'http://www.hhhstz.com/Home/Index/productDetail/action_name/product/id/6.html&name=千石华宝汇升优选一号',
                'http://www.hhhstz.com/Home/Index/productDetail/action_name/product/id/20.html&name=大有期货-华量汇鸿汇升一号资产管理计划',
                'http://www.hhhstz.com/Home/Index/productDetail/action_name/product/id/22.html&name=汇升共盈尊享',
                'http://www.hhhstz.com/Home/Index/productDetail/action_name/product/id/29.html&name=汇升智选二号',
                'http://www.hhhstz.com/Home/Index/productDetail/action_name/product/id/2.html&name=汇升稳进一号',
                'http://www.hhhstz.com/Home/Index/productDetail/action_name/product/id/23.html&name=汇升多策略二号',
                'http://www.hhhstz.com/Home/Index/productDetail/action_name/product/id/8.html&name=平安信托金蕴九期',
                'http://www.hhhstz.com/Home/Index/productDetail/action_name/product/id/11.html&name=汇升稳进价值增长',
                'http://www.hhhstz.com/Home/Index/productDetail/action_name/product/id/18.html&name=汇升融创二号',
                'http://www.hhhstz.com/Home/Index/productDetail/action_name/product/id/19.html&name=汇升稳进三号',
                'http://www.hhhstz.com/Home/Index/productDetail/action_name/product/id/26.html&name=汇升稳进融享',
                'http://www.hhhstz.com/Home/Index/productDetail/action_name/product/id/4.html&name=广发汇盛MOM2号',
                'http://www.hhhstz.com/Home/Index/productDetail/action_name/product/id/9.html&name=汇升智选一号']
        for url in urls:
            self.ips.append({
                'url': url,
                'ref': 'http://www.hhhstz.com',
            })
            yield self.request_next()

    def parse_item(self, response):
        fund_name = response.xpath('//h2//text()').extract_first()
        navs = re.findall('var data1= \[(.*?)\];', response.text)[0].replace('"', '').split(',')
        added_navs = re.findall(r'var data2= \[(.*?)\];', response.text)[0].replace('"', '').split(',')
        statistic_dates = re.findall(r'var data3= \[(.*?)\];', response.text)[0].replace('"', '').split(',')
        for nav, added_nav, statistic_date in zip(navs, added_navs, statistic_dates):
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if nav is not None else None
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item
