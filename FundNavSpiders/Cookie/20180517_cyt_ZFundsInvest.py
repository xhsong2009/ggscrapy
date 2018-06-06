# Department : 保障部
# Author : 陈雅婷
# Create_date : 2018-05-17

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin


class ZFundsInvestSpider(GGFundNavSpider):
    name = 'FundNav_ZFundsInvest'
    sitename = '深圳知方石投资'
    channel = '投顾净值'
    allowed_domains = ['www.zfunds.com.cn']
    start_urls = ['http://www.zfunds.com.cn/plus/list.php?tid=82']

    username = '18601692933'
    password = '18601692933'
    cookies = 'PHPSESSID=d9l1n7atcdqncabgjl5oj65sh1; DedeUserID=31; DedeUserID__ckMd5=882ba998b483692b; DedeLoginTime=1526520012; DedeLoginTime__ckMd5=d90bf43eb449b42d; layerPopup2=hide'

    fps = [{'url': 'http://www.zfunds.com.cn/plus/list.php?tid=82'}]

    def parse_fund(self, response):
        fund_list = response.xpath('//div[@class="bggg"]/li/a/@href').extract()
        for key in fund_list:
            fund_url = urljoin('http://www.zfunds.com.cn', key)
            self.ips.append({
                'url': fund_url,
                'ref': response.url
            })

    def parse_item(self, response):
        fund_info = response.xpath('//div[@class="gundong2"]/ul/div[@class="bb"]/div')
        for row in fund_info:
            row_info = row.xpath('div/text()').extract()
            statistic_date = row_info[1].strip()
            nav = row_info[2]
            added_nav = row_info[3]
            if response.url == 'http://www.zfunds.com.cn/plus/list.php?tid=88':
                fund_name = '前海开源知方石1号'
            else:
                fund_name = row_info[0]

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d') if statistic_date else None
            item['nav'] = float(nav) if nav else None
            item['added_nav'] = float(added_nav) if added_nav else None

            yield item
