# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url


class YinLiAssetSpider(GGFundNoticeSpider):
    name = 'FundNotice_YinLiAsset'
    sitename = '银莅资产'
    entry = 'http://www.ylzcgl.com'
    cookies = 'cookie_authState=1'
    ips = [{'url': 'http://www.ylzcgl.com/news1.asp'}]

    def parse_item(self, response):
        next_url = response.xpath('/html/body/table[2]//div[@class="xianshi"]//a[text()="下一页"]/@href').extract_first()
        rows = response.xpath('/html/body/table[2]//div[@class="xianshi"]/table//tr')
        for row in rows:
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            title = row.xpath('./td[2]/a/text()').extract_first()
            url = row.xpath('./td[2]/a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            publish_time = row.xpath('./td[3]/text()').extract_first()
            publish_time = datetime.strptime(publish_time, '%Y/%m/%d')
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time
            yield item
        if next_url:
            next_url = urljoin(get_base_url(response), next_url)
            self.ips.append({'url': next_url, 'ref': response.url})

