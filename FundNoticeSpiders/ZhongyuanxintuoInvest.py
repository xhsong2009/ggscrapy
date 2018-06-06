# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class ZhongyuanxintuoInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_ZhongyuanxintuoInvest'
    sitename = '中原信托'
    entry = 'http://www.zyxt.com.cn/product.php?fid=25&fup=3&pageid=1'

    ips = [{
        'url': 'http://www.zyxt.com.cn/product.php?fid=25&fup=3&pageid=1',
    }]

    def parse_item(self, response):
        rows = response.xpath('//ul[@class="jList fadeUp"]/li')

        for row in rows:
            url = row.xpath('./a[1]/@href').extract_first()
            url = urljoin(get_base_url(response), url)

            title = row.xpath('./a[1]/text()').extract_first()

            publish_time = row.xpath('./a[2]/text()').extract_first()
            if publish_time == str('0201-12-24'):  # 特殊情况存在： #网页时间格式有错误： 0201-12-24
                publish_time = str('2010-12-24')
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time

            yield item

        next_url = response.xpath('//div[@class="pages fadeUp"]/a[text()=">"]/@href').extract_first()
        if next_url:
            next_url = urljoin(get_base_url(response), next_url)
            self.ips.append({
                'url': next_url,
                'ref': response.url
            })
        yield self.request_next()
