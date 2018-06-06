# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class YunchengtaiInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_YunchengtaiInvest'
    sitename = '北京云程泰投资'
    entry = 'http://www.yctchina.com.cn/'

    ips = [{
        'url': 'http://www.yctchina.com.cn/a/pics/list_6_1.html',
    }]

    def parse_item(self, response):
        rows = response.xpath('//div[@class="list_content"]/ul/li')

        for row in rows:
            url = row.xpath('./a/@href').extract_first()
            url = urljoin(get_base_url(response), url)

            title = row.xpath('./a/text()').extract_first()

            publish_time = row.xpath('./span/text()').extract_first()
            publish_time = publish_time[1:-1]
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time

            yield item

        next_url = response.xpath('//div[@class="fenye"]/ul/li/a[text()="下一页"]/@href').extract_first()
        if next_url:
            next_url = urljoin(get_base_url(response), next_url)
            self.ips.append({
                'url': next_url,
                'ref': response.url
            })