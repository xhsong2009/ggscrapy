# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin


class ZhongTouFuturesSpider(GGFundNoticeSpider):
    name = 'FundNotice_ZhongTouFutures'
    sitename = '中投期货'
    entry = 'http://www.tqfutures.com/'

    ips = [
        {
            'url': 'http://www.tqfutures.com/zggg/list_296.html',
            'ref': 'http://www.tqfutures.com/'
        }
    ]

    def parse_item(self, response):
        datas = response.xpath('//div[@class="News_List ContNews_List"]/ul/li')
        for notice in datas:
            href = notice.xpath('./a/@href').extract_first()
            url = urljoin(get_base_url(response), href)
            title = notice.xpath('normalize-space(./a/text())').extract_first()
            publish_time = notice.xpath('./span/text()').extract_first()

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        next_url = response.xpath('//a[contains(text(), "下一页")]/@href').extract_first()
        if next_url is not None and next_url != 'javascript:void(0);':
            url = self.entry + next_url
            self.ips.append({'url': url, 'ref': response.url})


