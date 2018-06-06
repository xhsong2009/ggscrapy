# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy import FormRequest
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class YiBoInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_YiBoInvest'
    sitename = '绎博投资'
    entry = 'http://www.everinvestment.cn/'

    username = 'yuangh@go-goal.com'
    password = 'ZYYXSM123'

    ips = [
        {
            'url': 'http://www.everinvestment.cn/xxplybyq',
            'ref': 'http://www.everinvestment.cn/'
        },
        {
            'url': 'http://www.everinvestment.cn/xxplybeq',
            'ref': 'http://www.everinvestment.cn/'
        }
    ]

    def start_requests(self):
        yield FormRequest(url='http://www.everinvestment.cn/userlogin?returnurl=',
                      formdata={
                          'Username': self.username,
                          'Password': self.password
                      })

    def parse_item(self, response):
        times = response.xpath('//div[@class="yibuSmartViewMargin absPos"]/div/div/div/p/span/text()').extract()
        rows = response.xpath('//div[@class="yibuSmartViewMargin absPos"]/div/a/span/i')
        for (row, time) in zip(rows, times[3:]):
            title = row.xpath('./following-sibling::span/text()').extract_first()
            url = row.xpath('./../../@href').extract_first()
            url = urljoin(get_base_url(response), url)
            publish_time = time

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['title'] = title
            item['url'] = url
            item['publish_time'] = datetime.strptime(publish_time, '%Y年%m月%d日')
            yield item
