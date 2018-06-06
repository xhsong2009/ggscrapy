import json
from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class DongFangZQSpider(GGFundNavSpider):
    name = 'FundNav_DongFangZhengQuan'
    sitename = '东方证券'
    channel = '券商资管净值'

    username = '18638871675'
    password = '123456ll'

    fps = [
        {'url': 'http://www.dfham.com/product/big/piangu/910004/index.html'},
        {'url': 'http://www.dfham.com/product/small/piangu/918002/index.html'}
    ]

    def parse_fund(self, response):
        fundnames = response.xpath('//div[@class = "wrap-left"]//div[@class = "type"]//a//text()').extract()
        nums = response.xpath('//div[@class = "wrap-left"]//div[@class = "type"]//a//@href').extract()
        for num, fundname in zip(nums, fundnames):
            # 取链接当中的id，用split拆不出来，所以直接取了
            id = num[-17:-11]
            ips_url = 'http://www.dfham.com/common-web/chart/fundnetchart!getFundNetChartJson?fundcode=' + id
            self.ips.append({
                'url': ips_url,
                'ref': response.url,
                'ext': fundname
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']
        funds = json.loads(response.text)
        navs = funds['seriesData0']
        add_navs = funds['seriesData1']
        dates = funds['xAxisData']
        for nav, add_nav, date in zip(navs, add_navs, dates):
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d')
            item['nav'] = float(nav)
            item['added_nav'] = float(add_nav)
            yield item
