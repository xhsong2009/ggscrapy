from datetime import datetime
from scrapy import FormRequest, Request
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url


class YingDunAssetNavSpider(GGFundNavSpider):
    name = 'FundNav_YingDunAssetNav'
    sitename = '盈盾资本'
    channel = '投资顾问'

    username = 'ZYYXSM'
    password = 'ZYYXSM123'

    fps = [{'url': 'http://www.profitshields.com/plus/list.php?tid=3', 'ref': 'http://www.profitshields.com/index.html'}]

    def start_requests(self):
        yield Request(url='http://www.profitshields.com/member/login.php', callback=self.parse_pre_login)

    def parse_pre_login(self, response):
        url = 'http://www.profitshields.com/member/index_do.php'
        form = {'fmdo': 'login',
                'dopost': 'login',
                'gourl': '',
                'userid': self.username,
                'pwd': self.password,
                'keeptime': '2592000'}
        yield FormRequest(url=url, formdata=form, callback=self.parse_login)

    def parse_login(self, response):
        yield Request(url='http://www.profitshields.com/index.html')

    def parse_fund(self, response):
        funds = response.xpath('/html/body/div[@class="con"]/div[1]/div[1]/ul/li/a')
        for fund in funds[0:(len(funds)-2)]:
            url = fund.xpath('./@href').extract_first()
            fund_name = fund.xpath('./text()').extract_first()
            url = urljoin(get_base_url(response), url)
            self.ips.append({'url': url, 'ext': {'fund_name': fund_name}})

    def parse_item(self, response):
        ext = response.meta['ext']
        fund_name = ext['fund_name']
        rows = response.xpath('//*[@id="blogs_spacerank_2"]/div/table/tbody/tr')
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['fund_name'] = fund_name
            item['channel'] = self.channel
            item['url'] = response.url
            statistic_date = row.xpath('./td[2]//text()').re_first(r'\d+-\d+-\d+')
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            nav = row.xpath('./td[1]//text()').extract_first()
            item['nav'] = float(nav) if nav is not None and nav != '' else None
            added_nav = row.xpath('./td[3]//text()').extract_first()
            item['added_nav'] = float(added_nav) if added_nav is not None and added_nav != '' else None
            yield item
