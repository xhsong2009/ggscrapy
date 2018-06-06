# Department : 保障部
# Author : 钱斌
# Create_date : 2018-05-08

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
import re


class CaiKaFeiFundSalesSpider(GGFundNavSpider):
    name = 'FundNav_CaiKaFeiFundSales'
    sitename = '上海财咖啡基金销售有限公司'
    channel = '投顾净值'

    fps = [{
        'url': 'http://www.rffund.com/list/407/1.shtml',
        'pg': 1
    }]

    def parse_fund(self, response):
        if response.status != '404':
            href_list = response.xpath('//a[contains(@title,"净值公告")]/@href').extract()
            for href in href_list:
                self.ips.append({
                    'url': urljoin(get_base_url(response), href),
                    'ref': response.url,
                })

            next_pg = response.meta['pg'] + 1
            self.fps.append({
                'url': re.sub('\d+\.shtml', str(next_pg) + r'.shtml', response.url),
                'ref': response.url,
                'pg': next_pg
            })

    def parse_item(self, response):
        title = response.css('h2.padding-top35::text').extract_first()
        content = response.xpath('string(//div[@class="new-detaiList padding-bottom25"])').extract_first()
        # 截至2015年10月30日，日发资产灵活配置9号基金基金净值为0.77元
        date_reg = re.compile('截\D+(\d+年\d+月\d+日)', re.DOTALL)
        # name_reg = re.compile('(日发.*)基金净值', re.DOTALL)
        nav_reg = re.compile('净值\D*(\d\.\d*)', re.DOTALL)

        fund_name = title.split('基金')[0]
        date = date_reg.findall(content)
        # name = name_reg.findall(content)
        nav = nav_reg.findall(content)

        item = GGFundNavItem()
        item['sitename'] = self.sitename
        item['fund_name'] = fund_name
        item['channel'] = self.channel
        item['url'] = response.url
        item['nav'] = float(nav[0]) if nav else None
        item['statistic_date'] = datetime.strptime(date[0], '%Y年%m月%d日') if date else None
        yield item
