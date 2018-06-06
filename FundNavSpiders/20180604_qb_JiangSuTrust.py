# Department : 保障部
# Author : 钱斌
# Create_date : 2018-06-04


from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from datetime import datetime


class JiangSuTrustSpider(GGFundNavSpider):
    name = 'FundNav_JiangSuTrust'
    sitename = '江苏信托'
    channel = '信托净值'

    fps = [{'url': 'http://www.jsitic.net/418.html'}]

    def parse_fund(self, response):
        href_list = response.xpath('//div[@class="float_left hand text-left"][contains(text(), "历史净值")]/@onclick'
                                   ).re("window.location.href='(.*)'")
        for href in href_list:
            self.ips.append({
                'url': 'http://www.jsitic.net' + href,
                'ref': response.url,
            })

    def parse_item(self, response):
        rows = response.xpath('//div[@style="height:30px;"]')
        for r in rows:
            fund_name = r.xpath('div[1]/text()').extract_first()
            date = r.xpath('div[2]/text()').re_first('\S+')
            nav = r.xpath('div[3]/text()').re_first('\S+')
            if date:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name.strip()
                item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d') if date else None
                item['nav'] = float(nav) if nav else None
                yield item
