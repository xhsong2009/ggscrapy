# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-02

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy import Request
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url


class GuoLianZhengQuanSecutiesSpider(GGFundNavSpider):
    name = 'FundNav_GuoLianZhengQuanSecuties'
    sitename = '国联证券'
    channel = '券商资管净值'

    username = '13228803'
    cookies = 'JSESSIONID=F27241BAFE251EC87E7FE95412FCE0EA; UM_distinctid=162f6c25511322-0c2a257239f065-3c604504-15f900-162f6c25512358; CNZZDATA5813404=cnzz_eid%3D488101347-1524553576-%26ntime%3D1524701933; lcLastUrl="http://www.glsc.com.cn/glzq/financing/management/gf_4.jsp"'

    def start_requests(self):
        yield Request(
            url='http://www.glsc.com.cn/glzq/financing/management/management_business.html?sub_top=FinancingIndex&child_top=management_business',
            callback=self.parse_pre_fund)

    def parse_pre_fund(self, response):
        fund_urls = response.xpath("//div[@id='menu_zzjsnet' or @id='menu_yzz' or  @id='menu_abc']/ul//a")
        for url in fund_urls:
            fund_url = url.xpath("./@href").extract_first()
            fund_url = urljoin(get_base_url(response), fund_url)
            self.fps.append({
                'url': fund_url,
                'ref': response.url,
            })

    def parse_fund(self, response):
        fund_into = response.xpath("//table[@id='News4']")
        fund_urls = fund_into.xpath('.//tr')
        urls = fund_urls.xpath('.//@src').extract()
        name = fund_urls.xpath('./td//text()').extract()
        names = [i for i in name if ' ' not in i]
        for i in zip(urls, names):
            fund_url = i[0]
            fund_name = i[1].replace('集合净值', '').replace('收益', '').replace('预估年化收益率', '')
            self.ips.append({
                'url': 'http://www.glsc.com.cn' + fund_url + '&current_page=1',
                'pg': 1,
                'ref': response.url,
                'ext': {'fund_name': fund_name},
            })

    def parse_item(self, response):
        rows = response.xpath("//tr[@class='table-td2']")
        fund_name = response.meta['ext']['fund_name']
        if len(rows) > 0:
            for row in rows:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                if '预估年化收益率' in response.xpath('//tr[@class="table-title1"]/td[1]/text()').extract_first():
                    statistic_date = row.xpath("./td[2]//text()").extract_first()
                    item['statistic_date'] = datetime.strptime(statistic_date, '%Y/%m/%d')
                    annualized_return = row.xpath('./td[1]//text()').extract_first()
                    item['annualized_return'] = float(annualized_return) if annualized_return else None
                elif '七日年化收益率' in response.xpath('//tr[@class="table-title1"]/td[3]/text()').extract_first():
                    statistic_date = row.xpath("./td[1]//text()").extract_first()
                    item['statistic_date'] = datetime.strptime(statistic_date, '%Y/%m/%d')
                    d7_annualized_return = row.xpath('./td[2]//text()').extract_first()
                    income_value_per_ten_thousand = row.xpath('./td[3]//text()').re_first('[0-9.]+')
                    item['d7_annualized_return'] = float(d7_annualized_return)
                    item['income_value_per_ten_thousand'] = float(income_value_per_ten_thousand)
                else:
                    nav = row.xpath('./td[1]//text()').extract_first()
                    add_nav = row.xpath('./td[2]//text()').extract_first()
                    item['nav'] = float(nav)if nav else None
                    item['added_nav'] = float(add_nav)if add_nav else None
                    statistic_date = row.xpath("./td[3]//text()").extract_first()
                    item['statistic_date'] = datetime.strptime(statistic_date, '%Y/%m/%d')
                yield item

            pg = response.meta['pg']
            next_pg = int(pg) + 1
            next_url = response.url.replace('current_page=' + str(pg), 'current_page=' + str(next_pg))
            self.ips.append({
                'url': next_url,
                'ref': response.url,
                'pg': next_pg,
                'ext': {'fund_name': fund_name.replace('净值', '')},

            })
