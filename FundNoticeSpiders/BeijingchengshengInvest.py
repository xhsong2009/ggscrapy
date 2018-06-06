# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class BeijingchengshengInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_BeijingchengshengInvest'
    sitename = '北京诚盛投资'
    entry = 'http://www.chengshengtouzi.com/'
    cookies = 'JSESSIONID=9C21EA55E3DCD99460B24F0A85BE18F4; cookie_3962264_authState=1; companyCode=3962264; telephone=""; configCode=4048628; isRealHost=1'

    ips = [{
        'url': 'http://www.chengshengtouzi.com/website/w/h?mt=2&mc=4095037&cc=3962264&fp=paging&c=0',
    }]

    def parse_item(self, response):
        rows = response.xpath('//div[@class="list-box"]/a')
        for row in rows:
            url = row.xpath('./@href').extract_first()
            url = urljoin(get_base_url(response), url)

            title = row.xpath('./div/div/div[2]/div[1]/text()').extract_first().strip().replace('\t', '').replace('\r', '').replace('\n', '')

            publish_time = row.xpath('./div/div/div[1]/div/div[2]/text()').extract_first().strip().replace('\t', '').replace('\r', '').replace('\n', '')
            publish_time = datetime.strptime(publish_time, '%Y-%m')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time
            yield item

        next_url = response.xpath('//div[@class="simu-site-pagination"]/ul/li/a[contains(text(),"下一页")]/@href').extract_first()
        if next_url != 'javascript:;':
            next_url = urljoin(get_base_url(response), next_url)
            self.ips.append({
                'url': next_url,
                'ref': response.url
            })
        yield self.request_next()











