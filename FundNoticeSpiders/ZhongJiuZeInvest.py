# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class ZhongJiuZeInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_ZhongJiuZeInvest'
    sitename = '深圳前海中玖泽投资'
    entry = 'http://zjztz.com/news.html'

    ips = [
        {
            'url': 'http://zjztz.com/news.html'
        }
    ]

    def parse_item(self, response):
        rows = response.xpath('//div[@class="mcon"]/div[not(@style)]')
        for row in rows:
            url = row.xpath('./a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            title = row.xpath('./a/text()').extract_first()
            publish_time = row.xpath('./span/text()').re_first('\d+-\d+-\d+')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item
