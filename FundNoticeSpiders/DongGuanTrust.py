# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class DongGuanTrustSPider(GGFundNoticeSpider):
    name = 'FundNotice_DongGuanTrust'
    sitename = '东莞信托'
    entry = 'http://www.dgxt.com/searchContent.jspx'

    lps = [
        {
            'url': 'http://www.dgxt.com/searchContent.jspx'
        }
    ]

    def parse_list(self, response):
        rows = response.xpath('//ul[@class="cunb_list"]/li')
        for row in rows:
            url = row.xpath('./a/@href').extract_first()
            self.ips.append({
                'url': urljoin(get_base_url(response), url),
                'ref': response.url
            })

    def parse_item(self, response):
        rows = response.xpath('//ul[@class="xcpl"]/li[not(@class)]')
        for row in rows:
            url = row.xpath('./span[@class="xmcn_ry"]/a/@href').extract_first()
            if 'javascript:void(0);' != url:
                url = urljoin(get_base_url(response), url)
            else:
                # 加密公告取当前所在页面地址
                url = response.url
            title = row.xpath('./span[@class="xmcn_ry"]/a/text()').extract_first()
            publish_time = row.xpath('./span[@class="xmcn_njy"]/text()').re_first('\d+-\d+-\d+')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        next_url = response.xpath('//div[@class="pages"]/a[contains(text(),"下一页")]/@href').extract_first()
        if 'javascript:void(0);' != next_url:
            self.ips.append({
                'url': urljoin(get_base_url(response), next_url),
                'ref': response.url
            })
