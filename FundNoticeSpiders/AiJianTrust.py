# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class AiJianTrustSpider(GGFundNoticeSpider):
    name = 'FundNotice_AiJianTrust'
    sitename = '爱建信托'
    entry = 'http://www.ajxt.com.cn/ajxt/gywm/cpgg/'
    proxy = 5
    ips = [
        {
            'url': 'http://www.ajxt.com.cn/ajxt/gywm/cpgg/',
            'pg': 1
        }
    ]

    def parse_item(self, response):
        rows = response.xpath('//div[@class="cont_rig"]/ul/li')
        for row in rows:
            url = row.xpath('./a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            title = row.xpath('./a/span[@class="title"]/text()').extract_first()
            publish_time = row.xpath('./a/span[@class="time"]/text()').re_first('\d+-\d+-\d+')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        tp = response.xpath('//script/text()').re_first('var PAGE_COUNT =  (\d+)')
        if tp:
            pg = response.meta['pg'] + 1
            if pg <= int(tp):
                self.ips.append({
                    'url': 'http://www.ajxt.com.cn/ajxt/gywm/cpgg/index_{0}.shtml?page={1}'.format(pg - 1, pg),
                    'ref': response.url,
                    'pg': pg
                })
