# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy import Request
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class YingXueInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_YingXueInvest'
    sitename = '映雪投资'
    entry = 'http://www.snowlightcapital.cn/'

    username = '13916427906'
    password = 'ZYYXSM123'

    ips = [
        {
            'url': 'http://www.snowlightcapital.cn/moreNews',
            'ref': 'http://www.snowlightcapital.cn/',
            'pg': 1
        }
    ]

    def start_requests(self):
        yield Request(url='http://www.snowlightcapital.cn/getUserLogin?cellphone=13916427906&pwd=ZYYXSM&saveRank=Y&randnum=0.8588240370783373',

                      )

    def parse_item(self, response):
        rows = response.xpath('//div[@class="snowview_bot"]/ul/li')
        for row in rows:
            title = row.xpath('./a/text()').extract_first()
            url = row.xpath('./a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            publish_time = row.xpath('./span/text()').extract_first()

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['title'] = title
            item['url'] = url
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        tp = response.xpath('//div[@class="left tx_fye"]/a[contains(text(),"末页")]').re_first('\d+')
        pg = response.meta['pg']
        if pg < int(tp):
            pg = pg+1
            next_url = 'http://www.snowlightcapital.cn/moreNews?pageNum=' + tp + '&pageNo=' + str(pg)
            self.ips.append({
                'url': next_url,
                'ref': response.url,
                'pg': pg
            })
