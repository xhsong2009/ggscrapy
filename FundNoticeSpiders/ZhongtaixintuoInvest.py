# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class ZhongtaixintuoInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_ZhongtaixintuoInvest'
    sitename = '中泰信托'
    entry = 'http://www.zhongtaitrust.com/'

    ips = [{
        'url': 'http://www.zhongtaitrust.com/cn/fortune/products/info.jsp?pageIndex=1'
    }]

    def parse_item(self, response):
        rows = response.xpath('//div[@class="alist2"]/div[not(@class)]')
        for row in rows:
            url = row.xpath('./div[1]/a/@href').extract_first()
            url = urljoin(get_base_url(response), url)

            title = row.xpath('./div[1]/a/text()').extract_first()

            publish_time = row.xpath('./div[2]/text()').extract_first()
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time
            yield item

        next_page = response.xpath('//table[@class="w-all h-30"]/tr/td[3]/image[@class]/@onclick').re_first('\d+')
        next_url = 'http://www.zhongtaitrust.com/cn/fortune/products/info.jsp?pageIndex='+str(next_page)
        if next_page:
            self.ips.append({
                'url': next_url,
            })
