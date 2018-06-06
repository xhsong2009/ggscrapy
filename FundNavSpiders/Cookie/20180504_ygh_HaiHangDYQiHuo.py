# coding:utf-8
# Department : 保障部
# Author : 袁龚浩
# Create_date : 2018-05-02


from datetime import datetime
from FundNavSpiders import GGFundNavSpider
from FundNavSpiders import GGFundNavItem
import json


class HangHaiDYQiHuoSpider(GGFundNavSpider):
    name = 'FundNav_HaiHangDYQiHuo'
    sitename = '海航东银期货'
    channel = '期货净值'
    allowed_domains = ['www.dyqh.com.cn']
    username = '13916427906'
    password = 'ZYYXSM123'
    # 跑数据前请更换最新cookies，不更换会造成漏抓产品
    cookies = '__guid=98848536.420203476737738300.1516165948645.9883; ASP.NET_SessionId=5yq3xv5kiz4nz5hd5l511jwh; popped=yes; monitor_count=17'

    fps = [{
        'url': 'http://www.dyqh.com.cn/wealth-product.aspx?Index=4&Type=1&BItem=1&Item=0',
        'form': {
            '__VIEWSTATE': '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',
            '__EVENTTARGET': 'pgServer',
            '__EVENTARGUMENT': '1',
        },
        'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'},
        'pg': 1,
    }]

    def parse_fund(self, response):
        pg = response.meta['pg']
        codes = response.xpath('//div[@class = "notice-content-top"]//li//dt/a//@href').extract()
        fund_names = response.xpath('//div[@class = "notice-content-top"]//li//dt/a//p//text()').extract()
        for fund_code, fund_name in zip(codes, fund_names):
            ips_url = 'http://www.dyqh.com.cn/Handler/GetWealthNet.ashx?Id=' + fund_code.split('=')[1]
            self.ips.append({
                'url': ips_url,
                'ref': response.url,
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'},
                'ext': fund_name
            })
        max_page = response.xpath('//div[@id = "pgServer"]//text()').extract()[-4]
        if pg < int(max_page):
            next_pg = pg + 1
            self.fps.append({
                'url': 'http://www.dyqh.com.cn/wealth-product.aspx?Index=4&Type=1&BItem=1&Item=0',
                'form': {
                    '__VIEWSTATE': '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',
                    '__EVENTTARGET': 'pgServer',
                    '__EVENTARGUMENT': str(next_pg),
                },
                'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'},
                'pg': next_pg,
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']
        fund = json.loads(response.text)
        for i in fund:
            item = GGFundNavItem()
            statistic_date = i['NetDate'].replace('0:00:00', '')
            nav = i['NetEstimate']
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date,
                                                       '%Y/%m/%d')
            item['nav'] = float(nav) if nav is not None else None
            yield item
