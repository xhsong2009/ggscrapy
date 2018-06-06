# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class ZhongChengTrustSpider(GGFundNoticeSpider):
    name = 'FundNotice_ZhongChengTrust'
    sitename = '中诚信托'
    entry = 'http://www.cctic.com.cn/cpgg/index.jhtml'

    ips = [
        {
            'url': 'http://www.cctic.com.cn/cpgg/index.jhtml',
            'pg': 1
        }
    ]

    def parse_item(self, response):
        rows = response.xpath('//div[@class="item clearfix"]')
        for row in rows:
            url = row.xpath('./div/h1/a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            title = row.xpath('./div/h1/a/text()').extract_first()
            publish_time = row.xpath('./div/div[@class="fr"]/span//text()').re_first('\d+-\d+-\d+')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        pg = response.meta['pg'] + 1
        if pg <= 412:
            next_url = 'http://www.cctic.com.cn/cpgg/index_{}.jhtml'.format(str(pg))
            self.ips.append({
                'url': urljoin(get_base_url(response), next_url),
                'ref': response.url,
                'pg': pg
            })
