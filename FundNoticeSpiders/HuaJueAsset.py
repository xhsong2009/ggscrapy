# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin


class HuaJueAssetSpider(GGFundNoticeSpider):
    name = 'FundNotice_HuaJueAsset'
    sitename = '北京华觉资产'
    entry = 'http://huajue.cn.com/'

    ips = [
        {
            'url': 'http://huajue.cn.com/index.php?m=content&c=index&a=lists&catid=22',
            'ref': 'http://huajue.cn.com/index.asp',
            'pg': 1
        }
    ]

    def parse_item(self, response):
        datas = response.xpath('//div[@class="news_title"]')
        for notice in datas:
            href = notice.xpath('./a/@href').extract_first()
            title = notice.xpath('./a/text()').extract_first()
            publish_time = notice.xpath('./span/text()').extract_first()

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = href
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        next_url = response.xpath('//div[@id="pages"]/a[contains(text(), "下一页")]/@href').extract_first()
        next_url = urljoin(get_base_url(response), next_url)
        if next_url is not None and next_url != response.url:
            self.ips.append({'url': next_url, 'ref': response.url})


