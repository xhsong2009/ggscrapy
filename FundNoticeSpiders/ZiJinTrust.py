# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
import re


class ZiJinTrustSpider(GGFundNoticeSpider):
    name = 'FundNotice_ZiJinTrust'
    sitename = '紫金信托'
    entry = 'http://www.zjtrust.com.cn/'

    lps = [
        {
            'url': 'https://www.zjtrust.com.cn/cn/page/33.html',
            'ref': 'http://www.zjtrust.com.cn',
            'ext': {'flag': 0}
        }
    ]

    def parse_list(self, response):
        if response.meta['ext']['flag'] == 1:
            pg = response.meta['pg']
            self.ips.append({
                'url': response.url + '?pageIndex=' + str(pg),
                'ref': response.url,
                'pg': pg,
                'ext': {'baseUrl': response.url}
            })
        else:
            urls = response.xpath("//div[contains(text(),'公告') or contains(text(),'报告')]")
            for url in urls:
                href = url.xpath('./@onclick').extract_first()
                if href is None:
                    continue
                href = re.findall('=\\\'([^\s]*)\\\'', href)[0]
                type = url.xpath('./text()').extract_first()
                self.lps.append({
                    'url': urljoin(get_base_url(response),href),
                    'ref': 'http://www.zjtrust.com.cn',
                    'pg': 1,
                    'ext': {'flag': 1, 'type': type}
                })

    def parse_item(self, response):
        datas = response.xpath('/html/body/div[2]/div[2]/div[3]/div[2]/div/table/tbody/tr')
        for notice in datas:
            href = notice.xpath('./td[1]/a/@onclick').extract_first()
            href = re.findall('\d+', href)
            url = urljoin(get_base_url(response), href[0] + '/' + href[1] + '.html')
            title = notice.xpath('./td[1]/a/text()').extract_first()
            publish_time = notice.xpath('normalize-space(./td[2]/text())').extract_first()

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        np = response.xpath('//li[@class="next"]/a[contains(text(),"下一页")]/@href').re_first('\d+')
        if np is not None:
            next_url = response.meta['ext']['baseUrl'] + '?pageIndex=' + np
            self.ips.append({
                'url': next_url,
                'ref': response.url,
                'ext': {'baseUrl': response.meta['ext']['baseUrl']}
            })


