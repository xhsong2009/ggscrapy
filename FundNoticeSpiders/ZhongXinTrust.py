# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class ZhongXinTrustSpider(GGFundNoticeSpider):
    name = 'FundNotice_ZhongXinTrust'
    sitename = '中信信托'
    entry = 'https://trust.ecitic.com/information/index.shtml'

    ips = [
        {
            'url': 'https://trust.ecitic.com/information/clgg/index.shtml',
            'ext': {'url_type': 'clgg'},
            'pg': 1
        },
        {
            'url': 'https://trust.ecitic.com/information/xtswglbg/index.shtml',
            'ext': {'url_type': 'xtswglbg'},
            'pg': 1
        },
        {
            'url': 'https://trust.ecitic.com/information/qsbg/index.shtml',
            'ext': {'url_type': 'qsbg'},
            'pg': 1
        },
        {
            'url': 'https://trust.ecitic.com/information/qtbg/index.shtml',
            'ext': {'url_type': 'qtbg'},
            'pg': 1
        }
    ]

    def parse_item(self, response):
        ext = response.meta['ext']
        rows = response.xpath('//div[@class="newsList"]/div')
        for row in rows:
            title = row.xpath('./a/@title').extract_first()
            url = row.xpath('./a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            publish_time = row.xpath('./span/text()').re_first('\d+-\d+-\d+')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['title'] = title
            item['url'] = url
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        url_type = ext['url_type']
        tp = int(response.xpath('//div[@class="pageinfo"]/text()').re_first('\d+'))
        pg = response.meta['pg'] + 1
        if pg <= tp:
            self.ips.append({
                'url': 'https://trust.ecitic.com/information/{0}/index_{1}.shtml'.format(url_type, pg),
                'ref': response.url,
                'ext': {'url_type': url_type},
                'pg': pg
            })
