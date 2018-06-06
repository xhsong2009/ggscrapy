# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class YiFangBoInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_YiFangBoInvest'
    sitename = '浙江亿方博投资'
    entry = 'http://www.yfbtz.com/news.asp'

    ips = [
        {
            'url': 'http://www.yfbtz.com/news.asp',
            'pg': 1
        }
    ]

    def parse_item(self, response):
        rows = response.xpath('//div[@class="newconall"]')
        for row in rows:
            url = row.xpath('./div[2]/a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            title = row.xpath('./div[2]/a/text()').extract_first()
            publish_time = row.xpath('./div[3]/text()').re_first('\d+-\d+-\d+')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        count = int(response.xpath('//div[@class="newconnext"]/script[2]/text()').re_first('Cls_jsPage\(([\d]+)'))
        tp = int(count / 15 if count % 15 == 0 else count // 15 + 1)
        pg = response.meta['pg'] + 1
        if pg <= tp:
            self.ips.append({
                'url': 'http://www.yfbtz.com/news.asp?Pages={0}'.format(pg),
                'ref': response.url,
                'pg': pg
            })
