# -*- coding: utf-8 -*-
import json
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class ZhaoShangSecuritySpider(GGFundNoticeSpider):
    name = 'FundNotice_ZhaoShangSecurity'
    sitename = '招商证券'
    entry = 'https://amc.cmschina.com/news/gonggao'

    lps = [
        {
            'url': 'https://amc.cmschina.com/news/gonggao'
        }
    ]

    def parse_list(self, response):
        rows = response.xpath('//div[@class="left_nav left"]/ul/li/a')
        for row in rows:
            url = row.xpath('./@href').extract_first()
            name = row.xpath('./text()').extract_first()
            if name == '最新公告':
                url_param = 'https://amc.cmschina.com/news/detail?type=gonggao&id='
                url_type = 'gonggao'
            elif name == '定期报告':
                url_param = 'https://amc.cmschina.com/news/detail?type=dqbg&id='
                url_type = 'dqbg'
            self.ips.append({
                'url': urljoin(get_base_url(response), url),
                'ref': response.url,
                'form': {
                    'type': url_type,
                    'page': '1'
                },
                'headers': {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Accept': 'application/json, text/javascript, */*; q=0.01'
                },
                'pg': 1,
                'ext': {'url_param': url_param, 'url_type': url_type}
            })

    def parse_item(self, response):
        url_type = response.meta['ext']['url_type']
        url_param = response.meta['ext']['url_param']
        data = json.loads(response.text)['data']
        rows = data['rows']
        for row in rows:
            url_id = row[0]
            title = row[1]
            publish_time = row[2]
            url = url_param + url_id

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d') if '-' in publish_time else datetime.strptime(publish_time, '%Y%m%d')
            yield item

        total = int(data['total'])
        page_size = int(data['pagesize'])
        tp = int(total / page_size if total % page_size == 0 else total // page_size + 1)
        pg = response.meta['pg'] + 1
        if pg <= tp:
            self.ips.append({
                'url': 'https://amc.cmschina.com/news/{0}'.format(url_type),
                'ref': response.url,
                'form': {
                    'type': url_type,
                    'page': str(pg)
                },
                'headers': {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Accept': 'application/json, text/javascript, */*; q=0.01'
                },
                'pg': pg,
                'ext': {'url_param': url_param, 'url_type': url_type}
            })
