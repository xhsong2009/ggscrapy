# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class YueCaiInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_YueCaiInvest'
    sitename = '粤财信托'
    entry = 'http://www.utrusts.com/product/list_15.html'

    lps = [
        {
            'url': 'http://www.utrusts.com/product/list_15.html'
        }
    ]

    def parse_list(self, response):
        rows = response.xpath('//ul[@class="ul gg_ul"]/li/a')
        for row in rows:
            url = row.xpath('./@href').extract_first()
            self.ips.append({
                'url': urljoin(get_base_url(response), url),
                'ref': response.url
            })

    def parse_item(self, response):
        rows = response.xpath('//ul[@class="prod_ul"]/li')
        for row in rows:
            url = row.xpath('./a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            title = row.xpath('./a/text()').extract_first()
            publish_time = row.xpath('./span/text()').re_first('\d+-\d+-\d+')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        next_url = response.xpath('//a[@class="a_next"]/@href').extract_first()
        if 'javascript:void(0);' != next_url:
            self.ips.append({
                'url': urljoin(get_base_url(response), next_url),
                'ref': response.url
            })
