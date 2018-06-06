# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class ShangHaiYiZhouAssetSpider(GGFundNoticeSpider):
    name = 'FundNotice_ShangHaiYiZhouAsset'
    sitename = '上海亿舟资产'
    entry = 'http://www.yizhouzichan.com/article/cpgg'

    lps = [
        {
            'url': 'http://www.yizhouzichan.com/article/cpgg'
        }
    ]

    def parse_list(self, response):
        rows = response.xpath('//ul[@class="prodectlixl"]/li')[1:]
        for row in rows:
            url = row.xpath('./a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            self.ips.append({
                'url': url,
                'ref': response.url,
                'pg': 1,
                'ext': {'entry': url.replace('#introduce', '')}
            })

    def parse_item(self, response):
        entry = response.meta['ext']['entry']
        rows = response.xpath('//div[@class="baogaobox"]')
        for row in rows:
            url = row.xpath('./p/a/@href').extract_first()
            if 'javascript' not in url:
                url = urljoin(get_base_url(response), url)
            else:
                # 加密公告取当前所在页面地址
                url = response.url
            title = row.xpath('./p/a/text()').extract_first()
            publish_time = row.xpath('./div/text()').re_first('\d+-\d+-\d+')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        tp = response.xpath('//span[@id="totalPage"]/text()').re_first('共(\d+)页')
        if tp:
            pg = response.meta['pg'] + 1
            if pg <= int(tp):
                self.ips.append({
                    'url': entry + '/' + str(pg),
                    'ref': response.url,
                    'pg': pg,
                    'ext': {'entry': entry}
                })
