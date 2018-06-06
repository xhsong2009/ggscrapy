# -*- coding: utf-8 -*-
import time
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class GuoTaiJunAnSpider(GGFundNoticeSpider):
    name = 'FundNotice_GuoTaiJunAn'
    sitename = '国泰君安'
    entry = 'https://www.gtjazg.com/disclosure?topicCode=dqbg'

    username = '13916427906'
    password = 'ZYYXSM123'
    cookies = 'gjzgs1=93258df25a7846b0f01e47621e0e11b2; Hm_lvt_8f8cb8797fca1e91d224d6a674006462=1524446374,1525238928,1525660102; showthemenr=show; remebermobile=13916427906; login_sign=7eed7b06bf24437a839be9ad7d51df7e; s201_SESSION=4E21CC50F282EDE32C26AD45813F378C; Hm_lpvt_8f8cb8797fca1e91d224d6a674006462=1526266297'

    lps = [
        {
            'url': 'https://www.gtjazg.com/disclosurePage?parent_ids=&topicCode=dqbg&p=1&starDate=&entDate=&name=&_={0}'.format(int(round(time.time() * 1000))),
            'ref': None,
            'pg': 1
        }
    ]

    def parse_list(self, response):
        rows = response.xpath('//ul[@class="list2 con-xxpl"]/li/a')
        for row in rows:
            url = row.xpath('./@href').extract_first()
            url = urljoin(get_base_url(response), url)
            title = row.xpath('./span[@class="title"]//text()').extract_first().strip()
            publish_time = row.xpath('.//text()').re_first('\d+-\d+-\d+')
            if '...' in title:
                self.ips.append({
                    'url': url,
                    'ref': response.url
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

        pg = response.meta['pg'] + 1
        tp = int(response.xpath('//div[@class="yl-page"]/p').xpath('string(.)').re_first(r'共([\d]+)页'))
        if tp >= pg:
            self.lps.append({
                'url': 'https://www.gtjazg.com/disclosurePage?parent_ids=&topicCode=dqbg&p={0}&starDate=&entDate=&name=&_={1}'.format(pg, int(round(time.time() * 1000))),
                'ref': response.url,
                'pg': pg
            })

    def parse_item(self, response):
        title = response.xpath('//div[@class="contentDetail"]/div/h3//text()').extract_first().strip()
        publish_time = response.xpath('//div[@class="contentDetail"]/div/div[@class ="dateBox"]/div[@class="date f-12px fl"]/text()').re_first('\d+-\d+-\d+')

        item = GGFundNoticeItem()
        item['sitename'] = self.sitename
        item['channel'] = self.channel
        item['url_entry'] = self.entry
        item['title'] = title
        item['url'] = response.url
        item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
        yield item
