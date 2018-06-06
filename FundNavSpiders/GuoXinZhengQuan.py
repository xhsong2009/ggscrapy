# coding:utf-8
# Department : 保障部
# Author : 袁龚浩
# Create_date : 2018-05-02

from datetime import datetime
from FundNavSpiders import GGFundNavSpider
from FundNavSpiders import GGFundNavItem
from scrapy import Request
import re


class GuoXinZhengQuanNavSpider(GGFundNavSpider):
    name = 'FundNav_GuoXinZhengQuanNav'
    sitename = '国信证券'
    channel = '券商资管净值'
    allowed_domains = ['www.guosen.com.cn']

    def start_requests(self):
        yield Request(url='http://www.guosen.com.cn/gxzq/gxyw/jhlc_xx.jsp?fundcode=931204',
                      callback=self.parse_pre_fund)

    def parse_pre_fund(self, response):
        urls = response.xpath('//ul[@id = "navLeft_jhlcjh"]//script').extract()
        for url in urls:
            pattern = re.compile(r'<li><a id=\\"(.*?)\\" href=\\"/gxzq/gxyw(.*?)">(.*?)</a></li>')
            fund_code = pattern.findall(url)[0][0]
            self.fps.append({
                'url': 'http://www.guosen.com.cn/gxzq/gxyw/jhlc_xx.jsp?fundcode=' + fund_code,
                'ext': fund_code,
                'ref': response.url
            })

    def parse_fund(self, response):
        pg = 1
        fund_code = response.meta['ext']
        fund_text = ''.join(response.xpath('//script[@type]').extract())
        pattern = re.compile(r'(\d+,\d+,.*?,\d+)')
        fund_type = pattern.findall(fund_text)[0][-1]
        self.ips.append({
            'url': 'http://www.guosen.com.cn/gxzq/gxyw/content_jzList.jsp',
            'form': {
                'funcNo': '2000053',
                'type': str(fund_type),
                'fundcode': str(fund_code),
                'pageIndex': str(pg),
                'pageSize': '20',
            },
            'pg': 1,
            'ext': [fund_type, fund_code]
        })

    def parse_item(self, response):
        fund_code = response.meta['ext'][1]
        fund_type = response.meta['ext'][0]
        pg = response.meta['pg']
        fund = response.xpath('//table//tr')
        # 普通净值
        if fund_type == '1':
            for i in fund[1:]:
                t = i.xpath('td//text()').extract()
                fundname = t[1]
                statistic_date = t[2].replace('(分红权益登记日)', '')
                # 含有"美元"字样,且有'null'
                nav = re.findall(r'\S*', t[3])[0].replace('null', '')
                added_nav = re.findall(r'\S*', t[4])[0].replace('null', '')
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fundname
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                item['nav'] = float(nav) if nav != '' else None
                item['added_nav'] = float(added_nav) if added_nav != '' else None
                yield item

        # 货币净值
        elif fund_type == '2':
            for i in fund[1:]:
                t = i.xpath('td//text()').extract()
                fundname = t[1]
                statistic_date = t[2]
                annualized_return = t[3].strip()
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fundname
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                item['annualized_return'] = float(annualized_return) if annualized_return != '' else None
                yield item

        # 国信8号等..带A份额
        elif fund_type == '3':
            for i in fund[1:]:
                t = i.xpath('td//text()').extract()
                fundname = t[0]
                statistic_date = t[1]
                nav = t[2].replace('null', '')
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fundname
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                item['nav'] = float(nav) if nav != '' else None
                yield item

            for i in fund[1:]:
                t = i.xpath('td//text()').extract()
                fundname = t[0] + '份额B'
                statistic_date = t[1]
                nav = t[3].replace('null', '')
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fundname
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                item['nav'] = float(nav) if nav != '' else None
                yield item

        # 国信久立成长1号等..带A，B份额
        elif fund_type == '4':
            for i in fund[1:]:
                t = i.xpath('td//text()').extract()
                fundname = t[1]
                statistic_date = t[2]
                nav = t[3].replace('null', '')
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fundname
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                item['nav'] = float(nav) if nav != '' else None
                yield item

            for i in fund[1:]:
                t = i.xpath('td//text()').extract()
                fundname = t[1] + '份额A'
                statistic_date = t[2]
                nav = t[4].replace('null', '')
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fundname
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                item['nav'] = float(nav) if nav != '' else None
                yield item

            for i in fund[1:]:
                t = i.xpath('td//text()').extract()
                fundname = t[1] + '份额B'
                statistic_date = t[2]
                nav = t[5].replace('null', '')
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fundname
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                item['nav'] = float(nav) if nav != '' else None
                yield item

        if response.xpath('//table/tr[2]'):
            next_pg = int(pg) + 1
            self.ips.append({
                'url': 'http://www.guosen.com.cn/gxzq/gxyw/content_jzList.jsp',
                'form': {
                    'funcNo': '2000053',
                    'type': str(fund_type),
                    'fundcode': str(fund_code),
                    'pageIndex': str(next_pg),
                    'pageSize': '20',
                },
                'pg': next_pg,
                'ext': [fund_type, fund_code]
            })
