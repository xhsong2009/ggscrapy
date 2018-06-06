# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class AnHuiXiangHaiAssetNoticeSpider(GGFundNoticeSpider):
    name = 'FundNotice_AnHuiXiangHaiAssetNotice'
    sitename = '安徽翔海资产'
    entry = 'http://www.xianghaizg.com/'

    ips = [{
        'url': 'http://www.xianghaizg.com/a/chanpinjingzhi/shouyigonggao/',
    }]

    def parse_item(self, response):
        title = response.xpath('//div[@class="picnews"]/div[1]/span/strong/span/text()').extract_first()
        url = response.url
        item = GGFundNoticeItem()
        item['sitename'] = self.sitename
        item['channel'] = self.channel
        item['url_entry'] = self.entry
        item['url'] = url
        item['title'] = title
        publish_time = datetime.strptime('2017-01-26', '%Y-%m-%d')
        item['publish_time'] = publish_time
        yield item
