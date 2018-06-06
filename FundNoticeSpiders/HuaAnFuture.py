# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class HuaAnFutureSpider(GGFundNoticeSpider):
    name = 'FundNotice_HuaAnFuture'
    sitename = '华安期货'
    entry = 'http://www.haqh.com/index.php?m=content&c=index&a=lists&catid=132'

    ips = [
        {
            'url': 'http://www.haqh.com/index.php?m=content&c=index&a=lists&catid=132',
            'pg': 1
        }
    ]

    def parse_item(self, response):
        rows = response.xpath('//table[@class="newstable"]/tr')[1:]
        for row in rows:
            url = row.xpath('./td[1]/a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            title = row.xpath('./td[1]/a/@title').extract_first()
            publish_time = row.xpath('./td[2]/text()').re_first('\d+-\d+-\d+')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        count = int(response.xpath('//div[@id="pages"]/a[@class="a1"]/text()').re_first('\d+'))
        tp = count / 25 if count % 25 == 0 else count // 25 + 1
        pg = response.meta['pg'] + 1
        if pg <= tp:
            self.ips.append({
                'url': 'http://www.haqh.com/index.php?m=content&c=index&a=lists&catid=132&page={0}'.format(pg),
                'ref': response.url,
                'pg': pg
            })
