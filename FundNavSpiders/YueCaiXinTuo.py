import json
from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class YueCaiXinTuoSpider(GGFundNavSpider):
    name = 'FundNav_YueCaiXinTuo'
    sitename = '粤财信托'
    channel = '信托净值'
    entry = 'http://www.utrusts.com'

    fps = [
        {
            'url': 'http://www.utrusts.com/product/list_20_page_1.html',
            'ext': {'type': '1'}
        }
    ]

    def parse_fund(self, response):
        ext = response.meta['ext']
        type = int(ext['type'])
        if type == 1:
            fund_list = response.xpath(
                '//*[@id="warpper"]/section[2]//div[@class="jingzhi"]//div[@class="div5"]/a/@href').extract()
            next_url = response.xpath(
                '//*[@id="warpper"]/section[2]//div[@class="Pages"]//a[@class="a_next"]/@href').extract_first()
            for fund in fund_list:
                url = fund.strip()
                url = self.entry + url
                self.fps.append({
                    'url': url,
                    'ref': response.url,
                    'ext': {'type': '2'}
                })
            if next_url is not None and next_url != 'javascript:void(0);':
                url = self.entry + next_url
                self.fps.append({'url': url, 'ref': response.url, 'ext': {'type': '1'}})
        else:
            url = 'http://www.utrusts.com/Ajax/GetWorthSingleAllData.aspx'
            pro_code = re.search(r'proCode = "(\d+)"', response.text).group(1)
            self.ips.append({
                'url': url,
                'form': {'procode': pro_code},
                'ref': response.url
            })

    def parse_item(self, response):
        datas = json.loads(response.text)
        for data in datas:
            fund_date = data['ProNetDate']
            nav = data['NetWorth']
            nav = re.search('[0-9.]+', nav)
            nav = nav.group(0) if nav else None
            added_nav = data['CumulativeNet']
            added_nav = re.search('[0-9.]+', added_nav)
            added_nav = added_nav.group(0) if added_nav else None
            fund_name = data['ProductCode']

            item = GGFundNavItem()

            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(fund_date, '%Y-%m-%d')
            item['nav'] = float(nav) if nav else None
            item['added_nav'] = float(added_nav) if added_nav else None
            yield item
