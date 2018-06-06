from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
import json


class XingyeSecuriesSpider(GGFundNoticeSpider):
    name = 'FundNav_XingyeSecuries'
    sitename = '兴业证券'
    url_entry = 'http://www.ixzzcgl.com/web/views/product/index.html'
    username = '13916427906'
    password = 'ZYYXSM123'

    cookies = 'JSESSIONID=abcYuzEZfX5ukdUVZbbow; session_id=abck2C5zSNCzjgep7wbow; js_clientno=; js_clientinfo=13916427906; js_clientid=a343c6fbb0ae899789db0bf84ee556345f913a13a86ecc0fa4fec34c68c5e8fbecae051bf63e30eafb1831e19f9f717c6502576715d8d81d5d0badd1b1ad578000d8bd7d0bab541fb189e9a0031156af2afd34dbd7d7bfde87c43dcf2b920e0b5c69859f39c3ec80fec457f1ceb4b97a392a31ec164bae5161dd3d37fc5b60b9; js_clientname=; js_uid=341963; Hm_lvt_9c8d76c7b5119b23db5872e584aba945=1526887338; Hm_lpvt_9c8d76c7b5119b23db5872e584aba945=1526887467; phone_number=13916427906; clientinfo=7f00a222dcb0471cd9b9ace4344efc174e9c1a1d6a140bdf2bcddd166847224d5c5ee6f24efa198cc5bb1adda93a5dfb030b8128d90d87ff27e32c12d80e9966d14fe7c2017f9540a9f9aafd583e599d4b06ce30e669b1bbab901f009b58ef47e5beab4e6b4a012919bb0012e5eeb107021883a44c6b4070548946f8fd61000f; session_id=abck2C5zSNCzjgep7wbow; clientno=; client1_id=a343c6fbb0ae899789db0bf84ee556345f913a13a86ecc0fa4fec34c68c5e8fbecae051bf63e30eafb1831e19f9f717c6502576715d8d81d5d0badd1b1ad578000d8bd7d0bab541fb189e9a0031156af2afd34dbd7d7bfde87c43dcf2b920e0b5c69859f39c3ec80fec457f1ceb4b97a392a31ec164bae5161dd3d37fc5b60b9; clientid=341963; clientname='
    lps = [{
        'url': 'http://www.ixzzcgl.com/servlet/json?funcNo=955621002&key_word=&type_id=&sub_type_id=&p_open_status=&curPage=1&numPerPage=1500&1=1.js'
    }]

    def parse_list(self, response):
        funds = json.loads(response.text)['DataSet'][0]['data']
        for fund in funds:
            fund_code = fund['p_code']
            self.ips.append({
                'url': 'http://www.ixzzcgl.com/servlet/json',
                'form': {
                    'funcNo': '955622004',
                    'keyword': fund_code,
                    'curPage': '1',
                    'length': '80',
                    'rowOfPage': '500',
                },
            })
            self.ips.append({
                'url': 'http://www.ixzzcgl.com/web/views/product/{}/product.html'.format(fund_code),
                'ref': response.url
            })

    def parse_item(self, response):
        if 'json' in response.url:
            rows = json.loads(response.text)['data']
            for row in rows:
                item = GGFundNoticeItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url_entry'] = self.url_entry
                url = row['weburl']
                item['url'] = 'http://www.ixzzcgl.com' + url
                item['title'] = row['short_title']
                publish_time = row['notice_date']
                item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d') if publish_time else None

                yield item
        else:
            rows = response.xpath('//div[@class="dync_state dashed_bd"][2]/a')
            for row in rows:
                item = GGFundNoticeItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url_entry'] = self.url_entry
                url = row.xpath('./@href').extract_first()
                item['url'] = 'http://www.ixzzcgl.com' + url
                item['title'] = row.xpath('./b/text()').extract_first()
                publish_time = row.xpath('./em/text()').extract_first()
                item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d') if publish_time else None
                yield item
