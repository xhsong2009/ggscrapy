from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import FormRequest
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class AbmFundSpider(GGFundNavSpider):
    name = 'FundNav_AbmFund'
    sitename = '珠海阿巴马资产'
    channel = '投顾净值'

    username = '350982198506242251'
    password = '123456'
    fps = [{'url': 'http://www.abmfund.com/index.php?c=product&a=index&pid=1'}]

    def start_requests(self):
        yield FormRequest(url='http://www.abmfund.com/index.php?c=member&a=login',
                          formdata={'username': '350982198506242251',
                                    'pwd': '123456',
                                    })

    def parse_fund(self, response):
        funds = response.xpath("//ul[@class='menubox']/li/div/a")
        for fund in funds:
            url = fund.xpath("./@href").extract_first()
            fund_url = urljoin(get_base_url(response), url)
            fund_name = fund.xpath("./text()").extract_first()
            self.ips.append({
                'url': fund_url,
                'ref': response.url,
                'pg': 1,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        fund_name1 = response.meta['ext']['fund_name']
        date = re.search('categories:\s*\[(.*?)\]', response.text, re.S)
        date = date.group(1)if date else None
        dates = re.findall('\d+-\d+-\d+', date.replace('/', '-'))if date else []
        navs1 = re.search("name:\s*'整体净值',\s*data:\s*\[(.*?)\]", response.text, re.S)
        navs1 = navs1.group(1)if navs1 else None
        navs1 = re.findall('[0-9.]+', navs1)if navs1 else []
        navs2 = re.search("name:\s*'进取[级]*净值',\s*marker:\s*\{\s*symbol:\s*'diamond'\s*\},\s*data:\s*\[(.*?)\]", response.text, re.S)
        navs2 = navs2.group(1)if navs2 else None
        navs2 = re.findall('[0-9.]+', navs2)if navs2 else []
        navs3 = re.search("name:\s*'费前净值|单位净值',\s*marker:\s*\{\s*symbol:\s*'diamond'\s*\},\s*data:\s*\[(.*?)\]",
                          response.text, re.S)
        navs3 = navs3.group(1) if navs3 else None
        navs3 = re.findall('[0-9.]+', navs3) if navs3 else []
        if navs1 and navs2:
            for fund_name in [fund_name1, fund_name1+'进取级']:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                if '进取级' in fund_name:
                    for date, nav in zip(dates, navs2):
                        item['fund_name'] = fund_name
                        item['nav'] = float(nav)
                        item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d')
                        yield item
                else:
                    for date, nav in zip(dates, navs1):
                        item['fund_name'] = fund_name
                        item['nav'] = float(nav)
                        item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d')
                        yield item
        elif len(navs2) == 0 and navs1:
            for date, nav in zip(dates, navs1):
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name1
                item['nav'] = float(nav)
                item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d')
                yield item
        elif len(navs1) + len(navs2) == 0 and navs3:
            for date, nav in zip(dates, navs3):
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name1
                item['nav'] = float(nav)
                item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d')
                yield item


