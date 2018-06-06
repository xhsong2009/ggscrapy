# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class JinbailingFutureSpider(GGFundNoticeSpider):
    name = 'FundNotice_JinbailingFuture'
    sitename = '江苏金百灵资产'
    entry = 'http://www.jblfund.com/'

    ips = [{
        'url': 'http://www.jblfund.com/About/Index/gsgg',#定位到数据详情页面
    }]

    def parse_item(self, response):
        rows = response.xpath('//ul[@class="list2"]/li')
        for row in rows:
            url = row.xpath('./a/@href').extract_first()
            url = urljoin(get_base_url(response), url)

            title = row.xpath('./a/text()').extract_first().strip().replace('\t', '').replace('\r', '').replace('\n', '')#标题

            publish_time = row.xpath('./span/text()').re_first(r'(\d+-\d+-\d+)')#时间格式,进行限制来提取(时间用 - 进行连接) , 如： <span>2018-3-7 0</span>
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time
            yield item
