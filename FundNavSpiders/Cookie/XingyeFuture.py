from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import json
import re


class XingyeFutureSpider(GGFundNavSpider):
    name = 'FundNav_XingyeFuture'
    sitename = '兴业证券'
    channel = '券商资管净值'

    username = '13916427906'
    password = 'ZYYXSM123'

    cookies = 'JSESSIONID=abcYuzEZfX5ukdUVZbbow; session_id=abck2C5zSNCzjgep7wbow; js_clientno=; js_clientinfo=13916427906; js_clientid=a343c6fbb0ae899789db0bf84ee556345f913a13a86ecc0fa4fec34c68c5e8fbecae051bf63e30eafb1831e19f9f717c6502576715d8d81d5d0badd1b1ad578000d8bd7d0bab541fb189e9a0031156af2afd34dbd7d7bfde87c43dcf2b920e0b5c69859f39c3ec80fec457f1ceb4b97a392a31ec164bae5161dd3d37fc5b60b9; js_clientname=; js_uid=341963; Hm_lvt_9c8d76c7b5119b23db5872e584aba945=1526887338; Hm_lpvt_9c8d76c7b5119b23db5872e584aba945=1526887467; phone_number=13916427906; clientinfo=7f00a222dcb0471cd9b9ace4344efc174e9c1a1d6a140bdf2bcddd166847224d5c5ee6f24efa198cc5bb1adda93a5dfb030b8128d90d87ff27e32c12d80e9966d14fe7c2017f9540a9f9aafd583e599d4b06ce30e669b1bbab901f009b58ef47e5beab4e6b4a012919bb0012e5eeb107021883a44c6b4070548946f8fd61000f; session_id=abck2C5zSNCzjgep7wbow; clientno=; client1_id=a343c6fbb0ae899789db0bf84ee556345f913a13a86ecc0fa4fec34c68c5e8fbecae051bf63e30eafb1831e19f9f717c6502576715d8d81d5d0badd1b1ad578000d8bd7d0bab541fb189e9a0031156af2afd34dbd7d7bfde87c43dcf2b920e0b5c69859f39c3ec80fec457f1ceb4b97a392a31ec164bae5161dd3d37fc5b60b9; clientid=341963; clientname='
    fps = [{
        'url': 'http://www.ixzzcgl.com/servlet/json?funcNo=955621002&key_word=&type_id=&sub_type_id=&p_open_status=&curPage=1&numPerPage=1500&1=1.js'
    }]

    # ips = [{
    #     'url': 'http://www.ixzzcgl.com/servlet/json',
    #     'form': {
    #         'funcNo': '955622011',
    #         'p_code': 'AB0009',
    #         'curPage': '1',
    #         'numPerPage': '1000',
    #     },
    #     'ext': {'fund_name': '金麒麟现金添利'}
    # }]

    def parse_fund(self, response):
        funds = json.loads(response.text)['DataSet'][0]['data']
        for fund in funds:
            fund_code = fund['p_code']
            fund_name = fund['p_abbreviation']
            self.ips.append({
                'url': 'http://www.ixzzcgl.com/servlet/json',
                'form': {
                    'funcNo': '955622011',
                    'p_code': fund_code,
                    'curPage': '1',
                    'numPerPage': '1000',
                },
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = json.loads(response.text)['results'][0]['data']
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel

            codestring = row['p_code']
            item['url'] = 'http://www.ixzzcgl.com/web/views/product/' + str(codestring) + '/product.html'
            item['fund_name'] = fund_name

            statistic_date = row['netvalue_date']
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d') if statistic_date else None
            if fund_name[-1] == '天' or fund_name[-2:] == '天期' or fund_name[-2:] == '份额':
                return
            if fund_name == '金麒麟现金添利' or fund_name == '现金管理1号':
                nav_cur5 = row['nav_cur5']
                nav_cur5 = float(nav_cur5) * 100
                item['d7_annualized_return'] = float(nav_cur5) if nav_cur5 else None
                sum_netvalue = row['sum_netvalue']
                item['income_value_per_ten_thousand'] = float(sum_netvalue) if sum_netvalue else None
            else:
                nav = row['unit_netvalue']
                nav = re.search('[0-9.]+', nav)
                nav = nav.group(0) if nav else None
                item['nav'] = float(nav) if nav else None

                added_nav = row['sum_netvalue']
                added_nav = re.search('[0-9.]+', added_nav)
                added_nav = added_nav.group(0) if added_nav else None
                item['added_nav'] = float(added_nav) if added_nav else None

            yield item
