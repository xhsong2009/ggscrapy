# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin


class HaoenInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_HongChengInvest'
    sitename = '泓澄投资'
    entry = 'http://www.hccapital.com.cn/'

    lps = [
        {
            'url': 'http://www.hccapital.com.cn/notice.jsp',
            'ref': 'http://www.hccapital.com.cn/notice.jsp',
            'form': {
                'method': 'checkin'
            },
            'ext': {'flag': 0}
        }
    ]

    def parse_list(self, response):
        flag = response.meta['ext']['flag']
        if flag == 0:
            self.lps.append({
                'url': 'http://www.hccapital.com.cn/list/41.html',
                'ref': response.url,
                'ext': {'flag': 1}
            })
        else:
            urls = response.xpath('//ul[@class="news-list"]/li/a')
            for url in urls:
                href = url.xpath('./@href').extract_first()
                title = url.xpath('./h5/text()').extract_first()
                link = urljoin(get_base_url(response), href)
                self.ips.append({
                    'url': link,
                    'ref': response.url,
                    'ext': {'title': title, 'url': link}
                })

        next_url = response.xpath('//div[@id="pager"]/ul/li/a[contains(text(), "»")]/@href').extract_first()
        if next_url is not None and urljoin(get_base_url(response), next_url) != response.url:
            self.lps.append({
                'url': urljoin(get_base_url(response), next_url),
                'ref': response.url,
                'ext': {'flag': 1}
            })

    def parse_item(self, response):
        publish_time = response.xpath('//div[@class="detail_title"]/p').re_first('\d+-\d+-\d+')
        title = response.meta['ext']['title']
        url = response.meta['ext']['url']

        item = GGFundNoticeItem()
        item['sitename'] = self.sitename
        item['channel'] = self.channel
        item['url_entry'] = self.entry
        item['url'] = url
        item['title'] = title
        item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
        yield item



