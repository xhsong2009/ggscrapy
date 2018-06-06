from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy import FormRequest


class FujianxuchengFutureSpider(GGFundNavSpider):
    name = 'FundNav_FujianxuchengFuture'
    sitename = '旭诚资产'
    channel = '投顾净值'

    username = '13916427906'
    password = 'ZYYXSM'

    fps = [{
        'url': 'http://www.xuchengfund.com/cpjzs.asp'
    }]

    def start_requests(self):
        yield FormRequest(url='http://www.xuchengfund.com/logins.asp',
                          formdata={'mob': '13916427906',
                                    'pass': 'ZYYXSM',
                                    'submit2': '(unable to decode value)'},
                          meta={
                              'handle_httpstatus_list': [302]
                          })

    def parse_fund(self, response):
        urls = response.xpath('/html/body/table[5]/tr/td/table[2]/tr[position()>1]')
        for url in urls:
            href = url.xpath('./td/a/@href').extract_first()
            code = href.rsplit('=', 1)[1]
            fund_name = url.xpath('./td/a/text()').extract_first()
            self.ips.append({
                'url': 'http://www.xuchengfund.com/cpjzs.asp?pid=' + str(code) + '&page=1',
                'ref': response.url,
                'ext': {'code': code, 'fund_name': fund_name}
            })

    def parse_item(self, response):
        ext = response.meta['ext']
        code = ext['code']
        fund_names = ext['fund_name']
        rows = response.xpath('/html/body/table[5]/tr/td[3]/table[5]/tr')
        rows = rows[1:-1]

        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_names

            statistic_date = row.xpath("./td[6]/text()").re_first('\d+-\d+-\d+')
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d') if statistic_date else None

            nav = row.xpath('./td[2]/text()').extract_first()
            item['nav'] = float(nav) if nav else None

            added_nav = row.xpath("./td[3]/text()").extract_first()
            item['added_nav'] = float(added_nav) if added_nav else None
            yield item
        next_url = response.xpath(
            '/html/body/table[5]/tr/td[3]/table[5]/tr[24]/td/table/tr/td[2]/a[text()="下页"]/@href').extract_first()
        if next_url:
            url = urljoin(get_base_url(response), next_url)
            self.ips.append({
                'url': url,
                'ref': response.url,
                'ext': {'code': code, 'fund_name': fund_names}
            })
