from datetime import datetime
from urllib.parse import urljoin
from urllib import parse
from scrapy import FormRequest, Request
from scrapy.utils.response import get_base_url
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class XingHuiAssetSpider(GGFundNavSpider):
    name = 'FundNav_XingHuiAsset'
    sitename = '星惠资产'
    channel = '投资顾问'

    username = '13916427906'
    password = 'ZYYXSM123'

    def start_requests(self):
        yield Request(url='http://www.starwint.com/tanc.html', callback=self.parse_pre_login)

    def parse_pre_login(self, response):
        url = 'http://www.starwint.com//user_reg_check.aspx?callback=jQuery31002569703387914626_1525855147766&type=login&phone='+self.username+'&pass='+self.password+'&reme=1&rn=1&_=1525855147770'
        yield FormRequest(url=url,
                          callback=self.parse_login)

    def parse_login(self, response):
        self.fps = [{
            'url': 'http://www.starwint.com/news/list/24_1.htm',
            'ref': response.url,
            'ext': {'type': '1'}
        }]

    def parse_fund(self, response):
        ext = response.meta['ext']
        type = int(ext['type'])
        if type == 1:
            funds = response.xpath('//*[@id="shizhi"]/ul/li/a/@href').extract()
            for url in funds:
                url = urljoin(get_base_url(response), url)
                self.fps.append({
                    'url': url,
                    'ref': response.url,
                    'ext': {'type': '2'}
                })
        else:
            url = response.xpath('//*[@id="nav"]//div[@class="bt02"]/iframe/@src').extract_first()
            url = urljoin(get_base_url(response), url)
            self.ips.append({
                'url': url,
                'ref': response.url
            })

    def parse_item(self, response):
        line = response.url
        fund_name = re.search(r'name=(\S+)', line).group(1)
        fund_name = parse.unquote_plus(fund_name)
        rows = response.xpath('//*[@id="form1"]/div[2]/table[2]//tr[4]/td/table//tr')
        for row in rows[1:]:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['fund_name'] = fund_name
            item['channel'] = self.channel
            item['url'] = parse.unquote_plus(response.url)
            nav = row.xpath('./td[2]//text()').re_first(r'(\d+\.?\d*)')
            item['nav'] = float(nav)
            statistic_date = row.xpath('./td[1]//text()').extract_first()
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item
