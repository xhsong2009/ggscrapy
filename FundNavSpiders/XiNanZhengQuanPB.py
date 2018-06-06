import re
from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url


class XiNanZhengQuanPBSpider(GGFundNavSpider):
    name = 'FundNav_XiNanZhengQuanPB'
    sitename = '西南证券'
    channel = '券商PB净值列表'

    fps = [{
        'url': 'http://jdz.swsc.com.cn:8080/tg102/tgSmjj1_getByfilterC.action',
        'ref': 'http://jdz.swsc.com.cn:8080/tg102/tgSmjj1_getByfilterC.action',
        'pg': 1,
        'ext': {'flag': 0}
    }]

    def parse_fund(self, response):
        ext = response.meta['ext']
        flag = ext['flag']
        if flag == 1:
            fund_name = response.meta['ext']['fund_name']
            fund_id = re.split('\?', response.url)[1]
            url = "/tg102/tgProductValue1_getByfilterC.action?pfNa="+fund_name+"&"+fund_id
            self.ips.append({
                'url': urljoin(get_base_url(response), url),
                'ref': response.url,
                'pg': 1,
                'ext': {'fund_name': fund_name}
            })
        else:
            funds = response.xpath('//table[@class="tuoguan_table_porduct"]/tbody/tr/td[2]/a')
            for fund in funds:
                url = fund.xpath('./@href').extract_first()
                fund_name = fund.xpath('normalize-space(./text())').extract_first()
                self.fps.append({
                    'url': urljoin(get_base_url(response), url),
                    'ref': response.url,
                    'pg': 1,
                    'ext': {'flag': 1, 'fund_name': fund_name}
                })
            tp = response.xpath('//span[@class="cpb"]/text()').extract_first()
            tp = re.findall('共(\d+)', tp)[0]
            cp = response.meta['pg']
            if cp < int(tp):
                cp = cp + 1
                self.fps.append({
                    'url': response.url,
                    'ref': response.url,
                    'form': {
                        'search.code': '',
                        'search.productInfo.name': '',
                        'search.state': '',
                        'pagination.pageNum': str(cp),
                        'pagination.pageSize': '10'
                    },
                    'pg': cp,
                    'ext': {'flag': 0}
                })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = response.xpath('//table[@class="tuoguan_table_porduct"]/tbody/tr')
        for row in rows[1:]:
            statistic_date = row.xpath('normalize-space(./td[2]/span/text())').extract_first()
            if statistic_date == '':
                continue
            nav = row.xpath('normalize-space(./td[3]/span/text())').extract_first()
            added_nav = row.xpath('normalize-space(./td[4]/span/text())').extract_first()

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if added_nav is not None else None
            yield item

        tp = response.xpath('//span[@class="cpb"]/text()').extract_first()
        tp = re.findall('共(\d+)', tp)[0]
        cp = response.meta['pg']
        if cp < int(tp):
            cp = cp+1
            self.ips.append({
                'url': response.url,
                'ref': response.url,
                'form': {
                    'search.code': '',
                    'search.productInfo.name': '',
                    'search.state': '',
                    'pagination.pageNum': str(cp),
                    'pagination.pageSize': '10'
                },
                'pg': cp,
                'ext': {'fund_name': fund_name}
            })
