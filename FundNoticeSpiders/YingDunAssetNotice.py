# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url


class YingDunAssetNoticeSpider(GGFundNoticeSpider):
    name = 'FundNotice_YingDunAssetNotice'
    sitename = '盈盾资本'
    entry = 'http://www.profitshields.cn/'

    ips = [{'url': 'http://www.profitshields.com/html/news/gongsi/list_1.html',
            'ref': 'http://www.profitshields.com/index.html',
            'ext': {'page': '1'}}]

    def parse_item(self, response):
        next_url = response.xpath('/html/body/div[3]//ul[@class="pagelist"]/li/a[text()="下一页"]/@href').extract_first()
        rows = response.xpath('/html/body/div[3]//div[@class="xinwen"]/dl/dt')
        for row in rows:
            title = row.xpath('./a/text()').extract_first()
            url = row.xpath('./a/@href').extract_first()
            publish_time = row.xpath('./span/text()').extract_first()
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = urljoin(get_base_url(response), url)
            item['title'] = title
            item['publish_time'] = publish_time
            yield item
        if next_url:
            next_url = urljoin(get_base_url(response), next_url)
            self.ips.append({
                'url': next_url,
                'ref': response.url
            })
