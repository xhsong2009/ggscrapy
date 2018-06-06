from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url


class YinShiInvestSpider(GGFundNavSpider):
    name = 'FundNav_YinShiInvest'
    sitename = '银石投资'
    channel = '投顾净值'

    username = '123'
    password = '123456'
    cookies = 'ASPSESSIONIDCQCSBRCS=BNIPKAKAGFIPCEGMCILKLKEJ; UM_distinctid=1635dde3124186-01657901838b6-3c3c5f0c-15f900-1635dde312535c; ASPSESSIONIDCCSCRQRS=FMENINKBMOECHMBPPCELELDK; ASPSESSIONIDACRBTRRS=DCELAEFCEHDBBLHMGNBEMAPN; CNZZDATA5752077=cnzz_eid%3D616721198-1526285665-http%253A%252F%252Fwww.silver-stone.com.cn%252F%26ntime%3D1527041074'
    fps = [
        {'url': 'http://www.silver-stone.com.cn/product.asp'}
    ]

    def parse_fund(self, response):
        urls = response.xpath(
            '//*[@id="Container"]/div[2]//div[@class="prv_con"]/table//tr/td[1]/a/@href').extract()
        for url in urls:
            url = urljoin(get_base_url(response), url)
            self.ips.append({
                'url': url,
                'ref': response.url
            })

    def parse_item(self, response):
        fund_name = response.xpath('//*[@id="show1"]/table//tr[1]/th[2]/text()').extract_first()
        rows = response.xpath('//*[@id="show2"]/div[2]/table//tr')
        for row in rows[1:]:
            fund_date = row.xpath('./td[2]/text()').extract_first().strip()
            nav = row.xpath('./td[3]/text()').extract_first().strip()
            added_nav = row.xpath('./td[4]/text()').extract_first().strip()
            item = GGFundNavItem()

            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(fund_date, '%Y年%m月%d日')
            item['nav'] = float(nav) if nav is not None else None
            if added_nav is not None and added_nav.count('%') == 0 and added_nav != '-':
                item['added_nav'] = float(added_nav) if nav is not None else None
            yield item
