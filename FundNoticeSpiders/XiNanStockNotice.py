# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class XiNanStockNoticeSpider(GGFundNoticeSpider):
    name = 'FundNotice_XiNanStockNotice'
    sitename = '西南证券'
    entry = 'http://www.swsc.com.cn/'

    lps = [{'url': 'http://www.swsc.com.cn/xnsecu/cpzx/jhlc.jsp?classid=0001000100120011'}]

    def parse_list(self, response):
        funds = response.xpath('/html/body/div[3]//div[@class="cl_cats"]/ul/li/a/@title').extract()
        base_url = 'http://www.swsc.com.cn/xnsecu/cpzx/server/jhlc.jsp?channelid='
        for channel_id in funds:
            for show_num in [4, 5, 6]:
                url = base_url + channel_id + '&shownum=' + str(show_num)
                self.ips.append({'url': url, 'ref': response.url})

    def parse_item(self, response):
        rows = response.css('.flwj dd')
        for row in rows:
            url = row.xpath('./a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            title = row.xpath('./a//text()').extract_first().strip()
            publish_time = row.xpath('./span/text()').extract_first().strip()
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time
            yield item

