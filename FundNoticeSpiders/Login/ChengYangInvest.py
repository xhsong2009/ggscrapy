# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from scrapy import FormRequest
from FundNoticeSpiders import GGFundNoticeSpider


class ChengYangInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_ChengYangInvest'
    sitename = '辰阳投资'
    entry = 'http://www.ifc-cherami.com/'

    username = '13916427906'
    password = 'ZYYXSM123'

    ips = [
        {
            'url': 'http://www.ifc-cherami.com/index.php?g=portal&m=prod&a=announce',
            'ref': None,
        }
    ]

    def start_requests(self):
        yield FormRequest(url='http://www.ifc-cherami.com/index.php?g=portal&m=user&a=dologin',
                          method='POST',
                          formdata={'login_phone': self.username, 'login_passwd': self.password, 'checkbox': 'on'},
                          headers={
                              'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                          },
                          )

    def parse_item(self, response):
        datas = response.xpath('/html/body//div[@class="zxxw_C"]/ul/li')
        for notice in datas:
            href = notice.xpath('./div/p/a/@href').extract_first().strip()
            title = notice.xpath('./div/span/text()').extract_first().strip()
            publish_time = notice.xpath('./div/text()').re_first('\d+-\d+-\d+')
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = self.entry + href
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item
