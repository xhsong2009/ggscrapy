from datetime import datetime
from urllib.parse import urljoin
import html
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class YinShiInvestNoticeSpider(GGFundNoticeSpider):
    name = 'FundNotice_YinShiInvestNotice'
    sitename = '银石投资'
    entry = 'http://www.silver-stone.com.cn/'

    username = '123'
    password = '123456'
    cookies = 'UM_distinctid=16348fa54cf1ad-09ec6f52a4d502-333f5902-1fa400-16348fa54d0394; ASPSESSIONIDAASATQRT=CBOFKHKDLEBFGDJOKPCJADKJ'

    ips = [{
        'url': 'http://www.silver-stone.com.cn/news.asp?tid=2',
        'ref': 'http://www.silver-stone.com.cn/index.asp'
    }]

    def parse_item(self, response):
        next_page = response.xpath('//*[@id="Container"]//form[@name="frmPage"]//span[@class="current"]/following-sibling::a[1]/@href').re_first(r'viewPage\((\d+)\)')
        rows = response.xpath('//*[@id="Container"]/div[2]//div[@class="news_list"]/p')
        for row in rows:
            url = row.xpath('./a/@href').extract_first()
            title = row.xpath('./a/@title').extract_first()
            publish_time = row.xpath('./em/text()').extract_first()
            url = urljoin(get_base_url(response), url)
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item
        if next_page:
            self.ips.append({'url': 'http://www.silver-stone.com.cn/news.asp?tid=2',
                             'ref': response.url,
                             'form': {'m_page': str(next_page)}})
