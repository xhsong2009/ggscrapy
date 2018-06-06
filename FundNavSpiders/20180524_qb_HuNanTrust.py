# Department : 保障部
# Author : 钱斌
# Create_date : 2018-05-24

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class HuNanTrustSpider(GGFundNavSpider):
    name = 'FundNav_HuNanTrust'
    sitename = '湖南信托'
    channel = '信托净值'

    trs_key_url = 'http://www.huntic.com/channels/71.html'
    trs_fname = '湖南信托•湘军彭大帅2号证券投资集合资金信托计划'
    fps = [{'url': trs_key_url}]

    def parse_fund(self, response):
        href_list = response.css('div.xxlb a::attr(href)').extract()
        for href in href_list:
            self.ips.append({
                'url': 'http://www.huntic.com' + href,
                'ref': response.url,
                'ext': self.trs_fname
            })

        next_href = response.xpath('//div[@class="pages"]//a[contains(text(),"下一页")]/@href').extract_first()
        if next_href:
            self.fps.append({
                'url': 'http://www.huntic.com' + next_href,
                'ref': response.url,
                'ext': self.trs_fname
            })

    def parse_item(self, response):
        date = response.css('div.nrmb p ::text').re_first('20\d{2}\.\d{2}\.\d{2}')
        if date:
            values = response.css('div.nrmb p ::text').re('\d{1}\.\d{3,}')
            nav = values[0]
            add_nav = values[1]

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['fund_name'] = response.meta['ext']
            item['channel'] = self.channel
            item['url'] = response.url
            item['nav'] = float(nav) if nav else None
            item['added_nav'] = float(add_nav) if add_nav else None
            item['statistic_date'] = datetime.strptime(date, '%Y.%m.%d') if date else None

            yield item
