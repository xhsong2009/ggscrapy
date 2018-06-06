# -*- coding: utf-8 -*-

from urllib.parse import urljoin
from datetime import datetime
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class ZhongYinGuoJiSpider(GGFundNoticeSpider):
    name = 'FundNotice_ZhongYinGuoJi'
    sitename = '中银国际'
    entry = 'http://www.bocichina.com/boci/asset/mfinancing/productIntro.jsp?productCode=A80001&forthMenu=qtcd_asset_jhlc_one_cpjj&secondMenu=qtcd_asset_jhlc'

    lps = [
        {
            'url': 'http://www.bocichina.com/boci/asset/mfinancing/productIntro.jsp?productCode=A80001&forthMenu=qtcd_asset_jhlc_one_cpjj&secondMenu=qtcd_asset_jhlc'
        }
    ]

    ips = [
        {
            'url': 'http://www.bocichina.com/boci/asset/cms/commonNewsList.jsp?productCode=A80001&whichCat=zcgl_jhlc_cpgg&state=1&showSize=20&catName=产品公告',
            'pg': 1,
            'ext': {'product_code': 'A80001'}
        }
    ]

    def parse_list(self, response):
        rows = response.xpath('//table[@class="border1"]/tr/td/a')[1:]
        for row in rows:
            product_code = row.xpath('./@onclick').re_first('productCode=([^/]+)\', \'q')
            self.ips.append({
                'url': 'http://www.bocichina.com/boci/asset/cms/commonNewsList.jsp?productCode={0}&whichCat=zcgl_jhlc_cpgg&state=1&showSize=20&catName=产品公告'.format(product_code),
                'ref': response.url,
                'pg': 1,
                'ext': {'product_code': product_code}
            })

    def parse_item(self, response):
        ext = response.meta['ext']
        product_code = ext['product_code']
        rows = response.xpath('//body/table[1]/tr')
        if rows:
            for row in rows:
                title = row.xpath('./td[1]/a/text()').re_first('・([^/]+)')
                url = row.xpath('./td[1]/a/@href').extract_first()
                url = urljoin(get_base_url(response), url)
                publish_time = row.xpath('./td[2]/text()').re_first('\d+-\d+-\d+')

                item = GGFundNoticeItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url_entry'] = self.entry
                item['title'] = title
                item['url'] = url
                item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
                yield item

            count = response.xpath('//td[@class="float_left"]/a')[-1].xpath('./@href').re_first('totalCount=([\d]+)')
            if count is not None:
                pg = response.meta['pg'] + 1
                tp = int(response.xpath('//td[@class="float_left"]/a')[-1].xpath('./@href').re_first('pageno=([\d]+)'))
                if pg <= tp:
                    self.ips.append({
                        'url': 'http://www.bocichina.com/boci/asset/cms/commonNewsList.jsp?state=1&whichCat=zcgl_jhlc_cpgg&productCode={0}&totalCount={1}&pageShowSize=20&pageno={2}'.format(product_code, count, pg),
                        'ref': response.url,
                        'pg': pg,
                        'ext': {'product_code': product_code, 'count': count}
                    })
