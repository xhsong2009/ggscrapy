# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
import json


class ChongQingGuoJiTrustSpider(GGFundNoticeSpider):
    name = 'FundNotice_ChongQingGuoJiTrust'
    sitename = '重庆国际信托'
    entry = 'http://www.cqitic.com/'
    lps = [{'url': 'http://www.cqitic.com/info/'}]

    def parse_list(self, response):
        funds = response.xpath('//*[@id="ourBusinessSlider"]/div[@class="item"]')
        fund_names = '成立公告,管理报告,清算公告,其他公告'
        for fund in funds:
            fund_name = fund.xpath('./img/@title').extract_first()
            if fund_name in fund_names:
                fund_id = fund.xpath('.//a/@sitemapid').extract_first()
                url = 'http://www.cqitic.com/more/'+fund_id+'_1_20.shtml'
                self.ips.append({'url': url,
                                 'ref': response.url,
                                 'ext': {'page': '1', 'fund_id': fund_id}
                                 })

    def parse_item(self, response):
        ext = response.meta['ext']
        page = int(ext['page'])
        fund_id = ext['fund_id']
        if response.text:
            rows = json.loads(response.text)
            for row in rows:
                item = GGFundNoticeItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url_entry'] = self.entry
                url = row['url']
                title = row['title']
                publish_time = row['displayTime']
                publish_time = datetime.strptime(publish_time, '%Y.%m.%d')
                item['url'] = url
                item['title'] = title
                item['publish_time'] = publish_time
                yield item
            url = 'http://www.cqitic.com/more/' + fund_id + '_'+str(page+1)+'_20.shtml'
            self.ips.append({'url': url,
                             'ref': response.url,
                             'ext': {'page': str(page+1), 'fund_id': fund_id}
                             })
