# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy import FormRequest
from scrapy.utils.response import get_base_url
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class YuJinFundSpider(GGFundNavSpider):
    name = 'FundNav_YuJinFund'
    sitename = '裕晋投资'
    channel = '投顾净值'

    username = '466255332@qq.com'
    password = 'ZYYXSM123'

    def start_requests(self):
        yield FormRequest(url='http://www.yujinfund.com/Yzm_consent.html',
                          formdata={'sdsa': '已了解并接受上述所有条款和条件'},
                          callback=self.parse_login)

    def parse_login(self, response):
        yield FormRequest(url='http://www.yujinfund.com/Index_ajaxLogin.html',
                          formdata={'email': self.username, 'password': self.password},
                          callback=self.parse_fund)

    fps = [
        {
            'url': 'http://www.yujinfund.com/Home/Product_index.html',
            'ref': None
        }
    ]

    def parse_fund(self, response):
        rows = response.xpath('//table[@class="container h_pro pro"]/tr')[1:]
        for row in rows:
            product_details_id = row.xpath('./td[@class="proname"]/a/@href').re_first(r'Product_details_id_[\d]+')
            fund_name = row.xpath('./td[@class="proname"]/a/text()').extract_first()
            self.ips.append({
                'url': 'http://www.yujinfund.com/{0}_type_unit.html'.format(product_details_id),
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = response.xpath('//table[@class="h_pro"]/tr')[1:]
        for row in rows:
            statistic_date = row.xpath('./td[1]/text()').re_first('\d+-\d+-\d+')
            nav = row.xpath('./td[2]/text()').re_first('[0-9.]+')
            added_nav = row.xpath('./td[3]/text()').re_first('[0-9.]+')
            if fund_name in ['平安*安蕴10期B类', '建信*3号普通级']:
                nav = row.xpath('./td[5]/text()').re_first('[0-9.]+')
                added_nav = row.xpath('./td[6]/text()').re_first('[0-9.]+')

            if nav is not None:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav)
                item['added_nav'] = float(added_nav)
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item

        next_url = response.xpath('//div[@class="page"]/div/a[contains(text(), "下一页")]/@href').extract_first()
        if next_url:
            self.ips.append({
                'url': urljoin(get_base_url(response), next_url),
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })
