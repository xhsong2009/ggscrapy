# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from scrapy import Request


class YueHaiAssetSpider(GGFundNoticeSpider):
    name = 'FundNotice_YueHaiAsset'
    sitename = '上海岳海资产'
    entry = 'http://www.yuehaizichan.com'

    ips = [{
        'url': 'http://www.yuehaizichan.com/News_index_catid_4.html',
    }]

    def start_requests(self):
        yield Request(url='http://www.yuehaizichan.com/',
                      method='POST',
                      headers={
                          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                          'Content-Type': 'application/x-www-form-urlencoded',
                          'Referer': 'http://www.yuehaizichan.com/'},
                      callback=self.parse_login)

    def parse_login(self, response):
        yield Request(
            url='http://www.yuehaizichan.com/Index_index.html',
            headers={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
            })

    def parse_item(self, response):
        rows = response.xpath('//ul[@class="container_2 new_list clearbox"]/li/a')
        for row in rows:
            url = row.xpath('./@href').extract_first()
            url = urljoin(get_base_url(response), url)
            title = row.xpath('normalize-space(./div/h3/text())').extract_first()
            publish_time = row.xpath('normalize-space(./div/time/text())').extract_first()
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time
            yield item






















