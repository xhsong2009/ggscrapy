from datetime import datetime
from urllib.parse import urljoin
import html
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
import json


class JinYuanSecuritiesSpider(GGFundNoticeSpider):
    name = 'FundNotice_JinYuanSecurities'
    sitename = '金元证券'
    entry = 'http://www.jyzq.cn/osoa/views/main/asset_management/Asset_list/index.shtml'

    username = '13916427906'
    password = 'ZYYXSM123'
    cookies = 'loginumber=0.5687556305170236201805299827; JSESSIONID=abc2EkbsvGpPE8UPeCPow; _isLoginIn=83@%7C@%7C@1527556127012; user_id=83; nick_name=%E6%9C%9D%E6%9C%9D; userid=0b36ba4b8309331b123cc76bcf2915bc; ismechanism=0; isAccordWith=; url='

    lps = [
        {
            'url': 'http://www.jyzq.cn/servlet/json',
            'form': {'funcNo': '502001', 'pageNum': '1', 'pageSize': '500', 'i_product_small_type': '1',
                     'i_product_stat': '0'},
        },
        {
            'url': 'http://www.jyzq.cn/servlet/json',
            'form': {'funcNo': '502001', 'pageNum': '1', 'pageSize': '500', 'i_product_small_type': '1',
                     'i_product_stat': '1'},
        },
    ]

    def parse_list(self, response):
        funds = json.loads(response.text)['results'][0]['data']
        for fund in funds:
            fund_id = fund['i_product_id']
            i_id = fund['i_id']
            self.ips.append({
                'url': 'http://www.jyzq.cn/servlet/json',
                'form': {'funcNo': '501019', 'pageNum': '1', 'pageSize': '500', 'product_id': fund_id, 'l_article_type': '1'},
                'ext': {'i_id': i_id}
            })
            self.ips.append({
                'url': 'http://www.jyzq.cn/servlet/json',
                'form': {'funcNo': '501019', 'pageNum': '1', 'pageSize': '500', 'product_id': fund_id, 'l_article_type': '2'},
                'ext': {'i_id': i_id}
            })

    def parse_item(self, response):
        i_id = response.meta['ext']['i_id']
        rows = json.loads(response.text)['results'][0]['data']
        for row in rows:
            url = 'http://www.jyzq.cn/osoa/views/main/asset_management/special_assets_list/article_details.shtml?id={0}&i_id={1}&product_id={2}&i_product_small_type=1'.format(
                row['l_article_id'], i_id, row['l_product_id'])
            title = row['l_tiltie']
            publish_time = row['l_creation_time']
            url = urljoin(get_base_url(response), url)
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = html.unescape(title)
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item
