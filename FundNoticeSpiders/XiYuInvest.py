# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
import json


class XiYuInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_XiYuInvest'
    sitename = '西域投资'
    entry = 'http://www.xiyu88.com/'

    # 固定Cookie
    cookies = 'isagree=agree'

    ips = [{
        'url': 'http://www.xiyu88.com/notices/json/listNotices',
        'ref': 'http://www.xiyu88.com/notices/json/listNotices',
        'form': {'currentPage': '1', 'everyPage': '10'},
        'ext': {'page': '1'}
    }]

    def parse_item(self, response):
        rows = json.loads(response.text)
        ext = response.meta['ext']
        for row in rows[1]:
            url = urljoin(get_base_url(response), '/notices/view?id=' + str(row[0]))
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['title'] = row[1]
            item['url'] = url
            item['publish_time'] = datetime.strptime(row[2], '%Y-%m-%d %H:%M')
            yield item
        tp = int(rows[0])
        tp = tp / 10 if tp % 10 == 0 else tp // 10 + 1
        pg = int(ext['page']) + 1
        if pg <= tp:
            self.ips.append({
                'url': 'http://www.xiyu88.com/notices/json/listNotices',
                'ref': 'http://www.xiyu88.com/notices/json/listNotices',
                'form': {'currentPage': str(pg), 'everyPage': '10'},
                'ext': {'page': str(pg)}
            })
