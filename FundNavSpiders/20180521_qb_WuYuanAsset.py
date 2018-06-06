# Department : 保障部
# Author : 钱斌
# Create_date : 2018-05-21

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class WuYuanAssetSpider(GGFundNavSpider):
    name = 'FundNav_WuYuanAsset'
    sitename = '悟源资产'
    channel = '投资顾问'

    fps = [{'url': 'http://www.wyamc.cn/index.php?g=&m=list&a=index&id=24'}]

    def parse_fund(self, response):
        href_list = response.xpath('//div[@class="ny_zblb1"]//ul[@style=" display:block"]//@href').extract()
        name_list = response.xpath('//div[@class="ny_zblb1"]//ul[@style=" display:block"]//a/text()').extract()
        for href, fname in zip(href_list, name_list):
            self.ips.append({
                'url': 'http://www.wyamc.cn%s' % href,
                'ref': response.url,
                'ext': fname
            })

    def parse_item(self, response):
        rows = response.css('div.product_con:nth-child(2) tr')[1:]
        for r in rows:
            dt = r.css('td:nth-child(1) ::text').extract()
            nav = r.css('td:nth-child(2) ::text').extract_first()
            add_nav = r.css('td:nth-child(3) ::text').extract_first()

            date = ''.join(dt)

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['fund_name'] = response.meta['ext']
            item['channel'] = self.channel
            item['url'] = response.url
            item['nav'] = float(nav) if nav else None
            item['added_nav'] = float(add_nav) if add_nav else None
            item['statistic_date'] = datetime.strptime(date, '%Y%m%d') if date else None

            yield item
