# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from scrapy import FormRequest


class ShenzhenqianhaitangshiInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_ShenzhenqianhaitangshiInvest'
    sitename = '深圳前海唐氏投资'
    entry = 'http://www.tszg168.com'

    def start_requests(self):
        yield FormRequest(
            url='http://www.tszg168.com/index.html?sid=pkrbn4s2n3kn312nd2ubr5jc36',  # 同意页面
            callback=self.parse_list  # 回调下面方法
        )

    def parse_list(self, response):
        self.ips.append({
            'url': 'http://www.tszg168.com/a/tangshifabu/index.html',  # 数据列表页面
        })
        yield self.request_next()

    def parse_item(self, response):

        rows = response.xpath('//div[@class="text"]/ul/li')
        for row in rows:
            url = row.xpath('./a/@href').extract_first()  # 获取路径
            url = urljoin(get_base_url(response), url)  # 拼接绝对路径

            title = row.xpath('./a/text()').extract_first().strip().replace('\t', '').replace('\r', '').replace('\n', '')  # 标题

            publish_time = row.xpath('./b/text()').extract_first().strip().replace('\t', '').replace('\r', '').replace('\n', '')  # 时间格式
            publish_time = datetime.strptime(publish_time, '%Y-%m-%d')  # 转换时间格式

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time
            yield item

        next_url = response.xpath('//ul[@class="pagelist"]/li/a[text()="下一页"]/@href').extract_first()
        if next_url:
            next_url = urljoin(get_base_url(response), next_url)
            self.ips.append({
                'url': next_url,
                'ref': response.url
            })
        yield self.request_next()













