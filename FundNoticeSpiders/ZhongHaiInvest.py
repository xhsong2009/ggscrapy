# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class ZhongHaiInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_ZhongHaiInvest'
    sitename = '中海信托'
    entry = 'http://www.zhtrust.com/product/index.shtml'

    lps = [
        {
            'url': 'http://www.zhtrust.com/front/fund/Product/findProductBySearch.do?gotoPage=1',
            'pg': 1
        }
    ]

    def parse_list(self, response):
        rows = response.xpath('//div[@class="pan"]/h4/a')
        for row in rows:
            fund_code = row.xpath('./@href').re_first('fundcode=([^/]+)')
            self.ips.append({
                'url': 'http://www.zhtrust.com/front/fund/Product/findProductArticle.do?gotoPage=1&fundcode={0}'.format(fund_code),
                'ref': response.url,
                'pg': 1,
                'ext': {'fund_code': fund_code}
            })
        tp = int(response.xpath('//div[@class="page"]/ul/li/text()').re_first('共\d+/(\d+)页'))
        pg = response.meta['pg'] + 1
        if pg <= tp:
            self.lps.append({
                'url': 'http://www.zhtrust.com/front/fund/Product/findProductBySearch.do?gotoPage={0}'.format(pg),
                'ref': response.url,
                'pg': pg
            })

    def parse_item(self, response):
        rows = response.xpath('//li[@class="glist"]')
        if rows:
            for row in rows:
                url = row.xpath('./a/@href').extract_first()
                url = urljoin(get_base_url(response), url)
                title = row.xpath('./a/text()').extract_first().strip()
                publish_time = row.xpath('./span/text()').re_first('\d+-\d+-\d+')

                item = GGFundNoticeItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url_entry'] = self.entry
                item['url'] = url
                item['title'] = title
                item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
                yield item

            ext = response.meta['ext']
            fund_code = ext['fund_code']
            tp = int(response.xpath('//div[@class="page"]/ul/li/text()').re_first('共\d+/(\d+)页'))
            pg = response.meta['pg'] + 1
            if pg <= tp:
                self.ips.append({
                    'url': 'http://www.zhtrust.com/front/fund/Product/findProductArticle.do?gotoPage={0}&fundcode={1}'.format(pg, fund_code),
                    'ref': response.url,
                    'pg': pg,
                    'ext': {'fund_code': fund_code}
                })
