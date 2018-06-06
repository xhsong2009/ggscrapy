# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 李婧
# Create_date : 2018-05-11

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin
import re


class HuaRongTrustSpider(GGFundNavSpider):
    name = 'FundNav_HuaRongTrust'
    sitename = '华融信托'
    channel = '信托净值'
    allowed_domains = ['www.huarongtrust.com.cn']
    fps = [{'url': 'http://www.huarongtrust.com.cn/?jzgb/page/1.html'}, ]

    def parse_fund(self, response):
        fund_infos = response.xpath('//div[@class="jzgb"]/table//tr')
        for fund_info in fund_infos[1:]:
            fund_name = fund_info.xpath('.//td[2]//text()').extract_first()
            fund_href = fund_info.xpath('.//td[9]//@href').extract_first()
            added_nav = fund_info.xpath('.//td[5]//text()').extract_first()
            ips_url = (urljoin('http://www.huarongtrust.com.cn/?jzgb.html', fund_href.replace('/./', '')).replace(
                '.html', '')) + '/page/1' + '.html'
            self.ips.append({
                'url': ips_url,
                'ref': response.url,
                'pg': 1,
                'ext': {'fund_name': fund_name, 'added_nav': added_nav},
            })
        end_page = re.findall('"last_page":(.*?),', response.text)[0]
        pg = response.url.replace('http://www.huarongtrust.com.cn/?jzgb/page/', '').replace('.html', '')
        next_pg = int(pg) + 1

        if next_pg <= int(end_page):
            self.fps.append({
                'url': 'http://www.huarongtrust.com.cn/?jzgb/page/' + str(next_pg) + '.html',
                'ref': response.url
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        added_nav = response.meta['ext']['added_nav']
        rows = response.xpath('//div[@class="jzgbShow"]/table//tr')
        for row in rows[1:]:
            statistic_date = row.xpath('.//td[1]//text()').extract_first()
            nav = row.xpath('.//td[2]//text()').extract_first()
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav)
            item['added_nav'] = float(added_nav) if added_nav is not None else None
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y%m%d')
            added_nav = None
            yield item

        end_page = re.findall('"last_page":(.*?),', response.text)[0]
        pg = response.meta['pg']
        old_str = '/page/' + str(pg)
        if pg < int(end_page):
            new_str = '/page/' + str(pg + 1)
            next_url = response.url.replace(old_str, new_str)
            self.ips.append({
                'url': next_url,
                'ref': response.url,
                'pg': pg + 1,
                'ext': {'fund_name': fund_name, 'added_nav': added_nav}
            })
