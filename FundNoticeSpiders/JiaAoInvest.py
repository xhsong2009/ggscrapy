# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin


class JiaAoInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_JiaAoInvest'
    sitename = '嘉澳投资'
    entry = 'http://www.jiaaocap.com/'

    ips = [
        {
            'url': 'http://www.jiaaocap.com/index.php?m=article&a=index&id=54&lid=54',
            'ref': 'http://www.jiaaocap.com/',
            'pg': 0
        }
    ]

    def parse_item(self, response):
        datas = response.xpath('//div[contains(@class, "newsList")]')
        for notice in datas:
            href = notice.xpath('./div[@class="newsName"]/a/@href').extract_first()
            url = urljoin(get_base_url(response), href)
            title = notice.xpath('./div[@class="newsName"]/a/text()').extract_first()
            publish_time = notice.xpath('./div[@class="newsDate"]/text()').extract_first()

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        next_url = response.xpath('//a[contains(text(), "下一页")]/@href').extract_first()
        if next_url is not None and next_url != '':
            url = self.entry + next_url
            self.ips.append({'url': url, 'ref': response.url})


