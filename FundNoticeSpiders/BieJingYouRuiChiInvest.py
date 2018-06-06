# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
import json


class BieJingYouRuiChiInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_BieJingYouRuiChiInvest'
    sitename = '北京佑瑞持投资'
    entry = 'http://www.urich.cn/'
    ips = [{
        'url': 'http://www.urich.cn/news.asp?page=1',
        'ref': 'http://www.urich.cn/',
        'ext': {'page': '1'}
    }]

    def parse_item(self, response):
        ext = response.meta['ext']
        page = int(ext['page'])
        total_page = int(response.xpath('//div[@class="digg"]/a[text()=">"]/@href').re_first(r'page=(\d+)'))
        notices = response.xpath('//td[@class="newslist"]')
        years = response.xpath('//td[@class="newslist2"]/text()').extract()
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
                'url': 'http://www.urich.cn/news.asp?page='+str(page+1),
                'ref': response.url,
                'ext': {'page': str(page+1)}
            })

