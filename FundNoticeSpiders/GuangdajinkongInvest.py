# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class GuangdajinkongInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_GuangdajinkongInvest'
    sitename = '上海光大金控投资'
    entry = 'http://www.ebasset.com/'

    ips = [{
        'url': 'http://www.ebasset.com/?q=notice-eba',
    }]

    def parse_item(self, response):
        rows = response.xpath('//table[@class="views-view-grid cols-1"]//tr')

        for row in rows:
            url = row.xpath('./td/span/span/a/@href').extract_first()
            url = urljoin(get_base_url(response), url)

            title = row.xpath('./td/span/span/a/text()').extract_first().replace('\t', '').replace('\r', '').replace('\n', '')

            publish_time = row.xpath('./td/div/div/span/@content').extract_first()
            publish_time = publish_time[0:10]
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time

            yield item

        next_url = response.xpath('//ul[@class="pager"]/li/a[contains(text(),"下一页")]/@href').extract_first()
        if next_url:
            next_url = urljoin(get_base_url(response), next_url)
            self.ips.append({
                'url': next_url,
                'ref': response.url
            })