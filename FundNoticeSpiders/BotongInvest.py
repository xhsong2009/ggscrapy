# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class BotongInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_BotongInvest'
    sitename = '泊通投资'
    entry = 'http://www.botongfund.com/'
    proxy = 2
    ips = [{
        'url': 'http://www.botongfund.com/menus/xKEeQwK8xEurkakaR6ybi5/child_menus/dE5xdrXwkwhzX9X9BxaRH3',
    }]

    def parse_item(self, response):
        rows = response.xpath('//div[@class="fem01_camall"]/a')

        for row in rows:
            url = row.xpath('./@href').extract_first()
            url = urljoin(get_base_url(response), url)

            title = row.xpath('./div[2]/p[1]/text()').extract_first()

            publish_time = row.xpath('./div[2]/p[2]/text()').extract_first()
            publish_time = datetime.strptime(publish_time, '%Y年%m月%d日')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time

            yield item

        next_url = response.xpath('//span[@class="next"]/a[text()="下一页"]/@href').extract_first()
        if next_url:
            next_url = urljoin(get_base_url(response), next_url)
            self.ips.append({
                'url': next_url,
                'ref': response.url
            })
        yield self.request_next()