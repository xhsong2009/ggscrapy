# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class HaiXiShengQianInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_HaiXiShengQianInvest'
    sitename = '福建海西晟乾投资'
    entry = 'http://www.fjhxsq.com/plus/list.php?tid=3'

    ips = [
        {
            'url': 'http://www.fjhxsq.com/plus/list.php?tid=3'
        }
    ]

    def parse_item(self, response):
        rows = response.xpath('//ul[@class="e2"]/li/table/tbody/tr')
        for row in rows:
            url = row.xpath('./td[1]/a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            title = row.xpath('./td[1]/a/text()').extract_first()
            publish_time = row.xpath('./td[2]/span/text()').re_first('\d+-\d+-\d+')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item
