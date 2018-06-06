# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class FangZhengDongYaXinTuoSpider(GGFundNoticeSpider):
    name = 'FundNotice_FangZhengDongYaXinTuo'
    sitename = '方正东亚信托'
    entry = 'http://www.gt-trust.com/'

    lps = [{
        'url': 'http://www.gt-trust.com/index.php/index-show-tid-16.html',
    }]

    def parse_list(self, response):
        notice_types = response.xpath('//div[@class="ny_tit_box"]/a/@href').extract()
        for notice_type in notice_types:
            if 'tid-18' not in notice_type:
                url = urljoin(get_base_url(response), notice_type)
                self.ips.append({'url': url, 'ref': response.url})

    def parse_item(self, response):
        rows = response.css('.pro_list ul li')
        next_url = response.xpath('//a[@class="page_right"]/@href').extract_first()
        for row in rows:
            url = row.xpath('./h1/a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            title = row.xpath('./h1/a/text()').extract_first()
            publish_time = row.xpath('./span/text()').re_first(r'(\d+-\d+-\d+)')
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time
            yield item
        if next_url:
            next_url = urljoin(get_base_url(response), next_url)
            self.ips.append({
                'url': next_url,
                'ref': response.url
            })
