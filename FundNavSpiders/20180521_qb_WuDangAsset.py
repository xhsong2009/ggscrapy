# Department : 保障部
# Author : 钱斌
# Create_date : 2018-05-21

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class WuDangAssetSpider(GGFundNavSpider):
    name = 'FundNav_WuDangAsset'
    sitename = '武当资产'
    channel = '投顾净值'

    fps = [{'url': 'http://www.wudangfund.com/Home/Products/index.html'}]

    def parse_fund(self, response):
        fid_list = response.css('div.box1_c  div.left li > a::attr(href)').re('id/(\d+)/type')
        name_list = response.css('div.box1_c  div.left li > a::text').extract()
        for fid, fname in zip(fid_list, name_list):
            self.ips.append({
                'url': 'http://www.wudangfund.com/Home/Products/clist/id/%s/type/3.html' % fid,
                'ref': response.url,
                'ext': fname
            })

    def parse_item(self, response):
        rows = response.css('table.table_3 tr')[1:]

        for r in rows:
            dt = r.css('td:nth-child(2)::text').extract_first()
            add_nav = r.css('td:nth-child(3)::text').extract_first()

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['fund_name'] = response.meta['ext']
            item['channel'] = self.channel
            item['url'] = response.url
            item['added_nav'] = float(add_nav) if add_nav else None
            item['statistic_date'] = datetime.strptime(dt, '%Y-%m-%d') if dt else None

            yield item
