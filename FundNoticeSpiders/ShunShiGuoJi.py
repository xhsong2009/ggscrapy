# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class ShunShiGuoJiSpider(GGFundNoticeSpider):
    name = 'FundNotice_ShunShiGuoJi'
    sitename = '顺时国际'
    entry = 'http://www.timewise.com.cn/website/w/h?mt=2&mc=3665612&cc=1519602'

    ips = [
        {
            'url': 'http://www.timewise.com.cn/website/w/h?mt=2&mc=3665612&cc=1519602',
            'pg': 0
        }
    ]

    def parse_item(self, response):
        rows = response.xpath('//div[@class="simu-site-list"]/ul/a')
        for row in rows:
            click_url = row.xpath('./@clickurl').extract_first()
            href = urljoin(get_base_url(response), row.xpath('./@href').extract_first())
            url = click_url if click_url is not '' else href
            title = row.xpath('./li/div[@class="simu-site-right"]/div[1]/text()').extract_first().strip()
            publish_time = row.xpath('./li/div[@class="simu-site-right"]/div[3]/div[2]/text()').re_first('\d+-\d+-\d+')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        tp = int(response.xpath('//div[@class="simu-site-pagination"]/ul/li[last()]/a[contains(text(),"末页")]/@href').re_first('paging&c=(\d+)'))
        pg = response.meta['pg'] + 1
        if pg <= tp:
            self.ips.append({
                'url': 'http://www.timewise.com.cn/website/w/h?mt=2&mc=3665612&cc=1519602&fp=paging&c={0}'.format(pg),
                'ref': response.url,
                'pg': pg
            })
