# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urljoin
from scrapy import FormRequest, Request
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class BeiJingFuRuiDeInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_BeiJingFuRuiDeInvest'
    sitename = '北京福睿德投资'
    entry = 'http://www.freedchina.com/news/notice'

    username = '13916427906'
    password = 'ZYYXSM123'

    ips = [
        {
            'url': 'http://www.freedchina.com/news/notice',
            'pg': 1
        }
    ]

    def start_requests(self):
        yield Request(url='http://www.freedchina.com/ti/agree/status/agree',
                      meta={'handle_httpstatus_list': [302]},
                      callback=self.parse_login)

    def parse_login(self, response):
        yield FormRequest(url='http://www.freedchina.com/Login/login',
                          formdata={
                              'username': self.username,
                              'password': self.password
                          },
                          meta={'handle_httpstatus_list': [302]})

    def parse_item(self, response):
        rows = response.xpath('//div[@class="new_box clearbox"]/ul/li/a')
        for row in rows:
            url = row.xpath('./@href').extract_first()
            url = urljoin(get_base_url(response), url)
            title = row.xpath('./h6/text()').extract_first()
            publish_time = row.xpath('./time/text()').re_first('\d+-\d+-\d+')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        tp = response.xpath('//div[@class="page ha-waypoint"]/a[text() = "最后一页"]/@href').re_first('page=([\d]+)')
        pg = response.meta['pg'] + 1
        if tp and pg <= int(tp):
            self.ips.append({
                'url': 'http://www.freedchina.com/news/notice?page={0}'.format(pg),
                'ref': response.url,
                'pg': pg
            })
