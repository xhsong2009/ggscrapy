from datetime import datetime
from urllib.parse import urljoin
from scrapy import FormRequest
from scrapy.utils.response import get_base_url
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class YinlingInvestSpider(GGFundNavSpider):
    name = 'FundNav_YinlingInvest'
    sitename = '引领投资'
    channel = '投资顾问'

    username = '吴迪'
    password = '123456'
    cookies = 'shengming=yes'

    def start_requests(self):
        yield FormRequest(url='http://www.yinlinggroup.com/ashx/login.ashx',
                          formdata={
                              'UserName': self.username,
                              'UserPwd': self.password,
                              'UserType': '1'
                          },
                          callback=self.parse_list)

    def parse_list(self, response):
        self.fps.append({
            'url': 'http://www.yinlinggroup.com/product/zhengquan/'
        })

    def parse_fund(self, response):
        urls = response.xpath('//ul[@class="nyLejUL"]/li')
        for url in urls:
            href = url.xpath('./a/@href').extract_first()
            urls = urljoin(get_base_url(response), href)

            code = urls.rsplit('=', 1)[1]
            fund_name = url.xpath('./a/text()').extract_first()

            self.ips.append({
                'url': 'http://www.yinlinggroup.com/product/zhengquan/?ProID=' + str(code),
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        ext = response.meta['ext']
        fund_names = ext['fund_name']

        rows = response.xpath('//table[@class="cpxxkNR1_bg1"]/tr')

        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url

            item['fund_name'] = fund_names

            statistic_date = row.xpath("./td[2]/text()").re_first('\d+-\d+-\d+')
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            nav = row.xpath('./td[3]/text()').extract_first()
            item['nav'] = float(nav) if nav else None

            added_nav = row.xpath("./td[4]/text()").extract_first()
            item['added_nav'] = float(added_nav) if added_nav else None

            yield item
