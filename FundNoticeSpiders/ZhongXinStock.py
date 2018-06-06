# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
import json


class ZhongXinStockSpider(GGFundNoticeSpider):
    name = 'FundNotice_ZhongXinStock'
    sitename = '中信证券'
    entry = 'http://www.cs.ecitic.com/'
    allowed_domains = ['www.eagle-fund.com/']

    ips = [{'url': 'http://www.cs.ecitic.com/finance/dynamicInfor.jsp?notifyType=_product_report&type=4',
            'ext': {'report_type': '1'}}]
    lps = [{'url': 'http://www.cs.ecitic.com/productInfo.do?method=getProduct', 'form': {'type': '1'}}]

    def parse_list(self, response):
        funds = json.loads(response.text)
        if funds:
            funds = funds['list']
            base_url1 = 'http://www.cs.ecitic.com/finance/prodListIframe.jsp?whichCat=_product_report&pageno=1&product_id='
            base_url2 = 'http://www.cs.ecitic.com/finance/prodListIframe.jsp?whichCat=_periodical_report&product_id='
            for fund in funds:
                fund_id = fund['productCode']
                url1 = base_url1 + str(fund_id)
                url2 = base_url2 + str(fund_id)
                self.ips.append({'url': url1, 'ref':response.url, 'ext': {'report_type': '2'}})
                self.ips.append({'url': url2, 'ref': response.url, 'ext': {'report_type': '2'}})

    def parse_item(self, response):
        ext = response.meta['ext']
        report_type = int(ext['report_type'])
        if report_type == 1:
            rows = response.xpath('/html/body/div[2]/div[2]//div[@class="rightdiv_n"]/ul/li')
            next_url = response.xpath('//*[@id="page"]/div[2]/ul/a[last()]/@href').extract_first()
        else:
            rows = response.xpath('//li')
            next_url = response.xpath('//*[@id="page"]//a[text()="下一页"]/@href').extract_first()
        for row in rows:
            url = row.xpath('./a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            title = row.xpath('./a//text()').extract_first().strip()
            publish_time = row.xpath('./span/text()').extract_first()
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time
            yield item
        if next_url and next_url != 'javascript:void(0);':
            next_url = urljoin(get_base_url(response), next_url)
            self.ips.append({
                'url': next_url,
                'ref': response.url,
                'ext': {'report_type': str(report_type)}
            })
