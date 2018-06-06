# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
import re


class ZhongRongTrustSpider(GGFundNoticeSpider):
    name = 'FundNotice_ZhongRongTrust'
    sitename = '中融信托'
    entry = 'http://www.zritc.com'

    lps = [
        {
            'url': 'http://www.zritc.com/zrcf_zyyw/gbbg/new/',
            'ref': 'http://www.zritc.com',
        }
    ]

    def parse_list(self, response):
        urls = response.xpath('//div[@class="nav-sub mb20"]/div[4]/a')
        for url in urls[1:]:
            href = url.xpath('./@href').extract_first()
            self.ips.append({
                'url': urljoin(get_base_url(response), href),
                'ref': response.url,
                'pg': 0
            })

    def parse_item(self, response):
        datas = response.xpath('//ul[@id="ggul"]/li')
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
            item['publish_time'] = datetime.strptime(publish_time, '%Y/%m/%d')
            yield item

        tp = response.xpath('//div[@class="page"]/table/tr/td/script').extract_first()
        tp = re.findall('var countPage = (\d+)', tp)[0]
        cp = response.meta['pg']
        if (cp+1) < int(tp):
            cp = cp+1
            next_url = urljoin(get_base_url(response), 'index_' + str(cp) + '.html')
            self.ips.append({
                'url': next_url,
                'ref': response.url,
                'pg': cp
            })



