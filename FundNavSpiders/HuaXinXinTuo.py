# -*- coding: utf-8 -*-

# Department : 保障部
# Author : 袁龚浩
# Create_date : 2018-05-07


from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class GuoXinXinTuoSpider(GGFundNavSpider):
    name = 'FundNav_HuaXinXinTuo'
    sitename = '华信信托'
    channel = '信托净值'
    proxy = 1
    # 此站点经常出现连接超时
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 240,
    }

    fps = [{
        'url': 'http://www.huaxintrust.com/news2.asp?nid=36-46',
    }]

    def parse_fund(self, response):
        next_href = response.xpath('//a[contains(text(),"下页")]//@href').extract_first()
        if next_href:
            self.fps.append({
                'url': 'http://www.huaxintrust.com/news2.asp' + next_href,
                'ref': response.url,
            })

        fund_urls = response.xpath('//ul[@class = "neirong33"]//a//@href').extract()
        for url in fund_urls:
            self.ips.append({
                'url': 'http://www.huaxintrust.com/' + url,
                'ref': response.url,
            })

    def parse_item(self, response):
        item = GGFundNavItem()
        funds = response.xpath('//table//tr[2]')
        fund_name = ''.join((''.join(funds.xpath('//td[1]//div//text()').extract())).split())
        if funds.xpath('td[3]//div//text()'):
            nav = funds.xpath('td[3]//div//text()').extract_first()
            added_nav = funds.xpath('td[4]//div//text()').extract_first()
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if added_nav is not None else None
        else:
            nav = funds.xpath('td[2]//div//text()').extract_first()
            item['nav'] = float(nav) if nav is not None else None
        statistic_date = response.xpath('//div[@class="rer"]').re_first('数据截止到(\d+年\d+月\d+日)')
        item['sitename'] = self.sitename
        item['channel'] = self.channel
        item['url'] = response.url
        item['fund_name'] = fund_name
        item['statistic_date'] = datetime.strptime(statistic_date, '%Y年%m月%d日')
        yield item
