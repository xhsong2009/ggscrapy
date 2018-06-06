# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin


class ZhongOuRuiBoInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_ZhongOuRuiBoInvest'
    sitename = '中欧瑞博'
    entry = 'http://www.rabbitfund.com.cn'

    ips = [
        {
            'url': 'http://www.rabbitfund.com.cn/cn/news/notice.html?cateid=14034',
            'ref': 'http://www.rabbitfund.com.cn',
        }
    ]

    def parse_item(self, response):
        datas = response.xpath('//ul[@class="announ-ul"]/li/a')
        for notice in datas:
            href = notice.xpath('./@href').extract_first()
            title = notice.xpath('normalize-space(./div[@class="announ-cont"]/h3/text())').extract_first()
            year = notice.xpath('./div[@class="announ-time"]/p/text()').extract_first()
            publish_time = year + '-' + notice.xpath('./div[@class="announ-time"]/h3/text()').extract_first()

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = href
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        next_url = response.xpath('//a[contains(text(),"下一页")]/@href').extract_first()
        if next_url is not None and next_url != '':
            url = self.entry + next_url
            self.ips.append({'url': url, 'ref': response.url})


