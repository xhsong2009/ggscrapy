from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy import Request, FormRequest


class DongFangGangWanSpider(GGFundNavSpider):
    name = 'FundNav_DongFangGangWan'
    sitename = '东方港湾'
    channel = '投顾净值'

    username = 'admin888'
    password = 'admin888'

    fps = [{
        'url': 'http://www.ebay-invest.com/Home/Product_detail.html'
    }]

    def start_requests(self):
        yield Request(url='http://www.ebay-invest.com/index_index.html', callback=self.parse_pre_login)

    def parse_pre_login(self, response):
        yield FormRequest(url='http://www.ebay-invest.com/Yzm_consent.html',
                          formdata={'sdsa': '确认'},
                          callback=self.parse_login)

    def parse_login(self, response):
        yield FormRequest(url='http://www.ebay-invest.com/Members_login.html',
                          formdata={'username': 'admin888',
                                    'password': 'admin888'})

    def parse_fund(self, response):
        codes = response.xpath('//div[@class = "fl w260"]//li//a//@href').extract()
        fundnames = response.xpath('//div[@class = "fl w260"]//li//a/text()').extract()
        for code, fundname in zip(codes, fundnames):
            ips_url = 'http://www.ebay-invest.com' + code.replace('.html', '') + '_catid_1_type_unit.html'
            self.ips.append({
                'url': ips_url,
                'ref': response.url,
                'ext': fundname
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']
        fund_list = response.xpath('//table//tr')
        for i in fund_list[1:]:
            t = i.xpath('td//text()').extract()
            statistic_date = t[1]
            nav = t[2]
            added_nav = t[3]

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            item['nav'] = float(nav)
            item['added_nav'] = float(added_nav)
            yield item

        if response.xpath('//div//a[@class = "next"]//@href'):
            next_href = response.xpath('//div//a[@class = "next"]//@href').extract_first()
            next_url = 'http://www.ebay-invest.com' + next_href
            self.ips.append({
                'url': next_url,
                'ref': response.url,
                'ext': fund_name
            })
