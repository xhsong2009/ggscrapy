# -*- coding: utf-8 -*-
# Department：保障部
# Author：王卓诚
# Create_Date：2018-05-28


from datetime import datetime
from scrapy import Request
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class WeiLuInvestSpider(GGFundNavSpider):
    name = 'FundNav_WeiLuInvest'
    sitename = '围炉投资'
    channel = '投顾净值'
    allowed_domains = ['www.valuefund.cnm']
    cookies = 'PHPSESSID=r8d5eaibe3dnsca0lrn3phdvn6; 480cc6234107423cdd913fecaebc469a=86; think_template=default'
    username = '13916427906'
    password = 'ZYYXSM123'

    fps = [{
        'url': 'http://www.valuefund.cn/index.php/Product_index_navid_24.html',
        'ref': 'http://www.valuefund.cn'
    }]

    def start_requests(self):
        href = 'userName=%s&password=%s&autoLogin=1' % (self.username, self.password)
        yield Request(
            url='http://www.valuefund.cn/index.php/Home/Members_ajaxLogin.html?' + href)

    def parse_fund(self, response):
        arul = response.xpath('//div[@class="row pro_list"]/div[@class="col-lg-12 col-md-12 col-sm-12"]')
        for uu in arul:
            url = uu.xpath('a/@href').extract_first()
            url = url.replace('/index.php/Product_details_navid_24_goodsid_', '').replace('.html', '')
            url2 = 'http://www.valuefund.cn/index.php/Product_details_navid_24_goodsid_' + url + '_type_unit_p_1.html'
            pname = uu.xpath('a/div[1]/h4/text()').extract_first()
            self.ips.append({
                'url': url2,
                'ref': response.url,
                'pg': 1,
                'ext': {'pname': pname, 'pid': url}
            })

    def parse_item(self, response):
        rows = response.xpath("//table[@class='table table-striped table-hover text-center']/tbody/tr")
        fund_name = response.meta['ext']['pname']
        pid = response.meta['ext']['pid']

        for row in rows:
            statistic_date = row.xpath("./td[1]//text()").extract_first()
            nav = row.xpath("./td[2]//text()").extract_first()
            added_nav = row.xpath("./td[3]//text()").extract_first()
            if len(statistic_date) == 10:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                item['nav'] = float(nav) if nav else None
                item['added_nav'] = float(added_nav) if added_nav else None
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item

        if len(rows) > 2:
            next_pg = response.meta['pg'] + 1
            self.ips.append({
                'url': 'http://www.valuefund.cn/index.php/Product_details_navid_24_goodsid_' + pid + '_type_unit_p_' + str(
                    next_pg) + '.html',
                'pg': next_pg,
                'ext': {'pname': fund_name, 'pid': pid}
            })
