# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-04-27




from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class HongTaZhengQuanSecutiesSpider(GGFundNavSpider):
    name = 'FundNav_HongTaZhengQuanSecuties'
    sitename = '红塔证券'
    channel = '券商资管净值'
    allowed_domains = ['www.hongtastock.com']
    proxy = 2
    fps = [{'url': 'http://www.hongtastock.com/funddaily/funddaily.aspx?id=C58888'}]

    def parse_fund(self, response):
        fund_ids = re.findall('<option(.*?)value="(.*?)">(.*?)</option>', response.text)
        zz1 = '<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*?)" />'
        zz2 = '<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(.*?)" />'
        __VIEWSTATE = re.findall(zz1, response.text)[0]
        __EVENTVALIDATION = re.findall(zz2, response.text)[0]
        for id in fund_ids:
            fund_id = id[1]
            fund_name = id[2]
            self.ips.append({
                'url': 'http://www.hongtastock.com/funddaily/funddaily.aspx?id=' + fund_id,
                'ref': response.url,
                'form': {'__VIEWSTATE': __VIEWSTATE,
                         '__VIEWSTATEGENERATOR': '5ED276C6',
                         '__EVENTTARGET': 'pager1',
                         '__EVENTARGUMENT': "1",
                         '__EVENTVALIDATION': __EVENTVALIDATION,
                         'ProductName': fund_id,
                         },
                'ext': {'fund_name': fund_name, 'fund_id': fund_id},
                'pg': 1
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = response.xpath("//table[@class='listtable']//tr")
        for row in rows[4:]:
            statistic_date = row.xpath("./td[1]//text()").extract_first().strip()
            nav = row.xpath("./td[2]//text()").extract_first().strip()
            added_nav = row.xpath("./td[3]//text()").extract_first().strip()
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav)
            item['added_nav'] = float(added_nav)
            item['statistic_date'] = datetime.strptime(
                statistic_date.replace('年', '-').replace('月', '-').replace('日', ''), '%Y-%m-%d')
            yield item

        if '</span><a disabled' not in response.text:
            pg = response.meta['pg']
            fund_id = response.meta['ext']['fund_id']
            next_pg = str(int(pg) + 1)
            zz1 = '<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*?)" />'
            zz2 = '<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(.*?)" />'
            __VIEWSTATE = re.findall(zz1, response.text)[0]
            __EVENTVALIDATION = re.findall(zz2, response.text)[0]
            self.ips.append({
                'url': 'http://www.hongtastock.com/funddaily/funddaily.aspx?id=' + fund_id,
                'ref': response.url,
                'form': {'__VIEWSTATE': __VIEWSTATE,
                         '__VIEWSTATEGENERATOR': '5ED276C6',
                         '__EVENTTARGET': 'pager1',
                         '__EVENTARGUMENT': str(next_pg),
                         '__EVENTVALIDATION': __EVENTVALIDATION,
                         'ProductName': fund_id,
                         },
                'ext': {'fund_name': fund_name, 'fund_id': fund_id},
                'pg': next_pg
            })


