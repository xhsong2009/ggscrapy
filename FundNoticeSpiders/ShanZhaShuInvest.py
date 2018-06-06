from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url


class ShanZhaShuInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_ShanZhaShuInvest'
    sitename = '山楂树投资'
    entry = 'http://www.hawthorninvest.com/'

    lps = [
        {
            'url': 'http://www.hawthorninvest.com/asset/dynamic',
            'ref': None
        }
    ]

    def parse_list(self, response):
        notices = response.xpath('/html/body/div[4]//div[@class="trends"]/dl')
        for notice in notices:
            url = notice.xpath('./dd/a/@href').extract_first().strip()
            url = urljoin(get_base_url(response), url)
            title = notice.xpath('./dd/a/h3/text()').extract_first()
            publish_time_year = notice.xpath('./dt/text()').extract_first()
            publish_time_day = notice.xpath('./dt/b/text()').extract_first()
            publish_time = publish_time_year + '-' +  publish_time_day

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time.strip(), '%Y-%m-%d')
            yield item
        next_page = response.xpath('/html/body/div[4]/div[2]/div[@class="paging"]//a[text()="下一页"]/@href').extract_first()
        if next_page is not None and next_page != 'javascript:':
            next_url = urljoin(get_base_url(response), next_page)
            self.lps.append({
                'url': next_url,
                'ref': response.url,
            })
