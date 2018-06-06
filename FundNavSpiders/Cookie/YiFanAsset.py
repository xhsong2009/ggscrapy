from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class YiFanAssetSpider(GGFundNavSpider):
    name = 'FundNav_YiFanAsset'
    sitename = '易凡资产'
    channel = '投顾净值'

    username = '13916427906'
    password = 'ZYYXSM123'
    cookies = "CODEIMG=e2a7555f7cabd6e31aef45cb8cda4999; MUSER=13916427906; MENAME=%E9%83%91%E7%9B%8A%E6%98%8E; MEMBERID=248; MEMBERTYPE=%E4%B8%AA%E4%BA%BA%E5%90%88%E6%A0%BC%E6%8A%95%E8%B5%84%E8%80%85; MEMBERTYPEID=35; ZC=d54dc3f140e0b9cf94769bf2fe887796"
    fps = [{'url': 'http://www.zj-yifan.com/product/class/', 'ref': None}]

    def parse_fund(self, response):
        funds = response.xpath(
            '//*[@id="content"]/div[2]//div[@class="pdv_border"]/div[2]//div[@class="picFit"]/a/@href').extract()
        for url in funds:
            url = urljoin(get_base_url(response), url)
            self.ips.append({
                'url': url,
                'ref': response.url,
                'ext': {'page': '1','url': url}
            })

    def parse_item(self, response):
        ext = response.meta['ext']
        url = ext['url']
        page = int(ext['page'])
        next_page = response.xpath('//*[@id="productcontent"]/div[3]/div[2]/select[@name="page"]/option[last()]/text()').re_first(r'(\d+)')
        fund_name = response.xpath('//*[@id="prodtitle"]/text()').extract_first()
        rows = response.xpath('//*[@id="productcontent"]/div[3]/table//tr')
        for row in rows[1:]:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['fund_name'] = fund_name
            item['channel'] = self.channel
            item['url'] = response.url
            nav = row.xpath('./td[1]/text()').extract_first()
            item['nav'] = float(nav)
            added_nav = row.xpath('./td[2]/text()').extract_first()
            item['added_nav'] = float(added_nav)
            statistic_date = row.xpath('./td[3]/text()').extract_first()
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y%m%d')
            yield item
        if page < int(next_page):
            self.ips.append({
                'url': url+'&page='+str(page+1),
                'ref': response.url,
                'ext': {'page': str(page+1), 'url': url}
            })
