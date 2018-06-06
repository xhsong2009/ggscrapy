from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
import re


class ZunDaoAssetSpider(GGFundNavSpider):
    name = 'FundNav_ZunDaoAsset'
    sitename = '尊道投资'
    channel = '投资顾问'

    fps = [{
        'url': 'http://www.topwayinvest.com/product.aspx?&jsid=3',
        'ext': {'type': '1'}
    }]

    username = '15838867575'
    password = '123456'
    cookies = 'ASP.NET_SessionId=tx24lhz5hqk3ko45jxmna4bp; UserNmae=123; UserId=99'

    def parse_fund(self, response):
        link_list = response.xpath('//ul[@class = "lmenu"]//li/a//@href').extract()

        type = response.meta['ext']['type']
        if type == '1':
            for link in link_list:
                self.fps.append({
                    'url': 'http://www.topwayinvest.com/' + link,
                    'ref': response.url,
                    'ext': {'type': '2'}
                })
        if type == '2':
            rows = response.xpath('//table[@class = "pro_table all productAll"]//tr')[1:]
            for row in rows:
                fund_id = re.search(r'cateid=(\d+)', row.xpath('./td[1]/a/@href').extract_first()).group(1)
                fund_url = row.xpath('./td[1]/a/@href').extract_first()
                fund_name = row.xpath('./td[1]/a/@title').extract_first()
                url = urljoin(get_base_url(response), fund_url)
                self.ips.append({
                    'url': url,
                    'form': {'id': str(fund_id), 'action': '1'},
                    'ref': response.url,
                    'ext': {'fund_name': fund_name}
                })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        # //*[@id="con_one_4"]/table/tbody/tr[1]
        datas = response.xpath('//*[@id="con_one_4"]/table//tr')
        for row in datas[1:]:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name

            statistic_date = row.xpath('./td[1]/text()').extract_first().strip()
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            nav = row.xpath('./td[2]/text()').extract_first().strip()
            nav = nav.replace('元', '')
            item['nav'] = float(nav) if nav is not None else None

            added_nav = row.xpath('./td[4]/text()').extract_first().strip()
            added_nav = added_nav.replace('元', '')
            item['added_nav'] = float(added_nav) if added_nav != '' else None

            yield item
