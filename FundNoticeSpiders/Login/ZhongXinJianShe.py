# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
import json
import re


class ZhongXinJianSheSpider(GGFundNoticeSpider):
    name = 'FundNotice_ZhongXinJianShe'
    sitename = '中信建投'
    entry = 'https://www.csc108.com/'

    proxy = 2
    cookies = '__jsluid=9f8ce8eb51aab6705d8a908f91634fbd; SERVERID=b6f09cec80b80dc50f5a41b77b6cee7e|1526537676|1526537676; JSESSIONID=_jxs151mash1VkzEvfwO5IcLu4wIAMlVbco_eWGTJ37UvuP8yBtC!-1252920085'
    username = '15138719815'
    password = '123456'
    lps = [{'url': 'https://www.csc108.com/zgcp/assetManageIndex.jspx'}]

    def parse_list(self, response):
        base_url = 'https://www.csc108.com/zgcp/getAttachUploadList.jspx'
        funds = response.xpath(
            '/html/body/div[5]/div//div[@class="zuocefudhul"]/ul/ul[position()>1]/li/a/@href').extract()
        for url in funds:
            fund_id = re.search(r'productCode=(\S+)', url).group(1)
            self.ips.append({'url': base_url, 'ref': response.url,
                             'form': {'curPage': '1', 'file_type': '1', 'productCode': str(fund_id)},
                             'ext': {'report_type': '1', 'file_type': '1', 'page': '1', 'fund_id': str(fund_id)}})
            self.ips.append({'url': base_url, 'ref': response.url,
                             'form': {'curPage': '1', 'file_type': '2', 'productCode': str(fund_id)},
                             'ext': {'report_type': '1', 'file_type': '2', 'page': '1', 'fund_id': str(fund_id)}})
            self.ips.append({'url': base_url, 'ref': response.url,
                             'form': {'curPage': '1', 'file_type': '3', 'productCode': str(fund_id)},
                             'ext': {'report_type': '1', 'file_type': '3', 'page': '1', 'fund_id': str(fund_id)}})

    def parse_item(self, response):
        ext = response.meta['ext']
        report_type = int(ext['report_type'])
        page = int(ext['page'])
        fund_id = ext['fund_id']
        file_type = ext['file_type']
        if report_type == 1:
            rows = response.xpath('//li')
            if len(rows) > 0:
                for row in rows:
                    url = row.xpath('.//a/@href').extract_first()
                    url = urljoin(get_base_url(response), url)
                    title = row.xpath('.//a/text()').extract_first()
                    publish_time = row.xpath('./span/text()').extract_first()
                    if publish_time:
                        publish_time = datetime.strptime(publish_time, '%Y-%m-%d')
                    item = GGFundNoticeItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url_entry'] = self.entry
                    item['url'] = url
                    item['title'] = title
                    item['publish_time'] = publish_time
                    yield item
                base_url = 'https://www.csc108.com/zgcp/getAttachUploadList.jspx'
                url = base_url + '?curPage=' + str(page+1)
                url = url + '&file_type=' + str(file_type)
                url = url + '&productCode=' + str(fund_id)
                self.ips.append({
                    'url': url,
                    'ref': response.url,
                    'ext': {'report_type': str(report_type), 'file_type': str(file_type),
                            'page': str(page+1), 'fund_id': str(fund_id)}
                })
