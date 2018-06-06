# Department : 保障部
# Author : 钱斌
# Create_date : 2018-06-01
# Alter_date : 2018-06-01

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class GuoDuSecuritiesSpider(GGFundNavSpider):
    name = 'FundNav_GuoDuSecurities'
    sitename = '国都证券'
    channel = '券商资管净值'

    fps = [{'url': 'http://www.guodu.com/finance/financing_zxjz.jsp'}]

    def parse_fund(self, response):
        pid_list = response.css('div.container_common td a::attr(href)').re('productMore\.jsp\?(.*)')
        pname_list = response.css('div.container_common td a::text').extract()
        stamp = int(datetime.now().timestamp() * 1000)
        for pid, pname in zip(pid_list, pname_list):
            self.ips.append({
                'url': 'http://www.guodu.com/finance/ajax/product_cpjz.jsp?' + pid + '&random=%s' % stamp,
                'form': {
                    'byAjax': '1',
                    'pagesize': '200',
                    'pageNo': '1',
                    'status': '2',
                    'columnid': '3'
                },
                'ref': response.url,
                'pg': 1,
                'ext': re.sub('（.*|\(.*', '', pname)
            })

    def parse_item(self, response):
        rows = response.css('tr')
        f_name = response.meta['ext']
        col_cnt = len(response.css('tr.tr_class_color ::text').re('\S+'))
        col_str = '/'.join(response.css('tr.tr_class_color ::text').re('\S+'))
        for r in rows[1:-1]:
            date = r.xpath('td[1]/text()').extract_first()
            item = GGFundNavItem()
            if '七日年化' in response.text:
                per_ten = r.xpath('td[2]/text()').extract_first()
                d7 = r.xpath('td[3]/text()').extract_first()
                item['sitename'] = self.sitename
                item['fund_name'] = f_name
                item['channel'] = self.channel
                item['url'] = response.url
                item['income_value_per_ten_thousand'] = float(per_ten) if per_ten else None
                item['d7_annualized_return'] = float(d7) if d7 else None
                item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d') if date else None
                yield item

            elif '优先级' in col_str:
                fund_name = f_name
                if col_cnt == 5 and '中间级' in col_str:
                    nav = r.xpath('td[2]/text()').extract_first()
                    item['sitename'] = self.sitename
                    item['fund_name'] = fund_name
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['nav'] = float(nav) if nav else None
                    item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d') if date else None
                    yield item

                    nav_middle = r.xpath('td[3]/text()').extract_first()
                    item['sitename'] = self.sitename
                    item['fund_name'] = f_name + '优先级'
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['nav'] = float(nav_middle) if nav_middle else None
                    item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d') if date else None
                    yield item

                    nav_ordinary = r.xpath('td[4]/text()').extract_first()
                    item['sitename'] = self.sitename
                    fund_name = f_name + '中间级'
                    item['fund_name'] = fund_name
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['nav'] = float(nav_ordinary) if nav_ordinary else None
                    item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d') if date else None
                    yield item

                    nav_ordinary = r.xpath('td[5]/text()').extract_first()
                    item['sitename'] = self.sitename
                    fund_name = f_name + '普通级'
                    item['fund_name'] = fund_name
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['nav'] = float(nav_ordinary) if nav_ordinary else None
                    item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d') if date else None
                    yield item

                else:
                    nav = r.xpath('td[2]/text()').extract_first()
                    add_nav = r.xpath('td[5]/text()').extract_first()
                    item['sitename'] = self.sitename
                    item['fund_name'] = fund_name
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['nav'] = float(nav) if nav else None
                    item['added_nav'] = float(add_nav) if add_nav else None
                    item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d') if date else None
                    yield item

                    nav_priority = r.xpath('td[3]/text()').extract_first()
                    add_nav_priority = r.xpath('td[6]/text()').extract_first()
                    item['sitename'] = self.sitename
                    item['fund_name'] = f_name + '优先级'
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['nav'] = float(nav_priority) if nav_priority else None
                    item['added_nav'] = float(add_nav_priority) if add_nav_priority else None
                    item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d') if date else None
                    yield item

                    nav_ordinary = r.xpath('td[4]/text()').extract_first()
                    add_nav_ordinary = r.xpath('td[7]/text()').extract_first()
                    item['sitename'] = self.sitename
                    if '进取级' in col_str:
                        fund_name = f_name + '进取级'
                    elif '普通级' in col_str:
                        fund_name = f_name + '普通级'
                    item['fund_name'] = fund_name
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['nav'] = float(nav_ordinary) if nav_ordinary else None
                    item['added_nav'] = float(add_nav_ordinary) if add_nav_ordinary else None
                    item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d') if date else None
                    yield item

            elif 'B类份额' in response.text:
                nav = r.xpath('td[2]/text()').extract_first()
                add_nav = r.xpath('td[5]/text()').extract_first()
                item['sitename'] = self.sitename
                item['fund_name'] = f_name
                item['channel'] = self.channel
                item['url'] = response.url
                item['nav'] = float(nav) if nav else None
                item['added_nav'] = float(add_nav) if add_nav else None
                item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d') if date else None
                yield item

                nav_a = r.xpath('td[3]/text()').extract_first()
                add_nav_a = r.xpath('td[6]/text()').extract_first()
                item['sitename'] = self.sitename
                item['fund_name'] = f_name + 'A类'
                item['channel'] = self.channel
                item['url'] = response.url
                item['nav'] = float(nav_a) if nav_a else None
                item['added_nav'] = float(add_nav_a) if add_nav_a else None
                item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d') if date else None
                yield item

                nav_b = r.xpath('td[4]/text()').extract_first()
                add_nav_b = r.xpath('td[7]/text()').extract_first()
                item['sitename'] = self.sitename
                item['fund_name'] = f_name + 'B类'
                item['channel'] = self.channel
                item['url'] = response.url
                item['nav'] = float(nav_b) if nav_b else None
                item['added_nav'] = float(add_nav_b) if add_nav_b else None
                item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d') if date else None
                yield item

            else:
                nav = r.xpath('td[2]/text()').extract_first()
                add_nav = r.xpath('td[3]/text()').extract_first()
                item['sitename'] = self.sitename
                item['fund_name'] = f_name
                item['channel'] = self.channel
                item['url'] = response.url
                item['nav'] = float(nav.replace('..', '.')) if nav else None
                item['added_nav'] = float(add_nav.replace('..', '.')) if add_nav else None
                item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d') if date else None
                yield item

        if len(rows) > 2:
            next_pg = response.meta['pg'] + 1
            self.ips.append({
                'url': response.url,
                'form': {
                    'byAjax': '1',
                    'pagesize': '200',
                    'pageNo': str(next_pg),
                    'status': '2',
                    'columnid': '3'
                },
                'ref': response.url,
                'pg': next_pg,
                'ext': f_name
            })
