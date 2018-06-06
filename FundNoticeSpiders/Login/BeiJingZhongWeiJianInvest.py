# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
import json


class BeiJingZhongWeiJianInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_BeiJingZhongWeiJianInvest'
    sitename = '北京中外建投资'
    entry = 'http://www.cciif.cn/product/JN'

    proxy = 2
    cookies = 'JSESSIONID=52F91E698D2ED23089DEA7854BE09812'
    username = '13916427906'
    password = 'ZYYXSM123'
    ips = [{'url': 'http://www.cciif.cn/getProductList?pageIndex=1&siteType=JN&pageSize=5',
            'ref': None,
            'ext': {'page': '1'}}]

    def parse_item(self, response):
        page = int(response.meta['ext']['page'])
        rows = json.loads(response.text)
        rows = rows['rows']
        if len(rows) > 0:
            for row in rows:
                url = 'http://www.cciif.cn/showSiteDetail?id='
                title = row['title']
                publish_time = row['last_update_time'][0:10]
                publish_time = datetime.strptime(publish_time, '%Y-%m-%d')
                item = GGFundNoticeItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url_entry'] = self.entry
                item['url'] = url + str(row['id'])
                item['title'] = title
                item['publish_time'] = publish_time
                yield item
            self.ips.append({
                'url': 'http://www.cciif.cn/getProductList?siteType=JN&pageSize=5&pageIndex='+str(page+1),
                'ref': response.url,
                'ext': {'page': str(page+1)}
            })
        yield self.request_next()
