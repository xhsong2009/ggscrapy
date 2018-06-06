# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class GuMuInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_GuMuInvest'
    sitename = '古木投资'
    entry = 'http://www.goomoo.com.cn/'

    ips = [{
        'url': 'http://www.goomoo.com.cn/website/w/h?mt=2&mc=1674918&cc=9520',
    }]

    def parse_item(self, response):
        rows = response.xpath('//div[@class="simu-site-list"]/ul/a')
        for row in rows:
            title = row.xpath('normalize-space(./li/div[1]/text())').extract_first()
            if '公告' not in title:
                continue
            url = row.xpath('./@href').extract_first()
            url = urljoin(get_base_url(response), url)

            publish_time = row.xpath('normalize-space(./li/div[2]/text())').extract_first()
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
        if next_url and next_url != 'javascript:;':
            next_url = urljoin(get_base_url(response), next_url)
            self.ips.append({
                'url': next_url,
                'ref': response.url
            })






















