# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class ZhongruiheyinInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_ZhongruiheyinInvest'
    sitename = '西藏中睿合银投资'
    entry = 'http://www.chinassic.com'

    ips = [{
        'url': 'http://www.chinassic.com/website/w/h?mt=2&mc=2788557&cc=2780862&fp=paging&c=0',
    }]

    def parse_item(self, response):
        rows = response.xpath('//div[@class="simu-site-list"]/ul/a')

        for row in rows:
            url = row.xpath('./@href').extract_first()
            url = urljoin(get_base_url(response), url)

            title = row.xpath('./li/div[1]/text()').extract_first().replace('\t', '').replace('\r', '').replace('\n', '')

            publish_time = row.xpath('./li/div[2]/text()').extract_first().replace('\t', '').replace('\r', '').replace('\n', '')
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time

            yield item

        next_url = response.xpath('//div[@class="simu-site-pagination"]/ul/li/a[contains(text(),"下一页")]/@href').extract_first()
        if next_url != 'javascript:;':
            next_url = urljoin(get_base_url(response), next_url)
            self.ips.append({
                'url': next_url,
                'ref': response.url
            })