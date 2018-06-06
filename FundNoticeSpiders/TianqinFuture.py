# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class TianqinFutureSpider(GGFundNoticeSpider):
    name = 'FundNotice_TianqinFuture'
    sitename = '天勤资产'
    entry = 'http://www.tianqinassets.com/'

    ips = [{
        'url': 'http://www.tianqinassets.com/index.php?catid=2&page=1',
    }]

    def parse_item(self, response):
        rows = response.xpath('//ul[@class="noborder"]/li')

        for row in rows:
            url = row.xpath('./a/@href').extract_first()
            url = urljoin(get_base_url(response), url)

            title = row.xpath('./a/text()').extract_first().replace('\t', '').replace('\r', '').replace('\n', '')

            publish_time = row.xpath('./span/text()').extract_first()
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time

            yield item

        next_url = response.xpath('//div[@class="xiaocms-page"]/a[contains(text(),"下一页")]/@href').extract_first()
        if next_url:
            next_url = urljoin(get_base_url(response), next_url)
            self.ips.append({
                'url': next_url,
                'ref': response.url
            })
