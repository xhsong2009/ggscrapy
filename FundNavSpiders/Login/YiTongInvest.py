from datetime import datetime
from urllib.parse import urljoin
from scrapy import FormRequest, Request
from scrapy.utils.response import get_base_url
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class YiTongInvestSpider(GGFundNavSpider):
    name = 'FundNav_YiTongInvest'
    sitename = '易同投资'
    channel = '投顾净值'

    username = '15538536932'
    password = '123456'

    def start_requests(self):
        yield Request(url='http://www.etock.com.cn/member/member.php?c=login', callback=self.parse_pre_login)

    def parse_pre_login(self, response):
        yield FormRequest(url='http://www.etock.com.cn/member/member.php?a=login',
                          formdata={
                              'username': self.username,
                              'password': self.password,
                              'btnSubmit': '登 录'
                          },
                          headers={
                              'Content-Type': 'application/x-www-form-urlencoded'
                          },
                          callback=self.parse_login)

    def parse_login(self, response):
        self.fps = [{
            'url': 'http://www.etock.com.cn/member/products.php',
            'ref': response.url
        }]

    def parse_fund(self, response):
        funds = response.xpath('/html/body/div[3]/div[@class="pdtlist"]/ul/li/a/@href').extract()
        for url in funds:
            url = urljoin(get_base_url(response), url)
            self.ips.append({
                'url': url,
                'ref': response.url
            })

    def parse_item(self, response):
        fund_name = response.xpath(
            '/html/body/div[3]/div[1]/div[@class="product"]/h1/text()').extract_first()
        line = response.text
        dates = re.search(r"\['(\d+.*)'\]", line)
        if dates:
            dates = dates.group(1)
            dates = dates.split(',')
            rows = re.search(r"\[(\d+\..*\d+)]", line).group(1)
            rows = rows.split(',')
            for date in dates:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['fund_name'] = fund_name
                item['channel'] = self.channel
                item['url'] = response.url
                nav = rows.pop(0)
                item['nav'] = float(nav)
                date = re.search(r'(\d+-\d+-\d+)', date).group(1)
                item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d')
                yield item
