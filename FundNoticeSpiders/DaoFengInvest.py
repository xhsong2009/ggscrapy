# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class DaoFengInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_DaoFengInvest'
    sitename = '上海稻沣投资'
    entry = 'http://www.daofengfund.com'
    proxy = 1
    lps = [
        {
            'url': 'http://www.daofengfund.com/website/w/h?mt=2&mc=60148&cc=54902',
            'ref': None
        }
    ]

    def parse_list(self, response):
        noticeList = response.xpath('//div[@class="simu-site-list"]/ul/a')

        for notice in noticeList:
            noticeLink = notice.xpath('./@href').extract_first().strip()
            noticeLink = urljoin(get_base_url(response), noticeLink)
            title = notice.xpath('normalize-space(./li/div/div[1]/text())').extract_first()
            publish_time = notice.xpath('./li/div/div[3]/div[2]/text()').extract_first()

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = noticeLink
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        # next_url = response.xpath('//a[contains(text(), "下一页")]/@href').extract_first()
        # if next_url != None:
        #     self.lps.append({'url': urljoin(get_base_url(response), next_url), 'ref': response.url})
