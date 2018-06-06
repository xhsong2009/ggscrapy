# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class RongtongFutureSpider(GGFundNoticeSpider):
    name = 'FundNotice_RongtongFuture'
    sitename = '融通资本'
    entry = 'http://www.rtcapital.cn/'

    ips = [{
        'url': 'http://www.rtcapital.cn/',
    }]

    def parse_item(self, response):
        ext = response.meta['ext']
        if 'one' in ext:
            url = ext['url']
            title = ext['title']
            publish_time = response.xpath('//div[@class="blog-post"]/ul/li[1]/text()').extract_first().strip().replace('\t', '').replace('\r', '').replace('\n', '')  # 时间格式
            publish_time = publish_time[5:15]
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry

            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time

            yield item

        else:

            urlOne = response.xpath('//div[@id="tab6"]/dl/dd/h5/a/@href').extract_first()
            urlOne = urljoin(get_base_url(response), urlOne)

            titleOne = response.xpath('//div[@id="tab6"]/dl/dd/h5/a/text()').extract_first().strip().replace('\t', '').replace('\r', '').replace('\n', '')
            publish_timeOne = ''

            if publish_timeOne == '' or publish_timeOne is None:
                self.ips.append({
                    'url': 'http://www.rtcapital.cn/product/cpgg/qsbg/857.html',
                    'ext': {'one': '1', 'url': urlOne, 'title': titleOne}
                })

            rows = response.xpath('//div[@id="tab6"]/div/ul/li')

            for row in rows:
                url = row.xpath('./a/@href').extract_first()
                url = urljoin(get_base_url(response), url)

                title = row.xpath('./a/text()').extract_first().strip().replace('\t', '').replace('\r', '').replace('\n', '')

                publish_time = row.xpath('./span/text()').extract_first().strip().replace('\t', '').replace('\r', '').replace('\n', '')
                publish_time = publish_time[0:10]
                publish_time = datetime.strptime(publish_time, '%Y-%m-%d')
                item = GGFundNoticeItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url_entry'] = self.entry
                item['url'] = url
                item['title'] = title
                item['publish_time'] = publish_time
                yield item
