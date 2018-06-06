from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class TaoXuanYouShengAssetSpider(GGFundNoticeSpider):
    name = 'FundNotice_TaoXuanYouShengAsset'
    sitename = '深圳前海韬选优胜资产'
    entry = 'http://www.txysa.com/'

    lps = [
        {
            'url': 'http://www.txysa.com/news.php?cid=146',
            'ref': None
        }
    ]

    def parse_list(self, response):
        noticeList = response.xpath('//div[@class="r_news"]/ul/li')
        for notice in noticeList:
            noticeLink = notice.xpath('./a/@href').extract_first().strip()
            noticeLink = urljoin(get_base_url(response), noticeLink)
            title = notice.xpath('./a/text()').extract_first()
            publish_time = notice.xpath('./em/text()').extract_first()

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = noticeLink
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        next_url = response.xpath('//div[@class="quotes"]/a[contains(text(), "下一页")]/@href').extract_first()
        if next_url is not None:
            self.lps.append({'url': urljoin(get_base_url(response), next_url), 'ref': response.url})
