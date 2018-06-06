# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy import FormRequest
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class FengYiInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_FengYiInvest'
    sitename = '上海沣谊投资'
    entry = 'http://www.blossomfund.cn/news/index/id/6'

    username = '13916427906'
    password = 'ZYYXSM123'

    ips = [
        {
            'url': 'http://www.blossomfund.cn/news/index/id/6'
        }
    ]

    def start_requests(self):
        yield FormRequest(url='http://www.blossomfund.cn/user/login',
                          formdata={
                              'username': self.username,
                              'password': self.password
                          })

    def parse_item(self, response):
        rows = response.xpath('//div[@class="list"]')
        for row in rows:
            title = row.xpath('./div[@class="l"]/a/@title').extract_first()
            url = row.xpath('./div[@class="l"]/a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            publish_time = row.xpath('./div[@class="r"]/text()').re_first('\d+-\d+-\d+')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['title'] = title
            item['url'] = url
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        next_url = response.xpath('//div[@class="page"]/a[contains(text(),"下一页")]/@href').extract_first()
        if next_url:
            self.ips.append({
                'url': urljoin(get_base_url(response), next_url),
                'ref': response.url
            })
