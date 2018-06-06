# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from urllib.parse import unquote_plus


class XingYeGuoJiTrustNoticeSpider(GGFundNoticeSpider):
    name = 'FundNotice_XingYeGuoJiTrustNotice'
    sitename = '兴业国际信托'
    entry = 'http://www.ciit.com.cn/'

    lps = [{'url': 'http://www.ciit.com.cn/news/p-notice/ext/index.html', 'ext': {'report_type': '1'}}]

    def parse_list(self, response):
        ext = response.meta['ext']
        report_type = int(ext['report_type'])
        if report_type == 1:
            funds = response.xpath('//*[@id="about-list"]/li[3]/dl/dt/a[text()!="净值公告"]/@href').extract()
            for url in funds:
                self.lps.append({'url': url, 'ref': response.url, 'ext': {'report_type': '2'}})
        else:
            url = response.xpath('//*[@id="frame1"]/@src').extract_first()
            url = urljoin(get_base_url(response), url)
            self.ips.append({'url': url, 'ref': response.url, 'ext': {'base_url': url}})

    def parse_item(self, response):
        ext = response.meta['ext']
        base_url = ext['base_url']
        next_page = response.xpath('/html/body/div/div/div/li/a[text()="下一页"]/@href').re_first(r'turnto\(\'(\d+)\'\)')
        if next_page:
            next_url = base_url + '&currentpage=' + str(next_page)
            self.ips.append({'url': next_url, 'ref': response.url, 'ext': {'base_url': base_url}})
        rows = response.css('.innercont>ul>li')
        for row in rows:
            url = row.xpath('./a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            title = row.xpath('./a/@title').extract_first().strip().replace('.pdf', '')
            publish_time = row.xpath('./span/text()').extract_first().strip()
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = unquote_plus(url)
            item['title'] = title
            item['publish_time'] = publish_time
            yield item
