# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
import json
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url


class YinHeStockNoticeSpider(GGFundNoticeSpider):
    name = 'FundNotice_YinHeStockNotice'
    sitename = '银河金汇证券'
    allowed_domains = ['www.chinastock.com.cn']
    entry = 'http://yhjh.chinastock.com.cn'

    cookies = 'JSESSIONID=qp6VTEKbiG88N-qKGnBRTnKqRaH6l9u_1GlkSWz27ADW9mpBQjJQ!-1352806688; WT_FPC=id=2c910a547c8f47b74fe1522637769135:lv=1527218235556:ss=1527218211544'
    username = '18625981663'
    password = '123456'
    lps = [{'url': 'http://yhjh.chinastock.com.cn/yhwz/managemoney/product.jsp?nav=',
            'ref': None,
            'ext': {'report_type': '1'}}]

    def parse_list(self, response):
        ext = response.meta['ext']
        report_type = int(ext['report_type'])
        if report_type == 1:
            funds = response.xpath('//*[@id="service"]/div[2]/div[1]/div[1]/div[2]/div[2]//a/@href').extract()
            for url in funds:
                url = urljoin(get_base_url(response), url)
                self.lps.append({'url': url, 'ref': response.url, 'ext': {'report_type': '2'}})
        else:
            url_pro = response.xpath('//*[@id="dne3"]/@href').extract_first()
            url_pro = urljoin(get_base_url(response), url_pro)
            url_money = response.xpath('//*[@id="dne5"]/@href').extract_first()
            url_money = urljoin(get_base_url(response), url_money)
            url_law = response.xpath('//*[@id="dne8"]/@href').extract_first()
            url_law = urljoin(get_base_url(response), url_law)
            self.ips.append({'url': url_pro, 'ref': response.url, 'ext': {'report_type': '1', 'url': url_pro}})
            self.ips.append({'url': url_money, 'ref': response.url, 'ext': {'report_type': '1', 'url': url_money}})
            self.ips.append({'url': url_law, 'ref': response.url, 'ext': {'report_type': '1', 'url': url_law}})

    def parse_item(self, response):
        ext = response.meta['ext']
        report_type = int(ext['report_type'])
        if report_type == 1:
            base_url = ext['url']
            next_page = response.xpath('//*[@id="pager"]/div/div[@class="pagination_next"]/a/@pagenum').extract_first()
            if next_page:
                url = base_url + '&pageNum=' + str(next_page)
                self.ips.append({'url': url, 'ref': response.url, 'ext': {'report_type': '1', 'url': base_url}})
            rows = response.xpath('/html/body/div/div[1]/ul/li/a/@href').extract()
            for url in rows:
                url = urljoin(get_base_url(response), url)
                self.ips.append({'url': url, 'ref': response.url, 'ext': {'report_type': '2'}})
        else:
            url = response.url
            title = response.xpath('//*[@id="dleft1"]/div[1]/text()').extract_first().strip()
            publish_time = response.xpath('//*[@id="dleft1"]/div[2]/text()').re_first('\d+-\d+-\d+')
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time
            yield item
