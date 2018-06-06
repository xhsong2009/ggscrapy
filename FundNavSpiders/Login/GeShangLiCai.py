# coding:utf-8

import json
from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from FundNavSpiders import FormRequest


class GeShangLiCaiSpider(GGFundNavSpider):
    name = 'FundNav_GeShangLiCai'
    sitename = '格上理财'
    channel = '第三方净值'

    username = '13916427906'
    password = 'ZYYXSM123'

    def start_requests(self):
        payload = '{"password":"ZYYXSM123","username":"13916427906"}'
        yield FormRequest(
            url='https://www.licai.com/api/v1/auth/login/pass',
            method='PUT',
            body=payload,
            headers={
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json; charset=utf-8',
                'Accept': 'application/json, text/plain, */*'
            },
            callback=self.parse_pre_fund
        )

    def parse_pre_fund(self, response):
        payload = {"offset": '0', "sortName": "rr_since_this_year", "sortType": "-",
                   "investment_strategy_1": "-1", "investment_strategy_2": "0", "annualized_rr_since_start": "-1",
                   "investment_risk": "-1", "achievement_since_this_year": "0", "achievement_in_1_year": "0",
                   "achievement_in_3_year": "0", "achievement_in_5_year": "0", "manager_type": "0",
                   "amac_private_aum": "0", "establishment_date": "0", "product_status": "-1", "keyname": ""}

        self.fps.append({
            'url': "https://www.licai.com/api/v1/private/productlist",
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                'Referer': 'https://www.licai.com/simu/product/',
                'Content-Type': 'application/json; charset=utf-8',
            },
            'body': json.dumps(payload),
            'ext': 0
        })

    def parse_fund(self, response):
        next_offset = response.meta['ext'] + 50
        fund_urls = json.loads(response.text)['result']
        if fund_urls:
            for url in fund_urls:
                fundname = url['product_full_name']
                fund_id = url['product_id']
                self.ips.append({
                    'url': "https://www.licai.com/simu/product/" + fund_id + '.html',
                    'ref': response.url,
                    'ext': fundname
                })

            self.fps.append({
                'url': "https://www.licai.com/api/v1/private/productlist",
                'ref': response.url,
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                    'Referer': 'https://www.licai.com/simu/product/',
                    'Content-Type': 'application/json; charset=utf-8',
                },
                'body': json.dumps({"offset": str(next_offset), "sortName": "rr_since_this_year", "sortType": "-",
                                    "investment_strategy_1": "-1", "investment_strategy_2": "0",
                                    "annualized_rr_since_start": "-1", "investment_risk": "-1",
                                    "achievement_since_this_year": "0", "achievement_in_1_year": "0",
                                    "achievement_in_3_year": "0", "achievement_in_5_year": "0", "manager_type": "0",
                                    "amac_private_aum": "0", "establishment_date": "0", "product_status": "-1",
                                    "keyname": ""}),
                'ext': next_offset
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']
        fund_list = response.xpath('//div[@name ="data"]/div[@class = "nr_con"][1]//table[@class = "tab tab_01"]//tr')
        for i in fund_list:
            t = i.xpath('td//text()').extract()
            statistic_date = ''.join(t[0].split())
            nav = ''.join(t[1].split())

            # 网站复权累计净值不抓取
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            item['nav'] = float(nav)
            yield item

