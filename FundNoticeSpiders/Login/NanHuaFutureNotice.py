# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy import FormRequest
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
import json


class NanHuaFutureNoticeSpider(GGFundNoticeSpider):
    name = 'FundNotice_NanHuaFutureNotice'
    sitename = '南华期货'
    entry = 'https://www.nanhua.net/'
    username = '13916427906'
    password = 'ZYYXSM123'

    ips = [
        {
            'url': 'https://www.nanhua.net/jSearch/queryNewsListByTypeForJson.shtm?site=newnanhua&type=201201&start=1&limit=16',
            'ref': 'https://www.nanhua.net/amc/diagnosis/announcements.html',
            'ext': {'page': '1'}
        }
    ]

    def start_requests(self):
        url = 'https://www.nanhua.net/member/newLogin.shtm?start=0'
        yield FormRequest(url=url,
                          headers={'X-Requested-With': 'XMLHttpRequest',
                                   'Referer': 'https://www.nanhua.net/member/login.html?url=aHR0cHM6Ly93d3cubmFuaHVhLm5ldC8='
                                   },
                          formdata={
                             'account': self.username,
                             'password': self.password,
                             'isagree': 'on',
                             'rememberme': '1'})

    def parse_item(self, response):
        ext = response.meta['ext']
        page = int(ext['page'])
        rows = json.loads(response.text)
        total_pages = int(rows['totalPages'])
        rows = rows['recordList']
        for row in rows:
            url = row['href']
            url = urljoin(get_base_url(response), url)
            title = row['subject']
            publish_time = row['createTime']
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d %H:%M:%S')
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time
            yield item
        if page < total_pages:
            url = 'http://www.nanhua.net/jSearch/queryNewsListByTypeForJson.shtm?site=newnanhua&type=201201&limit=16&start='
            url = url + str(page+1)
            self.ips.append({
                'url': url,
                'ref': response.url,
                'ext': {'page': str(page+1)}
            })

