# Department : 保障部
# Author : 李婧
# Create_date : 2018-04-26

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin


class GuoLingAssetSpider(GGFundNavSpider):
    name = 'FundNav_GuoLingAsset'
    sitename = '国领资产'
    channel = '投顾净值'
    allowed_domains = ['http://guolingzichan.com/']
    fps = [
        {
            'url': 'http://guolingzichan.com/product_93895.html#visualmodule_1'
        }
    ]

    def parse_fund(self, response):
        fund_infos = response.xpath("//div[@class='m-theme10-title']/a")
        for fund_info in fund_infos:
            ips_url = fund_info.xpath('.//@href').extract_first()
            fund_name = fund_info.xpath('.//text()').extract_first()
            fund_url = urljoin('http://guolingzichan.com/', ips_url)
            self.ips.append({
                'url': fund_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        rows = response.xpath("//div[@id='out_ph']/table[@class='ke-zeroborder'][2]/tbody/tr")
        fund_name = response.meta['ext']['fund_name']
        if len(rows) == 0:
            rows = response.xpath("//div[@class='m-view-list']/div[@id='out_ph']//tr")
            for row in rows[1:]:
                statistic_date = row.xpath("./td[1]//text()").extract_first().strip()
                if '2' in statistic_date:
                    nav = row.xpath("./td[3]//text()").extract_first().strip()
                    added_nav = row.xpath("./td[2]//text()").extract_first().strip()

                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['fund_name'] = fund_name
                    item['nav'] = float(nav)
                    item['added_nav'] = float(added_nav)
                    item['statistic_date'] = datetime.strptime(statistic_date.replace('/', '-'), '%Y-%m-%d')
                    yield item
        else:
            for row in rows[1:]:
                statistic_date = row.xpath("./td[1]//text()").extract_first().strip()
                if '2' in statistic_date:
                    nav = row.xpath("./td[3]//text()").extract_first().strip()
                    added_nav = row.xpath("./td[2]//text()").extract_first().strip()

                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['fund_name'] = fund_name
                    item['nav'] = float(nav)
                    item['added_nav'] = float(added_nav)
                    item['statistic_date'] = datetime.strptime(statistic_date.replace('/', '-'), '%Y-%m-%d')
                    yield item
