from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class YiHuInvestSpider(GGFundNavSpider):
    name = 'FundNav_YiHuInvest'
    sitename = '翼虎投资'
    channel = '投顾净值'

    username = '15538536932'
    password = '123456'
    cookies = 'PHPSESSID=0j0t74bfgft5vlg2pvam4bos14; username=25e9Bug0%2B4rNbzBCso4RWn3Z0EOi%2Fpo41884IVmms%2B0XvwQWvecC0Q; lastlogintime=6992h88Sqso4AzzBqaQpTpWrQBSOqT8DKcjvllCD084ZCQDsRpXO; lastloginip=3e3aTmXzbSxDfFmlwW54AGgXag4YyGlnQZzu8cmSk8aZcKAG8VTyZEAT'
    fps = [
        {'url': 'http://www.szyihu.com/product.php?cid=51',
         'ext': {'type': '1'}}
    ]

    def parse_fund(self, response):
        funds = response.xpath(
            '/html/body/div[4]/div[2]//div[@class="tab_main"]//div/table[1]//tr[position()>1]/td[1]/a')
        for fund in funds:
            url = fund.xpath('./@href').extract_first()
            fund_name = fund.xpath('./text()').extract_first()
            fund_name = fund_name.strip()
            id = re.search(r'id=(\d+)', url).group(1)
            url = 'http://www.szyihu.com/show.php?c=show&id=' + id
            self.ips.append({
                'url': url + '&page=1',
                'ref': response.url,
                'ext': {'fund_name': fund_name, 'page': '1', 'url': url}
            })

    def parse_item(self, response):
        rows = response.xpath('//tr')
        ext = response.meta['ext']
        fund_name = ext['fund_name']
        url = ext['url']
        next_page = response.xpath('/html/body/div/a[text()="下一页"]/@href').re_first(r'&page=(\d+)')
        for row in rows[1:]:
            fund_date = row.xpath('./td[4]/text()').extract_first()
            nav = row.xpath('./td[1]/text()').extract_first()
            added_nav = row.xpath('./td[2]/text()').extract_first()
            item = GGFundNavItem()

            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            try:
                item['statistic_date'] = datetime.strptime(fund_date, '%Y/%m/%d')
            except ValueError:
                continue
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if nav is not None else None
            yield item
        if next_page:
            self.ips.append({
                'url': url + '&page=' + str(next_page),
                'ref': response.url,
                'ext': {'fund_name': fund_name, 'url': url}
            })
