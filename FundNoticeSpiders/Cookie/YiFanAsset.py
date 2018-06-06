from datetime import datetime
from urllib.parse import urljoin
import html
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class YiFanAssetSpider(GGFundNoticeSpider):
    name = 'FundNotice_YiFanAsset'
    sitename = '易凡资产'
    entry = 'http://www.zj-yifan.com/'
    proxy = 1
    username = '13916427906'
    password = 'ZYYXSM123'
    cookies = 'CODEIMG=502cc2c94be1a7c4ca7ef25b8b50bc04; MUSER=13916427906; MENAME=%E9%83%91%E7%9B%8A%E6%98%8E; MEMBERID=248; MEMBERTYPE=%E4%B8%AA%E4%BA%BA%E5%90%88%E6%A0%BC%E6%8A%95%E8%B5%84%E8%80%85; MEMBERTYPEID=35; ZC=d54dc3f140e0b9cf94769bf2fe887796'

    lps = [{
        'url': 'http://www.zj-yifan.com/product/class/',
        'ext': {'type': '1'}
    }]

    def parse_list(self, response):
        type = int(response.meta['ext']['type'])
        if type == 1:
            funds = response.xpath('//*[@id="spdv_16951"]/div/div[2]/div[@class="productquery_dolphin"]')
            for fund in funds:
                url = fund.xpath('.//a/@href').extract_first()
                url = urljoin(get_base_url(response), url)
                self.lps.append({'url': url,
                                 'ref': response.url,
                                 'ext': {'type': '2'}})
        else:
            urls = response.xpath('//*[@id="spdv_17288"]/div//ul[@class="newslist"]/li/a/@href').extract()
            for url in urls:
                url = urljoin(get_base_url(response), url)
                self.ips.append({'url': url,
                                 'ref': response.url})

    def parse_item(self, response):
        url = response.url
        title = response.xpath('//*[@id="newscontent"]/div[1]/text()').extract_first()
        publish_time = response.xpath('//*[@id="newscontent"]/div[2]/text()[1]').re_first('\d+-\d+-\d+ \d+:\d+:\d+')
        url = urljoin(get_base_url(response), url)
        item = GGFundNoticeItem()
        item['sitename'] = self.sitename
        item['channel'] = self.channel
        item['url_entry'] = self.entry
        item['url'] = url
        item['title'] = html.unescape(title)
        item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d %H:%M:%S')
        yield item
