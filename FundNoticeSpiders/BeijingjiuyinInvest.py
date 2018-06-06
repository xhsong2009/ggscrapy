# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class BeijingjiuyinInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_BeijingjiuyinInvest'
    sitename = '北京久银投资'
    entry = 'http://www.eagle-fund.com/'
    allowed_domains = ['www.eagle-fund.com/']

    def __init__(self, *args, **kwargs):
        super(BeijingjiuyinInvestSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        self.ips.append({
            'url': 'http://www.eagle-fund.com/index.php?m=list&a=index&id=11',
        })
        yield self.request_next()

    def parse_item(self, response):
        rows = response.css('ul.mid_ul_span li')
        for row in rows:
            url = row.xpath('./p[1]/a/@href').extract_first()#获取路径
            url = urljoin(get_base_url(response), url)#拼接绝对路径

            title = row.xpath('./p[1]/a/span/text()').extract_first().strip().replace('\t', '').replace('\r', '').replace('\n', '')#标题

            publish_time = row.xpath('./p[2]/span/text()').extract_first().strip().replace('\t', '').replace('\r', '').replace('\n', '')#时间格式
            publish_time = datetime.strptime(publish_time, '%Y.%m.%d')#转换时间格式

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time
            yield item

        next_url = response.xpath('//ul[@class="pagination mid_page"]/li/a[text()="下一页"]/@href').extract_first()
        if next_url:
            next_url = urljoin(get_base_url(response), next_url)
            self.ips.append({
                'url': next_url,
                'ref': response.url
            })
        yield self.request_next()
