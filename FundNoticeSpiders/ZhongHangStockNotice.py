# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
import re


class ZhongHangStockNoticeSpider(GGFundNoticeSpider):
    name = 'FundNotice_ZhongHangStockNotice'
    sitename = '中航证券'
    entry = 'http://www.avicsec.com/'

    lps = [{'url': 'http://www.avicsec.com/main/invest/stockDividend/C00001/collectiveInvestment.shtml',
            'ref': 'http://www.avicsec.com/main/invest/stockDividend/index.shtml'}]

    def parse_list(self, response):
        funds = response.xpath('//*[@id="showLeft3418"]/dd/a/@href').extract()
        for fund in funds:
            url1 = 'http://www.avicsec.com/servlet/ArticlePageAction?catalogId=3445&state=3&titleLength=50&gpdm='
            url2 = 'http://www.avicsec.com/servlet/ArticlePageAction?catalogId=3444&state=3&titleLength=50&gpdm='
            gpdm = re.search(r'stockDividend\/(\S+)\/collectiveInvestment', fund).group(1)
            url1 = url1 + gpdm
            url2 = url2 + gpdm
            form = {'curPage': '1',
                    'numPerPage': '10',
                    'type': '1'}
            self.ips.append({'url': url1, 'form': form, 'ext': {'page': '1'}})
            self.ips.append({'url': url2, 'form': form, 'ext': {'page': '1'}})

    def parse_item(self, response):
        ext = response.meta['ext']
        page = int(ext['page'])
        total_page = re.search(r'pagecount\:(\d+),', response.text)
        if total_page:
            total_page = int(total_page.group(1))
        else:
            total_page = 0
        rows = response.xpath('//ul/li/a')
        for row in rows:
            title = row.xpath('./strong/text()').extract_first()
            url = row.xpath('./@href').extract_first()
            publish_time = row.xpath('./span/text()').extract_first()
            publish_time = datetime.strptime(publish_time, '%Y.%m.%d')
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = urljoin(get_base_url(response), url)
            item['title'] = title
            item['publish_time'] = publish_time
            yield item
        if page < total_page:
            form = {'curPage': str(page+1),
                    'numPerPage': '10',
                    'type': '1'}
            self.ips.append({
                'url': response.url,
                'form': form,
                'ext': {'page': str(page+1)},
                'ref': response.url
            })
