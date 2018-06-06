# -*- coding: utf-8 -*-

from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from scrapy import FormRequest


class AnzhouInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_AnzhouInvest'
    sitename = '安州投资'
    entry = 'http://www.anzhouinvest.com/'

    username = '1164281722@qq.com'
    password = '123456'

    ips = [{
        'url': 'http://www.anzhouinvest.com/News_index_catid_2_p_1.html',
    }]

    def start_requests(self):
        yield FormRequest(url='http://anzhouinvest.com/Home/Member_login.html',
                          formdata={'email': '1164281722@qq.com',
                                    'password': '123456',
                                    'submit': '提    交'
                                    })

    def parse_item(self, response):
        rows = response.xpath('//div[@class="news_list team_box"]/ul/li')

        for row in rows:
            url = row.xpath('./a/@href').extract_first()
            url = urljoin(get_base_url(response), url)

            title = row.xpath('./a/@title').extract_first().replace('\t', '').replace('\r', '').replace('\n', '')

            publish_time = row.xpath('./a/em/text()').extract_first()#2018-05-28
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time

            yield item

        next_url = response.xpath('//div[@class="page_list f_r"]/div/a[contains(text(),"下一页")]/@href').extract_first()
        if next_url:
            next_url = urljoin(get_base_url(response), next_url)
            self.ips.append({
                'url': next_url,
                'ref': response.url
            })
