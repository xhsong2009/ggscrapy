# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class YuanShiAssetSpider(GGFundNoticeSpider):
    name = 'FundNotice_YuanShiAsset'
    sitename = '源实资产'
    entry = 'http://www.jvam.com.cn'

    ips = [
        {
            'url': 'http://www.jvam.com.cn/news/notice?pageCurrent=1',
            'ref': 'http://www.jvam.com.cn',
            'ext': {'page': '1'}
        }
    ]

    def parse_item(self, response):
        ext = response.meta['ext']
        page = int(ext['page'])
        rows = response.xpath('//*[@id="body_content"]//div[@class="about_div cls"]/div[2]/div/div')
        if len(rows) >= 5:
            self.ips.append({'url': 'http://www.jvam.com.cn/news/notice?pageCurrent='+str(page+1),
                             'ref': response.url,
                             'ext': {'page': str(page+1)}})

        for notice in rows:
            href = notice.xpath('./a/@href').extract_first().strip()
            title = notice.xpath('./a/text()').extract_first().strip()
            publish_time = notice.xpath('./span/text()').extract_first()

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = self.entry + href
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item


