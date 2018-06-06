from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
import re


class ZhaoShangStockSpider(GGFundNavSpider):
    name = 'FundNav_ZhaoShangStock'
    sitename = '招商证券'
    channel = '券商资管净值'

    fps = [
        {
            'url': 'http://www.newone.com.cn/ws/html?arg=4financing/880014/2&',
            'ext': {'type': '1'}
        }
    ]

    def parse_fund(self, response):
        ext = response.meta['ext']
        type = int(ext['type'])
        if type == 1:
            funds = response.xpath('//*[@id="menu_list"]/li[3]/dl/dd/a')
            for fund in funds:
                url = fund.xpath('./@href').extract_first()
                fund_name = fund.xpath('./text()').extract_first()
                url = urljoin(get_base_url(response), url)
                self.fps.append({
                    'url': url,
                    'ref': response.url,
                    'ext': {'type': '2', 'fund_name': fund_name}
                })
        else:
            page_url = response.url
            # fund_name = response.xpath(
            #     '//*[@id="right"]/div[6]//table[@class="cont_table"]//td/*[text()="产品全称"]/../../td[2]/text()').extract_first()
            # if fund_name is None or fund_name == '':
            fund_name = ext['fund_name']
            jhdm = re.search(r'financing\/(\d+)\/', page_url).group(1)
            url = 'http://www.newone.com.cn/jzlb'
            self.ips.append({
                'url': url + '?page=1&jhdm=' + str(jhdm),
                'ref': response.url,
                'ext': {'fund_name': fund_name, 'page': '1', 'jhdm': str(jhdm)}
            })

    def parse_item(self, response):
        ext = response.meta['ext']
        page = int(ext['page'])
        jhdm = str(ext['jhdm'])
        fund_name = ext['fund_name']
        line = response.text
        funds = response.xpath('//table//tr')
        titles = funds.pop(0).xpath('./td/text()').extract()
        url = 'http://www.newone.com.cn/jzlb?page=' + str(page + 1) + '&jhdm=' + str(jhdm)
        i = len(funds) - 1
        if i >= 20:
            self.ips.append({
                'url': url,
                'ref': response.url,
                'ext': {'fund_name': fund_name, 'page': str(page + 1), 'jhdm': str(jhdm)}
            })
        for fund in funds[0:i]:
            fund_date = fund.xpath('./td[1]/text()').extract_first()
            nav = None
            added_nav = None
            d7_annualized_return = None
            income_value_per_ten_thousand = None
            if titles.count('单位净值（元）') > 0:
                nav = fund.xpath('./td[2]/text()').extract_first()
            if titles.count('累计净值（元）') > 0:
                added_nav = fund.xpath('./td[3]/text()').extract_first()
            if titles.count('每万份计划净收益（元）') > 0:
                income_value_per_ten_thousand = fund.xpath('./td[2]/text()').extract_first()
            if titles.count('七日年化收益率') > 0:
                d7_annualized_return = fund.xpath('./td[3]/text()').re_first(r'(\d+\.\d+)\%')
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(fund_date, '%Y-%m-%d')
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if added_nav is not None else None
            item['d7_annualized_return'] = float(d7_annualized_return) if d7_annualized_return is not None else None
            item['income_value_per_ten_thousand'] = float(
                income_value_per_ten_thousand) if income_value_per_ten_thousand is not None else None
            yield item

