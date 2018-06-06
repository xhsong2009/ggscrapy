# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin


class YunGuoInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_YunGuoInvest'
    sitename = '云国投'
    entry = 'http://www.yntrust.com'

    ips = [
        {
            'url': 'http://www.yntrust.com/Disclosure/Notice',
            'ref': 'http://www.yntrust.com/Disclosure/Index'
        }
    ]

    def __init__(self, *args, **kwargs):
        super(YunGuoInvestSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        datas = response.xpath('/html/body/section[2]/div//ul[@class="bulletin_main clearfix"]/li')
        next_url = response.xpath('/html/body/section[2]/div//div[@class="page"]/div/a[last()]/@href').extract_first()
        for notice in datas:
            href = notice.xpath('./a/@href').extract_first()
            url = urljoin(get_base_url(response), href)
            title = notice.xpath('./a/span/text()').extract_first().strip()
            publish_time = notice.xpath('./a/time/text()').extract_first()

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item
        if next_url is not None and next_url != '':
            url = self.entry + next_url
            self.ips.append({'url': url, 'ref': response.url})
        yield self.request_next()

