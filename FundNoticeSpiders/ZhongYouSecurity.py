# -*- coding: utf-8 -*-

import json
from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class ZhongYouSecuritySpider(GGFundNoticeSpider):
    name = 'FundNotice_ZhongYouSecurity'
    sitename = '中邮证券'

    entry = 'http://www.cnpsec.com.cn/web/list.htm?menuId=08&subId=0801&classId=080104'

    ips = [
        {
            'url': 'http://www.cnpsec.com.cn/web/list.ashx',
            'form': {'classid': '080104',
                     'pageIndex': '1',
                     'infoFlag': 'finfo',
                     'type': '1',
                     'keywords': 'null',
                     'datalen': '20',
                     'hrefURL': 'L2N0enEvenh6eC96eDAzLmh0bWw/bWVudUlkPTA4JnN1YklkPTA4MDEmY2xhc3NJZD0wODAxMDQ=',
                     'jsontype': 'json_4'
                     },
            'pg': 1
        }
    ]

    def parse_item(self, response):
        json_data = json.loads(response.text)
        rows = json_data['result']
        for row in rows:
            title = row['title']
            url = 'http://www.cnpsec.com.cn/web/News.htm?infoid={0}&subId=0801&classId=080104'.format(row['infoid'])
            publish_time = row['originaltime']

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['title'] = title
            item['url'] = url
            item['publish_time'] = datetime.strptime(publish_time, '%Y/%m/%d %H:%M:%S')
            yield item

        tp = json_data['totalPages']
        pg = response.meta['pg'] + 1
        if pg <= tp:
            self.ips.append({
                'url': 'http://www.cnpsec.com.cn/web/list.ashx',
                'form': {'classid': '080104',
                         'pageIndex': str(pg),
                         'infoFlag': 'finfo',
                         'type': '1',
                         'keywords': 'null',
                         'datalen': '20',
                         'hrefURL': 'L2N0enEvenh6eC96eDAzLmh0bWw/bWVudUlkPTA4JnN1YklkPTA4MDEmY2xhc3NJZD0wODAxMDQ=',
                         'jsontype': 'json_4'
                         },
                'pg': pg
            })
