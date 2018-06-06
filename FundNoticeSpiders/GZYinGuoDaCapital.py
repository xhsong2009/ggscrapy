# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class GZYinGuoDaCapitalSpider(GGFundNoticeSpider):
    name = 'FundNotice_GZYinGuoDaCapital'
    sitename = '广州银国达资产'
    entry = 'http://www.ingoalamc.com/index.php/Article_index_navid_79_cNavid_102.html'

    ips = [
        {
            'url': 'http://www.ingoalamc.com/index.php/Article_index_navid_79_cNavid_102.html',
            'ref': None
        }
    ]

    def parse_item(self, response):
        rows = response.xpath('//ul[@class="new_list"]/li/a')
        for row in rows:
            url = row.xpath('./@href').extract_first()
            url = urljoin(get_base_url(response), url)
            publish_time = row.xpath('./div/div[1]/time/text()').re_first('\d+.\d+.\d+')
            title = row.xpath('./div/div[1]/h4/text()').extract_first()

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['title'] = title
            item['url'] = url
            item['publish_time'] = datetime.strptime(publish_time, '%Y.%m.%d')
            yield item

        next_url = response.xpath('//a[@class="next"]/@href').extract_first()
        if next_url:
            self.ips.append({
                'url': urljoin(get_base_url(response), next_url),
                'ref': None
            })
