from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class YuanCeAssetSpider(GGFundNavSpider):
    name = 'FundNav_YuanCeAsset'
    sitename = '远策投资'
    channel = '投顾净值'

    fps = [{
        'url': 'http://www.yuancefund.com/newslist.php?cid=7',
        'ext': {'type': '1'}
    }]

    username = 'ZYYXSM'
    password = 'ZYYXSM123.'
    cookies = 'PHPSESSID=iddm66nipb4jh4fs477up8k2n1; yunsuo_session_verify=0ae6a7abca5f16cc0006651628c8893d'

    def parse_fund(self, response):
        link_list = response.xpath('//div[@class = "pro_class"]/a/@href').extract()
        type = response.meta['ext']['type']
        if type == '1':
            for link in link_list:
                cid = re.search(r'newslist\.php\?cid=(\d+)', link).group(1)
                self.fps.append({
                    'url': 'http://www.yuancefund.com/newslist.php?cid=' + cid,
                    'ref': response.url,
                    'ext': {'type': '2'}
                })
        if type == '2':
            rows = response.xpath('//ul[@id = "mycarousel"]/li/a')
            for row in rows:
                cid = re.search(r'newslist\.php\?cid=(\d+)', row.xpath('./@href').extract_first()).group(1)
                fund_name = row.xpath('./@title').extract_first()

                self.ips.append({
                    'url': 'http://www.yuancefund.com/newslist.php?cid=' + cid + '&t=1',
                    'ref': response.url,
                    'ext': {'fund_name': fund_name}
                })
        yield self.request_next()

    def parse_item(self, response):
        datas = response.xpath('//div[@class="li"]/table//tr')
        for row in datas[1:]:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = row.xpath('./td[1]/text()').extract_first().strip()

            statistic_date = row.xpath('./td[2]/text()').extract_first().strip()
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

            nav = row.xpath('./td[3]/text()').extract_first().strip()
            item['nav'] = float(nav) if nav is not None else None

            yield item
