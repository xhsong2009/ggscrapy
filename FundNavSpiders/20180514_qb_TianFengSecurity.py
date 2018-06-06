# Department : 保障部
# Author : 钱斌
# Create_date : 2018-05-14

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class TianFengSecuritySpider(GGFundNavSpider):
    name = 'FundNav_TianFengSecurity'
    sitename = '天风证券'
    channel = '券商资管净值'

    fps = [{
        'url': 'http://www.tfzq.com/business/fund.html?sale=0&page=1',
    }]

    def parse_fund(self, response):
        # self.ips.append({'url': 'http://www.tfzq.com/product/jingzhi.html?p_id=18'})
        href_list = response.css('ul.search_result_ul a::attr(href)').extract()
        title_list = response.css('ul.search_result_ul li:first-child::attr(title)').extract()
        next_href = response.css('li.next a::attr(href)').extract_first()
        if next_href not in response.url:
            # 下一页链接最大289页始终能取到，所以做个判断
            self.fps.append({
                'url': 'http://www.tfzq.com' + next_href,
                'ref': response.url,
            })

        for h, t in zip(href_list, title_list):
            self.ips.append({
                'url': 'http://www.tfzq.com' + h,
                'ref': response.url,
                'ext': {'fund_name': t}
            })

    def parse_item(self, response):
        if 'fundDetail' in response.url:
            dt_list = re.findall('x_data.*\[(.*)\];.*var series_data', response.text, re.DOTALL)[0].split(',')
            nav_list = re.findall('var series_data.*"data":\[(.*)\]\},\{', response.text, re.DOTALL)[0].split(',')
            add_nav_list = re.findall('var series_data.*\},\{.*"data":\[(.*)\]\}\];', response.text, re.DOTALL)[
                0].split(',')

            for date, nav, add_nav in zip(dt_list, nav_list, add_nav_list):
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['fund_name'] = response.meta['ext']['fund_name']
                item['channel'] = self.channel
                item['url'] = response.url
                item['nav'] = float(nav.replace('"', '')) if nav else None
                item['added_nav'] = float(add_nav.replace('"', '')) if add_nav else None
                item['statistic_date'] = datetime.strptime(date.replace('"', ''), '%Y-%m-%d') if date else None
                yield item

        if '?p_id=18' in response.url:
            table = response.css('table.table_worth tr')[1:]

            # date = table.xpath('//tr/td[1]/text()').extract()[1:]
            for r in table:
                date = r.xpath('td[1]/text()').extract_first()
                # 点金1期
                fund_name = '点金1期'
                nav = r.xpath('td[2]/text()').extract_first()
                add_nav = r.xpath('td[3]/text()').extract_first()

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['fund_name'] = fund_name
                item['channel'] = self.channel
                item['url'] = response.url
                item['nav'] = float(nav) if nav else None
                item['added_nav'] = float(add_nav) if add_nav else None
                item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d') if date else None
                yield item

                # 点金1期A级
                fund_name = '点金1期A级'
                nav_a = r.xpath('td[4]/text()').extract_first()
                add_nav_a = r.xpath('td[5]/text()').extract_first()

                if nav_a is not None or add_nav_a is not None:
                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['fund_name'] = fund_name
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['nav'] = float(nav_a) if nav else None
                    item['added_nav'] = float(add_nav_a) if add_nav else None
                    item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d') if date else None
                    yield item

                # 点金1期B级
                fund_name = '点金1期B级'
                nav_b = r.xpath('td[6]/text()').extract_first()
                add_nav_b = r.xpath('td[7]/text()').extract_first()
                nav2_b = r.xpath('td[8]/text()').extract_first()

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['fund_name'] = fund_name
                item['channel'] = self.channel
                item['url'] = response.url
                item['nav'] = float(nav_b) if nav_b else None
                item['added_nav'] = float(add_nav_b) if add_nav_b else None
                item['nav_2'] = float(nav2_b) if nav2_b else None
                item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d') if date else None
                yield item
