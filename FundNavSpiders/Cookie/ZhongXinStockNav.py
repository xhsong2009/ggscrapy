import json
from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import time
import re


class ZhongXinStockNavSpider(GGFundNavSpider):
    name = 'FundNav_ZhongXinStockNav'
    sitename = '中信证券'
    channel = '券商资管净值'

    username = '13916427906'
    cookies = '__jsluid=1613b909ac9687f95a1714f00e7deaa7; bdshare_firstime=1526364502593; JSESSIONID=MQL9h9VCHqhm8yZp1pvCvsSQyvLz7vnLQFvKjJjGPJNXvhcQ8dDz!-1747417922!541920766; token=eyJjaWQiOiJDU19mZGYwNGRmYjhkZDciLCJkRGF0ZSI6IjE1MjY1MzU2NzY2OTMiLCJ0b2tlbiI6%250AImU0NDAzYTQ5ZDJkMTgzYzQ2OThjMGVmMTQxMmEzMTM0MmQ1OWFiYjMiLCJ0b2tlbkhlYWQiOiJM%250AVDAwMTAiLCJ0b2tlbklkIjoiWk02OEI3NlRDQTgxQ0JaMDc1NzAifQ%253D%253D; code=900022; type=1; Hm_lvt_e64c4cc8f0e3ee65907bf65d0eff8496=1526364472,1526520132; Hm_lpvt_e64c4cc8f0e3ee65907bf65d0eff8496=1526539642; cursel=1'

    fps = [{'url': 'http://www.cs.ecitic.com/productInfo.do?method=getProduct', 'form': {'type': '1'}},
           {'url': 'http://www.cs.ecitic.com/productInfo.do?method=getProduct', 'form': {'type': '2'}},
           {'url': 'http://www.cs.ecitic.com/productWorth.do?method=getProLimitMinList',
            'form': {'keyCode': 'pro_limit_min'}},
           {'url': 'http://www.cs.ecitic.com/productInfo.do?method=getProduct', 'form': {'type': '4'}},
           {'url': 'http://www.cs.ecitic.com/productInfo.do?method=getProduct', 'form': {'type': '5'}},
           {'url': 'http://www.cs.ecitic.com/productInfo.do?method=getProduct', 'form': {'type': '6'}}]

    def parse_fund(self, response):
        cur_url = response.url
        funds = json.loads(response.text)
        if funds:
            if cur_url.count('getProLimitMinList') > 0:
                funds = funds['data']
                for fund in funds:
                    key_code = fund['keyCode']
                    url = 'http://www.cs.ecitic.com/productWorth.do?method=getQxMinByProductTypePage'
                    form = {'keyCode:pro': 'limit_min_qtxl',
                            'currPageNum': '1',
                            'pageRowSize': '50',
                            'firstResult': '0',
                            'maxResult': '50'}
                    self.fps.append({'url': url, 'form': form, 'ref': response.url,
                                     'ext': {'form': form}})
            else:
                funds = funds['list']
                if cur_url.count('getQxMinByProductTypePage') > 0 and len(funds) < 50:
                    url = 'http://www.cs.ecitic.com/productWorth.do?method=getQxMinByProductTypePage'
                    form = response.meta['ext']['form']
                    cur_page = int(form['currPageNum'])
                    form['currPageNum'] = str(cur_page + 1)
                    form['firstResult'] = str(cur_page * 50)
                    form['maxResult'] = str((cur_page + 1) * 50)
                    self.fps.append({'url': url, 'form': form, 'ref': response.url,
                                     'ext': {'form': form}})
                base_url = 'http://www.cs.ecitic.com/proValue.do?method=pagePValue'
                for fund in funds:
                    form = {'startTime': '',
                            'pCode': '',
                            'currPageNum': '1',
                            'pageRowSize': '100',
                            'firstResult': '0',
                            'maxResult': '100'}
                    fund_name = fund['productName']
                    fund_id = fund['productCode']
                    form['pCode'] = str(fund_id)
                    self.ips.append({'url': base_url, 'form': form, 'ref': response.url,
                                     'ext': {'fund_name': fund_name, 'form': form}})

    def parse_item(self, response):
        ext = response.meta['ext']
        form = ext['form']
        page = int(form['currPageNum'])
        rows = json.loads(response.text)
        rows = rows['list']
        fund_name = ext['fund_name']
        if len(rows) > 0:
            base_url = 'http://www.cs.ecitic.com/proValue.do?method=pagePValue'
            form['currPageNum'] = str(page + 1)
            form['firstResult'] = str(page * 100)
            form['maxResult'] = str((page + 1) * 100)
            self.ips.append(
                {'url': base_url, 'form': form, 'ref': response.url, 'ext': {'fund_name': fund_name, 'form': form}})
            for row in rows:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                statistic_date = row['submitDate']['time']
                statistic_date = time.localtime(int(statistic_date) / 1000)
                statistic_date = time.strftime('%Y-%m-%d', statistic_date)
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                if row['mwfRate'] and row['qrnhRate']:
                    income_value_per_ten_thousand = row['mwfRate']
                    income_value_per_ten_thousand = re.search('[0-9.]+', income_value_per_ten_thousand)
                    income_value_per_ten_thousand = income_value_per_ten_thousand.group(0) if income_value_per_ten_thousand else None
                    item['income_value_per_ten_thousand'] = float(
                        income_value_per_ten_thousand) if income_value_per_ten_thousand else None

                    d7_annualized_return = row['qrnhRate']
                    d7_annualized_return = re.search('[0-9.]+', d7_annualized_return)
                    d7_annualized_return = d7_annualized_return.group(0)if d7_annualized_return else None
                    item['d7_annualized_return'] = float(d7_annualized_return) if d7_annualized_return else None
                elif row['yearRate']:
                    annualized_return = row['yearRate']
                    annualized_return = re.search('[0-9.]+', annualized_return)
                    annualized_return = annualized_return.group(0) if annualized_return else None
                    item['annualized_return'] = float(annualized_return) if annualized_return else None
                else:
                    nav = row['dateValue']
                    item['nav'] = float(nav) if nav is not None else None

                    added_nav = row['totalValue']
                    item['added_nav'] = float(added_nav) if added_nav is not None else None
                yield item
