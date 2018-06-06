# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin


class ZhongJiangTrustSpider(GGFundNoticeSpider):
    name = 'FundNotice_ZhongJiangTrust'
    sitename = '中江信托'
    entry = 'http://www.jxi.cn'

    lps = [
        {
            'url': 'http://www.jxi.cn/News.aspx?id=15&hl=Ch',
            'ref': 'http://www.jxi.cn/',
        }
    ]

    def parse_list(self, response):
        urls = response.xpath('//ul[@id="ul_15"]/li/a')
        for url in urls:
            href = url.xpath('./@href').extract_first()
            self.ips.append({
                'url': urljoin(get_base_url(response), href),
                'ref': response.url
            })

    def parse_item(self, response):
        datas = response.xpath('//div[@class="nynews"]')
        for notice in datas:
            href = notice.xpath('./a/@href').extract_first()
            url = urljoin(get_base_url(response), href)
            title = notice.xpath('normalize-space(./a/text())').extract_first()
            publish_time = notice.xpath('./span/text()').extract_first()

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        next_url = response.xpath('//a[@class="next"]/@href').extract_first()
        if next_url is not None and next_url != '':
            url = self.entry + next_url
            self.ips.append({'url': url, 'ref': response.url})


