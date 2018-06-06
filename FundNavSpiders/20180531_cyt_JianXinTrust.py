# Department : 保障部
# Author : 陈雅婷
# Create_date : 2018-05-31


from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from datetime import datetime


class JianXinTrustSpider(GGFundNavSpider):
    name = 'FundNav_JianXinTrust'
    sitename = '建信信托'
    channel = '信托净值'
    allowed_domains = ['www.xingrunfund.com']
    start_urls = ['http://www.xingrunfund.com/product.asp']

    trs_keyid = [10812, 14149, 14005, 13979, 13980, 14001, 14002, 14003, 14004, 13798, 10814, 10815, 11670, 11465,
                 11463, 9896, 9744, 8072, 8758, 8931, 8933, 8935, 8937, 8939, 8920, 8922, 8941, 8943, 8945, 8925, 8927,
                 8913, 8915, 8917, 8924, 8901, 8902, 8903, 8904, 8905, 8784, 8907, 8786, 8787, 8789, 8912, 8788, 8747,
                 7911, 7794, 7817, 7224, 7028, 6976, 6912, 6681, 6682, 6683, 6321, 5678, 2733, 2818, 3107, 3118, 1664,
                 1663]

    main_url = 'http://www.ccbtrust.com.cn/templates/second/index.aspx?nodeid=16&page=ContentPage&contentid='
    ips = []
    for key in trs_keyid:
        ips.append({'url': main_url + str(key)})

    def parse_item(self, response):
        nav_rows = response.xpath('//div[@class="acc_content"]//tbody/tr')
        for row in nav_rows[1:]:
            nav = ''.join(row.xpath('td[3]//text()').re('\S+'))
            if nav:
                fund_name = ''.join(row.xpath('td[1]//text()').extract())
                date = ''.join(row.xpath('td[2]//text()').extract()).replace('（成立日）', '')
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name.strip()
                item['statistic_date'] = datetime.strptime(date.strip(), '%Y-%m-%d') if date else None
                item['nav'] = float(nav.strip()) if nav else None
                yield item
