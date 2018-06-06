
from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
import re


class XiNanStockSpider(GGFundNavSpider):
    name = 'FundNav_XiNanStock'
    sitename = '西南证券'
    channel = '券商资管净值'

    fps = [{
        'url': 'http://www.swsc.com.cn/xnsecu/cpzx/jhlc.jsp?classid=0001000100120011'
    }]

    def parse_fund(self, response):
        funds = response.xpath('/html/body/div[3]/div[2]/div[@class="cl_cats"]/ul/li/a/@title').extract()
        base_url = 'http://www.swsc.com.cn/xnsecu/cpzx/jhjzss.jsp?pageno=1&hrefURL=&filter=&channelId='
        for channel_id in funds:
            url = base_url + str(channel_id)
            self.ips.append({'url': url, 'ref': response.url, 'ext': {'page': '1', 'channel_id': str(channel_id)}})

    def parse_item(self, response):
        ext = response.meta['ext']
        page = int(ext['page'])
        channel_id = ext['channel_id']
        rows = response.xpath('//tr')
        fund_name = response.xpath('//tr[1]/th[2]/text()').extract_first()
        if len(rows) > 2:
            head_titles = rows[1].xpath('./th/text()').extract()
            for row in rows[2:]:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['fund_name'] = fund_name
                item['channel'] = self.channel
                item['url'] = response.url
                date = row.xpath('./td[1]/text()').extract_first()
                item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d') if date else None
                if head_titles.count('单位净值') > 0 or head_titles.count('单位净值(参考)') > 0:
                    nav = row.xpath('./td[2]/text()').extract_first()
                    item['nav'] = float(nav) if nav else None
                if head_titles.count('累计净值') > 0 or head_titles.count('累计净值(参考)') > 0:
                    added_nav = row.xpath('./td[3]/text()').extract_first()
                    item['added_nav'] = float(added_nav) if added_nav else None
                if head_titles.count('七日年化收益') > 0:
                    d7_annualized_return = row.xpath('./td[2]/text()').extract_first()
                    item['d7_annualized_return'] = float(d7_annualized_return) if d7_annualized_return else None
                if head_titles.count('每万分收益') > 0:
                    income_value_per_ten_thousand = row.xpath('./td[3]/text()').extract_first()
                    item['income_value_per_ten_thousand'] = float(income_value_per_ten_thousand) if income_value_per_ten_thousand else None
                yield item
            base_url = 'http://www.swsc.com.cn/xnsecu/cpzx/jhjzss.jsp?hrefURL=&filter=&channelId='
            url = base_url + str(channel_id)
            url = url + '&pageno=' + str(page+1)
            self.ips.append({'url': url, 'ref': response.url, 'ext': {'page': str(page+1), 'channel_id': str(channel_id)}})
