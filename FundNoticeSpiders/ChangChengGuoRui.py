# -*- coding: utf-8 -*-

import json
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class ChangChengGuoRuiSpider(GGFundNoticeSpider):
    name = 'FundNotice_ChangChengGuoRui'
    sitename = '长城国瑞证券'
    entry = 'https://www.gwgsc.com/main/zcgl/zxxx/index.shtml'

    lps = [
        {
            'url': 'https://www.gwgsc.com/servlet/json',
            'form': {
                'funcNo': '820001',
                'curPage': '1',
                'numPerPage': '10',
                'catalogId': '37'
            },
            'pg': 1
        }
    ]

    def parse_list(self, response):
        json_data = json.loads(response.text)
        results = json_data['results'][0]
        rows = results['data']
        for row in rows:
            url = row['url']
            url = urljoin(get_base_url(response), url)
            title = row['title']
            publish_time = row['c_data']
            # 公告名称不完整，进入详情获取
            if '...' in title:
                self.ips.append({
                    'url': url,
                    'ext': {'publish_time': publish_time}
                })
            else:
                item = GGFundNoticeItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url_entry'] = self.entry
                item['title'] = title
                item['url'] = url
                item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
                yield item

        tp = int(results['totalPages'])
        pg = response.meta['pg'] + 1
        if pg <= tp:
            self.lps.append({
                'url': 'https://www.gwgsc.com/servlet/json',
                'form': {
                    'funcNo': '820001',
                    'curPage': str(pg),
                    'numPerPage': '10',
                    'catalogId': '37'
                },
                'pg': pg
            })

    def parse_item(self, response):
        ext = response.meta['ext']
        publish_time = ext['publish_time']
        title = response.xpath('//div[@class="top"]/h4/text()').extract_first()
        item = GGFundNoticeItem()
        item['sitename'] = self.sitename
        item['channel'] = self.channel
        item['url_entry'] = self.entry
        item['title'] = title
        item['url'] = response.url
        item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
        yield item
