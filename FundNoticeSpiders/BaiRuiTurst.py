# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class BaiRuiTurstSpider(GGFundNoticeSpider):
    name = 'FundNotice_BaiRuiTurst'
    sitename = '百瑞信托'
    entry = 'http://www.brxt.net/product.php?fid=29&fup=3&pid=0&pageid=1'

    ips = [{
        'url': 'http://www.brxt.net/product.php?fid=29&fup=3&pid=0&pageid=1',
    }]

    def parse_item(self, response):
        rows = response.css('.proTable table tr')[1:]
        for row in rows:
            url = row.xpath('./td[1]/a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            title = row.xpath('./td[1]/a/text()').extract_first()
            publish_time = row.xpath('./td[3]/text()').re_first(r'(\d+-\d+-\d+)')
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time
            yield item
        next_url = response.xpath('//a[text()=">"]/@href').extract_first()
        if next_url:
            self.ips.append({
                'url': urljoin(get_base_url(response), next_url),
                'ref': response.url
            })
