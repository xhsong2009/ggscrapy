# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class LeruiTrustSpider(GGFundNoticeSpider):
    name = 'FundNotice_LeruiTrust'
    sitename = '乐瑞资产'
    entry = 'http://www.lowrisk.com.cn/'

    ips = [{
        'url': 'http://www.lowrisk.com.cn/plus/list.php?tid=27',
    }]

    def parse_item(self, response):  # 2 定位好后，进行解析数据
        rows = response.xpath('//div[@class="list1 clearfix"]/ul/li')

        for row in rows:
            url = row.xpath('./a/@href').extract_first()
            url = urljoin(get_base_url(response), url)

            title = row.xpath('./a/@title').extract_first()

            publish_time = row.xpath('./span/text()').extract_first().strip().replace('\t', '').replace('\r', '').replace('\n', '')  # 时间格式
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time
            yield item

        next_url = response.xpath('//div[@class="page"]/a[text()="下一页"]/@href').extract_first()
        if next_url:
            next_url = urljoin(get_base_url(response), next_url)
            self.ips.append({
                'url': next_url,
                'ref': response.url
            })
