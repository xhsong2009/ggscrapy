# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class BeiJingGuoJiTrustNoticeSpider(GGFundNoticeSpider):
    name = 'FundNotice_BeiJingGuoJiTrustNotice'
    sitename = '北京国际信托'
    entry = 'https://www.bjitic.com/'

    ips = [{
        'url': 'https://www.bjitic.com/news-54.html',
    }]

    def parse_item(self, response):
        rows = response.xpath('//*[@id="discover"]//div[@class="newslist"]/ul/li')
        next_url = response.xpath('//*[@id="discover"]/div[1]//a[text()="下一页"]/@href').extract_first()
        last_url = response.xpath('//*[@id="discover"]/div[1]//a[text()="末页"]/@href').extract_first()
        for row in rows:
            url = row.xpath('./div[2]/h3/a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            title = row.xpath('./div[2]/h3/a/text()').extract_first()
            publish_year = row.xpath('./div[1]/span[2]/text()').extract_first()
            publish_day = row.xpath('./div[1]/span[1]/text()').extract_first()
            publish_time = str(publish_year) + '-' + str(publish_day)
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time
            yield item
        if next_url and next_url != last_url:
            next_url = urljoin(get_base_url(response), next_url)
            self.ips.append({
                'url': next_url,
                'ref': response.url
            })
