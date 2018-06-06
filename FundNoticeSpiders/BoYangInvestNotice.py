# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class BoYangInvestNoticeSpider(GGFundNoticeSpider):
    name = 'FundNotice_BoYangInvestNotice'
    sitename = '博洋投资'
    entry = 'http://www.byfgroup.com/'

    ips = [{
        'url': 'http://www.byfgroup.com/news.jsp',
        'ref': 'http://www.byfgroup.com/',
        'ext': {'page': '1'}
    }]

    def parse_item(self, response):
        ext = response.meta['ext']
        page = int(ext['page'])
        total_page = response.xpath('//a[text()="最后一页"]/@href').re_first(r'pageDirect\((\d+)\)')
        if total_page is None or total_page == '':
            total_page = 0
        else:
            total_page = int(total_page)
        notices = response.xpath('//td[@class="newxxlist"]')
        years = response.xpath('//td[@class="newxxdate"]/text()').re(r'(\d+-\d+-\d+)')
        for row in notices:
            url = row.xpath('./a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            title = row.xpath('./a//text()').extract_first()
            publish_time = years.pop(0)
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time
            yield item
        if page < total_page:
            self.ips.append({
                'url': 'http://www.byfgroup.com/news.jsp',
                'form': {'page': str(page+1)},
                'ref': response.url,
                'ext': {'page': str(page+1)}
            })

