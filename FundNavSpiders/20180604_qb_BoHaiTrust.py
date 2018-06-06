# Department : 保障部
# Author : 钱斌
# Create_date : 2018-06-04


from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from datetime import datetime
import re


class BoHaiTrustSpider(GGFundNavSpider):
    name = 'FundNav_BoHaiTrust'
    sitename = '渤海信托'
    channel = '信托净值'
    allowed_domains = ['www.xingrunfund.com']
    start_urls = ['http://www.xingrunfund.com/product.asp']

    fps = [{'url': 'https://www.bohaitrust.com/Other/netvalue/cid/46/lid/47/p/1.html',
            'pg': 1}]

    def parse_fund(self, response):
        href_list = response.css('div.jzlist a::attr(href)').extract()
        for href in href_list:
            self.ips.append({
                'url': 'https://www.bohaitrust.com' + href,
                'ref': response.url,
            })

        if href_list:
            next_pg = response.meta['pg'] + 1
            next_url = re.sub('p/\d+\.', r'p/%s.' % next_pg, response.url)
            self.fps.append({
                'url': next_url,
                'ref': response.url,
                'pg': next_pg
            })

    def parse_item(self, response):
        p_name = response.xpath('//input[@name="productname"]/@value').extract_first()
        date_list = response.xpath('//input[@name="xx"]/@value').extract_first().split(',')
        nav_list = response.xpath('//input[@name="yy"]/@value').extract_first().split(',')
        for d, n in zip(date_list, nav_list):
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = p_name.strip()
            item['statistic_date'] = datetime.strptime(d.strip(), '%Y-%m-%d') if d else None
            item['nav'] = float(n.strip()) if n else None
            yield item

