# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin


class JHLAssetSpider(GGFundNoticeSpider):
    name = 'FundNotice_JHLAsset'
    sitename = '深圳前海进化论资产'
    entry = 'http://www.jhlfund.com/website/w/h'

    ips = [
        {
            'url': 'http://www.jhlfund.com/website/w/h?mt=2&mc=2909478&cc=2899337',
            'ref': 'http://www.jhlfund.com/website/w/h',
            'pg': 0
        }
    ]

    def parse_item(self, response):
        datas = response.xpath('//div[@class="simu-site-list"]/ul/a')
        for notice in datas:
            href = notice.xpath('./@href').extract_first()
            url = urljoin(get_base_url(response), href)
            title = notice.xpath('normalize-space(./li/div/div[1]/text())').extract_first()
            publish_time = notice.xpath('./li/div/div[3]/div[2]/text()').extract_first()

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        next_url = response.xpath('//a[contains(text(), "下一页")]/@href').extract_first()
        if next_url is not None and next_url != '':
            url = self.entry + next_url
            self.ips.append({'url': url, 'ref': response.url})


