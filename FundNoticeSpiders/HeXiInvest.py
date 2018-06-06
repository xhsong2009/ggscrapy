# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class HeXiInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_HeXiInvest'
    sitename = '和熙投资'
    entry = 'http://www.hexifund.com/info.php?class_id=102102'

    ips = [
        {
            'url': 'http://www.hexifund.com/info.php?class_id=102102',
            'pg': 1
        }
    ]

    def parse_item(self, response):
        rows = response.xpath('//div[@class="news01"]/ul/li')
        for row in rows:
            url = row.xpath('./div[@class="p2"]/a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            title = row.xpath('./div[@class="p2"]/a/text()').extract_first()
            publish_time = '2018-' + row.xpath('./div[@class="p1"]/text()').re_first('\d+-\d+')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        tp = response.xpath('//div[@class="page"]/span/a[contains(text(),"尾页")]/@href').re_first('page=(\d+)')
        if tp:
            pg = response.meta['pg'] + 1
            if pg <= int(tp):
                self.ips.append({
                    'url': 'http://www.hexifund.com/info.php?class_id=102102&page={0}'.format(pg),
                    'ref': response.url,
                    'pg': pg
                })
