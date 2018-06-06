from datetime import datetime
from urllib.parse import urljoin
from scrapy import FormRequest
from scrapy.utils.response import get_base_url
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class WayingInvestSpider(GGFundNavSpider):
    name = 'FundNav_WayingInvest'
    sitename = '洼盈投资'
    channel = '投资顾问'

    username = '13916427906'
    password = 'ZYYXSM123'
    cookies ='kerenLogin=userid=13916427906'

    fps = [{
        'url': 'http://www.wytzfund.com/product.aspx?sClass=3&sType=1&oid=18'
    }]

    def start_requests(self):
        yield FormRequest(url='http://www.wytzfund.com/index.aspx')

    def parse_fund(self, response):
        urls = response.xpath('//div[@class="quicksub"]/ul/li')
        for url in urls:
            href = url.xpath('./a/@href').extract_first()
            myurl = urljoin(get_base_url(response), href)
            fund_name = url.xpath('./a/@title').extract_first().replace('(已终结）', '').replace('（已结束）', '').replace('（已终结）', '')
            self.ips.append({
                'url': myurl,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        ext = response.meta['ext']
        fund_names = ext['fund_name']
        rows = response.xpath('//div[@class="text_jz"]//table//tr')
        rows.pop(0)

        item = GGFundNavItem()
        item['sitename'] = self.sitename
        item['channel'] = self.channel
        item['url'] = response.url
        item['fund_name'] = fund_names
        nav = rows.pop(0).xpath("./td[2]//text()").extract_first()
        item['nav'] = float(nav) if nav else None

        added_nav = rows.pop(0).xpath("./td[2]//text()").extract_first()
        item['added_nav'] = float(added_nav) if added_nav else None

        statistic_date = rows.pop(0).xpath(".//td[2]//text()").re_first('\d+-\d+-\d+')
        item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d') if statistic_date else None

        yield item
