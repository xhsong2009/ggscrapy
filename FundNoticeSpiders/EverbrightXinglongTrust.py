# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
import re


class EverbrightXinglongTrustSpider(GGFundNoticeSpider):
    name = 'FundNotice_EverbrightXinglongTrust'
    sitename = '光大兴陇信托'
    entry = 'https://www.ebtrust.com/notice.html'

    ips = [
        {
            'url': 'https://www.ebtrust.com/notice/tp/221/page/1.html',
            'ref': 'https://www.ebtrust.com/notice.html',
        },
        {
            'url': 'https://www.ebtrust.com/notice/tp/222/page/1.html',
            'ref': 'https://www.ebtrust.com/notice.html',
        },
    ]

    def parse_item(self, response):
        rows = response.xpath('//div[@class="noticeList"]/ul/li')
        for row in rows:
            title = row.xpath('./a/text()').extract_first().strip()
            url = row.xpath('./a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            publish_time = row.xpath('./span/text()').extract_first().strip()
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time
            yield item
        next_page = response.xpath("//div[@class='ims_pager']/text()").re_first('"next_page":(\d+),\s*"up_page"')
        last_page = response.xpath("//div[@class='ims_pager']/text()").re_first('"last_page":(\d+),\s*"next_page"')
        if next_page and int(next_page) < int(last_page):
            url = re.sub(r'page/\d+', 'page/' + next_page, response.url)
            self.ips.append({
                'url': url,
                'ref': response.url,
            })

