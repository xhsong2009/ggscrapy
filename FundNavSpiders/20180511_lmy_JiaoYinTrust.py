# -*- coding: utf-8 -*-

# Department : 保障部
# Author : 柳美云
# Create_date : 2018-05-04

from urllib.parse import urljoin
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from datetime import datetime


class JiaoYinTrustSpider(GGFundNavSpider):
    name = 'FundNav_JiaoYinTrust'
    sitename = '交银信托'
    channel = '信托净值'

    fps = [{
        'url': 'https://www.bocommtrust.com/index.php?id=209'
    }]

    def parse_fund(self, response):
        fund_list = response.xpath('//div[@class="number_tablebox"]//div//li//a//@href').extract()
        for key_fund in fund_list:
            link_fund = urljoin('https://www.bocommtrust.com/', key_fund)
            self.ips.append({
                'url': link_fund,
                'ref': response.url
            })

    def parse_item(self, response):
        rows = response.xpath('//div[@class="number_tablebox"]//tr')
        fund_name = response.xpath('//div[@class="title"]/text()').extract_first()
        for row in rows[1:]:
            row_info = row.xpath('td//text()').extract()
            statistic_date = row_info[0]
            nav = row_info[1]
            if len(row_info) > 2 and row_info[4] == '--':
                income_value_per_ten_thousand = row_info[2]
                d7_annualized_return = row_info[3]
                d30_annualized_return = None
            elif len(row_info) > 2 and row_info[4] != '--':
                d7_annualized_return = row_info[3]
                d30_annualized_return = row_info[4]
                if '（2017年7月20日向中央结算公司和上海清算所支付了债券账户维护费用。）' in row_info[2]:
                    income_value_per_ten_thousand = row_info[2].replace('（2017年7月20日向中央结算公司和上海清算所支付了债券账户维护费用。）', '')
                else:
                    income_value_per_ten_thousand = row_info[2]
            else:
                income_value_per_ten_thousand = None
                d7_annualized_return = None
                d30_annualized_return = None

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            item['nav'] = float(nav) if nav is not None else None
            item['income_value_per_ten_thousand'] = float(
                income_value_per_ten_thousand) if income_value_per_ten_thousand is not None else None
            item['d7_annualized_return'] = float(d7_annualized_return) if d7_annualized_return is not None else None
            item['d30_annualized_return'] = float(d30_annualized_return) if d30_annualized_return is not None else None
            yield item

        next_urls = response.xpath('//div/a[contains(., "下一")]//@href').extract_first()
        if next_urls:
            self.ips.append({
                'url': 'https://www.bocommtrust.com/' + next_urls,
                'ref': response.url
            })
