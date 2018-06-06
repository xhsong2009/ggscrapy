# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class WuXiZhiXinInvestSPider(GGFundNoticeSpider):
    name = 'FundNotice_WuXiZhiXinInvest'
    sitename = '无锡智信投资'
    entry = 'http://www.zxwealth.com.cn/gsdt'

    ips = [
        {
            'url': 'http://www.zxwealth.com.cn/gsdt',
            'pg': 1
        }
    ]

    def parse_item(self, response):
        rows = response.xpath('//div[@class="newslist"]/ul/li')
        for row in rows:
            url = row.xpath('./a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            title = row.xpath('./a/text()').extract_first()
            publish_time = row.xpath('./span/text()').re_first('\d+-\d+-\d+')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        tp = int(response.xpath('//div[@class="pagenavi"]/a[contains(text(),"尾页")]/@href').re_first('page/(\d+)'))
        pg = response.meta['pg'] + 1
        if pg <= tp:
            self.ips.append({
                'url': 'http://www.zxwealth.com.cn/gsdt/page/{0}'.format(pg),
                'ref': response.url,
                'pg': pg
            })
