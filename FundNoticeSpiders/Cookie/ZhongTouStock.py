# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
import re
import json


class ZhongTouStockSpider(GGFundNoticeSpider):
    name = 'FundNotice_ZhongTouStock'
    sitename = '中投证券'
    entry = 'http://www.china-invs.cn/d01/zcgl/index.html'

    cookies = 'BotMitigationCookie_1969904701684545095="548876001526977326ReMV07wqIjlG7bSU7Vrw9m2cwKM="; JSESSIONID=D5B7DF9BBD7719E096A3BD9D04286AE6'

    lps = [
        {
            'url': 'http://www.china-invs.cn/d01/zcgl/index.html#A60042_7',
            'ref': 'http://www.china-invs.cn/d01/zcgl/index.html',
            'ext': {'flag': 0}
        }
    ]

    def parse_list(self, response):
        flag = response.meta['ext']['flag']
        if flag == 0:
            ids = response.xpath('//ul[@id="menu"]/li[2]/ul/li/a/@href').extract()
            for id in ids:
                id = re.findall('(A\d+|S\d+)', id)[0]
                self.lps.append({
                    'url': 'http://www.china-invs.cn/d01/zcgl/product.jsp?id=' + id + '&li=7&textid=&tmp=0.8856078093043638',
                    'ref': response.url,
                    'ext': {'flag': 1}
                })
        else:
            code = response.xpath('//script').extract_first()
            code = re.findall('list_report\(\\\'(\d+)', code)[0]
            self.ips.append({
                'url': 'http://www.china-invs.cn/supermarket/A6_Report_JSON.jsp?code=' + code + '&page=1&0.5678455961605193',
                'ref': response.url,
                'pg': 1,
                'ext': {'code': code}
            })

    def parse_item(self, response):
        datas = json.loads(response.text)
        for data in datas:
            id = data['id']
            href = '/article5.html?id=' + str(id)
            url = urljoin(get_base_url(response), href)
            title = data['title']
            publish_time = data['date']

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        if len(datas) > 0:
            pg = response.meta['pg']
            code = response.meta['ext']['code']
            np = pg+1
            self.ips.append({
                'url': 'http://www.china-invs.cn/supermarket/A6_Report_JSON.jsp?code=' + code + '&page=' + str(np) + '&0.5678455961605193',
                'ref': response.url,
                'pg': np,
                'ext': {'code': code}
            })


