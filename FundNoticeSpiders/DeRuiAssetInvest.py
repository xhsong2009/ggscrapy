from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url


class DeRuiAssetInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_DeRuiAssetInvest'
    sitename = '杭州德锐资本投资'
    entry = 'http://www.winner98.net'

    lps = [
        {
            'url': 'http://www.winner98.net/news/typeid-3.html',
            'ref': None
        }
    ]

    def parse_list(self, response):
        noticeList = response.xpath('/html/body/div[@class="xiangqing"]/ul/li')
        for notice in noticeList:
            noticeLink = notice.xpath('./a/@href').extract_first().strip()
            title = notice.xpath('./h2/text()').extract_first()
            publish_time = notice.xpath('./h3/text()').extract_first()
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = urljoin(get_base_url(response), noticeLink)
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item
