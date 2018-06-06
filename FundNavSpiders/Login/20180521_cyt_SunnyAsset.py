# Department : 保障部
# Author : 陈雅婷
# Create_date : 2018-05-21

from datetime import datetime
from scrapy import FormRequest
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class SunnyAssetSpider(GGFundNavSpider):
    name = 'FundNav_SunnyAsset'
    sitename = '深圳前海阳光宝资产'
    channel = '投资顾问'
    allowed_domains = ['www.ygbqh.com']
    start_urls = ['http://www.ygbqh.com/products.php']

    username = '13916427906'
    password = 'ZYYXSM123'

    fps = [{'url': 'http://www.ygbqh.com/products.php'}]

    def start_requests(self):
        yield FormRequest(url='http://www.ygbqh.com/check_login.php',
                          headers={'Referer': 'http://www.ygbqh.com/userlogin.php'},
                          formdata={
                              'u_user': self.username,
                              'u_pass': self.password,
                              'button': '登 录',
                              'act': 'login'
                          })

    def parse_fund(self, response):
        fund_list = response.xpath('//div[@class="left_menu"]/a/@href').extract()
        fund_name_list = response.xpath('//div[@class="left_menu"]/a/text()').extract()
        pg = 1
        for key, name in zip(fund_list, fund_name_list):
            fund_url = 'http://www.ygbqh.com/' + key + '&cid=2&page=' + str(pg)
            self.ips.append({
                'url': fund_url,
                'ref': response.url,
                'pg': pg,
                'ext': {'fund_name': name}
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']

        page_number = response.xpath(
            '//div[@class="fypage_blk"]/div[@class="fypage"]/a[text()="尾页"]/@href').extract_first()
        end_page = int(page_number[-1])

        fund_info = response.xpath('//div[@id="products_jz"]/table').extract_first()
        fund_nav = re.findall('<td>(.*?)</td>', fund_info)
        fund_nav_list = [fund_nav[i:i + 5] for i in range(0, len(fund_nav), 5)]

        for nav_info in fund_nav_list:
            statistic_date = nav_info[2]
            nav = nav_info[3]
            added_nav = nav_info[4]

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d') if statistic_date else None
            item['nav'] = float(nav) if nav else None
            item['added_nav'] = float(added_nav) if nav else None

            yield item

        pg = response.meta['pg']
        if pg < end_page:
            next_pg = pg + 1
            next_url = response.url.replace('&page=' + str(pg), '&page=' + str(next_pg))
            self.ips.append({
                'url': next_url,
                'ref': response.url,
                'pg': next_pg,
                'ext': {'fund_name': fund_name}
            })
