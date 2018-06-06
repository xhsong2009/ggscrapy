# -*- coding: utf-8 -*-

# Department : 保障部
# Author : 王卓诚
# Create_date : 2018-04-27

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class BoRuiAiJianInvestSpider(GGFundNavSpider):
    name = 'FundNav_BoRuiAiJianInvest'
    sitename = '柏瑞爱建资产'
    channel = '公募专户净值'
    allowed_domains = ['www.pa-asset.com']

    username = '13916427906'
    password = 'ZYYXSM123'

    fps = [{
        'url': 'http://www.pa-asset.com/list/6521/1.shtml',
        'pg': 1
    }]

    def parse_fund(self, response):
        urls = response.xpath('//div[@class="right2"]/p')
        if urls:
            next_pg = response.meta['pg'] + 1
            self.fps = [{
                'url': 'http://www.pa-asset.com/list/6521/' + str(next_pg) + '.shtml',
                'ref': response.url,
                'pg': next_pg
            }]

            for uu in urls:
                infotext = uu.xpath('a/em/text()').extract_first()
                url = urljoin(get_base_url(response), uu.xpath('a/@href').extract_first())
                if infotext.find('净值公布') > -1:
                    chuanproductname = infotext.replace(' ', '').replace('净值公布', '')
                    self.ips.append({
                        'url': url,
                        'ref': response.url,
                        'ext': chuanproductname
                    })

    def parse_item(self, response):
        productname = response.meta['ext']
        rows = response.xpath('//div[@class="p"]/table/tbody/tr')
        tmpst_date = ''
        for k, row in enumerate(rows):
            tmpfundname = ''
            statistic_date = ''
            f0 = row.xpath(r'./td[1]/strong/span/text()').extract_first()
            f1 = row.xpath(r'./td[1]/span/text()').extract_first()
            f2 = row.xpath(r'./td[2]/span/text()').extract_first()

            if f0 is None and f1 is None and f2 is None:
                continue
            if (k == 0 or k % 4 == 0) and (not f0 is None or not f1 is None):
                if f0 is None and not f1 is None:
                    f0 = f1
                f0 = f0.strip().replace('/', '-')

                zhouqi1 = re.compile(r'\d{4}(/|-)\d{1,2}(/|-)\d{1,2}', re.S | re.I | re.M)
                zhouqi2 = re.findall(zhouqi1, f0)
                if len(zhouqi2) > 0 and tmpst_date == '' or f0 != tmpst_date:
                    tmpst_date = f0

            if k > 0 and k % 4 != 0 and not f2 is None:
                if f1 == '单位总净值：' or f1.find('总净值') > 0:
                    tmpfundname = productname
                elif f1 == '单位净值：优先级' or f1.find('优先级') > 0:
                    tmpfundname = productname + '优先级'
                elif f1 == '单位净值：次级' or f1.find('次级') > 0:
                    tmpfundname = productname + '次级'
                nav = f2.strip()
                if tmpst_date != '':
                    statistic_date = tmpst_date

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = tmpfundname
                item['nav'] = float(nav) if nav else None

                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

                yield item
