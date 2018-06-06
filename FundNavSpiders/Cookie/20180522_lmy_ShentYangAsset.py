# -*- coding: utf-8 -*-

# Department : 保障部
# Author : 柳美云
# Create_date : 2018-05-22

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin


class ShengYangAssetSpider(GGFundNavSpider):
    name = 'FundNav_ShengYangAsset'
    sitename = '升阳资产'
    channel = '投顾净值'
    allowed_domains = ['www.syzc.com.cn']

    username = '郑益明'
    password = '13916427906'

    fps = [{'url': 'http://www.syzc.com.cn/products.asp'}]
    cookies = 'ASPSESSIONIDSABCQABQ=KOAJNELCCKPJCKHKDADEHKNC; _D_SID=19D6E7D9CAEAC334EC653F3BCC544ECE; UserName=13916427906'

    def parse_fund(self, response):
        link = response.xpath('//div[@id="inner_left"]//ul//li//a//@href').extract()
        for href in link:
            # 对异常的未披露净值的三只产品，在此处先做剔除
            if href not in ('products.asp?id=2', 'products.asp?id=8', 'products.asp?id=9'):
                ips_url = urljoin('http://www.syzc.com.cn/', href)
                self.ips.append({
                    'url': ips_url,
                    'ref': response.url,
                })

    def parse_item(self, response):
        fund_name = response.xpath(
            '//div[@id="tagContent2"]/table/tbody//tr[2]//p//font//text()').extract_first().strip()
        rows = response.xpath('//div[@class="tagContent"]//table//tbody//tr')
        for row in rows[6:]:
            i = row.xpath("td//font//text()").extract()
            i2 = [_ for _ in i if _.strip()]
            if len(i2) > 3:
                nav = i2[0].replace(',', '').replace(' ', '')
                statistic_date = i2[3].replace(',', '')

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name.replace('净值披露表', '')
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                item['nav'] = float(nav) if nav is not None else None

                yield item
