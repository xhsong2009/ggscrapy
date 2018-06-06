# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
import json


class FengLingCapitalSpider(GGFundNoticeSpider):
    name = 'FundNotice_FengLingCapital'
    sitename = '丰岭资本'
    entry = 'http://www.szhvc.com/'

    ips = [{
        'url': 'http://www.szhvc.com/api/pc/message/news/paging?tagl2=REPORTS&pageSize=3&pageNum=1&_=1527477855432',
        'ref': 'http://www.szhvc.com/news/report',
        'pg': 1
    }]

    def parse_item(self, response):
        datas = json.loads(response.text)
        rows = datas['collection']
        for row in rows:
            title = row['title']
            url = '/news/detail/' + str(row['articleId'])
            url = urljoin(get_base_url(response), url)
            publish_time = row['publishTime']
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time
            yield item

        tp = datas['property']['pages']
        cp = response.meta['pg']
        if cp < tp:
            cp = cp+1
            self.ips.append({
                'url': 'http://www.szhvc.com/api/pc/message/news/paging?tagl2=REPORTS&pageSize=3&pageNum='+str(cp)+'&_=1527477855432',
                'ref': response.url,
                'pg': cp
            })






















