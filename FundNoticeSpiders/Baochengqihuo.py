# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from scrapy import FormRequest
import json


class BaochengqihuoSpider(GGFundNoticeSpider):
    name = 'FundNotice_Baochengqihuo'
    sitename = '宝城期货'
    entry = 'http://www.bcqhgs.com/'

    def start_requests(self):
        yield FormRequest(
            url='http://www.bcqhgs.com/handle/zcgl.ashx?action=getzcglcount',
            formdata={'fs': 'ZGGG'},
            callback=self.parse_list
        )

    def parse_list(self, response):
        count = int(response.text)
        self.ips.append({
            'url': 'http://www.bcqhgs.com/handle/zcgl.ashx?action=getzcgl',
            'form': {
                'fs': 'ZGGG',
                'pagecount': str(count),
                'pagesize': '15',
                'pageindex': '0'
            },
            'pg': 0
        })

    def parse_item(self, response):

        form = response.meta['form']
        pagecount = form['pagecount']
        pagesize = form['pagesize']

        rows = json.loads(response.text)
        for row in rows:
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry

            url = 'http://www.bcqhgs.com/zcgldetail.shtml#ZGGG_' + str(row['infor_id'])
            title = row['infor_title']
            publish_time = row['infor_addtime']
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')

            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time

            yield item

        pg = response.meta['pg'] + 1
        if (int(pagecount) / int(pagesize)) > int(pg):
            self.ips.append({
                'url': 'http://www.bcqhgs.com/handle/zcgl.ashx?action=getzcgl',

                'form': {
                    'fs': 'ZGGG',
                    'pagecount': pagecount,
                    'pagesize': '15',
                    'pageindex': str(pg)
                },
                'pg': pg
            })
        yield self.request_next()
