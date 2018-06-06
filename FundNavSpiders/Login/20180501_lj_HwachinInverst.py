# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 李婧
# Create_date : 2018-05-01

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class HwachinInvestSpider(GGFundNavSpider):
    name = 'FundNav_HwachinInvest'
    sitename = '华勤投资'
    channel = '投资顾问'

    username = 'ZYYXSM'
    password = 'ZYYXSM123'
    cookies = '__guid=36323750.1600720933798163000.1524909128435.6665; PHPSESSID=b45b6ef70eadce73c1e8273e066566f4; GWFiG_auth=36c2RPYSXZq7iCcYVSSu4ozBkOyiw6CE1eiEoJg-ddLJFZ2PZ1qdRsxKnZU3AcKjGZwTwaiUHjkqe3RfKr-CyYa_-rseiLRdjGlY5geZjeT2LtggUtnkrAUlzPH-PR_KUuQHSA6CdxX7lhqXv8lrsyHWJy4N; GWFiG__userid=cfc0VHWNOd-HPPs85Gm1BRrtvygPYZh9WehXArSiDs4I; GWFiG__username=09b1apC6kQLaxW_1bgQ9006b6yuYaOfemDm7H42sjMNrzq8; GWFiG__groupid=dbbd9nbPpz7B2H_yhVGKw15BUOeFA1eIpivuFi1W; GWFiG__nickname=a2daQiN0QY8wNu2uI7XoCkA--z1xnq28PYNoTcTTqZ51Zv4; monitor_count=32'

    fps = [{'url': 'http://www.hwachin.com/index.php?m=content&c=index&a=show&catid=33&id=1'}]

    def parse_fund(self, response):
        fund_urls = response.xpath("//div[@id='jquery-accordion-menu'][@class='jquery-accordion-menu red']/ul/li[3]/a")
        for url in fund_urls:
            ips_url = url.xpath('.//@href').extract_first()
            fund_name = url.xpath('.//text()').extract_first()
            self.ips.append({
                'url': ips_url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = response.xpath("//div[@id='tab2'][@class='tab_content']/table/tbody//tr")
        for row in rows[1:]:
            fund_date = row.xpath('.//td[2]//text()').extract_first()
            nav = row.xpath('.//td[3]//text()').extract_first()
            added_nav = row.xpath('.//td[4]//text()').extract_first()
            item = GGFundNavItem()

            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(fund_date.replace('/', '-'), '%Y-%m-%d')
            item['nav'] = float(nav)
            item['added_nav'] = float(added_nav)
            yield item

