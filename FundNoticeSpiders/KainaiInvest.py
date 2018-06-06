# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class KainaiInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_KainaiInvest'
    sitename = '广州凯纳投资'
    entry = 'http://www.knquant.com/'

    ips = [{
        'url': 'http://www.knquant.com/notice.html',
    }]

    def parse_item(self, response):
        rows = response.xpath('//div[@class="news_list"]/ul/li')
        for row in rows:
            url = row.xpath('./a/@href').extract_first()
            url = urljoin(get_base_url(response), url)

            title = row.xpath('./a/text()').extract_first().strip().replace('\t', '').replace('\r', '').replace('\n', '')

            publish_time = row.xpath('./span/text()').extract_first().strip().replace('\t', '').replace('\r', '').replace('\n', '')
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time
            yield item

        next_url = response.xpath('//div[@class="page"]/a[text()="下一页"]/@href').extract_first()
        if next_url:
            next_url = urljoin(get_base_url(response), next_url)
            if response.url != next_url:
                self.ips.append({
                    'url': next_url,
                })
