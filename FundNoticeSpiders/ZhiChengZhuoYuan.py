# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class ZhiChengZhuoYuanSpider(GGFundNoticeSpider):
    name = 'FundNotice_ZhiChengZhuoYuan'
    sitename = '厦门致诚卓远投资'
    entry = 'http://www.zczyfund.com/news.asp'

    ips = [
        {
            'url': 'http://www.zczyfund.com/news.asp'
        }
    ]

    def parse_item(self, response):
        rows = response.xpath('//table/tr[3]/td/table/tr')
        for row in rows:
            url = row.xpath('./th[2]/div/a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            title = row.xpath('./th[2]/div/a/text()').extract_first()
            publish_time = row.xpath('./th[3]/text()').re_first('\d+/\d+/\d+')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y/%m/%d')
            yield item

        next_url = response.xpath('//td/a[text() = "下一页"]/@href').extract_first()
        if next_url:
            self.ips.append({
                'url': urljoin(get_base_url(response), next_url),
                'ref': response.url
            })
