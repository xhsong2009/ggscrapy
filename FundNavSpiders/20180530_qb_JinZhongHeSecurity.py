# Department : 保障部
# Author : 钱斌
# Create_date : 2018-05-30

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from FundNavSpiders import Request
from urllib import parse
import re


class JinZhongHeSecuritySpider(GGFundNavSpider):
    name = 'FundNav_JinZhongHeSecurity'
    sitename = '金中和'
    channel = '投顾净值'
    username = '朝阳永续'
    password = 'ZYYXSM123'

    fps = [{'url': 'http://www.golden18.com/pzbz.asp?Title=%D0%C5%CD%D0%B2%FA%C6%B7'}]

    def start_requests(self):
        href = '?UserName=%B3%AF%D1%F4%D3%C0%D0%F8&Password=ZYYXSM123&Login=+%B5%C7%C2%BC+'
        yield Request(
            url='http://www.golden18.com/UserLogin.asp' + href,
            meta={
                'dont_redirect': True,
                'handle_httpstatus_list': [302, 301]
            })

    def parse_fund(self, response):
        title_list = response.css('a.left::attr(href)').re('Title=(.*)')

        for title in title_list:
            href = parse.urlencode({'Title': title}, encoding='gb2312')
            self.ips.append({
                'url': 'http://www.golden18.com/product.asp?' + href,
                'ref': response.url,
                'ext': title
            })

    def parse_item(self, response):
        res_text = re.sub('[\s,]', '', response.text)
        target_str = re.findall('单位净值报告(.*)深圳市金中和投资管理有限公司', res_text, re.DOTALL)
        if target_str:
            rows = target_str[0].split('</TR>')
            for tr in rows:
                date = re.findall('\d{4}\.\d{2}\.\d{2}', tr, re.DOTALL)
                nav = re.findall('[^\d\.](\d{2,3}\.\d{2})[^%]', tr, re.DOTALL)
                if date:
                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['fund_name'] = response.meta['ext']
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['nav'] = float(nav[0].strip()) if nav else None
                    item['statistic_date'] = datetime.strptime(date[0].strip(), '%Y.%m.%d') if date else None

                    yield item
