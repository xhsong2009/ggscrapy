# Department : 保障部
# Author : 陈雅婷
# Create_date : 2018-05-16

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin


class HuoLiAssetSpider(GGFundNavSpider):
    name = 'FundNav_HuoLiAsset'
    sitename = '货力资产'
    channel = '投资顾问'

    username = '18883929277'
    password = '123456'
    cookies = r'PHPSESSID=2pq7d4oro2fv7uifbbiqjgdm44; DedeUserID__ckMd5=386c326b098c13bf; DedeUserID=12; DedeLoginTime__ckMd5=aaddc98eab3669bf; DedeLoginTime=1526436874'
    fps = [
        {'url': 'http://www.huoliasset.com/plus/list.php?tid=4',
         'ref': 'http://www.huoliasset.com/index.html'}
    ]

    def parse_fund(self, response):
        link_key = response.xpath('//div[@class="brc_man"]/div[@class="bod"]/div[@class="in"]/div[@class="lst"]/div[@class="l"]/a/@href').extract()
        fund_name = response.xpath('//div[@class="brc_man"]/div[@class="bod"]/div[@class="in"]/div[@class="lst"]/div[@class="l"]/a/@title').extract()

        for name, key in zip(fund_name, link_key):
            nav_link = urljoin('http://www.huoliasset.com', key)
            self.ips.append({
                'url': nav_link,
                'ref': response.url,
                'ext': {'fund_name': name}
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        nav_rows = response.xpath('//div[@id="coc"]/table/tbody/tr[2]/td[1]/div[@class="pro_box"]/div[@class="pro_con"]//tr')

        for row in nav_rows[1:]:
            nav_info = row.xpath('td/text()').extract()
            if nav_info[0].strip():
                statistic_date = nav_info[0].strip()
                nav = nav_info[1].strip()
                added_nav = nav_info[2].strip()

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                item['nav'] = float(nav) if nav else None
                item['added_nav'] = float(added_nav) if added_nav else None

                yield item


